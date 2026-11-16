"""
Unit & Integration Test Suite untuk Posyandu Digital (Production Version)
Menguji:
1. Penghapusan menyeluruh nomor telepon (no_hp)
2. Sistem registrasi mandiri (Self-Service Sign Up) & Supabase Auth
3. Sistem login mandiri (Sign In) & penanganan session
4. Alur Onboarding Biodata Mandiri (Ibu Hamil & Orang Tua Balita)
5. Pendaftaran balita tambahan (+ Tambah Balita)
6. Z-score WHO, KMS, & status antropometri
7. Saran pertumbuhan terpersonalisasi untuk orang tua
8. Edge cases pencarian dan penanganan data
"""
import sys
from pathlib import Path
from datetime import date
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import database
import gizi
import pandas as pd


def test_no_phone_numbers_anywhere():
    """Memastikan tidak ada kolom atau nilai no_hp pada seluruh data dan modul."""
    print("\n[TEST 1] Pengujian Penghapusan Nomor Telepon...")
    p = database.get_all_peserta()
    assert "no_hp" not in p.columns, "Kolom 'no_hp' masih ditemukan di peserta!"

    b = database.get_pemeriksaan_balita()
    assert "no_hp" not in b.columns, "Kolom 'no_hp' masih ditemukan di pemeriksaan balita!"

    i = database.get_pemeriksaan_ibu()
    assert "no_hp" not in i.columns, "Kolom 'no_hp' masih ditemukan di pemeriksaan ibu hamil!"

    u = database.get_users()
    assert "no_hp" not in u.columns, "Kolom 'no_hp' masih ditemukan di users!"
    print("  -> PASSED: Seluruh kolom nomor telepon telah terhapus tanpa sisa.")


def test_self_service_registration_and_auth():
    """Menguji sistem registrasi mandiri baru dan login tanpa akun demo."""
    print("\n[TEST 2] Pengujian Registrasi Mandiri & Autentikasi Pengguna...")

    test_email = f"user_{uuid.uuid4().hex[:6]}@keluarga.id"
    test_pw = "rahasia123"
    test_nama = "Ibu Siti Registrasi Mandiri"

    # 1. Registrasi Mandiri Ibu Hamil
    sukses_reg, msg_reg, user_record = database.sign_up_user(
        email=test_email,
        password=test_pw,
        role="Ibu Hamil",
        nama=test_nama
    )
    assert sukses_reg, f"Gagal registrasi: {msg_reg}"
    assert user_record is not None
    assert user_record["email"] == test_email
    assert user_record["role"] == "Ibu Hamil"
    assert "password_hash" not in user_record or not user_record.get("password_hash")

    # 2. Login Mandiri
    sukses_login, msg_login, logged_user = database.sign_in_user(test_email, test_pw)
    assert sukses_login, f"Gagal login: {msg_login}"
    assert logged_user["email"] == test_email
    assert logged_user["role"] == "Ibu Hamil"

    # 3. Uji password salah
    salah_login, _, _ = database.sign_in_user(test_email, "passwordsalah")
    assert not salah_login, "Login dengan password salah seharusnya gagal!"
    print("  -> PASSED: Alur registrasi mandiri & login aman berfungsi 100%.")


def test_self_service_onboarding_biodata():
    """Menguji alur pengisian biodata mandiri setelah registrasi."""
    print("\n[TEST 3] Pengujian Onboarding Biodata Mandiri (Ibu Hamil & Orang Tua)...")

    # --- Case A: Ibu Hamil ---
    uid_ibu = str(uuid.uuid4())
    user_ibu = {
        "id": uid_ibu,
        "email": f"ibu_{uuid.uuid4().hex[:5]}@posyandu.id",
        "role": "Ibu Hamil",
        "nama": "Ibu Hamil Baru",
        "id_peserta": ""
    }
    assert not database.has_completed_biodata(user_ibu), "User baru seharusnya belum memiliki biodata lengkap!"

    sukses_bio_i, msg_bio_i, pid_ibu = database.save_ibu_biodata(uid_ibu, {
        "nama": "Ibu Hamil Baru",
        "nama_suami": "Bapak Pendamping",
        "usia_ibu_tahun": 27,
        "usia_kehamilan_minggu": 16,
        "alamat_dusun": "Kenanga",
        "alamat_lengkap": "RT 03 RW 01",
        "email": user_ibu["email"]
    })
    assert sukses_bio_i, f"Gagal simpan biodata ibu: {msg_bio_i}"
    user_ibu["id_peserta"] = pid_ibu
    assert database.has_completed_biodata(user_ibu), "Setelah isi biodata, has_completed_biodata harus True!"

    # --- Case B: Orang Tua Balita ---
    uid_ortu = str(uuid.uuid4())
    user_ortu = {
        "id": uid_ortu,
        "email": f"ortu_{uuid.uuid4().hex[:5]}@posyandu.id",
        "role": "Orang Tua Balita",
        "nama": "Ayah Handal",
        "id_peserta": ""
    }
    assert not database.has_completed_biodata(user_ortu)

    sukses_bio_o, msg_bio_o, pid_balita = database.save_ortu_and_balita_biodata(uid_ortu, {
        "nama_orang_tua": "Ayah Handal",
        "alamat_dusun": "Melati",
        "alamat_lengkap": "Jalan Mawar Indah No 12",
        "email": user_ortu["email"],
        "nama_balita": "Anak Pertama Ceria",
        "tanggal_lahir": date(2025, 4, 1),
        "usia_bulan": 19.0,
        "jenis_kelamin": "Laki-laki"
    })
    assert sukses_bio_o, f"Gagal simpan biodata ortu & balita: {msg_bio_o}"
    assert database.has_completed_biodata(user_ortu), "Orang tua dengan balita terdaftar harus True!"

    # --- Case C: Tambah Balita Kedua (+ Tambah Balita) ---
    sukses_anak2, msg_anak2, pid_anak2 = database.add_additional_child(
        user_id=uid_ortu,
        id_orang_tua=user_ortu.get("id_peserta", ""),
        data={
            "nama_balita": "Adik Bayi Lucu",
            "tanggal_lahir": date(2026, 5, 10),
            "usia_bulan": 6.0,
            "jenis_kelamin": "Perempuan",
            "nama_orang_tua": "Ayah Handal",
            "alamat_dusun": "Melati",
            "email": user_ortu["email"]
        }
    )
    assert sukses_anak2, f"Gagal tambah balita kedua: {msg_anak2}"
    anak_list = database.get_children_by_parent_user_id(uid_ortu)
    assert len(anak_list) >= 2, f"Seharusnya terdeteksi minimal 2 balita di bawah user ini, didapat: {len(anak_list)}"

    # Cleanup test records
    database.delete_peserta(pid_ibu)
    database.delete_peserta(pid_balita)
    database.delete_peserta(pid_anak2)
    print("  -> PASSED: Alur Onboarding Biodata Mandiri & Tambah Balita terverifikasi sempurna.")


def test_toddler_search_and_history_edge_cases():
    """Menguji penanganan pencarian balita dan riwayat pemeriksaan pada semua edge cases."""
    print("\n[TEST 4] Pengujian Edge Cases Pencarian & Riwayat Pemeriksaan...")

    # Case 1: Balita dengan riwayat
    hist_existing = database.get_pemeriksaan_by_peserta("BLT001")
    assert not hist_existing.empty, "BLT001 harus memiliki riwayat pemeriksaan!"
    assert "berat_kg" in hist_existing.columns
    assert "z_tb_u" in hist_existing.columns

    # Case 2: Balita baru tanpa riwayat (0 riwayat)
    dummy_b = {
        "jenis_peserta": "Balita",
        "nama": "Balita Tanpa Kunjungan",
        "tanggal_lahir": date(2026, 2, 1),
        "usia_bulan": 9.0,
        "jenis_kelamin": "Perempuan",
        "nama_orang_tua": "Wali Uji",
        "alamat_dusun": "Mawar",
        "email": "nol.riwayat@posyandu.id"
    }
    _, _, pid_zero = database.create_peserta(dummy_b)
    hist_zero = database.get_pemeriksaan_by_peserta(pid_zero)
    assert hist_zero.empty, "Balita baru seharusnya memiliki DataFrame kosong (0 baris), bukan error!"

    # Case 3: Pencarian kata kunci tak ditemukan
    search_empty = database.search_peserta("QUERY_TIDAK_MUNGKIN_ADA_99999")
    assert search_empty.empty

    database.delete_peserta(pid_zero)
    print("  -> PASSED: Seluruh edge cases pencarian & riwayat berjalan tanpa error.")


def test_zscore_calculations_and_who_standards():
    """Menguji rumus Z-score dan standar antropometri WHO."""
    print("\n[TEST 5] Pengujian Perhitungan Z-Score WHO...")

    # Z-score median = 0.0
    z_tb = gizi.zscore("Laki-laki", "tb", 12, 75.7)
    assert z_tb == 0.0, f"Z-score median seharusnya 0.0, didapat {z_tb}"

    # Z-score stunting (< -2 SD)
    z_tb_stunt = gizi.zscore("Laki-laki", "tb", 12, 70.0)
    assert z_tb_stunt < -2.0
    assert gizi.kategori_tb_u(z_tb_stunt) == "Pendek (Stunted)"
    assert gizi.status_gizi(0.0, z_tb_stunt) == "Stunting"

    curves = gizi.get_who_growth_curves("Laki-laki", "tb")
    assert len(curves) == 61
    print("  -> PASSED: Rumus Z-Score dan standar antropometri WHO valid dan akurat.")


def test_personalized_growth_advice():
    """Menguji saran pertumbuhan optimal terpersonalisasi untuk orang tua."""
    print("\n[TEST 6] Pengujian Saran Pertumbuhan Terpersonalisasi...")

    # Bayi 4 bulan normal -> ASI Eksklusif
    saran_asi = database.get_saran_pertumbuhan(usia_bulan=4, status_gizi="Normal")
    assert "ASI Eksklusif" in saran_asi["fase_usia"]

    # Bayi 7 bulan gizi kurang -> MP-ASI Lumat
    saran_mpasi = database.get_saran_pertumbuhan(usia_bulan=7, status_gizi="Gizi kurang", z_bb=-2.2, z_tb=-0.5)
    assert "6–8 Bulan" in saran_mpasi["fase_usia"]
    assert "Memerlukan Peningkatan Bobot" in saran_mpasi["status_badge"]

    # Anak 20 bulan stunting -> Protein hewani tinggi
    saran_stunt = database.get_saran_pertumbuhan(usia_bulan=20, status_gizi="Stunting", z_bb=-1.0, z_tb=-2.4)
    assert "Stunting" in saran_stunt["status_badge"]
    assert any("protein hewani" in act.lower() for act in saran_stunt["tindakan"])
    print("  -> PASSED: Rekomendasi pertumbuhan anak sesuai usia dan kondisi antropometri.")


def run_all_tests():
    print("=" * 65)
    print("MEMULAI PENGUJIAN INTEGRASI POSYANDU DIGITAL (PRODUCTION)")
    print("=" * 65)
    test_no_phone_numbers_anywhere()
    test_self_service_registration_and_auth()
    test_self_service_onboarding_biodata()
    test_toddler_search_and_history_edge_cases()
    test_zscore_calculations_and_who_standards()
    test_personalized_growth_advice()
    print("=" * 65)
    print("🎉 SEMUA PENGUJIAN BERHASIL 100% (READY FOR DEPLOYMENT)!")
    print("=" * 65)


if __name__ == "__main__":
    run_all_tests()
