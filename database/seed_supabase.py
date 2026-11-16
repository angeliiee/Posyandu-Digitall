"""
Skrip Migrasi dan Seed Data ke Supabase
Membaca dataset CSV lokal dan mengunggahnya ke tabel Supabase PostgreSQL.
Jalankan:
    python posyandu_digital_v2/database/seed_supabase.py
"""
import sys
from pathlib import Path
import pandas as pd

# Pastikan path modul terdeteksi
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from database.connection import get_supabase_client, is_connected, get_credentials, DATA_DIR


def seed():
    url, key = get_credentials()
    print(f"[*] Menghubungkan ke Supabase: {url[:25]}...")
    client = get_supabase_client()

    if not is_connected() or not client:
        print("[!] Gagal terhubung ke Supabase. Periksa kembali SUPABASE_URL dan SUPABASE_KEY di .env atau secrets.toml.")
        return False

    print("[+] Terkoneksi ke Supabase. Memulai proses migrasi...")

    # 1. Migrasi Users
    users_path = DATA_DIR / "users.csv"
    if users_path.exists():
        import uuid
        df_u = pd.read_csv(users_path).fillna("")
        records_u = df_u.to_dict(orient="records")
        for u in records_u:
            if not u.get("id"):
                u["id"] = str(uuid.uuid4())
            try:
                client.table("users").upsert(u, on_conflict="email").execute()
            except Exception as e:
                print(f"    [!] Error upsert user {u.get('email')}: {e}")
        print(f"[+] Migrasi {len(records_u)} users selesai.")

    # 2. Migrasi Orang Tua
    # Buat dari peserta balita
    peserta_path = DATA_DIR / "peserta.csv"
    if peserta_path.exists():
        df_p = pd.read_csv(peserta_path).fillna("")
        ortu_rows = df_p[df_p["id_orang_tua"] != ""][["id_orang_tua", "nama_orang_tua", "alamat_dusun", "email"]].drop_duplicates("id_orang_tua")
        for _, r in ortu_rows.iterrows():
            try:
                client.table("orang_tua").upsert({
                    "id_orang_tua": r["id_orang_tua"],
                    "nama_ayah": r["nama_orang_tua"],
                    "alamat_dusun": r["alamat_dusun"],
                    "email": r["email"]
                }, on_conflict="id_orang_tua").execute()
            except Exception as e:
                print(f"    [!] Error upsert orang_tua {r['id_orang_tua']}: {e}")
        print(f"[+] Migrasi {len(ortu_rows)} orang_tua selesai.")

        # 3. Migrasi Peserta
        p_records = df_p.to_dict(orient="records")
        for p in p_records:
            # Bersihkan tipe data kosong
            cleaned = {}
            for k, v in p.items():
                if v == "" or pd.isna(v):
                    cleaned[k] = None
                else:
                    cleaned[k] = v
            try:
                client.table("peserta").upsert(cleaned, on_conflict="id_peserta").execute()
            except Exception as e:
                print(f"    [!] Error upsert peserta {p.get('id_peserta')}: {e}")
        print(f"[+] Migrasi {len(p_records)} peserta selesai.")

    # 4. Migrasi Pemeriksaan Balita
    b_path = DATA_DIR / "pemeriksaan_balita.csv"
    if b_path.exists():
        df_b = pd.read_csv(b_path).fillna("")
        b_records = df_b.to_dict(orient="records")
        for b in b_records:
            cleaned = {k: (None if v == "" or pd.isna(v) else v) for k, v in b.items()}
            try:
                client.table("pemeriksaan_balita").insert(cleaned).execute()
            except Exception as e:
                print(f"    [!] Error insert pemeriksaan balita {b.get('id_peserta')}: {e}")
        print(f"[+] Migrasi {len(b_records)} pemeriksaan balita selesai.")

    # 5. Migrasi Pemeriksaan Ibu Hamil
    i_path = DATA_DIR / "pemeriksaan_ibu_hamil.csv"
    if i_path.exists():
        df_i = pd.read_csv(i_path).fillna("")
        i_records = df_i.to_dict(orient="records")
        for i in i_records:
            cleaned = {k: (None if v == "" or pd.isna(v) else v) for k, v in i.items()}
            try:
                client.table("pemeriksaan_ibu_hamil").insert(cleaned).execute()
            except Exception as e:
                print(f"    [!] Error insert pemeriksaan ibu {i.get('id_peserta')}: {e}")
        print(f"[+] Migrasi {len(i_records)} pemeriksaan ibu selesai.")

    print("\n[SUCCESS] Seluruh data berhasil disinkronkan ke Supabase PostgreSQL!")
    return True


if __name__ == "__main__":
    seed()
