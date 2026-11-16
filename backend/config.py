"""
Konfigurasi Aplikasi Posyandu Digital (Jejak Tumbuh)
Menyimpan path direktori, konstanta tema pastel pink cerah, menu navigasi, dan konfigurasi lingkungan.
"""
from pathlib import Path
from datetime import date

# Direktori Utama
BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
ASSETS_DIR = ROOT_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "JEJAK_TUMBUH.jpeg"
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = "Posyandu Digital"
APP_SUBTITLE = "Jejak Tumbuh"
APP_VERSION = "v4.0 (Modular & Pastel Edition)"
APP_ICON = "🌸"

TODAY = date.today()
BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

# PALET WARNA IDENTITAS VISUAL ORIGINAL: BRIGHT PASTEL PINK & SOFT PEACH
THEME = {
    "primary": "#E8A9BD",            # Bright pastel pink utama
    "primary_hover": "#D889A1",      # Pastel pink hover
    "primary_light": "#FFF0F4",      # Soft pink tint
    "primary_dark": "#B8657E",       # Deep pastel rose for emphasis
    "bg_main": "#FFF9FB",            # Background utama (bright & clean)
    "bg_card": "#FFFFFF",            # Card background
    "bg_secondary": "#FCE4EC",       # Soft pink secondary background
    "bg_peach": "#FFF3ED",           # Soft peach tint
    "accent_peach": "#FB923C",       # Peach accent
    "accent_green": "#10B981",       # Status normal / rujukan WHO median
    "accent_amber": "#F59E0B",       # Perlu pemantauan / gizi kurang
    "accent_red": "#EF4444",         # Stunting / risiko tinggi
    "accent_lavender": "#C084FC",    # Risiko gizi lebih / aksen
    "accent_sky": "#38BDF8",         # Info / aksen anak laki-laki
    "text_main": "#343044",          # Dark neutral text
    "text_muted": "#6B6576",         # Muted body text
    "text_light": "#8C8599",         # Subtitle text
    "border_light": "rgba(232, 169, 189, 0.35)", # Pastel pink border
    "border_glow": "rgba(232, 169, 189, 0.65)",
    "shadow_soft": "0 8px 24px rgba(232, 169, 189, 0.15)",
    "shadow_hover": "0 14px 32px rgba(232, 169, 189, 0.28)",
}

CHART_PALETTE = [
    THEME["primary"],
    THEME["accent_green"],
    THEME["accent_peach"],
    THEME["accent_lavender"],
    THEME["accent_sky"],
    THEME["accent_red"],
    "#EC4899",
    "#14B8A6"
]

FONT_FAMILY = "Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"

MENU = {
    "Kader": [
        "🏠 Dashboard Posyandu",
        "👥 Data Peserta & Riwayat",
        "🧒 Pemeriksaan Balita",
        "🤰 Pemeriksaan Ibu Hamil",
        "📊 Laporan Visualisasi Dinamis",
        "🗂️ Riwayat Laporan Puskesmas",
        "📚 Pusat Edukasi Posyandu"
    ],
    "Ibu Hamil": [
        "🏠 Dashboard Kehamilan",
        "📖 Buku KIA Digital",
        "👤 Profil & Biodata Ibu",
        "📚 Pusat Edukasi Posyandu"
    ],
    "Orang Tua Balita": [
        "🏠 Dashboard Tumbuh Kembang",
        "📈 Grafik Z-Score & KMS",
        "👶 Data & Tambah Balita",
        "📚 Pusat Edukasi Posyandu"
    ]
}
