"""
Modul Pengelolaan Data Peserta Posyandu Digital
Mencakup pendaftaran mandiri (onboarding biodata), pendaftaran oleh kader,
pencarian, pembaruan, dan relasi langsung dengan user ID akun Supabase.
"""
from datetime import date
from typing import Optional, Dict, Any, Tuple, List
import pandas as pd
from .connection import get_supabase_client, is_connected, load_local_csv, save_local_csv
from .users import update_user_profile


def get_all_peserta() -> pd.DataFrame:
    """Mengambil seluruh data peserta (Balita & Ibu Hamil)."""
    client = get_supabase_client()
    if is_connected() and client:
        try:
            res = client.table("peserta").select("*").order("id_peserta").execute()
            if res.data:
                return pd.DataFrame(res.data)
        except Exception as e:
            print(f"[Supabase] Error get_all_peserta: {e}")

    df = load_local_csv("peserta")
    if not df.empty and "no_hp" in df.columns:
        df = df.drop(columns=["no_hp"], errors="ignore")
    return df


def get_peserta_by_id(id_peserta: str) -> Optional[Dict[str, Any]]:
    """Mencari data peserta spesifik berdasarkan ID peserta."""
    if not id_peserta:
        return None
    pid = id_peserta.strip().upper()

    client = get_supabase_client()
    if is_connected() and client:
        try:
            res = client.table("peserta").select("*").eq("id_peserta", pid).limit(1).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception as e:
            print(f"[Supabase] Error get_peserta_by_id: {e}")

    df = get_all_peserta()
    if not df.empty and "id_peserta" in df.columns:
        match = df[df["id_peserta"].astype(str).str.upper() == pid]
        if len(match) > 0:
            return match.iloc[0].fillna("").to_dict()
    return None


def get_peserta_by_user_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Mencari peserta yang terhubung dengan akun user ID tertentu (khusus Ibu Hamil)."""
    if not user_id:
        return None
    client = get_supabase_client()
    if is_connected() and client:
        try:
            res = client.table("peserta").select("*").eq("user_id", user_id).limit(1).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception as e:
            print(f"[Supabase] Error get_peserta_by_user_id: {e}")

    df = get_all_peserta()
    if not df.empty and "user_id" in df.columns:
        match = df[df["user_id"].astype(str) == str(user_id)]
        if not match.empty:
            return match.iloc[0].fillna("").to_dict()
    return None


def get_children_by_parent_user_id(user_id: str) -> pd.DataFrame:
    """Mengambil daftar anak balita yang berada di bawah akun orang tua tertentu."""
    if not user_id:
        return pd.DataFrame()

    client = get_supabase_client()
    if is_connected() and client:
        try:
            # 1. Cari id_orang_tua yang terhubung dengan user_id
            ortu_res = client.table("orang_tua").select("id_orang_tua").eq("user_id", user_id).execute()
            ortu_ids = [r["id_orang_tua"] for r in (ortu_res.data or [])]

            if ortu_ids:
                # 2. Ambil semua balita dengan id_orang_tua tersebut atau user_id langsung
                kids_res = client.table("peserta").select("*").in_("id_orang_tua", ortu_ids).execute()
                if kids_res.data:
                    return pd.DataFrame(kids_res.data)

            # Cek jika balita langsung terhubung via user_id
            kids_direct = client.table("peserta").select("*").eq("user_id", user_id).eq("jenis_peserta", "Balita").execute()
            if kids_direct.data:
                return pd.DataFrame(kids_direct.data)
        except Exception as e:
            print(f"[Supabase] Error get_children_by_parent_user_id: {e}")

    # Fallback lokal
    df = get_all_peserta()
    if df.empty:
        return pd.DataFrame()

    ortu_df = load_local_csv("orang_tua")
    matched_ortu_ids = []
    if not ortu_df.empty and "user_id" in ortu_df.columns:
        matched_ortu_ids = ortu_df[ortu_df["user_id"].astype(str) == str(user_id)]["id_orang_tua"].tolist()

    mask = pd.Series([False] * len(df))
    if matched_ortu_ids and "id_orang_tua" in df.columns:
        mask = mask | df["id_orang_tua"].isin(matched_ortu_ids)
    if "user_id" in df.columns:
        mask = mask | (df["user_id"].astype(str) == str(user_id))

    return df[mask & (df["jenis_peserta"] == "Balita")]


def search_peserta(query: str = "", jenis: str = "Semua") -> pd.DataFrame:
    """Mencari peserta berdasarkan kata kunci nama atau ID dan filter jenis."""
    df = get_all_peserta()
    if df.empty:
        return pd.DataFrame()

    if jenis in ["Balita", "Ibu Hamil"]:
        df = df[df["jenis_peserta"] == jenis]

    if query and query.strip():
        q = query.strip()
        mask = (
            df["nama"].astype(str).str.contains(q, case=False, na=False) |
            df["id_peserta"].astype(str).str.contains(q, case=False, na=False)
        )
        if "nama_orang_tua" in df.columns:
            mask = mask | df["nama_orang_tua"].astype(str).str.contains(q, case=False, na=False)
        df = df[mask]

    return df


def generate_next_id(prefix: str) -> str:
    """Menghasilkan ID urut baru berdasarkan prefix (contoh: BLT001, IBU001, ORT001)."""
    df = get_all_peserta()
    max_num = 0
    if not df.empty and "id_peserta" in df.columns:
        matches = df[df["id_peserta"].astype(str).str.startswith(prefix)]
        if not matches.empty:
            nums = pd.to_numeric(matches["id_peserta"].astype(str).str[len(prefix):], errors="coerce")
            max_num = int(nums.max()) if pd.notna(nums.max()) else 0

    if prefix == "ORT":
        ortu_df = load_local_csv("orang_tua")
        if not ortu_df.empty and "id_orang_tua" in ortu_df.columns:
            matches_o = ortu_df[ortu_df["id_orang_tua"].astype(str).str.startswith("ORT")]
            if not matches_o.empty:
                nums = pd.to_numeric(matches_o["id_orang_tua"].astype(str).str[3:], errors="coerce")
                if pd.notna(nums.max()):
                    max_num = max(max_num, int(nums.max()))

    return f"{prefix}{max_num + 1:03d}"


# ====================================================================
# ONBOARDING BIODATA MANDIRI (USER REGISTRATION FLOW)
# ====================================================================
def save_ibu_biodata(user_id: str, data: Dict[str, Any]) -> Tuple[bool, str, str]:
    """Menyimpan pengisian biodata mandiri pertama kali oleh Ibu Hamil."""
    nama_ibu = data.get("nama", "").strip()
    if not nama_ibu:
        return False, "Nama lengkap ibu hamil wajib diisi.", ""

    new_pid = generate_next_id("IBU")
    today = date.today().isoformat()

    record = {
        "id_peserta": new_pid,
        "user_id": user_id,
        "jenis_peserta": "Ibu Hamil",
        "nama": nama_ibu,
        "email": data.get("email", "").strip(),
        "tanggal_lahir": None,
        "usia_bulan": None,
        "jenis_kelamin": "Perempuan",
        "nama_orang_tua": data.get("nama_suami", "").strip(),
        "id_orang_tua": None,
        "usia_ibu_tahun": int(data.get("usia_ibu_tahun", 28)),
        "usia_kehamilan_minggu": int(data.get("usia_kehamilan_minggu", 12)),
        "alamat_dusun": data.get("alamat_dusun", "Melati"),
        "alamat_lengkap": data.get("alamat_lengkap", ""),
        "status": "Terdaftar",
        "tanggal_daftar": today
    }

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("peserta").insert(record).execute()
            update_user_profile(user_id, {
                "id_peserta": new_pid,
                "nama": nama_ibu,
                "alamat_dusun": record["alamat_dusun"]
            })
            return True, f"Biodata kehamilan berhasil disimpan! ID Peserta Anda: {new_pid}", new_pid
        except Exception as e:
            print(f"[Supabase] Error save_ibu_biodata: {e}")

    # Fallback lokal
    df = load_local_csv("peserta")
    new_df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    save_local_csv("peserta", new_df)
    update_user_profile(user_id, {
        "id_peserta": new_pid,
        "nama": nama_ibu,
        "alamat_dusun": record["alamat_dusun"]
    })
    return True, f"Biodata kehamilan berhasil disimpan! ID Peserta Anda: {new_pid}", new_pid


def save_ortu_and_balita_biodata(user_id: str, data: Dict[str, Any]) -> Tuple[bool, str, str]:
    """Menyimpan pengisian biodata orang tua dan balita pertama kali."""
    nama_ortu = data.get("nama_orang_tua", "").strip()
    nama_balita = data.get("nama_balita", "").strip()

    if not nama_ortu:
        return False, "Nama orang tua wajib diisi.", ""
    if not nama_balita:
        return False, "Nama balita wajib diisi.", ""

    ortu_id = generate_next_id("ORT")
    balita_id = generate_next_id("BLT")
    today = date.today().isoformat()
    dusun = data.get("alamat_dusun", "Melati")
    alamat = data.get("alamat_lengkap", "")
    email = data.get("email", "")

    # 1. Simpan profil orang tua
    ortu_record = {
        "id_orang_tua": ortu_id,
        "user_id": user_id,
        "nama_ayah": nama_ortu,
        "email": email,
        "alamat_dusun": dusun,
        "alamat_lengkap": alamat
    }

    # 2. Simpan profil balita pertama
    tgl_lahir = data.get("tanggal_lahir", today)
    usia_bln = float(data.get("usia_bulan", 0.0))
    balita_record = {
        "id_peserta": balita_id,
        "user_id": user_id,
        "jenis_peserta": "Balita",
        "nama": nama_balita,
        "email": email,
        "tanggal_lahir": str(tgl_lahir),
        "usia_bulan": usia_bln,
        "jenis_kelamin": data.get("jenis_kelamin", "Laki-laki"),
        "id_orang_tua": ortu_id,
        "nama_orang_tua": nama_ortu,
        "alamat_dusun": dusun,
        "alamat_lengkap": alamat,
        "status": "Terdaftar",
        "tanggal_daftar": today
    }

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("orang_tua").insert(ortu_record).execute()
            client.table("peserta").insert(balita_record).execute()
            update_user_profile(user_id, {
                "id_peserta": ortu_id,
                "nama": nama_ortu,
                "alamat_dusun": dusun
            })
            return True, f"Biodata berhasil disimpan! Data si kecil terdaftar dengan ID: {balita_id}", balita_id
        except Exception as e:
            print(f"[Supabase] Error save_ortu_biodata: {e}")

    # Fallback lokal
    df_o = load_local_csv("orang_tua")
    save_local_csv("orang_tua", pd.concat([df_o, pd.DataFrame([ortu_record])], ignore_index=True))

    df_p = load_local_csv("peserta")
    save_local_csv("peserta", pd.concat([df_p, pd.DataFrame([balita_record])], ignore_index=True))

    update_user_profile(user_id, {
        "id_peserta": ortu_id,
        "nama": nama_ortu,
        "alamat_dusun": dusun
    })
    return True, f"Biodata berhasil disimpan! Data si kecil terdaftar dengan ID: {balita_id}", balita_id


def add_additional_child(user_id: str, id_orang_tua: str, data: Dict[str, Any]) -> Tuple[bool, str, str]:
    """Menambahkan balita berikutnya untuk orang tua yang sudah terdaftar."""
    nama_balita = data.get("nama_balita", "").strip()
    if not nama_balita:
        return False, "Nama balita wajib diisi.", ""

    balita_id = generate_next_id("BLT")
    today = date.today().isoformat()
    tgl_lahir = data.get("tanggal_lahir", today)

    balita_record = {
        "id_peserta": balita_id,
        "user_id": user_id,
        "jenis_peserta": "Balita",
        "nama": nama_balita,
        "email": data.get("email", ""),
        "tanggal_lahir": str(tgl_lahir),
        "usia_bulan": float(data.get("usia_bulan", 0.0)),
        "jenis_kelamin": data.get("jenis_kelamin", "Laki-laki"),
        "id_orang_tua": id_orang_tua,
        "nama_orang_tua": data.get("nama_orang_tua", ""),
        "alamat_dusun": data.get("alamat_dusun", "Melati"),
        "alamat_lengkap": data.get("alamat_lengkap", ""),
        "status": "Terdaftar",
        "tanggal_daftar": today
    }

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("peserta").insert(balita_record).execute()
            return True, f"Balita baru berhasil ditambahkan dengan ID {balita_id}!", balita_id
        except Exception as e:
            print(f"[Supabase] Error add_additional_child: {e}")

    df_p = load_local_csv("peserta")
    save_local_csv("peserta", pd.concat([df_p, pd.DataFrame([balita_record])], ignore_index=True))
    return True, f"Balita baru berhasil ditambahkan dengan ID {balita_id}!", balita_id


def has_completed_biodata(user: Dict[str, Any]) -> bool:
    """Mengecek apakah pengguna telah melengkapi biodata profilnya."""
    if not user:
        return False

    role = user.get("role", "")
    uid = str(user.get("id", ""))
    pid = user.get("id_peserta", "")

    if role == "Ibu Hamil":
        if pid and pid.startswith("IBU"):
            return True
        p = get_peserta_by_user_id(uid)
        return p is not None

    elif role == "Orang Tua Balita":
        kids = get_children_by_parent_user_id(uid)
        if not kids.empty:
            return True
        if pid and pid.startswith("ORT"):
            # Cek apakah ada balita dengan ortu_id ini
            all_p = get_all_peserta()
            if not all_p.empty and "id_orang_tua" in all_p.columns:
                return (all_p["id_orang_tua"] == pid).any()
        return False

    elif role == "Kader":
        # Kader dapat langsung mengakses dashboard
        return True

    return True


# Fungsi pendaftaran oleh Kader
def create_peserta(data: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
    """Mendaftarkan peserta baru oleh Kader posyandu."""
    jenis = data.get("jenis_peserta", "").strip()
    nama = data.get("nama", "").strip()
    if not nama:
        return False, "Nama peserta wajib diisi.", None

    prefix = "BLT" if jenis == "Balita" else "IBU"
    new_pid = generate_next_id(prefix)
    today = date.today().isoformat()

    record = {
        "id_peserta": new_pid,
        "jenis_peserta": jenis,
        "nama": nama,
        "alamat_dusun": data.get("alamat_dusun", "Melati"),
        "alamat_lengkap": data.get("alamat_lengkap", ""),
        "email": data.get("email", "").strip() or f"{new_pid.lower()}@posyandu.id",
        "status": "Terdaftar",
        "tanggal_daftar": today,
    }

    if jenis == "Balita":
        tgl_lahir = data.get("tanggal_lahir", today)
        record["tanggal_lahir"] = str(tgl_lahir)
        record["usia_bulan"] = float(data.get("usia_bulan", 0))
        record["jenis_kelamin"] = data.get("jenis_kelamin", "Laki-laki")
        record["nama_orang_tua"] = data.get("nama_orang_tua", "").strip()
        record["id_orang_tua"] = data.get("id_orang_tua", "") or generate_next_id("ORT")
    else:
        record["nama_orang_tua"] = data.get("nama_suami", "").strip()
        record["usia_ibu_tahun"] = int(data.get("usia_ibu_tahun", 28))
        record["usia_kehamilan_minggu"] = int(data.get("usia_kehamilan_minggu", 12))
        record["jenis_kelamin"] = "Perempuan"

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("peserta").insert(record).execute()
            return True, f"Peserta berhasil didaftarkan di Supabase dengan ID {new_pid}.", new_pid
        except Exception as e:
            print(f"[Supabase] Error create_peserta: {e}")

    df = load_local_csv("peserta")
    new_df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    if save_local_csv("peserta", new_df):
        return True, f"Peserta berhasil disimpan dengan ID {new_pid}.", new_pid
    return False, "Gagal menyimpan data peserta.", None


def update_peserta(id_peserta: str, data: Dict[str, Any]) -> Tuple[bool, str]:
    """Memperbarui informasi data peserta."""
    pid = id_peserta.strip().upper()
    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("peserta").update(data).eq("id_peserta", pid).execute()
            return True, f"Data peserta {pid} berhasil diperbarui di Supabase."
        except Exception as e:
            print(f"[Supabase] Error update_peserta: {e}")

    df = load_local_csv("peserta")
    if not df.empty and "id_peserta" in df.columns:
        idx = df[df["id_peserta"].astype(str).str.upper() == pid].index
        if len(idx) > 0:
            for k, v in data.items():
                if k in df.columns:
                    df.loc[idx, k] = v
            save_local_csv("peserta", df)
            return True, f"Data peserta {pid} berhasil diperbarui secara lokal."
    return False, f"Peserta dengan ID {pid} tidak ditemukan."


def delete_peserta(id_peserta: str) -> Tuple[bool, str]:
    """Menghapus peserta beserta riwayat pemeriksaannya."""
    pid = id_peserta.strip().upper()
    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("peserta").delete().eq("id_peserta", pid).execute()
            return True, f"Peserta {pid} berhasil dihapus dari Supabase."
        except Exception as e:
            print(f"[Supabase] Error delete_peserta: {e}")

    df = load_local_csv("peserta")
    if not df.empty and "id_peserta" in df.columns:
        df = df[df["id_peserta"].astype(str).str.upper() != pid]
        save_local_csv("peserta", df)
        return True, f"Peserta {pid} berhasil dihapus."
    return False, f"Peserta {pid} tidak ditemukan."
