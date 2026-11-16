"""
Modul Pengelolaan Data Pemeriksaan Balita dan Ibu Hamil Posyandu Digital
Menghitung parameter antropometri standar WHO, risiko maternal, dan sinkronisasi Supabase.
"""
from datetime import date, timedelta
from typing import Optional, Dict, Any, Tuple
import numpy as np
import pandas as pd
from ..database.connection import get_supabase_client, is_connected, load_local_csv, save_local_csv
from ..services import gizi_service as gizi
from .peserta_repo import get_all_peserta, get_peserta_by_id


def get_pemeriksaan_balita() -> pd.DataFrame:
    """
    Mengambil data pemeriksaan balita dan menggabungkannya
    dengan data peserta (tanpa ketergantungan nomor telepon).
    """
    client = get_supabase_client()
    b_df = pd.DataFrame()
    if is_connected() and client:
        try:
            res = client.table("pemeriksaan_balita").select("*").order("tanggal_pemeriksaan").execute()
            if res.data:
                b_df = pd.DataFrame(res.data)
        except Exception as e:
            print(f"[Supabase] Error get_pemeriksaan_balita: {e}")

    if b_df.empty:
        b_df = load_local_csv("pemeriksaan_balita")

    if b_df.empty:
        return pd.DataFrame(columns=[
            "id_peserta", "tanggal_pemeriksaan", "usia_bulan", "berat_kg", "tinggi_cm",
            "lingkar_kepala_cm", "vitamin_a", "imunisasi", "z_bb_u", "z_tb_u", "status_gizi",
            "jadwal_berikutnya", "catatan", "nama", "jenis_kelamin", "alamat_dusun",
            "tanggal_lahir", "id_orang_tua", "nama_orang_tua", "email", "bulan", "tahun", "periode"
        ])

    b_df["tanggal_pemeriksaan"] = pd.to_datetime(b_df["tanggal_pemeriksaan"], errors="coerce")
    for col in ["usia_bulan", "berat_kg", "tinggi_cm", "lingkar_kepala_cm", "z_bb_u", "z_tb_u"]:
        if col in b_df.columns:
            b_df[col] = pd.to_numeric(b_df[col], errors="coerce")

    p = get_all_peserta()
    if not p.empty and "id_peserta" in p.columns:
        cols_to_merge = [c for c in ["id_peserta", "nama", "jenis_kelamin", "alamat_dusun", "email",
                                     "tanggal_lahir", "id_orang_tua", "nama_orang_tua"] if c in p.columns]
        b_df = b_df.merge(p[cols_to_merge], on="id_peserta", how="left")

    # Kolom waktu derivatif
    b_df["bulan"] = b_df["tanggal_pemeriksaan"].dt.month
    b_df["tahun"] = b_df["tanggal_pemeriksaan"].dt.year
    b_df["periode"] = b_df["tanggal_pemeriksaan"].dt.strftime("%Y-%m")

    return b_df


def get_pemeriksaan_ibu() -> pd.DataFrame:
    """
    Mengambil data pemeriksaan ibu hamil beserta klasifikasi trimester
    dan gabungan data peserta (tanpa nomor telepon).
    """
    client = get_supabase_client()
    i_df = pd.DataFrame()
    if is_connected() and client:
        try:
            res = client.table("pemeriksaan_ibu_hamil").select("*").order("tanggal_pemeriksaan").execute()
            if res.data:
                i_df = pd.DataFrame(res.data)
        except Exception as e:
            print(f"[Supabase] Error get_pemeriksaan_ibu: {e}")

    if i_df.empty:
        i_df = load_local_csv("pemeriksaan_ibu_hamil")

    if i_df.empty:
        return pd.DataFrame(columns=[
            "id_peserta", "tanggal_pemeriksaan", "usia_kehamilan_minggu", "berat_kg", "lila_cm",
            "sistol", "diastol", "hb_gdl", "tfu_cm", "djj_bpm", "tablet_fe", "status_kek",
            "status_anemia", "status_hipertensi", "risiko", "jadwal_berikutnya", "hpl", "catatan",
            "nama", "alamat_dusun", "email", "trimester", "bulan", "tahun", "periode"
        ])

    i_df["tanggal_pemeriksaan"] = pd.to_datetime(i_df["tanggal_pemeriksaan"], errors="coerce")
    for col in ["usia_kehamilan_minggu", "berat_kg", "lila_cm", "sistol", "diastol", "hb_gdl", "tfu_cm", "djj_bpm"]:
        if col in i_df.columns:
            i_df[col] = pd.to_numeric(i_df[col], errors="coerce")

    p = get_all_peserta()
    if not p.empty and "id_peserta" in p.columns:
        cols_to_merge = [c for c in ["id_peserta", "nama", "alamat_dusun", "email"] if c in p.columns]
        i_df = i_df.merge(p[cols_to_merge], on="id_peserta", how="left")

    if "usia_kehamilan_minggu" in i_df.columns:
        i_df["trimester"] = pd.cut(
            i_df["usia_kehamilan_minggu"],
            [0, 13, 27, 45],
            labels=["Trimester 1", "Trimester 2", "Trimester 3"]
        ).astype(str)

    i_df["bulan"] = i_df["tanggal_pemeriksaan"].dt.month
    i_df["tahun"] = i_df["tanggal_pemeriksaan"].dt.year
    i_df["periode"] = i_df["tanggal_pemeriksaan"].dt.strftime("%Y-%m")

    return i_df


def get_pemeriksaan_by_peserta(id_peserta: str) -> pd.DataFrame:
    """Mengambil riwayat pemeriksaan spesifik untuk satu peserta (Balita atau Ibu Hamil)."""
    if not id_peserta:
        return pd.DataFrame()
    pid = id_peserta.strip().upper()
    if pid.startswith("BLT"):
        df = get_pemeriksaan_balita()
    else:
        df = get_pemeriksaan_ibu()

    if df.empty or "id_peserta" not in df.columns:
        return pd.DataFrame()

    match = df[df["id_peserta"].astype(str).str.upper() == pid]
    if match.empty:
        return pd.DataFrame()

    return match.sort_values("tanggal_pemeriksaan", ascending=False)


def get_latest_pemeriksaan(df: pd.DataFrame) -> pd.DataFrame:
    """Mengambil pemeriksaan terakhir per peserta."""
    if df.empty or "id_peserta" not in df.columns or "tanggal_pemeriksaan" not in df.columns:
        return pd.DataFrame()
    return df.sort_values("tanggal_pemeriksaan").groupby("id_peserta", as_index=False).tail(1)


def add_pemeriksaan_balita(data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """Menyimpan pemeriksaan balita baru dan menghitung Z-score WHO secara akurat."""
    pid = data.get("id_peserta", "").strip().upper()
    peserta_info = get_peserta_by_id(pid)
    if not peserta_info:
        return False, f"Peserta {pid} tidak ditemukan.", {}

    tgl = pd.to_datetime(data.get("tanggal_pemeriksaan", date.today())).date()
    bb = float(data.get("berat_kg", 0))
    tb = float(data.get("tinggi_cm", 0))
    lk = float(data.get("lingkar_kepala_cm", 0))

    # Hitung usia bulan saat pemeriksaan
    tgl_lahir = pd.to_datetime(peserta_info.get("tanggal_lahir", tgl)).date()
    age = round(max(0.0, (tgl.year - tgl_lahir.year) * 12 + tgl.month - tgl_lahir.month + (tgl.day - tgl_lahir.day) / 30.4), 1)

    sex = peserta_info.get("jenis_kelamin", "Laki-laki")
    zb = gizi.zscore(sex, "bb", age, bb)
    zt = gizi.zscore(sex, "tb", age, tb)
    status = gizi.status_gizi(zb, zt)
    next_date = tgl + timedelta(days=28)

    row = {
        "id_peserta": pid,
        "tanggal_pemeriksaan": str(tgl),
        "usia_bulan": age,
        "berat_kg": bb,
        "tinggi_cm": tb,
        "lingkar_kepala_cm": lk,
        "vitamin_a": data.get("vitamin_a", "Tidak"),
        "imunisasi": data.get("imunisasi", "Lengkap sesuai usia"),
        "z_bb_u": zb,
        "z_tb_u": zt,
        "status_gizi": status,
        "jadwal_berikutnya": str(next_date),
        "catatan": data.get("catatan", "")
    }

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("pemeriksaan_balita").insert(row).execute()
            return True, f"Pemeriksaan balita {pid} berhasil disimpan di Supabase.", row
        except Exception as e:
            print(f"[Supabase] Error add_pemeriksaan_balita: {e}")

    # Fallback lokal
    df = load_local_csv("pemeriksaan_balita")
    new_df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    if save_local_csv("pemeriksaan_balita", new_df):
        return True, f"Pemeriksaan balita {pid} berhasil disimpan.", row
    return False, "Gagal menyimpan pemeriksaan balita.", {}


def add_pemeriksaan_ibu(data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """Menyimpan pemeriksaan ibu hamil baru dan menghitung faktor risiko maternal."""
    pid = data.get("id_peserta", "").strip().upper()
    peserta_info = get_peserta_by_id(pid)
    if not peserta_info:
        return False, f"Peserta {pid} tidak ditemukan.", {}

    tgl = pd.to_datetime(data.get("tanggal_pemeriksaan", date.today())).date()
    w = int(data.get("usia_kehamilan_minggu", 20))
    bb = float(data.get("berat_kg", 60.0))
    lila = float(data.get("lila_cm", 25.0))
    hb = float(data.get("hb_gdl", 11.5))
    sis = int(data.get("sistol", 115))
    dia = int(data.get("diastol", 75))
    tfu = float(data.get("tfu_cm", 0.0)) if data.get("tfu_cm") else None
    djj = int(data.get("djj_bpm", 0)) if data.get("djj_bpm") else None
    fe = data.get("tablet_fe", "Diberikan")

    kek, an, hip, r = gizi.risiko_ibu(sis, dia, hb, lila)
    next_date = tgl + timedelta(days=14 if r == "Risiko tinggi" else 28)
    hpl_date = tgl + timedelta(days=max(0, 40 - w) * 7)

    row = {
        "id_peserta": pid,
        "tanggal_pemeriksaan": str(tgl),
        "usia_kehamilan_minggu": w,
        "berat_kg": bb,
        "lila_cm": lila,
        "sistol": sis,
        "diastol": dia,
        "hb_gdl": hb,
        "tfu_cm": tfu,
        "djj_bpm": djj,
        "tablet_fe": fe,
        "status_kek": kek,
        "status_anemia": an,
        "status_hipertensi": hip,
        "risiko": r,
        "jadwal_berikutnya": str(next_date),
        "hpl": str(hpl_date),
        "catatan": data.get("catatan", "")
    }

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("pemeriksaan_ibu_hamil").insert(row).execute()
            return True, f"Pemeriksaan ibu hamil {pid} berhasil disimpan di Supabase.", row
        except Exception as e:
            print(f"[Supabase] Error add_pemeriksaan_ibu: {e}")

    # Fallback lokal
    df = load_local_csv("pemeriksaan_ibu_hamil")
    new_df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    if save_local_csv("pemeriksaan_ibu_hamil", new_df):
        return True, f"Pemeriksaan ibu hamil {pid} berhasil disimpan.", row
    return False, "Gagal menyimpan pemeriksaan ibu hamil.", {}
