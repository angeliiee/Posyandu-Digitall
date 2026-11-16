"""
Layanan Gizi, Antropometri WHO & Skrining Maternal Kemenkes RI.
Menghitung Z-Score akurat (TB/U dan BB/U), kurva KMS WHO, serta klasifikasi risiko ibu hamil.
"""
import hashlib
import numpy as np
import pandas as pd
from typing import Tuple

AGES = [0, 6, 12, 24, 36, 48, 60]
REF = {
    ("Laki-laki", "tb"): ([49.9, 67.6, 75.7, 87.8, 96.1, 103.3, 110.0], [1.9, 2.3, 2.5, 3.2, 3.7, 4.1, 4.5]),
    ("Perempuan", "tb"): ([49.1, 65.7, 74.0, 86.4, 95.1, 102.7, 109.4], [1.9, 2.3, 2.6, 3.3, 3.8, 4.2, 4.6]),
    ("Laki-laki", "bb"): ([3.3, 7.9, 9.6, 12.2, 14.3, 16.3, 18.3], [0.4, 0.9, 1.1, 1.4, 1.7, 2.0, 2.4]),
    ("Perempuan", "bb"): ([3.2, 7.3, 8.9, 11.5, 13.9, 16.1, 18.2], [0.4, 0.9, 1.1, 1.5, 1.8, 2.2, 2.6]),
}


def ref(sex: str, kind: str, age: float) -> Tuple[float, float]:
    """Mengambil nilai median dan SD berdasarkan jenis kelamin, indikator (bb/tb), dan usia bulan."""
    s_key = sex if sex in ("Laki-laki", "Perempuan") else "Perempuan"
    m, s = REF[(s_key, kind)]
    return float(np.interp(age, AGES, m)), float(np.interp(age, AGES, s))


def zscore(sex: str, kind: str, age: float, val: float) -> float:
    """Menghitung nilai Z-score: (nilai_ukur - median) / SD."""
    m, s = ref(sex, kind, age)
    return round((val - m) / s, 2)


def kategori_tb_u(z: float) -> str:
    """Klasifikasi status tinggi/panjang badan menurut umur (TB/U) standar WHO/Permenkes."""
    if z < -3.0:
        return "Sangat Pendek (Severely Stunted)"
    elif z < -2.0:
        return "Pendek (Stunted)"
    elif z <= 3.0:
        return "Normal"
    else:
        return "Tinggi"


def kategori_bb_u(z: float) -> str:
    """Klasifikasi status berat badan menurut umur (BB/U) standar WHO/Permenkes."""
    if z < -3.0:
        return "Berat Badan Sangat Kurang (Severely Underweight)"
    elif z < -2.0:
        return "Berat Badan Kurang (Underweight)"
    elif z <= 1.0:
        return "Berat Badan Normal"
    else:
        return "Risiko Berat Badan Lebih"


def status_gizi(z_bb: float, z_tb: float) -> str:
    """Klasifikasi ringkas status gizi kombinasi TB/U dan BB/U."""
    if z_tb < -2:
        return "Stunting"
    if z_bb < -2:
        return "Gizi kurang"
    if z_bb > 2:
        return "Risiko gizi lebih"
    return "Normal"


def risiko_ibu(sis: int, dia: int, hb: float, lila: float) -> Tuple[str, str, str, str]:
    """
    Penilaian risiko maternal kehamilan:
    - KEK: LILA < 23.5 cm
    - Anemia: Hb < 11 g/dL
    - Hipertensi: Sistol >= 140 atau Diastol >= 90
    """
    kek = lila < 23.5
    anemia = hb < 11.0
    hip = (sis >= 140 or dia >= 90)
    n = int(kek) + int(anemia) + int(hip)
    r = "Risiko tinggi" if (hip or hb < 8.0 or n >= 2) else "Perlu pemantauan" if n == 1 else "Risiko rendah"
    return ("KEK" if kek else "Tidak KEK"), ("Anemia" if anemia else "Tidak anemia"), ("Hipertensi" if hip else "Normal"), r


def get_who_growth_curves(sex: str, kind: str) -> pd.DataFrame:
    """Menghasilkan dataset kurva standar WHO (usia 0-60 bulan) dengan garis -3SD, -2SD, Median, +2SD, +3SD."""
    ages = np.arange(0, 61)
    medians = [ref(sex, kind, a)[0] for a in ages]
    sds = [ref(sex, kind, a)[1] for a in ages]
    m_arr = np.array(medians)
    s_arr = np.array(sds)

    return pd.DataFrame({
        "usia_bulan": ages,
        "minus_3sd": np.round(m_arr - 3 * s_arr, 2),
        "minus_2sd": np.round(m_arr - 2 * s_arr, 2),
        "median": np.round(m_arr, 2),
        "plus_2sd": np.round(m_arr + 2 * s_arr, 2),
        "plus_3sd": np.round(m_arr + 3 * s_arr, 2),
    })


def hash_pw(p: str) -> str:
    """Mengenkripsi password menggunakan SHA-256 tersalt."""
    salt = "posyandu_digital_salt_2026"
    return hashlib.sha256((p + salt).encode("utf-8")).hexdigest()
