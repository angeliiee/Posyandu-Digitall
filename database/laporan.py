"""
Modul Pengelolaan Laporan Bulanan Posyandu Digital
Mendukung penyimpanan ringkasan laporan, unduhan, dan penyerahan status ke Puskesmas.
"""
from datetime import date
from typing import Optional, Dict, Any, Tuple
import pandas as pd
from .connection import get_supabase_client, is_connected, load_local_csv, save_local_csv


def get_all_laporan() -> pd.DataFrame:
    """Mengambil seluruh riwayat laporan bulanan posyandu."""
    client = get_supabase_client()
    if is_connected() and client:
        try:
            res = client.table("laporan").select("*").order("tanggal_dibuat", desc=True).execute()
            if res.data:
                return pd.DataFrame(res.data)
        except Exception as e:
            print(f"[Supabase] Error get_all_laporan: {e}")

    df = load_local_csv("laporan")
    if df.empty:
        return pd.DataFrame(columns=[
            "id_laporan", "periode", "kelompok", "variabel", "dibuat_oleh",
            "tanggal_dibuat", "status", "tanggal_serah", "catatan"
        ])
    return df


def save_laporan(periode: str, kelompok: str, variabel: str, dibuat_oleh: str, catatan: str = "") -> Tuple[bool, str, str]:
    """Menyimpan berkas laporan bulanan baru ke database."""
    existing = get_all_laporan()
    count = len(existing) + 1
    new_id = f"LAP{count:03d}"
    today = date.today().isoformat()

    row = {
        "id_laporan": new_id,
        "periode": periode,
        "kelompok": kelompok,
        "variabel": variabel,
        "dibuat_oleh": dibuat_oleh,
        "tanggal_dibuat": today,
        "status": "Siap diserahkan",
        "tanggal_serah": "",
        "catatan": catatan
    }

    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("laporan").insert(row).execute()
            return True, f"Laporan {new_id} berhasil disimpan di Supabase.", new_id
        except Exception as e:
            print(f"[Supabase] Error save_laporan: {e}")

    # Fallback lokal
    df = load_local_csv("laporan")
    new_df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    if save_local_csv("laporan", new_df):
        return True, f"Laporan {new_id} berhasil disimpan.", new_id
    return False, "Gagal menyimpan laporan.", ""


def update_status_laporan(id_laporan: str, status: str = "Diserahkan ke Puskesmas") -> Tuple[bool, str]:
    """Memperbarui status penyerahan laporan ke Puskesmas."""
    today = date.today().isoformat()
    client = get_supabase_client()
    if is_connected() and client:
        try:
            client.table("laporan").update({
                "status": status,
                "tanggal_serah": today
            }).eq("id_laporan", id_laporan).execute()
            return True, f"Laporan {id_laporan} berhasil diserahkan ke Puskesmas."
        except Exception as e:
            print(f"[Supabase] Error update_status_laporan: {e}")

    df = load_local_csv("laporan")
    if not df.empty and "id_laporan" in df.columns:
        match = df["id_laporan"] == id_laporan
        if match.any():
            df.loc[match, "status"] = status
            df.loc[match, "tanggal_serah"] = today
            save_local_csv("laporan", df)
            return True, f"Laporan {id_laporan} berhasil diperbarui statusnya."
    return False, f"Laporan {id_laporan} tidak ditemukan."
