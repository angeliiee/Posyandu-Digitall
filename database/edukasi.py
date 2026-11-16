"""
Modul Edukasi Kesehatan dan Rekomendasi Pertumbuhan Posyandu Digital
Menyediakan materi edukasi resmi berbasis pedoman Kemenkes RI / WHO
serta generator saran pertumbuhan terpersonalisasi untuk balita.
"""
from typing import Dict, Any, List


EDUKASI_ARTIKEL: List[Dict[str, Any]] = [
    {
        "id": "anc-10t",
        "icon": "🤰",
        "kategori": "Ibu Hamil",
        "judul": "Pemeriksaan Rutin Kehamilan (ANC 10T)",
        "ringkasan": "Pentingnya pemeriksaan minimal 6 kali selama kehamilan untuk memastikan ibu dan janin sehat optimal.",
        "poin_kunci": [
            "Pemeriksaan Trimester 1 (minimal 1x) oleh dokter untuk skrining awal risiko.",
            "Pemeriksaan Trimester 2 (minimal 2x) memantau tumbuh kembang janin & DJJ.",
            "Pemeriksaan Trimester 3 (minimal 3x) persiapan persalinan aman.",
            "Konsumsi rutin tablet tambah darah (minimal 90 tablet selama hamil) cegah anemia."
        ],
        "saran": "Pastikan membawa Buku KIA setiap kunjungan ke Posyandu atau Fasilitas Kesehatan.",
        "quiz": [
            {
                "q": "Berapa kali minimal pemeriksaan kehamilan (ANC) yang direkomendasikan selama masa hamil?",
                "opts": ["2 kali", "4 kali", "6 kali", "10 kali"],
                "ans": 2
            },
            {
                "q": "Berapa jumlah tablet tambah darah (TTD) yang harus dikonsumsi selama kehamilan?",
                "opts": ["30 tablet", "60 tablet", "90 tablet", "120 tablet"],
                "ans": 2
            },
            {
                "q": "Pemeriksaan ANC Trimester 1 paling tepat dilakukan oleh siapa untuk skrining awal?",
                "opts": ["Dukun beranak", "Dokter", "Apoteker", "Kader Posyandu"],
                "ans": 1
            },
            {
                "q": "Dokumen apa yang wajib dibawa setiap kunjungan ANC ke Posyandu?",
                "opts": ["KTP", "Kartu BPJS", "Buku KIA", "Akta Kelahiran"],
                "ans": 2
            }
        ]
    },
    {
        "id": "pantau-balita",
        "icon": "👶",
        "kategori": "Balita",
        "judul": "Pemantauan Tumbuh Kembang Setiap Bulan",
        "ringkasan": "Menimbang berat badan dan mengukur tinggi/panjang badan balita setiap bulan di Posyandu.",
        "poin_kunci": [
            "Timbangan naik (N) menunjukkan balita tumbuh sehat sesuai kurva KMS.",
            "Timbangan tidak naik (T) atau berada di bawah garis merah memerlukan evaluasi kader/bidan segera.",
            "Pengukuran lingkar kepala mendeteksi dini perkembangan volume otak.",
            "Pemberian Kapsul Vitamin A setiap bulan Februari dan Agustus."
        ],
        "saran": "Jangan lewatkan jadwal Posyandu bulanan untuk mendeteksi dini risiko gangguan pertumbuhan.",
        "quiz": []
    },
    {
        "id": "gizi-seimbang",
        "icon": "🥗",
        "kategori": "Gizi",
        "judul": "Pedoman Gizi Seimbang: Isi Piringku",
        "ringkasan": "Porsi makan seimbang untuk ibu hamil dan anak balita kaya protein hewani.",
        "poin_kunci": [
            "1/2 piring terdiri dari sayuran dan buah-buahan sumber vitamin dan mineral.",
            "1/2 piring lainnya dibagi antara makanan pokok (karbohidrat) dan lauk pauk (protein).",
            "Prioritaskan protein hewani (telur, ikan kembung, ayam, daging, hati) untuk cegah stunting.",
            "Batasi konsumsi gula, garam, dan minyak tambahan pada makanan balita."
        ],
        "saran": "Satu butir telur per hari sangat efektif mendukung percepatan pertumbuhan linear balita.",
        "quiz": [
            {
                "q": "Berapa bagian piring yang idealnya diisi sayuran dan buah-buahan?",
                "opts": ["1/4 piring", "1/3 piring", "1/2 piring", "3/4 piring"],
                "ans": 2
            },
            {
                "q": "Protein hewani mana yang direkomendasikan untuk mencegah stunting pada balita?",
                "opts": ["Mie instan", "Telur, ikan, daging, hati ayam", "Kerupuk", "Permen"],
                "ans": 1
            },
            {
                "q": "Apa yang harus dibatasi dalam makanan balita untuk menjaga gizi seimbang?",
                "opts": ["Sayuran", "Buah-buahan", "Gula, garam, dan minyak tambahan", "Nasi"],
                "ans": 2
            },
            {
                "q": "Panduan porsi makan seimbang yang dianjurkan Kemenkes disebut...?",
                "opts": ["Isi Piringku", "4 Sehat 5 Sempurna", "Diet Sehat", "Piring Sehat WHO"],
                "ans": 0
            }
        ]
    },
    {
        "id": "asi-mpasi",
        "icon": "🍼",
        "kategori": "Nutrisi Bayi",
        "judul": "Tahapan ASI Eksklusif dan MP-ASI Bertahap",
        "ringkasan": "Panduan pemberian makan bayi usia 0-24 bulan sesuai rekomendasi IDAI dan WHO.",
        "poin_kunci": [
            "0–6 Bulan: ASI Eksklusif tanpa makanan atau minuman lain sama sekali.",
            "6–8 Bulan: Mulai MP-ASI tekstur lumat/puree kental, 2–3 kali makan utama + ASI.",
            "9–11 Bulan: MP-ASI tekstur lembik/cincang halus (mashed), 3–4 kali makan utama + selingan.",
            "12–23 Bulan: Makanan keluarga bertekstur utuh dengan menu bergizi seimbang."
        ],
        "saran": "Selalu jaga kebersihan tangan dan peralatan saat mengolah dan menyajikan MP-ASI.",
        "quiz": []
    },
    {
        "id": "imunisasi-dasar",
        "icon": "💉",
        "kategori": "Imunisasi",
        "judul": "Jadwal Imunisasi Dasar Lengkap",
        "ringkasan": "Perlindungan terbaik anak dari bahaya penyakit yang dapat dicegah dengan imunisasi (PD3I).",
        "poin_kunci": [
            "< 24 Jam: Hepatitis B (HB-0).",
            "1 Bulan: BCG dan Polio 1.",
            "2, 3, 4 Bulan: DPT-HB-Hib 1-2-3, Polio tetes/suntik (IPV), dan PCV.",
            "9 Bulan: Campak-Rubella (MR) dosis pertama.",
            "18 Bulan: Imunisasi lanjutan (booster) DPT-HB-Hib dan Campak-Rubella."
        ],
        "saran": "Imunisasi aman, halal, dan tersedia gratis di Posyandu serta Puskesmas.",
        "quiz": [
            {
                "q": "Imunisasi Hepatitis B (HB-0) diberikan pada usia berapa?",
                "opts": ["1 bulan", "< 24 jam setelah lahir", "2 bulan", "6 bulan"],
                "ans": 1
            },
            {
                "q": "Imunisasi Campak-Rubella (MR) dosis pertama diberikan pada usia?",
                "opts": ["6 bulan", "9 bulan", "12 bulan", "18 bulan"],
                "ans": 1
            },
            {
                "q": "Di mana imunisasi dasar lengkap dapat diperoleh secara gratis?",
                "opts": ["Rumah Sakit Swasta", "Klinik Berbayar", "Posyandu dan Puskesmas", "Apotek"],
                "ans": 2
            },
            {
                "q": "Imunisasi BCG dan Polio 1 diberikan pada usia berapa?",
                "opts": ["< 24 jam", "1 bulan", "2 bulan", "6 bulan"],
                "ans": 1
            }
        ]
    },
    {
        "id": "cegah-stunting",
        "icon": "🛡️",
        "kategori": "Pencegahan",
        "judul": "Gerakan Bersama Pencegahan Stunting (1000 HPK)",
        "ringkasan": "Fokus pada 1000 Hari Pertama Kehidupan (sejak janin dalam kandungan hingga anak usia 2 tahun).",
        "poin_kunci": [
            "Penuhi nutrisi ibu sejak awal masa kehamilan.",
            "Inisiasi Menyusu Dini (IMD) dalam 1 jam pertama setelah kelahiran.",
            "Terapkan Pola Hidup Bersih dan Sehat (PHBS) serta gunakan air bersih dan jamban sehat.",
            "Pantau berkala grafik panjang/tinggi badan balita di Posyandu."
        ],
        "saran": "Stunting dapat dicegah dengan intervensi tepat pada 1000 Hari Pertama Kehidupan.",
        "quiz": [
            {
                "q": "Berapa lama periode '1000 Hari Pertama Kehidupan' dihitung?",
                "opts": ["Sejak lahir hingga 1 tahun", "Sejak janin dalam kandungan hingga anak usia 2 tahun", "Sejak lahir hingga 3 tahun", "Sejak usia 6 bulan hingga 2 tahun"],
                "ans": 1
            },
            {
                "q": "Apa singkatan dari IMD dalam konteks pencegahan stunting?",
                "opts": ["Imunisasi Massal Dasar", "Inisiasi Menyusu Dini", "Intervensi Makanan Dini", "Ikatan Medis Dasar"],
                "ans": 1
            },
            {
                "q": "Kapan IMD (Inisiasi Menyusu Dini) sebaiknya dilakukan?",
                "opts": ["6 jam setelah kelahiran", "24 jam setelah kelahiran", "1 jam pertama setelah kelahiran", "3 hari setelah kelahiran"],
                "ans": 2
            },
            {
                "q": "Faktor lingkungan apa yang berperan penting dalam pencegahan stunting?",
                "opts": ["Punya gadget", "Air bersih, jamban sehat, dan PHBS", "Rumah besar", "Hiburan yang banyak"],
                "ans": 1
            }
        ]
    }
]


def get_edukasi_list() -> List[Dict[str, Any]]:
    """Mengembalikan daftar materi edukasi kesehatan."""
    return EDUKASI_ARTIKEL


def get_saran_pertumbuhan(usia_bulan: float, status_gizi: str, z_bb: float = 0.0, z_tb: float = 0.0) -> Dict[str, Any]:
    """
    Menghasilkan saran pertumbuhan terpersonalisasi berdasarkan usia balita
    dan status antropometri saat ini (KMS / Z-Score).
    Bahasa sederhana, ramah orang tua, edukatif, dan bukan diagnosis medis.
    """
    age = float(usia_bulan)

    # 1. Tahap nutrisi berdasarkan usia
    if age < 6:
        fase_usia = "Fase ASI Eksklusif (0–5 Bulan)"
        rekomendasi_makan = (
            "Berikan ASI secara eksklusif sesering mungkin sesuai keinginan bayi (on-demand), "
            "minimal 8–12 kali sehari. Jangan berikan air putih, madu, formula, atau makanan lain "
            "sebelum genap berusia 6 bulan kecuali atas anjuran dokter."
        )
        tekstur_tips = "Hanya ASI tanpa makanan pendamping."
        stimulasi = "Lakukan kontak kulit (skin-to-skin), ajak bicara, dan beri stimulasi 'tummy time' saat bayi terjaga."
    elif age < 9:
        fase_usia = "Fase Pengenalan MP-ASI (6–8 Bulan)"
        rekomendasi_makan = (
            "Mulai berikan MP-ASI bertekstur bubur kental (puree) atau lumat halus. "
            "Berikan 2–3 kali makan per hari dengan porsi 2–3 sendok makan bertahap hingga 1/2 mangkuk (125 ml). "
            "Tetap lanjutkan pemberian ASI sesering mungkin."
        )
        tekstur_tips = "Bubur saring kental (tidak tumpah saat sendok dimiringkan)."
        stimulasi = "Kenalkan variasi rasa alami bahan makanan: protein hewani (telur, hati ayam, ikan), sayuran, dan buah."
    elif age < 12:
        fase_usia = "Fase MP-ASI Lembik / Mashed (9–11 Bulan)"
        rekomendasi_makan = (
            "Tingkatkan tekstur menjadi cincang halus, cincang kasar, atau makanan lunak (mashed). "
            "Jadwal makan: 3–4 kali makan utama ditambah 1–2 kali makanan selingan sehat (buah, biskuit bayi). "
            "Porsi 1/2 mangkuk berukuran 250 ml."
        )
        tekstur_tips = "Makanan cincang halus / finger food lunak yang dapat digenggam si kecil."
        stimulasi = "Latih anak makan sendiri untuk melatih koordinasi motorik tangan dan mulut."
    elif age < 24:
        fase_usia = "Fase Makanan Keluarga & Balita (12–23 Bulan)"
        rekomendasi_makan = (
            "Anak sudah dapat menikmati menu makanan keluarga yang diiris atau dicincang secukupnya. "
            "Pastikan menu seimbang mengandung karbohidrat, protein hewani berkualitas tinggi, lemak sehat, dan sayuran. "
            "ASI dapat dilanjutkan hingga usia 2 tahun."
        )
        tekstur_tips = "Menu makanan keluarga bergizi seimbang."
        stimulasi = "Ajak anak aktif bergerak, bermain interaktif, dan hindari paparan layar (screen time) berlebihan."
    else:
        fase_usia = "Fase Pertumbuhan Anak Balita (24–59 Bulan)"
        rekomendasi_makan = (
            "Terapkan panduan 'Isi Piringku': porsi seimbang karbohidrat, protein hewani, sayur, dan buah. "
            "Berikan 3 kali makan utama dan 2 kali selingan bergizi. Batasi jajanan berpemanis buatan dan pewarna."
        )
        tekstur_tips = "Makanan keluarga normal dengan variasi kaya warna dan rasa."
        stimulasi = "Aktivitas fisik bermain di luar ruangan, stimulasi kemandirian, dan pola tidur teratur 10–12 jam."

    # 2. Rekomendasi berdasarkan status antropometri
    status_lower = status_gizi.lower()
    if "stunting" in status_lower:
        status_badge = "⚠️ Membutuhkan Perhatian Tinggi (Stunting / Perawakan Pendek)"
        warna_status = "#d98686"
        analisis = (
            f"Panjang/tinggi badan si kecil saat ini berada di bawah kurva rujukan (Z-score TB/U: {z_tb:.2f}). "
            "Kondisi ini menunjukkan pertumbuhan linear anak membutuhkan dukungan asupan nutrisi protein "
            "dan pemantauan khusus secara rutin."
        )
        tindakan = [
            "Fokuskan asupan protein hewani tinggi setiap hari: telur (1-2 butir/hari), ikan, daging ayam, atau susu pertumbuhan.",
            "Pastikan anak tidak sering mengalami infeksi berulang (seperti diare atau batuk pilek) dengan menjaga kebersihan lingkungan.",
            "Konsultasikan hasil pengukuran ini kepada Kader Posyandu, Bidan Desa, atau Petugas Puskesmas untuk evaluasi intervensi PMT (Pemberian Makanan Tambahan)."
        ]
    elif "gizi kurang" in status_lower:
        status_badge = "⚠️ Memerlukan Peningkatan Bobot (Gizi Kurang)"
        warna_status = "#e6b787"
        analisis = (
            f"Berat badan si kecil berada di bawah kurva pertumbuhan normal untuk usianya (Z-score BB/U: {z_bb:.2f}). "
            "Diperlukan peningkatan kepadatan energi dan frekuensi makan yang teratur."
        )
        tindakan = [
            "Tambahkan asupan lemak sehat pada MP-ASI/makanan anak, seperti sedikit santan, minyak kelapa/sayur, atau mentega.",
            "Berikan protein hewani di setiap jadwal makan utama.",
            "Buat suasana makan yang menyenangkan tanpa paksaan agar anak menikmati waktu makannya.",
            "Konsultasikan ke kader posyandu untuk pemantauan kenaikan bobot mingguan."
        ]
    elif "lebih" in status_lower:
        status_badge = "ℹ️ Risiko Gizi Lebih"
        warna_status = "#b9acd6"
        analisis = (
            f"Berat badan si kecil berada di atas rata-rata rujukan pertumbuhan (Z-score BB/U: {z_bb:.2f}). "
            "Pertahankan komposisi nutrisi sehat dan ajak anak lebih aktif bergerak."
        )
        tindakan = [
            "Kurangi minuman berpemanis, biskuit tinggi gula, atau camilan berkalori kosong.",
            "Perbanyak sayur dan buah segar sebagai camilan sehat harian.",
            "Tingkatkan aktivitas fisik si kecil melalui permainan bergerak aktif.",
            "Hindari diet ketat untuk anak balita; cukup seimbangkan porsi makannya."
        ]
    else:
        status_badge = "✅ Pertumbuhan Optimal (Gizi Baik & Normal)"
        warna_status = "#8fb59a"
        analisis = (
            f"Selamat! Pertumbuhan si kecil terpantau sangat baik dan sesuai dengan kurva standar WHO "
            f"(Z-score BB/U: {z_bb:.2f}, TB/U: {z_tb:.2f})."
        )
        tindakan = [
            "Pertahankan pola makan bergizi seimbang dan jadwal makan yang teratur.",
            "Terus beri stimulasi perkembangan sesuai tahapan usia si kecil.",
            "Rutin hadir di Posyandu setiap bulan untuk memantau keberlanjutan pertumbuhan sehatnya."
        ]

    return {
        "fase_usia": fase_usia,
        "status_badge": status_badge,
        "warna_status": warna_status,
        "analisis": analisis,
        "rekomendasi_makan": rekomendasi_makan,
        "tekstur_tips": tekstur_tips,
        "stimulasi": stimulasi,
        "tindakan": tindakan,
        "catatan_kesehatan": (
            "📌 Catatan: Panduan ini bersifat edukasi tumbuh kembang balita dan bukan pengganti diagnosis medis. "
            "Segera konsultasikan dengan dokter atau bidan jika terdapat keluhan kesehatan pada anak."
        )
    }
