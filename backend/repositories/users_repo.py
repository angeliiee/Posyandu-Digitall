"""
Modul Autentikasi dan Manajemen Pengguna Posyandu Digital
Mendukung Supabase Auth penuh (sign up, sign in, sign out, user session)
serta sinkronisasi profil pengguna ke tabel 'users' PostgreSQL dengan fallback lokal aman.
"""
import uuid
from typing import Optional, Dict, Any, List, Tuple
import pandas as pd
from ..database.connection import get_supabase_client, is_connected, load_local_csv, save_local_csv
from ..services import gizi_service as gizi


def sign_up_user(email: str, password: str, role: str, nama: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Registrasi mandiri pengguna baru menggunakan Supabase Auth.
    Mengenkripsi password secara aman dan menyimpan profil ke tabel users.
    """
    e_clean = email.strip().lower()
    n_clean = nama.strip()
    if not e_clean or "@" not in e_clean:
        return False, "Email tidak valid. Pastikan memasukkan alamat email yang benar.", None
    if len(password) < 6:
        return False, "Password minimal 6 karakter demi keamanan akun.", None
    if not n_clean:
        return False, "Nama lengkap wajib diisi.", None
    if role not in ["Kader", "Ibu Hamil", "Orang Tua Balita"]:
        return False, "Peran pengguna tidak valid.", None

    client = get_supabase_client()
    user_id = ""

    if is_connected() and client:
        try:
            # 1. Pendaftaran akun autentikasi di Supabase Auth
            auth_res = client.auth.sign_up({
                "email": e_clean,
                "password": password,
                "options": {
                    "data": {
                        "role": role,
                        "nama": n_clean,
                        "username": e_clean.split("@")[0]
                    }
                }
            })

            if auth_res.user:
                user_id = str(auth_res.user.id)
                user_record = {
                    "id": user_id,
                    "username": e_clean.split("@")[0],
                    "email": e_clean,
                    "role": role,
                    "nama": n_clean,
                    "id_peserta": ""
                }

                # 2. Simpan profil ke tabel public.users
                try:
                    client.table("users").upsert(user_record, on_conflict="id").execute()
                except Exception as insert_err:
                    print(f"[Supabase] Warning on profile upsert: {insert_err}")

                return True, "Registrasi akun berhasil di Supabase! Silakan login untuk melengkapi biodata.", user_record
            else:
                return False, "Gagal membuat akun autentikasi di Supabase.", None
        except Exception as e:
            err_msg = str(e)
            if "already registered" in err_msg.lower() or "unique" in err_msg.lower():
                return False, "Email ini sudah terdaftar. Silakan login atau gunakan email lain.", None
            print(f"[Supabase] Auth sign_up error: {e}")
            # Fallback ke penyimpanan lokal jika koneksi Supabase terputus
            pass

    # ==========================================
    # FALLBACK ENGINE (LOKAL)
    # ==========================================
    df = load_local_csv("users")
    if not df.empty and "email" in df.columns:
        if (df["email"].astype(str).str.lower() == e_clean).any():
            return False, "Email ini sudah terdaftar pada sistem.", None

    user_id = str(uuid.uuid4())
    pw_hash = gizi.hash_pw(password)
    user_record = {
        "id": user_id,
        "username": e_clean.split("@")[0],
        "email": e_clean,
        "password_hash": pw_hash,
        "role": role,
        "nama": n_clean,
        "id_peserta": ""
    }

    new_df = pd.concat([df, pd.DataFrame([user_record])], ignore_index=True)
    if save_local_csv("users", new_df):
        safe_record = dict(user_record)
        safe_record.pop("password_hash", None)
        return True, "Registrasi berhasil! Akun Anda telah aktif.", safe_record

    return False, "Gagal mendaftarkan akun. Silakan coba beberapa saat lagi.", None


def sign_in_user(email_or_username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Login mandiri pengguna menggunakan Supabase Auth (atau fallback lokal).
    Mengembalikan profil akun lengkap pengguna.
    """
    target = email_or_username.strip().lower()
    if not target or not password:
        return False, "Email dan password wajib diisi.", None

    client = get_supabase_client()

    # Coba via Supabase Auth jika online
    if is_connected() and client:
        try:
            # Jika user memasukkan username tanpa @, cek email terlebih dahulu di users table
            lookup_email = target
            if "@" not in target:
                u_lookup = client.table("users").select("email").eq("username", target).limit(1).execute()
                if u_lookup.data and len(u_lookup.data) > 0:
                    lookup_email = u_lookup.data[0]["email"]

            auth_res = client.auth.sign_in_with_password({
                "email": lookup_email,
                "password": password
            })

            if auth_res.user:
                uid = str(auth_res.user.id)
                # Ambil profil dari tabel users
                prof_res = client.table("users").select("*").eq("id", uid).limit(1).execute()
                if prof_res.data and len(prof_res.data) > 0:
                    profile = prof_res.data[0]
                else:
                    # Buat record default dari metadata jika belum ada
                    meta = auth_res.user.user_metadata or {}
                    profile = {
                        "id": uid,
                        "username": meta.get("username", lookup_email.split("@")[0]),
                        "email": lookup_email,
                        "role": meta.get("role", "Orang Tua Balita"),
                        "nama": meta.get("nama", lookup_email.split("@")[0]),
                        "id_peserta": ""
                    }
                    try:
                        client.table("users").insert(profile).execute()
                    except Exception:
                        pass

                return True, "Login berhasil!", profile
        except Exception as e:
            err_str = str(e).lower()
            if "invalid login credentials" in err_str or "invalid_grant" in err_str:
                return False, "Email atau password salah. Silakan periksa kembali.", None
            print(f"[Supabase] Sign in error: {e}")

    # Fallback lokal
    df = load_local_csv("users")
    if not df.empty:
        # Cari berdasarkan email atau username
        mask = (df["email"].astype(str).str.lower() == target) if "@" in target else (df["username"].astype(str).str.lower() == target)
        matched = df[mask]
        if not matched.empty:
            stored_hash = matched.iloc[0].get("password_hash", "")
            if stored_hash == gizi.hash_pw(password):
                user_safe = matched.iloc[0].fillna("").to_dict()
                user_safe.pop("password_hash", None)
                return True, "Login berhasil!", user_safe

    return False, "Akun tidak ditemukan atau password salah.", None


def sign_out_user() -> bool:
    """Mengakhiri session pengguna di Supabase."""
    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.auth.sign_out()
            return True
        except Exception as e:
            print(f"[Supabase] Sign out error: {e}")
    return True


def get_user_profile_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Mengambil profil pengguna berdasarkan User ID (UUID)."""
    if not user_id:
        return None
    client = get_supabase_client()
    if is_connected() and client:
        try:
            res = client.table("users").select("*").eq("id", user_id).limit(1).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception as e:
            print(f"[Supabase] Error get profile: {e}")

    df = load_local_csv("users")
    if not df.empty and "id" in df.columns:
        match = df[df["id"].astype(str) == str(user_id)]
        if not match.empty:
            return match.iloc[0].fillna("").to_dict()
    return None


def update_user_profile(user_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
    """Memperbarui informasi profil pengguna (misalnya id_peserta setelah mengisi biodata)."""
    if not user_id:
        return False, "User ID tidak valid."

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("users").update(updates).eq("id", user_id).execute()
            return True, "Profil berhasil diperbarui."
        except Exception as e:
            print(f"[Supabase] Error update profile: {e}")

    df = load_local_csv("users")
    if not df.empty and "id" in df.columns:
        idx = df[df["id"].astype(str) == str(user_id)].index
        if len(idx) > 0:
            for k, v in updates.items():
                if k in df.columns:
                    df.loc[idx, k] = v
                else:
                    df[k] = ""
                    df.loc[idx, k] = v
            save_local_csv("users", df)
            return True, "Profil berhasil diperbarui secara lokal."
    return False, "Gagal memperbarui profil pengguna."


def get_users() -> pd.DataFrame:
    """Mengambil daftar akun pengguna untuk monitoring administrasi."""
    client = get_supabase_client()
    if is_connected() and client:
        try:
            res = client.table("users").select("id,username,email,role,nama,id_peserta,created_at").execute()
            if res.data:
                return pd.DataFrame(res.data)
        except Exception as e:
            print(f"[Supabase] Error get_users: {e}")

    df = load_local_csv("users")
    if not df.empty:
        cols = [c for c in ["id", "username", "email", "role", "nama", "id_peserta", "created_at"] if c in df.columns]
        return df[cols]
    return pd.DataFrame(columns=["id", "username", "email", "role", "nama", "id_peserta"])


# Kompatibilitas fungsi terdahulu
def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    return get_user_profile_by_id(username) or sign_in_user(username, "")[2]


def authenticate_user(username: str, password_plain: str) -> Optional[Dict[str, Any]]:
    sukses, _, profile = sign_in_user(username, password_plain)
    return profile if sukses else None


def create_user(username: str, password_plain: str, role: str, nama: str,
                id_peserta: str = "", email: str = "") -> Tuple[bool, str]:
    target_email = email.strip() or f"{username.strip().lower()}@posyandu.id"
    sukses, msg, _ = sign_up_user(target_email, password_plain, role, nama)
    return sukses, msg
