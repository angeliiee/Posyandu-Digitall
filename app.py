"""
====================================================================
POSYANDU DIGITAL (JEJAK TUMBUH) - v3.5 (PRODUCTION & REDESIGN)
Full-Stack Web Application — Dark Navy Glassmorphism Theme
Terintegrasi Supabase Auth & PostgreSQL, WHO Antropometri,
KMS Digital, Laporan Visualisasi Dinamis, dan Modul Edukasi
====================================================================
"""
import base64
import io
from datetime import date, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import database
import gizi

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Posyandu Digital — Jejak Tumbuh",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Direktori dan Aset
ROOT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = ROOT_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "JEJAK_TUMBUH.jpeg"

TODAY = date.today()
BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

# Palet Warna Pastel Pink Identitas Utama
BG_DARK = "#15101a"
BG_CARD = "rgba(255, 255, 255, 0.94)"
BORDER_COLOR = "rgba(232, 169, 189, 0.35)"
TEXT_WHITE = "#2d1b2e"
TEXT_MUTED = "#8f7591"
TEXT_SUB = "#6e5270"
PRIMARY_PINK = "#e87a9e"
PRIMARY_BLUE = "#e87a9e"
ACCENT_PURPLE = "#a855f7"
ACCENT_GREEN = "#10b981"
ACCENT_PEACH = "#f97316"
ACCENT_RED = "#ef4444"
ACCENT_LAV = "#c084fc"
ACCENT_SKY = "#0284c7"

CHART_PALETTE = [PRIMARY_PINK, ACCENT_GREEN, ACCENT_PURPLE, ACCENT_PEACH, ACCENT_RED, ACCENT_LAV, ACCENT_SKY, "#fbbf24"]
FONT = "Plus Jakarta Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"

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
        "📚 Edukasi Kehamilan"
    ],
    "Orang Tua Balita": [
        "🏠 Dashboard Tumbuh Kembang",
        "📈 Grafik Z-Score & KMS",
        "👶 Data & Tambah Balita",
        "📚 Edukasi Gizi & MP-ASI"
    ]
}


# ====================================================================
# HELPER: LOGO BASE64 & TANGGAL
# ====================================================================
@st.cache_data
def get_logo_base64() -> str:
    """Mengambil logo resmi dalam bentuk data URI Base64."""
    if LOGO_PATH.exists():
        try:
            raw = LOGO_PATH.read_bytes()
            b64 = base64.b64encode(raw).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"
        except Exception:
            pass
    return "https://raw.githubusercontent.com/adindaadeliafutri6-gif/Posyandu-Digital/main/JEJAK%20TUMBUH.jpeg"


def fmt_date(d) -> str:
    """Format tanggal Indonesia yang aman."""
    if pd.isna(d) or d == "" or d is None:
        return "-"
    try:
        return pd.to_datetime(d).strftime("%d %b %Y")
    except Exception:
        return str(d)


# ====================================================================
# CSS PINK PASTEL — LANDING PAGE ONLY
# ====================================================================

# ====================================================================
# TEMA PASTEL PINK: DUAL ENGINE (LIGHT & DARK MODE)
# ====================================================================
from frontend.styles.css import inject_app_css, get_theme_palette
from frontend.components.posyandu_animation import get_posyandu_animation_svg
from frontend.components.edu_carousel import render_edu_carousel_html

def get_current_theme_is_dark() -> bool:
    """Mengambil status Dark Mode dari session state."""
    if "is_dark_theme" not in st.session_state:
        st.session_state["is_dark_theme"] = False
    return st.session_state["is_dark_theme"]

def inject_landing_css():
    """Inject CSS tema pastel pink untuk landing page."""
    is_dark = get_current_theme_is_dark()
    inject_app_css(is_dark=is_dark, is_landing=True)

def inject_custom_css(logged_in: bool = True):
    """Inject CSS tema pastel pink untuk aplikasi (dashboard & internal pages)."""
    is_dark = get_current_theme_is_dark()
    inject_app_css(is_dark=is_dark, is_landing=not logged_in)

def render_theme_toggle_button():
    """Komponen toggle Light / Dark Mode interaktif."""
    is_dark = get_current_theme_is_dark()
    col_t1, col_t2 = st.columns([8, 2])
    with col_t2:
        btn_label = "☀️ Mode Terang (Light)" if is_dark else "🌙 Mode Gelap (Dark)"
        if st.button(btn_label, key="theme_toggle_btn", use_container_width=True):
            st.session_state["is_dark_theme"] = not is_dark
            st.rerun()

def page_header(title: str, subtitle: str = ""):
    """Header Banner terpadu."""
    parts = title.split(" ", 1)
    icon = parts[0] if len(parts) > 1 else "🌸"
    clean_title = parts[1] if len(parts) > 1 else title
    st.markdown(
        f"""
        <div class="hdr-banner">
            <div class="hdr-icon">{icon}</div>
            <div>
                <h1>{clean_title}</h1>
                {"<p>" + subtitle + "</p>" if subtitle else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


_CARD_COUNTER = [0]
def chart_card(target, chart_obj):
    """Menampilkan grafik di dalam kartu visual yang seragam dengan palet pastel pink dinamis."""
    is_dark = get_current_theme_is_dark()
    pal = get_theme_palette(is_dark)
    
    ch = (
        chart_obj.configure(background="transparent", font=FONT)
        .configure_view(stroke=None)
        .configure_axis(
            gridColor=pal["chart_grid"],
            domainColor=pal["chart_domain"],
            tickColor=pal["chart_domain"],
            labelColor=pal["chart_label"],
            titleColor=pal["chart_title"],
            labelFontSize=11,
            titleFontSize=11,
            titleFontWeight=600
        )
        .configure_title(color=pal["chart_title"], fontSize=13, fontWeight=700, anchor="start", offset=10, font=FONT)
        .configure_legend(labelColor=pal["chart_label"], titleColor=pal["chart_title"], symbolType="circle", labelFontSize=11)
        .configure_range(category=pal["chart_palette"])
    )
    _CARD_COUNTER[0] += 1
    with target.container(border=True, key=f"card_{_CARD_COUNTER[0]}"):
        st.altair_chart(ch, theme=None, use_container_width=True)
def render_interactive_table(
    df: pd.DataFrame,
    default_columns: Optional[List[str]] = None,
    table_id: str = "table",
    search_placeholder: str = "🔍 Cari data..."
) -> pd.DataFrame:
    """Tabel interaktif dengan dropdown pemilih variabel kolom, pencarian, dan pengurutan."""
    if df.empty:
        st.info("Tidak ada data untuk ditampilkan.")
        return df

    all_cols = list(df.columns)
    valid_defaults = [c for c in (default_columns or all_cols) if c in all_cols]
    if not valid_defaults:
        valid_defaults = all_cols[:min(8, len(all_cols))]

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([3, 2, 1])

    selected_cols = col_ctrl1.multiselect(
        "Pilih variabel / kolom tabel:",
        options=all_cols,
        default=valid_defaults,
        key=f"col_sel_{table_id}"
    )

    if not selected_cols:
        st.warning("Silakan pilih minimal 1 variabel untuk menampilkan tabel.")
        return df

    q = col_ctrl2.text_input("Pencarian:", placeholder=search_placeholder, key=f"q_{table_id}")
    sort_col = col_ctrl3.selectbox("Urutkan:", options=selected_cols, key=f"sort_{table_id}")

    filtered_df = df.copy()
    if q.strip():
        mask = np.column_stack([
            filtered_df[col].astype(str).str.contains(q.strip(), case=False, na=False)
            for col in selected_cols
        ]).any(axis=1)
        filtered_df = filtered_df[mask]

    if sort_col and sort_col in filtered_df.columns:
        filtered_df = filtered_df.sort_values(sort_col, ascending=True)

    display_df = filtered_df[selected_cols]
    st.dataframe(
        display_df,
        hide_index=True,
        width="stretch",
        height=min(450, 40 + len(display_df) * 35)
    )
    st.caption(f"Menampilkan {len(display_df)} dari total {len(df)} baris data.")
    return display_df


# ====================================================================
# GRAFIK Z-SCORE WHO & PERKEMBANGAN WAKTU
# ====================================================================
def render_zscore_growth_view(history_df: pd.DataFrame, child_name: str, sex: str):
    """Visualisasi Z-Score WHO dengan batas -2 SD (stunting), 0 SD (median), +2 SD."""
    if history_df.empty:
        st.info(f"Belum ada riwayat pemeriksaan untuk {child_name}.")
        return

    hist = history_df.sort_values("tanggal_pemeriksaan").copy()
    latest = hist.iloc[-1]

    z_tb = float(latest.get("z_tb_u", 0.0))
    z_bb = float(latest.get("z_bb_u", 0.0))
    status = latest.get("status_gizi", "Normal")

    c1, c2, c3 = st.columns(3)
    c1.metric("Z-Score TB/U (Stunting)", f"{z_tb:+.2f}", gizi.kategori_tb_u(z_tb), delta_color="off")
    c2.metric("Z-Score BB/U (Gizi)", f"{z_bb:+.2f}", gizi.kategori_bb_u(z_bb), delta_color="off")
    c3.metric("Status Gizi Terkini", status, f"Usia {latest.get('usia_bulan', 0):.0f} bln", delta_color="off")

    hist["tanggal_label"] = hist["tanggal_pemeriksaan"].dt.strftime("%d/%m/%Y")
    long_z = hist[["tanggal_label", "tanggal_pemeriksaan", "z_tb_u", "z_bb_u"]].melt(
        id_vars=["tanggal_label", "tanggal_pemeriksaan"],
        value_vars=["z_tb_u", "z_bb_u"],
        var_name="Indikator",
        value_name="Z_Score"
    )
    long_z["Indikator"] = long_z["Indikator"].map({"z_tb_u": "TB/U (Tinggi)", "z_bb_u": "BB/U (Berat)"})

    r_minus2 = alt.Chart(pd.DataFrame({"y": [-2]})).mark_rule(color=ACCENT_RED, strokeDash=[5, 4]).encode(y="y:Q")
    r_zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color=ACCENT_GREEN, strokeDash=[2, 2]).encode(y="y:Q")
    r_plus2 = alt.Chart(pd.DataFrame({"y": [2]})).mark_rule(color=ACCENT_LAV, strokeDash=[5, 4]).encode(y="y:Q")

    chart_z = alt.Chart(long_z).mark_line(point=alt.OverlayMarkDef(size=75)).encode(
        x=alt.X("tanggal_label:N", sort=None, title="Tanggal Pemeriksaan"),
        y=alt.Y("Z_Score:Q", scale=alt.Scale(domain=[-4, 4]), title="Nilai Z-Score"),
        color=alt.Color("Indikator:N", scale=alt.Scale(range=[PRIMARY_BLUE, ACCENT_PURPLE])),
        tooltip=["tanggal_label", "Indikator", alt.Tooltip("Z_Score:Q", format="+.2f")]
    ).properties(title=f"Perkembangan Z-Score {child_name} dari Waktu ke Waktu", height=270)

    chart_card(st, chart_z + r_minus2 + r_zero + r_plus2)
    st.caption("Garis merah putus-putus = batas -2 SD (indikasi stunting/gizi kurang). Garis hijau = median normal (0 SD).")


# ====================================================================
# GRAFIK KURVA KMS WHO
# ====================================================================
def render_kms_chart(child_df: pd.DataFrame, sex: str, kind: str, ycol: str, title: str, ytitle: str):
    """Menampilkan kurva KMS WHO dengan pita -2 s.d. +2 SD dan titik balita."""
    curves = gizi.get_who_growth_curves(sex, kind)
    band = alt.Chart(curves).mark_area(opacity=0.2, color=ACCENT_GREEN).encode(
        x="usia_bulan:Q",
        y="minus_2sd:Q",
        y2="plus_2sd:Q"
    )
    med = alt.Chart(curves).mark_line(color="#10b981", strokeDash=[4, 3], strokeWidth=1.5).encode(
        x="usia_bulan:Q",
        y="median:Q"
    )
    pts = alt.Chart(child_df).mark_line(
        point=alt.OverlayMarkDef(size=80, color=PRIMARY_BLUE, filled=True),
        color=PRIMARY_BLUE,
        strokeWidth=2.5
    ).encode(
        x=alt.X("usia_bulan:Q", title="Usia (bulan)"),
        y=alt.Y(f"{ycol}:Q", scale=alt.Scale(zero=False), title=ytitle),
        tooltip=["tanggal_pemeriksaan:T", "usia_bulan", ycol]
    )
    return (band + med + pts).properties(title=title, height=270)


# ====================================================================
# LANDING PAGE REDESIGN: DARK NAVY, GLASSMORPHISM & PREVIEW DASHBOARD
# ====================================================================

# ====================================================================
# LANDING PAGE RESMI: TEMA PASTEL PINK MODERN & INTERAKTIF
# ====================================================================
def landing_and_auth_page():
    is_dark = get_current_theme_is_dark()
    inject_landing_css()
    logo_src = get_logo_base64()
    db_status = database.get_db_status()
    pal = get_theme_palette(is_dark)

    # ── THEME TOGGLE (POJOK ATAS) ──
    col_t1, col_t2 = st.columns([8, 2])
    with col_t2:
        btn_theme = "☀️ Light" if is_dark else "🌙 Dark"
        if st.button(btn_theme, key="landing_theme_toggle", use_container_width=True):
            st.session_state["is_dark_theme"] = not is_dark
            st.rerun()

    # ── HEADER RESMI: LOGO & JUDUL POSYANDU DIGITAL ──
    st.markdown(
        f"""
        <div style="text-align:center; padding: 2.2rem 1rem 1.2rem; max-width: 600px; margin: 0 auto;">
            <div style="position:relative; display:inline-block; margin-bottom: 1.2rem;">
                <img src="{logo_src}" style="width: 105px; height: 105px; border-radius: 28px; object-fit: cover; border: 3px solid {pal['primary']}; box-shadow: {pal['shadow_glow']};" alt="Logo Posyandu">
                <span style="position:absolute; bottom:-6px; right:-6px; font-size:1.6rem;">🌸</span>
            </div>
            <h1 style="font-size: 2.4rem; font-weight: 900; color: {pal['text_title']}; margin-bottom: 0.3rem; letter-spacing: -0.02em;">
                Posyandu Digital
            </h1>
            <p style="font-size: 1.05rem; font-weight: 600; color: {pal['primary']}; margin-bottom: 0.6rem;">
                Jejak Tumbuh &bull; Layanan Kesehatan Cerdas Keluarga
            </p>
            <div style="display:inline-flex; align-items:center; gap:6px; padding: 4px 14px; border-radius: 99px; background: {pal['primary_light']}; border: 1px solid {pal['border_glass']}; font-size: 0.78rem; font-weight: 700; color: {pal['primary']};">
                {db_status['mode_label']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── KOTAK LOGIN & DAFTAR AKUN BARU ──
    col_l, col_center, col_r = st.columns([1, 1.8, 1])
    with col_center:
        tab_login, tab_daftar = st.tabs(["🔐 Masuk (Login)", "📝 Daftar Akun Baru"])

        # --- TAB LOGIN ---
        with tab_login:
            st.markdown(f"<p style='color:{pal['text_muted']}; font-size:0.9rem; margin-top:0.4rem;'>Silakan masuk dengan email dan kata sandi terdaftar Anda.</p>", unsafe_allow_html=True)

            with st.form("form_login_landing"):
                email_in = st.text_input("Alamat Email", placeholder="contoh: ibu.siti@gmail.com")
                pw_in = st.text_input("Password", type="password", placeholder="Masukkan password Anda")
                submit_login = st.form_submit_button("Masuk ke Dashboard 🚀", type="primary", use_container_width=True)

                if submit_login:
                    if not email_in.strip() or not pw_in:
                        st.error("Silakan masukkan alamat email dan password.")
                    else:
                        sukses, msg, user_profile = database.sign_in_user(email_in, pw_in)
                        if sukses and user_profile:
                            st.session_state["user"] = user_profile
                            st.success("Login berhasil! Mengalihkan ke dashboard...")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")

            st.markdown(
                f"""
                <div style="text-align:center; margin-top: 1rem; padding: 10px; background:{pal['primary_light']}; border-radius:12px; border: 1px dashed {pal['border_glass']}; font-size:0.84rem; color:{pal['text_main']};">
                    Belum punya akun? Klik tab <b>'Daftar Akun Baru'</b> di atas untuk registrasi cepat.
                </div>
                """,
                unsafe_allow_html=True
            )

        # --- TAB DAFTAR AKUN BARU ---
        with tab_daftar:
            st.markdown(f"<p style='color:{pal['text_muted']}; font-size:0.9rem; margin-top:0.4rem;'>Registrasi mandiri terintegrasi langsung dengan database Posyandu.</p>", unsafe_allow_html=True)

            with st.form("form_register_landing", clear_on_submit=False):
                role_pilihan = st.selectbox(
                    "Daftar Sebagai *",
                    options=["Ibu Hamil", "Orang Tua Balita", "Kader"],
                    help="Pilih peran Anda di Posyandu"
                )
                nama_lengkap = st.text_input("Nama Lengkap Anda *", placeholder="contoh: Siti Aminah")
                email_reg = st.text_input("Alamat Email *", placeholder="contoh: siti.aminah@gmail.com")
                pw_reg = st.text_input("Password (minimal 6 karakter) *", type="password", placeholder="Buat password aman")
                pw_conf = st.text_input("Konfirmasi Password *", type="password", placeholder="Ulangi password di atas")

                submit_reg = st.form_submit_button("Daftarkan Akun Sekarang 🌸", type="primary", use_container_width=True)

                if submit_reg:
                    if not nama_lengkap.strip():
                        st.error("Nama lengkap wajib diisi.")
                    elif not email_reg.strip() or "@" not in email_reg:
                        st.error("Masukkan alamat email yang valid.")
                    elif len(pw_reg) < 6:
                        st.error("Password minimal 6 karakter.")
                    elif pw_reg != pw_conf:
                        st.error("Konfirmasi password tidak cocok.")
                    else:
                        sukses_reg, msg_reg, created_user = database.sign_up_user(
                            email=email_reg,
                            password=pw_reg,
                            role=role_pilihan,
                            nama=nama_lengkap
                        )
                        if sukses_reg:
                            st.success(f"✅ {msg_reg}")
                            st.balloons()
                            st.session_state["user"] = created_user
                            st.rerun()
                        else:
                            st.error(f"❌ {msg_reg}")

    # ── FOOTER MINIMALIS & BERSIH ──
    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 3.5rem; padding-bottom: 2rem; font-size: 0.82rem; color: {pal['text_muted']};">
            &copy; 2026 Posyandu Digital &bull; Jejak Tumbuh. Seluruh hak cipta dilindungi.
        </div>
        """,
        unsafe_allow_html=True
    )


def view_onboarding_biodata(user: Dict[str, Any]):
    """Tampilan pengisian biodata wajib setelah registrasi akun baru."""
    role = user.get("role", "")
    user_id = str(user.get("id", ""))
    nama_user = user.get("nama", "")
    email_user = user.get("email", "")

    page_header(f"👋 Selamat Datang, {nama_user}!", "Silakan lengkapi biodata Anda terlebih dahulu untuk memulai pemantauan kesehatan.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            if role == "Ibu Hamil":
                st.markdown("### 🤰 Lengkapi Biodata Kehamilan Anda")
                st.caption("Data ini akan digunakan untuk buku KIA digital dan pemantauan jadwal HPL.")

                with st.form("form_biodata_ibu"):
                    n_ibu = st.text_input("Nama Lengkap Ibu *", value=nama_user)
                    n_suami = st.text_input("Nama Suami / Pendamping *", placeholder="Nama suami/pendamping")
                    c_a, c_b = st.columns(2)
                    u_ibu = c_a.number_input("Usia Ibu (Tahun) *", min_value=15, max_value=55, value=28)
                    u_hamil = c_b.number_input("Usia Kehamilan Saat Ini (Minggu) *", min_value=1, max_value=43, value=12)

                    dusun = st.selectbox("Wilayah Dusun Domisili *", ["Melati", "Mawar", "Kenanga", "Anggrek"])
                    alamat = st.text_input("Alamat Lengkap / RT-RW", placeholder="RT 02 / RW 01...")

                    submit_bio_i = st.form_submit_button("Simpan Biodata & Buka Dashboard 🚀", type="primary", width="stretch")

                    if submit_bio_i:
                        if not n_ibu.strip() or not n_suami.strip():
                            st.error("Nama ibu dan nama suami/pendamping wajib diisi.")
                        else:
                            sukses, msg, new_pid = database.save_ibu_biodata(user_id, {
                                "nama": n_ibu,
                                "nama_suami": n_suami,
                                "usia_ibu_tahun": u_ibu,
                                "usia_kehamilan_minggu": u_hamil,
                                "alamat_dusun": dusun,
                                "alamat_lengkap": alamat,
                                "email": email_user
                            })
                            if sukses:
                                st.success(f"✅ {msg}")
                                st.session_state["user"]["id_peserta"] = new_pid
                                st.session_state["user"]["nama"] = n_ibu
                                st.session_state["user"]["alamat_dusun"] = dusun
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")

            elif role == "Orang Tua Balita":
                st.markdown("### 👶 Lengkapi Biodata Si Kecil & Keluarga")
                st.caption("Daftarkan anak balita pertama Anda untuk mulai memantau kurva KMS dan Z-Score.")

                with st.form("form_biodata_ortu"):
                    n_ortu = st.text_input("Nama Orang Tua (Ayah / Ibu) *", value=nama_user)
                    dusun = st.selectbox("Wilayah Dusun Domisili *", ["Melati", "Mawar", "Kenanga", "Anggrek"])
                    alamat = st.text_input("Alamat Lengkap / RT-RW", placeholder="RT 01 / RW 03...")

                    st.markdown("---")
                    st.markdown("#### Data Balita Pertama")
                    n_balita = st.text_input("Nama Lengkap Balita *", placeholder="contoh: Muhammad Rizki")
                    c_x, c_y = st.columns(2)
                    tgl_lahir = c_x.date_input("Tanggal Lahir Balita *", value=date(TODAY.year - 1, 1, 1))
                    jk = c_y.selectbox("Jenis Kelamin *", ["Laki-laki", "Perempuan"])

                    usia_bln = max(0.0, round((TODAY.year - tgl_lahir.year) * 12 + TODAY.month - tgl_lahir.month + (TODAY.day - tgl_lahir.day) / 30.4, 1))
                    st.caption(f"Usia si kecil saat ini: **{usia_bln:.1f} bulan**")

                    submit_bio_o = st.form_submit_button("Simpan Biodata & Buka Dashboard 🚀", type="primary", width="stretch")

                    if submit_bio_o:
                        if not n_ortu.strip() or not n_balita.strip():
                            st.error("Nama orang tua dan nama balita wajib diisi.")
                        else:
                            sukses, msg, new_bid = database.save_ortu_and_balita_biodata(user_id, {
                                "nama_orang_tua": n_ortu,
                                "alamat_dusun": dusun,
                                "alamat_lengkap": alamat,
                                "email": email_user,
                                "nama_balita": n_balita,
                                "tanggal_lahir": tgl_lahir,
                                "usia_bulan": usia_bln,
                                "jenis_kelamin": jk
                            })
                            if sukses:
                                st.success(f"✅ {msg}")
                                st.session_state["user"]["nama"] = n_ortu
                                st.session_state["user"]["alamat_dusun"] = dusun
                                st.rerun()
                            else:
                                st.error(f"❌ {msg}")


# ====================================================================
# 1. KADER: DASHBOARD
# ====================================================================
def view_kader_dashboard():
    p = database.get_all_peserta()
    b = database.get_pemeriksaan_balita()
    i = database.get_pemeriksaan_ibu()

    page_header("🏠 Dashboard Posyandu", f"Pemantauan wilayah & pencegahan stunting &bull; {TODAY.strftime('%d %B %Y')}")

    dusun_list = ["Semua Dusun"] + (sorted(p["alamat_dusun"].dropna().unique().tolist()) if not p.empty else [])
    dusun = st.selectbox("Filter Wilayah Dusun:", dusun_list)

    if dusun != "Semua Dusun":
        p = p[p["alamat_dusun"] == dusun]
        b = b[b["alamat_dusun"] == dusun]
        i = i[i["alamat_dusun"] == dusun]

    latest_b = database.get_latest_pemeriksaan(b)
    latest_i = database.get_latest_pemeriksaan(i)

    total_peserta = len(p)
    total_balita = int((p["jenis_peserta"] == "Balita").sum()) if not p.empty else 0
    total_ibu = int((p["jenis_peserta"] == "Ibu Hamil").sum()) if not p.empty else 0

    stunting_count = int(latest_b["status_gizi"].isin(["Stunting", "Gizi kurang"]).sum()) if not latest_b.empty else 0
    ibu_risiko_count = int((latest_i["risiko"] == "Risiko tinggi").sum()) if not latest_i.empty else 0
    tindak_lanjut = stunting_count + ibu_risiko_count

    cur_period = TODAY.strftime("%Y-%m")
    all_dates = pd.concat([b["tanggal_pemeriksaan"], i["tanggal_pemeriksaan"]]).dropna()
    pem_bln_ini = int((all_dates.dt.strftime("%Y-%m") == cur_period).sum()) if not all_dates.empty else 0

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Peserta", total_peserta, f"{total_balita} balita, {total_ibu} ibu", delta_color="off")
    kpi2.metric("Pemeriksaan Bulan Ini", pem_bln_ini, f"Periode {BULAN[TODAY.month - 1]}", delta_color="off")
    kpi3.metric("Balita Stunting / Kurang", stunting_count, "Intervensi Gizi", delta_color="off")
    kpi4.metric("Ibu Hamil Risiko Tinggi", ibu_risiko_count, "Rujukan Bidan", delta_color="off")
    kpi5.metric("Total Tindak Lanjut", tindak_lanjut, "Prioritas", delta_color="off")

    st.divider()

    c1, c2 = st.columns([3, 2])
    with c1:
        if not b.empty or not i.empty:
            t = pd.concat([
                b.assign(Kelompok="Balita"),
                i.assign(Kelompok="Ibu Hamil")
            ]).groupby(["periode", "Kelompok"]).size().reset_index(name="Jumlah")
            chart_t = alt.Chart(t).mark_line(point=True).encode(
                x=alt.X("periode:N", title="Periode"),
                y=alt.Y("Jumlah:Q", title="Jumlah Pemeriksaan"),
                color=alt.Color("Kelompok:N", scale=alt.Scale(range=[PRIMARY_BLUE, ACCENT_PURPLE])),
                tooltip=["periode", "Kelompok", "Jumlah"]
            ).properties(title="Tren Frekuensi Pemeriksaan Bulanan", height=260)
            chart_card(st, chart_t)
        else:
            st.info("Belum ada data pemeriksaan.")

    with c2:
        if not latest_b.empty:
            d_st = latest_b["status_gizi"].value_counts().reset_index()
            d_st.columns = ["status_gizi", "Jumlah"]
            chart_donut = alt.Chart(d_st).mark_arc(innerRadius=55).encode(
                theta=alt.Theta("Jumlah:Q"),
                color=alt.Color("status_gizi:N", scale=alt.Scale(range=[ACCENT_GREEN, ACCENT_PEACH, ACCENT_RED, ACCENT_LAV])),
                tooltip=["status_gizi", "Jumlah"]
            ).properties(title="Status Gizi Balita (Pemeriksaan Terakhir)", height=260)
            chart_card(st, chart_donut)

    c3, c4 = st.columns(2)
    with c3:
        if not latest_b.empty:
            chart_tb = alt.Chart(latest_b).mark_bar(color=PRIMARY_BLUE, cornerRadiusEnd=4).encode(
                x=alt.X("z_tb_u:Q", bin=alt.Bin(step=0.5), title="Z-Score TB/U"),
                y=alt.Y("count()", title="Jumlah Balita"),
                tooltip=["count()"]
            )
            rule_stunt = alt.Chart(pd.DataFrame({"x": [-2]})).mark_rule(color=ACCENT_RED, strokeDash=[5, 4]).encode(x="x:Q")
            chart_card(st, (chart_tb + rule_stunt).properties(title="Distribusi Z-Score TB/U (Garis Merah Batas Stunting -2 SD)", height=250))
    with c4:
        if not latest_i.empty:
            d_ibu = pd.DataFrame({
                "Faktor Risiko": ["KEK (LILA < 23.5)", "Anemia (Hb < 11)", "Hipertensi (>=140/90)", "Fe Belum Diberikan"],
                "Jumlah": [
                    int((latest_i["status_kek"] == "KEK").sum()),
                    int((latest_i["status_anemia"] == "Anemia").sum()),
                    int((latest_i["status_hipertensi"] == "Hipertensi").sum()),
                    int((latest_i["tablet_fe"] == "Belum diberikan").sum())
                ]
            })
            chart_f = alt.Chart(d_ibu).mark_bar(color=ACCENT_PEACH, cornerRadiusEnd=6).encode(
                x=alt.X("Jumlah:Q", title="Jumlah Kasus"),
                y=alt.Y("Faktor Risiko:N", sort="-x", title=None),
                tooltip=["Faktor Risiko", "Jumlah"]
            ).properties(title="Faktor Risiko Kesehatan Ibu Hamil", height=250)
            chart_card(st, chart_f)

    st.subheader("⚠️ Daftar Peserta Prioritas Tindak Lanjut")
    tl_balita = latest_b[latest_b["status_gizi"].isin(["Stunting", "Gizi kurang"])].assign(
        Kelompok="Balita",
        Kondisi=lambda x: x["status_gizi"]
    )
    tl_ibu = latest_i[latest_i["risiko"] == "Risiko tinggi"].assign(
        Kelompok="Ibu Hamil",
        Kondisi="Risiko tinggi"
    )

    tl_combined = pd.concat([tl_balita, tl_ibu], ignore_index=True)
    if not tl_combined.empty:
        tl_cols = [c for c in ["Kelompok", "id_peserta", "nama", "alamat_dusun", "Kondisi", "jadwal_berikutnya", "email"] if c in tl_combined.columns]
        render_interactive_table(
            tl_combined[tl_cols],
            default_columns=["Kelompok", "id_peserta", "nama", "alamat_dusun", "Kondisi", "jadwal_berikutnya"],
            table_id="tl_table"
        )
    else:
        st.success("Tidak ada peserta yang memerlukan tindak lanjut khusus saat ini.")


# ====================================================================
# 2. KADER: DATA PESERTA & RIWAYAT
# ====================================================================
def view_kader_peserta():
    page_header("👥 Data Peserta & Riwayat", "Pencarian interaktif, riwayat antropometri, dan pendaftaran peserta")

    peserta_df = database.get_all_peserta()
    tab_list, tab_tambah = st.tabs(["📋 Daftar & Riwayat Peserta", "➕ Tambah Peserta Baru"])

    with tab_list:
        st.subheader("Pencarian & Tabel Interaktif Peserta")
        filter_jenis = st.radio("Saring berdasarkan jenis peserta:", ["Semua", "Balita", "Ibu Hamil"], horizontal=True)

        df_view = peserta_df.copy()
        if filter_jenis != "Semua":
            df_view = df_view[df_view["jenis_peserta"] == filter_jenis]

        default_cols = [
            "id_peserta", "jenis_peserta", "nama", "alamat_dusun",
            "tanggal_lahir", "usia_bulan", "nama_orang_tua", "status", "email"
        ]
        render_interactive_table(
            df_view,
            default_columns=default_cols,
            table_id="peserta_main_table",
            search_placeholder="Ketik nama peserta atau ID..."
        )

        st.divider()

        st.subheader("🔍 Riwayat Pemeriksaan & Grafik Z-Score")
        if not df_view.empty:
            peserta_options = df_view["id_peserta"].tolist()
            selected_pid = st.selectbox(
                "Pilih peserta untuk menampilkan riwayat pemeriksaan:",
                options=peserta_options,
                format_func=lambda x: f"{x} — {df_view.loc[df_view['id_peserta'] == x, 'nama'].values[0]}"
            )

            if selected_pid:
                selected_info = database.get_peserta_by_id(selected_pid)
                if selected_info:
                    st.markdown(
                        f"""
                        <div style="background: rgba(15,23,42,0.7); padding: 14px 20px; border-radius: 14px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.08);">
                            <b style="color:#ffffff;">{selected_info.get('nama', '')}</b> ({selected_info.get('id_peserta', '')}) &bull;
                            Jenis: <span style="color:#38bdf8;">{selected_info.get('jenis_peserta', '')}</span> &bull;
                            Dusun: <b>{selected_info.get('alamat_dusun', '')}</b> &bull;
                            Email: <b>{selected_info.get('email', '-')}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                hist_df = database.get_pemeriksaan_by_peserta(selected_pid)
                if hist_df.empty:
                    st.info(f"Belum ada riwayat pemeriksaan untuk peserta {selected_pid}.")
                else:
                    if selected_pid.startswith("BLT"):
                        child_sex = selected_info.get("jenis_kelamin", "Laki-laki")
                        render_zscore_growth_view(hist_df, selected_info.get("nama", ""), child_sex)

                    clean_hist = hist_df.drop(
                        columns=["nama", "alamat_dusun", "no_hp", "bulan", "tahun", "periode", "id_orang_tua"],
                        errors="ignore"
                    )
                    st.write("**Data Riwayat Pemeriksaan:**")
                    st.dataframe(clean_hist, hide_index=True, width="stretch")
        else:
            st.info("Belum ada data peserta yang cocok.")

    with tab_tambah:
        st.subheader("Formulir Pendaftaran Peserta Dinamis (Kader)")
        jenis_pilihan = st.selectbox("Jenis Peserta:", ["Balita", "Ibu Hamil"], key="kader_reg_jenis")

        with st.form("form_kader_tambah_peserta", clear_on_submit=True):
            if jenis_pilihan == "Balita":
                nama_balita = st.text_input("Nama Lengkap Balita *")
                c1, c2 = st.columns(2)
                tgl_lahir = c1.date_input("Tanggal Lahir Balita *", value=date(TODAY.year - 2, 1, 1))
                jk = c2.selectbox("Jenis Kelamin *", ["Laki-laki", "Perempuan"])

                usia_bln = max(0.0, round((TODAY.year - tgl_lahir.year) * 12 + TODAY.month - tgl_lahir.month + (TODAY.day - tgl_lahir.day) / 30.4, 1))
                st.caption(f"Perkiraan usia balita: **{usia_bln:.1f} bulan**")

                c3, c4 = st.columns(2)
                nama_ayah = c3.text_input("Nama Ayah / Wali *")
                email_ortu = c4.text_input("Email Orang Tua")

                c5, c6 = st.columns(2)
                dusun_b = c5.selectbox("Dusun Domisili *", ["Melati", "Mawar", "Kenanga", "Anggrek"])
                alamat_detail_b = c6.text_input("Alamat Lengkap / RT-RW")

                submit_btn = st.form_submit_button("Simpan Data Balita 💾", type="primary")
                if submit_btn:
                    if not nama_balita.strip() or not nama_ayah.strip():
                        st.error("Nama balita dan nama orang tua wajib diisi.")
                    else:
                        sukses, pesan, new_id = database.create_peserta({
                            "jenis_peserta": "Balita",
                            "nama": nama_balita.strip(),
                            "tanggal_lahir": tgl_lahir,
                            "usia_bulan": usia_bln,
                            "jenis_kelamin": jk,
                            "nama_orang_tua": nama_ayah.strip(),
                            "alamat_dusun": dusun_b,
                            "alamat_lengkap": alamat_detail_b.strip(),
                            "email": email_ortu.strip()
                        })
                        if sukses:
                            st.success(f"✅ {pesan}")
                            st.balloons()
                        else:
                            st.error(f"❌ {pesan}")

            else:  # Ibu Hamil
                nama_ibu = st.text_input("Nama Lengkap Ibu Hamil *")
                c1, c2 = st.columns(2)
                nama_suami = c1.text_input("Nama Suami / Pendamping *")
                usia_ibu = c2.number_input("Usia Ibu (Tahun) *", min_value=15, max_value=55, value=28)

                c3, c4 = st.columns(2)
                usia_hamil = c3.number_input("Usia Kehamilan (Minggu) *", min_value=1, max_value=43, value=12)
                email_ibu = c4.text_input("Email Ibu Hamil")

                c5, c6 = st.columns(2)
                dusun_i = c5.selectbox("Dusun Domisili *", ["Melati", "Mawar", "Kenanga", "Anggrek"])
                alamat_detail_i = c6.text_input("Alamat Lengkap / RT-RW")

                submit_btn = st.form_submit_button("Simpan Data Ibu Hamil 💾", type="primary")
                if submit_btn:
                    if not nama_ibu.strip() or not nama_suami.strip():
                        st.error("Nama ibu dan nama suami wajib diisi.")
                    else:
                        sukses, pesan, new_id = database.create_peserta({
                            "jenis_peserta": "Ibu Hamil",
                            "nama": nama_ibu.strip(),
                            "nama_suami": nama_suami.strip(),
                            "usia_ibu_tahun": usia_ibu,
                            "usia_kehamilan_minggu": usia_hamil,
                            "alamat_dusun": dusun_i,
                            "alamat_lengkap": alamat_detail_i.strip(),
                            "email": email_ibu.strip()
                        })
                        if sukses:
                            st.success(f"✅ {pesan}")
                            st.balloons()
                        else:
                            st.error(f"❌ {pesan}")


# ====================================================================
# 3. KADER: PEMERIKSAAN BALITA
# ====================================================================
def view_kader_balita():
    page_header("🧒 Pemeriksaan Balita", "Input timbang & ukur balita — Z-score WHO & status gizi dihitung otomatis")

    all_peserta = database.get_all_peserta()
    balita_df = all_peserta[all_peserta["jenis_peserta"] == "Balita"]

    if balita_df.empty:
        st.warning("Belum ada data balita terdaftar.")
        return

    with st.form("form_pem_balita"):
        st.subheader("Form Pengukuran Antropometri")
        c1, c2 = st.columns(2)
        pid = c1.selectbox(
            "Pilih Balita:",
            options=balita_df["id_peserta"].tolist(),
            format_func=lambda x: f"{x} — {balita_df.loc[balita_df['id_peserta'] == x, 'nama'].values[0]}"
        )
        tgl = c2.date_input("Tanggal Pemeriksaan:", value=TODAY)

        c3, c4, c5 = st.columns(3)
        bb = c3.number_input("Berat Badan (kg) *", min_value=1.5, max_value=45.0, value=10.0, step=0.1)
        tb = c4.number_input("Tinggi / Panjang Badan (cm) *", min_value=35.0, max_value=135.0, value=80.0, step=0.5)
        lk = c5.number_input("Lingkar Kepala (cm)", min_value=25.0, max_value=60.0, value=46.0, step=0.5)

        c6, c7, c8 = st.columns(3)
        va = c6.selectbox("Pemberian Vitamin A:", ["Ya", "Tidak"])
        im = c7.selectbox("Status Imunisasi:", ["Lengkap sesuai usia", "Belum lengkap"])
        cat = c8.text_input("Catatan Kader:", placeholder="Kondisi aktif, nafsu makan baik...")

        submit = st.form_submit_button("Simpan & Hitung Status Antropometri 💾", type="primary")

    if submit:
        data_input = {
            "id_peserta": pid,
            "tanggal_pemeriksaan": tgl,
            "berat_kg": bb,
            "tinggi_cm": tb,
            "lingkar_kepala_cm": lk,
            "vitamin_a": va,
            "imunisasi": im,
            "catatan": cat
        }
        sukses, msg, row_saved = database.add_pemeriksaan_balita(data_input)
        if sukses:
            st.session_state["last_balita_result"] = row_saved
            st.success(f"✅ {msg}")
            st.balloons()
        else:
            st.error(f"❌ {msg}")

    if "last_balita_result" in st.session_state:
        res = st.session_state["last_balita_result"]
        st.subheader("📊 Hasil Perhitungan Z-Score Terkini")
        hist = database.get_pemeriksaan_by_peserta(res["id_peserta"])
        p_info = database.get_peserta_by_id(res["id_peserta"])
        if p_info:
            render_zscore_growth_view(hist, p_info.get("nama", ""), p_info.get("jenis_kelamin", "Laki-laki"))

    st.divider()
    st.subheader("📋 Riwayat Pemeriksaan Balita Terbaru")
    recent_b = database.get_pemeriksaan_balita()
    if not recent_b.empty:
        render_interactive_table(
            recent_b,
            default_columns=["tanggal_pemeriksaan", "id_peserta", "nama", "berat_kg", "tinggi_cm", "status_gizi", "jadwal_berikutnya"],
            table_id="recent_balita_table"
        )


# ====================================================================
# 4. KADER: PEMERIKSAAN IBU HAMIL
# ====================================================================
def view_kader_ibu():
    page_header("🤰 Pemeriksaan Ibu Hamil", "Input pemeriksaan maternal — skrining risiko KEK, anemia & hipertensi")

    all_peserta = database.get_all_peserta()
    ibu_df = all_peserta[all_peserta["jenis_peserta"] == "Ibu Hamil"]

    if ibu_df.empty:
        st.warning("Belum ada data ibu hamil terdaftar.")
        return

    with st.form("form_pem_ibu"):
        st.subheader("Form Pemeriksaan Kehamilan (ANC)")
        c1, c2, c3 = st.columns(3)
        pid = c1.selectbox(
            "Pilih Ibu Hamil:",
            options=ibu_df["id_peserta"].tolist(),
            format_func=lambda x: f"{x} — {ibu_df.loc[ibu_df['id_peserta'] == x, 'nama'].values[0]}"
        )
        tgl = c2.date_input("Tanggal Pemeriksaan:", value=TODAY)
        w = c3.number_input("Usia Kehamilan (Minggu) *", min_value=1, max_value=43, value=20)

        c4, c5, c6 = st.columns(3)
        bb = c4.number_input("Berat Badan Ibu (kg) *", min_value=30.0, max_value=160.0, value=60.0, step=0.1)
        lila = c5.number_input("Lingkar Lengan Atas / LILA (cm) *", min_value=12.0, max_value=45.0, value=25.0, step=0.1)
        hb = c6.number_input("Kadar Hemoglobin / Hb (g/dL) *", min_value=4.0, max_value=19.0, value=11.5, step=0.1)

        c7, c8, c9 = st.columns(3)
        sis = c7.number_input("Tekanan Darah Sistol (mmHg) *", min_value=60, max_value=230, value=115)
        dia = c8.number_input("Tekanan Darah Diastol (mmHg) *", min_value=40, max_value=150, value=75)
        tfu = c9.number_input("Tinggi Fundus Uteri / TFU (cm)", min_value=0.0, max_value=50.0, value=0.0, step=0.5)

        c10, c11 = st.columns(2)
        fe = c10.selectbox("Pemberian Tablet Tambah Darah (Fe):", ["Diberikan", "Belum diberikan"])
        cat = c11.text_input("Catatan Bidan/Kader:", placeholder="Keluhan mual, gerakan janin aktif...")

        submit = st.form_submit_button("Simpan & Analisis Risiko Maternal 💾", type="primary")

    if submit:
        data_input = {
            "id_peserta": pid,
            "tanggal_pemeriksaan": tgl,
            "usia_kehamilan_minggu": w,
            "berat_kg": bb,
            "lila_cm": lila,
            "sistol": sis,
            "diastol": dia,
            "hb_gdl": hb,
            "tfu_cm": tfu if tfu > 0 else None,
            "tablet_fe": fe,
            "catatan": cat
        }
        sukses, msg, row_saved = database.add_pemeriksaan_ibu(data_input)
        if sukses:
            st.session_state["last_ibu_result"] = row_saved
            st.success(f"✅ {msg}")
            st.balloons()
        else:
            st.error(f"❌ {msg}")

    if "last_ibu_result" in st.session_state:
        res = st.session_state["last_ibu_result"]
        st.subheader("🩺 Hasil Analisis Risiko Maternal")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Tingkat Risiko", res["risiko"], delta_color="off")
        m2.metric("Status KEK", res["status_kek"], f"LILA: {res['lila_cm']} cm", delta_color="off")
        m3.metric("Status Anemia", res["status_anemia"], f"Hb: {res['hb_gdl']} g/dL", delta_color="off")
        m4.metric("Tekanan Darah", f"{res['sistol']}/{res['diastol']}", res["status_hipertensi"], delta_color="off")
        m5.metric("Estimasi HPL", fmt_date(res["hpl"]), delta_color="off")

    st.divider()
    st.subheader("📋 Riwayat Pemeriksaan Ibu Hamil Terbaru")
    recent_i = database.get_pemeriksaan_ibu()
    if not recent_i.empty:
        render_interactive_table(
            recent_i,
            default_columns=["tanggal_pemeriksaan", "id_peserta", "nama", "usia_kehamilan_minggu", "risiko", "jadwal_berikutnya", "hpl"],
            table_id="recent_ibu_table"
        )


# ====================================================================
# 5. KADER: LAPORAN VISUALISASI DINAMIS & INTERPRETASI OTOMATIS
# ====================================================================
def view_kader_laporan():
    page_header("📊 Laporan Visualisasi Dinamis", "Bandingkan variabel, analisis statistik empiris, dan unduh Excel/CSV")

    b_df = database.get_pemeriksaan_balita()
    i_df = database.get_pemeriksaan_ibu()

    col1, col2, col3 = st.columns(3)
    kelompok = col1.selectbox("Kelompok Peserta:", ["Balita", "Ibu Hamil"])

    df_source = b_df if kelompok == "Balita" else i_df
    if df_source.empty:
        st.info(f"Belum ada data pemeriksaan untuk kelompok {kelompok}.")
        return

    available_years = sorted(df_source["tahun"].dropna().unique().tolist(), reverse=True)
    tahun = col2.selectbox("Tahun:", available_years if available_years else [TODAY.year])

    bulan_idx = col3.selectbox(
        "Bulan:",
        options=[0] + list(range(1, 13)),
        format_func=lambda x: "Semua Bulan" if x == 0 else BULAN[x - 1],
        index=TODAY.month
    )

    filtered = df_source[df_source["tahun"] == tahun]
    if bulan_idx != 0:
        filtered = filtered[filtered["bulan"] == bulan_idx]

    if filtered.empty:
        st.warning("Tidak ditemukan data pemeriksaan pada periode yang dipilih.")
        return

    st.divider()
    st.subheader("⚙️ Pemilihan Variabel Perbandingan")

    if kelompok == "Balita":
        var_options_num = {
            "Usia (bulan)": "usia_bulan",
            "Berat badan (kg)": "berat_kg",
            "Tinggi badan (cm)": "tinggi_cm",
            "Lingkar kepala (cm)": "lingkar_kepala_cm",
            "Z-Score BB/U": "z_bb_u",
            "Z-Score TB/U": "z_tb_u"
        }
        var_options_cat = {
            "Status Gizi": "status_gizi",
            "Dusun": "alamat_dusun",
            "Jenis Kelamin": "jenis_kelamin",
            "Imunisasi": "imunisasi",
            "Vitamin A": "vitamin_a"
        }
    else:
        var_options_num = {
            "Usia Kehamilan (minggu)": "usia_kehamilan_minggu",
            "Berat Badan (kg)": "berat_kg",
            "LILA (cm)": "lila_cm",
            "Kadar Hb (g/dL)": "hb_gdl",
            "Tekanan Sistol": "sistol",
            "Tekanan Diastol": "diastol"
        }
        var_options_cat = {
            "Tingkat Risiko": "risiko",
            "Status KEK": "status_kek",
            "Status Anemia": "status_anemia",
            "Status Hipertensi": "status_hipertensi",
            "Trimester": "trimester",
            "Dusun": "alamat_dusun"
        }

    all_var_options = {**var_options_num, **var_options_cat}
    vcol1, vcol2 = st.columns(2)
    v1_label = vcol1.selectbox("Variabel Pertama (Sumbu X):", list(all_var_options.keys()), index=0)
    v2_label = vcol2.selectbox("Variabel Kedua (Sumbu Y):", list(all_var_options.keys()), index=1 if len(all_var_options) > 1 else 0)

    col_x = all_var_options[v1_label]
    col_y = all_var_options[v2_label]
    is_x_num = col_x in var_options_num.values()
    is_y_num = col_y in var_options_num.values()

    chart_view = None
    interp_text = ""

    if is_x_num and is_y_num:
        chart_scatter = alt.Chart(filtered).mark_circle(size=70, opacity=0.8, color=PRIMARY_BLUE).encode(
            x=alt.X(f"{col_x}:Q", title=v1_label),
            y=alt.Y(f"{col_y}:Q", title=v2_label),
            tooltip=["id_peserta", "nama", f"{col_x}:Q", f"{col_y}:Q"]
        )
        trend_line = chart_scatter.transform_regression(col_x, col_y).mark_line(color=ACCENT_RED, strokeWidth=2)
        chart_view = (chart_scatter + trend_line).properties(
            title=f"Korelasi & Sebaran: {v1_label} vs {v2_label}",
            height=320
        )
        corr = filtered[[col_x, col_y]].dropna().corr().iloc[0, 1]
        arah = "positif (sejalan)" if corr > 0.2 else "negatif (berlawanan)" if corr < -0.2 else "mendatar"
        interp_text = (
            f"Berdasarkan {len(filtered)} data pemeriksaan, rata-rata **{v1_label}** adalah **{filtered[col_x].mean():.2f}** "
            f"dan rata-rata **{v2_label}** adalah **{filtered[col_y].mean():.2f}**. Terlihat kecenderungan korelasi {arah} (r = {corr:.2f})."
        )
    elif is_x_num and not is_y_num:
        chart_view = alt.Chart(filtered).mark_boxplot(extent="min-max").encode(
            x=alt.X(f"{col_y}:N", title=v2_label),
            y=alt.Y(f"{col_x}:Q", title=v1_label),
            color=alt.Color(f"{col_y}:N", scale=alt.Scale(range=CHART_PALETTE), legend=None),
            tooltip=[f"{col_y}:N", f"count({col_x})"]
        ).properties(title=f"Distribusi {v1_label} Berdasarkan {v2_label}", height=320)
        grp_stats = filtered.groupby(col_y)[col_x].mean().round(2)
        interp_text = f"Nilai rata-rata **{v1_label}** tertinggi berada pada kategori **{grp_stats.idxmax()}** ({grp_stats.max():.2f})."
    elif not is_x_num and is_y_num:
        avg_df = filtered.groupby(col_x)[col_y].mean().round(2).reset_index(name="Rata_Rata")
        chart_view = alt.Chart(avg_df).mark_bar(cornerRadiusEnd=6, color=ACCENT_GREEN).encode(
            x=alt.X(f"{col_x}:N", title=v1_label),
            y=alt.Y("Rata_Rata:Q", title=f"Rata-rata {v2_label}"),
            tooltip=[col_x, "Rata_Rata"]
        ).properties(title=f"Rata-rata {v2_label} per {v1_label}", height=320)
        interp_text = f"Rata-rata **{v2_label}** tertinggi tercatat pada kategori **{avg_df.loc[avg_df['Rata_Rata'].idxmax()][col_x]}**."
    else:
        grouped_cat = filtered.groupby([col_x, col_y]).size().reset_index(name="Jumlah")
        chart_view = alt.Chart(grouped_cat).mark_bar(cornerRadiusEnd=4).encode(
            x=alt.X(f"{col_x}:N", title=v1_label),
            y=alt.Y("Jumlah:Q", title="Jumlah Kasus"),
            color=alt.Color(f"{col_y}:N", scale=alt.Scale(range=CHART_PALETTE)),
            tooltip=[col_x, col_y, "Jumlah"]
        ).properties(title=f"Distribusi: {v1_label} dan {v2_label}", height=320)
        interp_text = f"Proporsi peserta terbesar berada pada kombinasi kategori **{grouped_cat.loc[grouped_cat['Jumlah'].idxmax()][col_x]}** - **{grouped_cat.loc[grouped_cat['Jumlah'].idxmax()][col_y]}**."

    c_graph, c_interp = st.columns([3, 2])
    with c_graph:
        if chart_view:
            chart_card(st, chart_view)
    with c_interp:
        with st.container(border=True):
            st.markdown("#### 💡 Interpretasi Otomatis Hasil Analisis")
            if len(filtered) < 3:
                st.warning("⚠️ Data belum mencukupi untuk dianalisis secara statistik (minimal 3 pemeriksaan).")
            else:
                st.write(interp_text)
                st.info("📌 **Catatan:** Interpretasi menggambarkan pola asosiasi data posyandu dan bukan hubungan sebab-akibat medis.")

    st.subheader("📑 Ringkasan Data Terpilih")
    if is_x_num and not is_y_num:
        summ_table = filtered.groupby(col_y)[col_x].describe().round(2).reset_index()
    elif not is_x_num and is_y_num:
        summ_table = filtered.groupby(col_x)[col_y].describe().round(2).reset_index()
    elif not is_x_num and not is_y_num:
        summ_table = pd.crosstab(filtered[col_x], filtered[col_y], margins=True, margins_name="Total").reset_index()
    else:
        summ_table = filtered[[col_x, col_y]].describe().round(2).reset_index()

    st.dataframe(summ_table, hide_index=True, width="stretch")

    period_str = f"{tahun}-{bulan_idx:02d}" if bulan_idx != 0 else str(tahun)
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
    btn_col1.download_button(
        "⬇️ Unduh Data (CSV)",
        data=csv_bytes,
        file_name=f"laporan_posyandu_{kelompok}_{period_str}.csv",
        mime="text/csv",
        width="stretch"
    )

    excel_buf = io.BytesIO()
    with pd.ExcelWriter(excel_buf, engine="openpyxl") as writer:
        filtered.to_excel(writer, sheet_name="Data_Pemeriksaan", index=False)
        summ_table.to_excel(writer, sheet_name="Ringkasan_Statistik", index=False)
    btn_col2.download_button(
        "⬇️ Unduh Laporan Lengkap (Excel)",
        data=excel_buf.getvalue(),
        file_name=f"laporan_posyandu_{kelompok}_{period_str}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch"
    )

    if btn_col3.button("Simpan ke Database Laporan 💾", type="primary", width="stretch"):
        curr_user = st.session_state.get("user", {}).get("nama", "Kader Posyandu")
        var_desc = f"{v1_label} vs {v2_label}"
        sukses, msg, lap_id = database.save_laporan(
            periode=period_str,
            kelompok=kelompok,
            variabel=var_desc,
            dibuat_oleh=curr_user,
            catatan=interp_text[:250]
        )
        if sukses:
            st.success(f"✅ {msg}")
            st.info("Buka menu '🗂️ Riwayat Laporan Puskesmas' untuk menyerahkan berkas ini ke Puskesmas.")
        else:
            st.error("Gagal menyimpan laporan.")


# ====================================================================
# 6. KADER: RIWAYAT LAPORAN & PENYERAHAN PUSKESMAS
# ====================================================================
def view_kader_riwayat_laporan():
    page_header("🗂️ Riwayat Laporan Posyandu", "Daftar berkas laporan bulanan dan status penyerahan ke Puskesmas")

    lap_df = database.get_all_laporan()
    if lap_df.empty:
        st.info("Belum ada laporan yang disimpan ke database.")
        return

    render_interactive_table(
        lap_df,
        default_columns=["id_laporan", "periode", "kelompok", "variabel", "dibuat_oleh", "tanggal_dibuat", "status", "tanggal_serah"],
        table_id="riwayat_lap_table"
    )

    st.divider()
    pending_lap = lap_df[lap_df["status"] != "Diserahkan ke Puskesmas"]
    if not pending_lap.empty:
        st.subheader("📤 Penyerahan Laporan ke Puskesmas")
        target_id = st.selectbox(
            "Pilih ID Laporan yang siap diserahkan:",
            options=pending_lap["id_laporan"].tolist(),
            format_func=lambda x: f"{x} — Periode {pending_lap.loc[pending_lap['id_laporan'] == x, 'periode'].values[0]} ({pending_lap.loc[pending_lap['id_laporan'] == x, 'kelompok'].values[0]})"
        )
        if st.button("Serahkan Berkas ke Puskesmas 🚀", type="primary"):
            sukses, msg = database.update_status_laporan(target_id, "Diserahkan ke Puskesmas")
            if sukses:
                st.success(f"✅ {msg}")
                st.rerun()
            else:
                st.error("Gagal memperbarui status laporan.")
    else:
        st.success("Semua laporan pada riwayat telah diserahkan ke Puskesmas.")


# ====================================================================
# 7. IBU HAMIL: DASHBOARD & BUKU KIA DIGITAL
# ====================================================================
def _resolve_ibu_record(user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    uid = str(user.get("id", ""))
    pid = user.get("id_peserta", "")
    if pid:
        p = database.get_peserta_by_id(pid)
        if p:
            return p
    return database.get_peserta_by_user_id(uid)


def view_ibu_dashboard(user: Dict[str, Any]):
    ibu_info = _resolve_ibu_record(user)
    if not ibu_info:
        st.info("Biodata kehamilan Anda belum tercatat lengkap.")
        return

    pid = ibu_info.get("id_peserta", "")
    all_ibu = database.get_pemeriksaan_ibu()
    h = all_ibu[all_ibu["id_peserta"] == pid].sort_values("tanggal_pemeriksaan")

    page_header(f"🏠 Selamat Datang, Ibu {ibu_info.get('nama', user.get('nama'))}", f"Wilayah Dusun: {ibu_info.get('alamat_dusun', '-')} &bull; ID: {pid}")

    if h.empty:
        st.info("Kader posyandu belum mencatat pemeriksaan ANC untuk Anda. Jadwal dan grafik akan otomatis muncul setelah kunjungan pemeriksaan pertama.")
        return

    last = h.iloc[-1]
    w = int(last.get("usia_kehamilan_minggu", 0))
    risiko = last.get("risiko", "Risiko rendah")
    next_ctrl = last.get("jadwal_berikutnya", "-")
    hpl = last.get("hpl", "-")

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Usia Kehamilan", f"{w} Minggu", last.get("trimester", ""), delta_color="off")
    k2.metric("Perkiraan Persalinan (HPL)", fmt_date(hpl), delta_color="off")
    k3.metric("Tingkat Risiko", risiko, delta_color="off")
    k4.metric("Kontrol Berikutnya", fmt_date(next_ctrl), delta_color="off")
    k5.metric("Tablet Fe", last.get("tablet_fe", "-"), delta_color="off")

    if risiko == "Risiko tinggi":
        st.error(f"Status Kehamilan: **{risiko}** — Terdeteksi KEK: {last.get('status_kek')}, Anemia: {last.get('status_anemia')}, Tekanan Darah: {last.get('status_hipertensi')}. Dianjurkan konsultasi segera dengan Bidan Desa atau Puskesmas.")
    elif risiko == "Perlu pemantauan":
        st.warning(f"Status Kehamilan: **{risiko}** — Tetap jaga asupan nutrisi gizi seimbang dan istirahat teratur.")
    else:
        st.success("Status Kehamilan: **Risiko Rendah (Kondisi Baik)** — Pertahankan pola makan sehat!")

    st.divider()
    st.subheader("📈 Kurva Perkembangan Fisik & Maternal")
    g1, g2 = st.columns(2)
    with g1:
        ch_bb = alt.Chart(h).mark_line(point=True, color=ACCENT_GREEN).encode(
            x=alt.X("usia_kehamilan_minggu:Q", title="Usia Kehamilan (Minggu)"),
            y=alt.Y("berat_kg:Q", title="Berat Badan (kg)", scale=alt.Scale(zero=False)),
            tooltip=["usia_kehamilan_minggu", "berat_kg"]
        ).properties(title="Kenaikan Berat Badan Ibu (kg)", height=240)
        chart_card(st, ch_bb)
    with g2:
        long_td = h[["usia_kehamilan_minggu", "sistol", "diastol"]].melt(
            id_vars=["usia_kehamilan_minggu"],
            value_vars=["sistol", "diastol"],
            var_name="Tekanan",
            value_name="Nilai"
        )
        ch_td = alt.Chart(long_td).mark_line(point=True).encode(
            x=alt.X("usia_kehamilan_minggu:Q", title="Usia Kehamilan (Minggu)"),
            y=alt.Y("Nilai:Q", title="mmHg", scale=alt.Scale(domain=[50, 180])),
            color=alt.Color("Tekanan:N", scale=alt.Scale(range=[ACCENT_RED, PRIMARY_BLUE])),
            tooltip=["usia_kehamilan_minggu", "Tekanan", "Nilai"]
        ).properties(title="Tekanan Darah (Garis Merah Batas Sistol 140)", height=240)
        rule_td = alt.Chart(pd.DataFrame({"y": [140]})).mark_rule(color=ACCENT_RED, strokeDash=[5, 4]).encode(y="y:Q")
        chart_card(st, ch_td + rule_td)

    g3, g4 = st.columns(2)
    with g3:
        ch_hb = alt.Chart(h).mark_line(point=True, color=ACCENT_PURPLE).encode(
            x=alt.X("usia_kehamilan_minggu:Q", title="Usia Kehamilan (Minggu)"),
            y=alt.Y("hb_gdl:Q", title="Hb (g/dL)", scale=alt.Scale(domain=[6, 16])),
            tooltip=["usia_kehamilan_minggu", "hb_gdl"]
        ).properties(title="Kadar Hemoglobin (Garis Merah Batas Anemia 11 g/dL)", height=240)
        rule_hb = alt.Chart(pd.DataFrame({"y": [11]})).mark_rule(color=ACCENT_RED, strokeDash=[5, 4]).encode(y="y:Q")
        chart_card(st, ch_hb + rule_hb)
    with g4:
        ch_lila = alt.Chart(h).mark_line(point=True, color=ACCENT_PEACH).encode(
            x=alt.X("usia_kehamilan_minggu:Q", title="Usia Kehamilan (Minggu)"),
            y=alt.Y("lila_cm:Q", title="LILA (cm)", scale=alt.Scale(domain=[15, 35])),
            tooltip=["usia_kehamilan_minggu", "lila_cm"]
        ).properties(title="LILA (Garis Merah Batas KEK 23.5 cm)", height=240)
        rule_lila = alt.Chart(pd.DataFrame({"y": [23.5]})).mark_rule(color=ACCENT_RED, strokeDash=[5, 4]).encode(y="y:Q")
        chart_card(st, ch_lila + rule_lila)


def view_ibu_kia(user: Dict[str, Any]):
    ibu_info = _resolve_ibu_record(user)
    if not ibu_info:
        st.info("Biodata kehamilan Anda belum tercatat.")
        return

    pid = ibu_info.get("id_peserta", "")
    all_ibu = database.get_pemeriksaan_ibu()
    h = all_ibu[all_ibu["id_peserta"] == pid].sort_values("tanggal_pemeriksaan", ascending=False)

    page_header("📖 Buku KIA Digital Ibu Hamil", f"Catatan riwayat kunjungan antenatal care (ANC) &bull; ID: {pid}")

    if h.empty:
        st.info("Belum ada riwayat kunjungan pemeriksaan tercatat.")
        return

    clean_h = h.drop(columns=["nama", "alamat_dusun", "no_hp", "bulan", "tahun", "periode", "id_peserta"], errors="ignore")
    st.dataframe(clean_h, hide_index=True, width="stretch")

    csv_data = clean_h.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Unduh Salinan Buku KIA (CSV)",
        data=csv_data,
        file_name=f"buku_kia_{pid}.csv",
        mime="text/csv"
    )


def view_ibu_profil(user: Dict[str, Any]):
    ibu_info = _resolve_ibu_record(user)
    page_header("👤 Profil & Biodata Ibu Hamil", "Informasi kontak dan data kehamilan terdaftar")

    if not ibu_info:
        st.info("Biodata belum tercatat.")
        return

    with st.container(border=True):
        st.markdown(f"**Nama Ibu:** {ibu_info.get('nama', user.get('nama'))}")
        st.markdown(f"**Nama Suami / Pendamping:** {ibu_info.get('nama_orang_tua', '-')}")
        st.markdown(f"**Usia Ibu:** {ibu_info.get('usia_ibu_tahun', '-')} tahun")
        st.markdown(f"**Usia Kehamilan Terdaftar:** {ibu_info.get('usia_kehamilan_minggu', '-')} minggu")
        st.markdown(f"**Wilayah Dusun:** {ibu_info.get('alamat_dusun', '-')}")
        st.markdown(f"**Alamat Lengkap:** {ibu_info.get('alamat_lengkap', '-')}")
        st.markdown(f"**Email Akun:** {ibu_info.get('email', user.get('email'))}")
        st.markdown(f"**ID Peserta:** `{ibu_info.get('id_peserta', '-')}`")


# ====================================================================
# 8. ORANG TUA: DASHBOARD BALITA & SARAN PERTUMBUHAN OPTIMAL
# ====================================================================
def _resolve_parent_kids(user: Dict[str, Any]) -> pd.DataFrame:
    uid = str(user.get("id", ""))
    return database.get_children_by_parent_user_id(uid)


def view_ortu_dashboard(user: Dict[str, Any]):
    kids_df = _resolve_parent_kids(user)
    if kids_df.empty:
        st.info("Belum ada data balita yang terhubung dengan akun Anda. Silakan daftarkan si kecil pada menu 'Data & Tambah Balita'.")
        return

    if len(kids_df) > 1:
        k_id = st.selectbox(
            "Pilih Balita Anda:",
            options=kids_df["id_peserta"].tolist(),
            format_func=lambda x: f"{kids_df.loc[kids_df['id_peserta'] == x, 'nama'].values[0]} ({x})"
        )
    else:
        k_id = kids_df["id_peserta"].iloc[0]

    child = kids_df[kids_df["id_peserta"] == k_id].iloc[0]
    hist = database.get_pemeriksaan_by_peserta(k_id)

    page_header(f"🏠 Pemantauan Tumbuh Kembang: {child['nama']}", f"Jenis Kelamin: {child['jenis_kelamin']} &bull; ID: {k_id}")

    if hist.empty:
        st.info(f"Belum ada data pemeriksaan antropometri tercatat untuk {child['nama']}. Data grafik dan Z-Score akan muncul setelah penimbangan pertama di Posyandu.")
        return

    latest = hist.iloc[0]
    age = float(latest.get("usia_bulan", 0.0))
    bb = float(latest.get("berat_kg", 0.0))
    tb = float(latest.get("tinggi_cm", 0.0))
    status = latest.get("status_gizi", "Normal")
    z_tb = float(latest.get("z_tb_u", 0.0))
    z_bb = float(latest.get("z_bb_u", 0.0))
    next_date = latest.get("jadwal_berikutnya", "-")

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Usia Saat Ini", f"{age:.0f} Bulan", delta_color="off")
    k2.metric("Berat / Tinggi", f"{bb} kg / {tb} cm", delta_color="off")
    k3.metric("Status Gizi WHO", status, delta_color="off")
    k4.metric("Imunisasi", latest.get("imunisasi", "-"), delta_color="off")
    k5.metric("Jadwal Posyandu", fmt_date(next_date), delta_color="off")

    st.divider()

    st.subheader("💡 Saran & Edukasi Pertumbuhan Optimal")
    saran_info = database.get_saran_pertumbuhan(
        usia_bulan=age,
        status_gizi=status,
        z_bb=z_bb,
        z_tb=z_tb
    )

    with st.container(border=True):
        st.markdown(f"#### {saran_info['status_badge']}")
        st.write(saran_info['analisis'])

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"**🥗 Pola Makan Sesuai Usia ({saran_info['fase_usia']}):**")
            st.write(saran_info['rekomendasi_makan'])
            st.caption(f"Tekstur makanan: {saran_info['tekstur_tips']}")

        with col_s2:
            st.markdown("**🏃 Stimulasi Perkembangan & Gerak:**")
            st.write(saran_info['stimulasi'])

        st.markdown("**📋 Rencana Tindakan yang Disarankan untuk Orang Tua:**")
        for act in saran_info['tindakan']:
            st.markdown(f"- {act}")

        st.caption(saran_info['catatan_kesehatan'])

    st.divider()

    st.subheader("📈 Kurva Pertumbuhan KMS (Kartu Menuju Sehat)")
    c_kms1, c_kms2 = st.columns(2)
    with c_kms1:
        ch_bb_u = render_kms_chart(
            hist, child["jenis_kelamin"], "bb", "berat_kg",
            "Kurva Berat Badan Menurut Umur (BB/U)", "Berat (kg)"
        )
        chart_card(st, ch_bb_u)

    with c_kms2:
        ch_tb_u = render_kms_chart(
            hist, child["jenis_kelamin"], "tb", "tinggi_cm",
            "Kurva Tinggi Badan Menurut Umur (TB/U)", "Tinggi (cm)"
        )
        chart_card(st, ch_tb_u)

    st.caption("Keterangan: Area hijau = batas normal (-2 s.d. +2 SD WHO). Titik warna = riwayat pengukuran si kecil.")


def view_ortu_grafik(user: Dict[str, Any]):
    kids_df = _resolve_parent_kids(user)
    if kids_df.empty:
        st.info("Belum ada data balita.")
        return

    if len(kids_df) > 1:
        k_id = st.selectbox(
            "Pilih Balita:",
            options=kids_df["id_peserta"].tolist(),
            format_func=lambda x: f"{kids_df.loc[kids_df['id_peserta'] == x, 'nama'].values[0]} ({x})",
            key="grafik_child_sel"
        )
    else:
        k_id = kids_df["id_peserta"].iloc[0]

    child = kids_df[kids_df["id_peserta"] == k_id].iloc[0]
    hist = database.get_pemeriksaan_by_peserta(k_id)

    page_header(f"📈 Grafik Pertumbuhan & Z-Score: {child['nama']}", "Riwayat longitudinal Z-score dan lingkar kepala")

    if hist.empty:
        st.info("Belum ada data pemeriksaan.")
        return

    render_zscore_growth_view(hist, child["nama"], child["jenis_kelamin"])

    ch_lk = alt.Chart(hist).mark_line(point=True, color=PRIMARY_BLUE).encode(
        x=alt.X("tanggal_pemeriksaan:T", title="Tanggal Pemeriksaan"),
        y=alt.Y("lingkar_kepala_cm:Q", title="Lingkar Kepala (cm)", scale=alt.Scale(zero=False)),
        tooltip=["tanggal_pemeriksaan:T", "lingkar_kepala_cm"]
    ).properties(title="Perkembangan Lingkar Kepala Anak (cm)", height=240)
    chart_card(st, ch_lk)

    st.write("**Riwayat Seluruh Pemeriksaan:**")
    clean_hist = hist[[
        "tanggal_pemeriksaan", "usia_bulan", "berat_kg", "tinggi_cm", "lingkar_kepala_cm",
        "vitamin_a", "imunisasi", "z_bb_u", "z_tb_u", "status_gizi", "catatan"
    ]].sort_values("tanggal_pemeriksaan", ascending=False)
    st.dataframe(clean_hist, hide_index=True, width="stretch")


def view_ortu_tambah_balita(user: Dict[str, Any]):
    page_header("👶 Data Balita & Tambah Anak", "Kelola daftar anak balita di bawah akun Anda")
    user_id = str(user.get("id", ""))
    kids_df = _resolve_parent_kids(user)

    st.subheader("Daftar Balita Terdaftar")
    if not kids_df.empty:
        st.dataframe(
            kids_df[["id_peserta", "nama", "jenis_kelamin", "tanggal_lahir", "usia_bulan", "status"]],
            hide_index=True,
            width="stretch"
        )
    else:
        st.info("Belum ada anak balita terdaftar.")

    st.divider()

    with st.expander("➕ Daftarkan Balita Lainnya (Adik / Kakak)", expanded=kids_df.empty):
        with st.form("form_tambah_anak_lagi", clear_on_submit=True):
            nama_b = st.text_input("Nama Lengkap Balita *")
            c1, c2 = st.columns(2)
            tgl_l = c1.date_input("Tanggal Lahir Balita *", value=date(TODAY.year - 1, 1, 1))
            jk = c2.selectbox("Jenis Kelamin *", ["Laki-laki", "Perempuan"])

            usia_bln = max(0.0, round((TODAY.year - tgl_l.year) * 12 + TODAY.month - tgl_l.month + (TODAY.day - tgl_l.day) / 30.4, 1))
            st.caption(f"Usia balita: **{usia_bln:.1f} bulan**")

            ortu_id = user.get("id_peserta", "") or (kids_df["id_orang_tua"].iloc[0] if not kids_df.empty and "id_orang_tua" in kids_df.columns else "")

            submit_anak = st.form_submit_button("Simpan Data Balita 💾", type="primary")

            if submit_anak:
                if not nama_b.strip():
                    st.error("Nama balita wajib diisi.")
                else:
                    sukses, msg, new_id = database.add_additional_child(
                        user_id=user_id,
                        id_orang_tua=ortu_id,
                        data={
                            "nama_balita": nama_b.strip(),
                            "tanggal_lahir": tgl_l,
                            "usia_bulan": usia_bln,
                            "jenis_kelamin": jk,
                            "nama_orang_tua": user.get("nama", ""),
                            "alamat_dusun": user.get("alamat_dusun", "Melati"),
                            "email": user.get("email", "")
                        }
                    )
                    if sukses:
                        st.success(f"✅ {msg}")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")


# ====================================================================
# PUSAT EDUKASI
# ====================================================================
def view_pusat_edukasi():
    is_dark = get_current_theme_is_dark()
    pal = get_theme_palette(is_dark)

    # Palet Tag Kategori Pastel Pink & Harmonis
    BADGE_COLORS = {
        "Ibu Hamil":    ("rgba(244, 114, 182, 0.20)", "#e87a9e"),
        "Balita":       ("rgba(168, 85, 247, 0.18)",  "#a855f7"),
        "Gizi":         ("rgba(16, 185, 129, 0.18)",  "#10b981"),
        "Nutrisi Bayi": ("rgba(251, 146, 60, 0.20)",  "#f97316"),
        "Imunisasi":    ("rgba(2, 132, 199, 0.18)",   "#0284c7"),
        "Pencegahan":   ("rgba(239, 68, 68, 0.18)",   "#ef4444"),
    }
    KATEGORI_LIST = ["Semua"] + list(BADGE_COLORS.keys())

    # State Init
    for key, default in [
        ("articles_read", set()),
        ("edu_bookmarks", set()),
        ("quiz_results", {}),
        ("edu_filter", "Semua"),
        ("edu_search", ""),
        ("selected_edu", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    artikel_all = database.get_edukasi_list()

    # ================================================================
    # HALAMAN DETAIL MATERI (JIKA SALAH SATU DIKLIK)
    # ================================================================
    if st.session_state.get("selected_edu"):
        art_id = st.session_state["selected_edu"]
        art_map = {a["id"]: a for a in artikel_all}
        art = art_map.get(art_id)

        if art is None:
            st.session_state["selected_edu"] = None
            st.rerun()

        st.session_state["articles_read"].add(art_id)

        # Tombol kembali
        col_back, col_bm = st.columns([6, 2])
        with col_back:
            if st.button("← Kembali ke Pusat Edukasi", key="btn_kembali_edu", type="secondary"):
                st.session_state["selected_edu"] = None
                st.rerun()

        is_bookmarked = art_id in st.session_state["edu_bookmarks"]
        with col_bm:
            bm_label = "🔖 Tersimpan" if is_bookmarked else "🤍 Simpan Materi"
            if st.button(bm_label, key=f"detail_bm_{art_id}", use_container_width=True):
                if is_bookmarked:
                    st.session_state["edu_bookmarks"].discard(art_id)
                else:
                    st.session_state["edu_bookmarks"].add(art_id)
                st.rerun()

        badge_bg, badge_fg = BADGE_COLORS.get(art.get("kategori", ""), (pal["primary_light"], pal["primary"]))

        # Banner Header Materi Interaktif
        st.markdown(
            f"""
            <div style="background:{pal['bg_card']}; border:2px solid {pal['border_glow']}; border-radius:24px; padding:30px; margin: 15px 0 25px; box-shadow:{pal['shadow']};">
                <div style="display:flex; align-items:center; gap:20px;">
                    <div style="width:72px; height:72px; border-radius:22px; background:{pal['primary_light']}; display:grid; place-items:center; font-size:2.8rem; border:1px solid {pal['border_glass']}; flex-shrink:0;">
                        {art.get('icon', '🌸')}
                    </div>
                    <div>
                        <div style="display:flex; gap:10px; align-items:center; margin-bottom:8px;">
                            <span style="background:{badge_bg}; color:{badge_fg}; padding:4px 14px; border-radius:99px; font-size:0.78rem; font-weight:700; text-transform:uppercase;">
                                {art.get('kategori', '')}
                            </span>
                            <span style="background:rgba(16,185,129,0.18); color:#10b981; padding:4px 12px; border-radius:99px; font-size:0.78rem; font-weight:700;">
                                ✅ Terverifikasi Kemenkes RI
                            </span>
                        </div>
                        <h2 style="font-size:1.85rem; font-weight:900; color:{pal['text_title']}; margin:0; line-height:1.25;">
                            {art.get('judul', '')}
                        </h2>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Ringkasan Card
        st.markdown(
            f"""
            <div style="background:{pal['primary_light']}; border-left:5px solid {pal['primary']}; border-radius:12px; padding:18px 22px; margin-bottom:24px; font-size:1.02rem; color:{pal['text_main']}; line-height:1.6;">
                💡 <b>Ringkasan Utama:</b><br>{art.get('ringkasan', '')}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Poin Kunci Edukasi
        st.markdown(f"<h3 style='color:{pal['text_title']}; margin-bottom:12px;'>📋 Panduan & Langkah Praktis</h3>", unsafe_allow_html=True)
        poin_kunci = art.get("poin_kunci", [])
        for idx, p in enumerate(poin_kunci, 1):
            st.markdown(
                f"""
                <div style="display:flex; align-items:flex-start; gap:14px; background:{pal['bg_card']}; border:1px solid {pal['border_glass']}; border-radius:14px; padding:16px 20px; margin-bottom:12px; box-shadow:{pal['shadow']};">
                    <span style="width:28px; height:28px; border-radius:50%; background:{pal['primary']}; color:#fff; display:grid; place-items:center; font-weight:800; font-size:0.85rem; flex-shrink:0;">
                        {idx}
                    </span>
                    <span style="font-size:0.96rem; color:{pal['text_main']}; line-height:1.5;">{p}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Saran & Rekomendasi Kader/Dokter
        saran = art.get("saran", "")
        if saran:
            st.markdown(
                f"""
                <div style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.35); border-radius:16px; padding:20px; margin-top:20px; display:flex; align-items:center; gap:16px;">
                    <span style="font-size:2rem;">🌟</span>
                    <div>
                        <b style="color:#10b981; font-size:0.95rem;">PESAN PENTING KADER & TENAGA KESEHATAN:</b>
                        <p style="margin:4px 0 0; color:{pal['text_main']}; font-size:0.95rem;">{saran}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Quiz Uji Pemahaman Interaktif
        quiz_items = art.get("quiz", [])
        if quiz_items:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="background:{pal['bg_card']}; border:2px dashed {pal['border_glow']}; border-radius:20px; padding:24px 28px; margin-top:20px;">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
                        <span style="font-size:1.8rem;">🧠</span>
                        <div>
                            <h4 style="margin:0; color:{pal['text_title']}; font-weight:800;">Kuis Pemahaman Kesehatan</h4>
                            <p style="margin:0; font-size:0.84rem; color:{pal['text_muted']};">Jawab pertanyaan singkat di bawah ini untuk menguji pemahaman Anda seputar materi ini.</p>
                        </div>
                    </div>
                """,
                unsafe_allow_html=True
            )

            prev_result = st.session_state["quiz_results"].get(art_id)
            if prev_result is not None:
                skor = prev_result["skor"]
                total = prev_result["total"]
                pct = int(skor / total * 100)
                if pct >= 75:
                    st.success(f"🎉 **Skor Anda: {skor}/{total} ({pct}%)** — Luar biasa! Pemahaman Anda sangat baik.")
                else:
                    st.warning(f"📝 **Skor Anda: {skor}/{total} ({pct}%)** — Ayo pelajari lagi poin penting di atas!")

                if st.button("🔄 Ulangi Kuis", key=f"retry_quiz_{art_id}"):
                    del st.session_state["quiz_results"][art_id]
                    st.rerun()
            else:
                answers = {}
                for qi, q_item in enumerate(quiz_items):
                    answers[qi] = st.radio(
                        f"**{qi+1}. {q_item['q']}**",
                        options=q_item["opts"],
                        key=f"quiz_{art_id}_{qi}",
                        index=None
                    )

                if st.button("📝 Kumpulkan Jawaban Kuis", key=f"submit_quiz_{art_id}", type="primary"):
                    unanswered = [i for i, v in answers.items() if v is None]
                    if unanswered:
                        st.warning(f"⚠️ Masih ada {len(unanswered)} pertanyaan yang belum dijawab.")
                    else:
                        skor = sum(
                            1 for qi, q_item in enumerate(quiz_items)
                            if answers[qi] == q_item["opts"][q_item["ans"]]
                        )
                        st.session_state["quiz_results"][art_id] = {"skor": skor, "total": len(quiz_items)}
                        st.balloons()
                        st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        return

    # ================================================================
    # HALAMAN UTAMA PUSAT EDUKASI: VISUAL MENARIK, INTERAKTIF & LENGKAP
    # ================================================================
    page_header("📚 Pusat Edukasi Posyandu", "Materi kesehatan interaktif, panduan gizi seimbang, kehamilan, ASI, dan pencegahan stunting")

    # ── 1. BANNER HERO VISUAL DENGAN STATISTIK PEMBACA ──
    total_art = len(artikel_all)
    read_count = len(st.session_state["articles_read"])
    saved_count = len(st.session_state["edu_bookmarks"])
    progress_pct = read_count / total_art if total_art else 0

    st.markdown(
        f"""
        <div style="background:{pal['bg_card']}; border:1px solid {pal['border_glass']}; border-radius:24px; padding:24px 28px; margin-bottom:20px; box-shadow:{pal['shadow']};">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
                <div>
                    <div style="display:inline-flex; align-items:center; gap:8px; padding:4px 14px; border-radius:99px; background:{pal['primary_light']}; border:1px solid {pal['border_glass']}; font-size:0.78rem; font-weight:700; color:{pal['primary']}; margin-bottom:8px;">
                        ✨ Ruang Edukasi & Literasi Posyandu
                    </div>
                    <h2 style="font-size:1.6rem; font-weight:900; color:{pal['text_title']}; margin:0;">
                        Tingkatkan Pengetahuan Kesehatan Keluarga Anda
                    </h2>
                    <p style="color:{pal['text_muted']}; font-size:0.92rem; margin:6px 0 0;">
                        Kumpulan pedoman resmi berbasis rujukan Kementerian Kesehatan RI dan WHO yang dikemas ceria & mudah dipahami.
                    </p>
                </div>
                <div style="display:flex; gap:14px;">
                    <div style="text-align:center; padding:12px 20px; background:{pal['primary_light']}; border-radius:18px; border:1px solid {pal['border_glass']};">
                        <div style="font-size:1.4rem; font-weight:900; color:{pal['primary']};">{read_count}/{total_art}</div>
                        <small style="color:{pal['text_muted']}; font-weight:600;">Materi Dibaca</small>
                    </div>
                    <div style="text-align:center; padding:12px 20px; background:rgba(168,85,247,0.12); border-radius:18px; border:1px solid rgba(168,85,247,0.25);">
                        <div style="font-size:1.4rem; font-weight:900; color:#a855f7;">{saved_count}</div>
                        <small style="color:{pal['text_muted']}; font-weight:600;">Tersimpan</small>
                    </div>
                </div>
            </div>
            <div style="margin-top:16px;">
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:700; color:{pal['text_muted']}; margin-bottom:6px;">
                    <span>Progres Pembacaan Mandiri</span>
                    <span>{int(progress_pct*100)}% Selesai</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.progress(progress_pct)

    # ── 2. AUTO-SLIDING CAROUSEL POPULER ──
    st.markdown(f"<h3 style='color:{pal['text_title']}; font-weight:800; margin-top:1.8rem; margin-bottom:0.2rem;'>🔥 Materi Edukasi Terpopuler</h3>", unsafe_allow_html=True)
    st.caption("Arahkan kursor pada card materi untuk menjeda putaran otomatis dan klik card untuk mempelajari materi.")
    st.html(render_edu_carousel_html(artikel_all, is_dark=is_dark))

    # ── 3. FILTER, PENCARIAN, & TABS DAFTAR MATERI ──
    st.markdown(f"<h3 style='color:{pal['text_title']}; font-weight:800; margin-top:1rem;'>📖 Jelajahi Seluruh Koleksi Edukasi</h3>", unsafe_allow_html=True)

    tab_koleksi, tab_favorit = st.tabs(["📚 Semua Koleksi Materi", "🔖 Materi Tersimpan (Favorit)"])

    def _render_cards(list_artikel):
        if not list_artikel:
            st.info("📭 Tidak ada materi yang cocok dengan pencarian atau filter yang dipilih.")
            return

        COLS = 3
        for i in range(0, len(list_artikel), COLS):
            chunk = list_artikel[i:i+COLS]
            cols = st.columns(COLS)
            for c_idx, art in enumerate(chunk):
                with cols[c_idx]:
                    b_bg, b_fg = BADGE_COLORS.get(art.get("kategori", ""), (pal["primary_light"], pal["primary"]))
                    is_read = art["id"] in st.session_state["articles_read"]
                    is_bm = art["id"] in st.session_state["edu_bookmarks"]

                    # Visual Card HTML
                    st.markdown(
                        f"""
                        <div style="background:{pal['bg_card']}; border:1.5px solid {pal['border_glass']}; border-radius:20px; padding:22px 20px; margin-bottom:10px; box-shadow:{pal['shadow']}; min-height:260px; display:flex; flex-direction:column; justify-content:space-between;">
                            <div>
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                                    <div style="width:48px; height:48px; border-radius:14px; background:{pal['primary_light']}; display:grid; place-items:center; font-size:1.8rem;">
                                        {art.get('icon', '🌸')}
                                    </div>
                                    <span style="background:{b_bg}; color:{b_fg}; padding:3px 12px; border-radius:99px; font-size:0.74rem; font-weight:700; text-transform:uppercase;">
                                        {art.get('kategori', '')}
                                    </span>
                                </div>
                                <h4 style="font-size:1.05rem; font-weight:800; color:{pal['text_title']}; margin:0 0 8px; line-height:1.35;">
                                    {art.get('judul', '')}
                                </h4>
                                <p style="font-size:0.84rem; color:{pal['text_muted']}; line-height:1.5; margin:0;">
                                    {art.get('ringkasan', '')[:110]}...
                                </p>
                            </div>
                            <div style="margin-top:14px; display:flex; align-items:center; justify-content:space-between;">
                                <span style="font-size:0.75rem; color:{'#10b981' if is_read else pal['text_muted']}; font-weight:700;">
                                    {'✅ Selesai Dibaca' if is_read else '⏳ Belum Dibaca'}
                                </span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    btn_c1, btn_c2 = st.columns([3, 1])
                    with btn_c1:
                        if st.button("Buka Materi ➜", key=f"btn_buka_{art['id']}", type="primary", use_container_width=True):
                            st.session_state["selected_edu"] = art["id"]
                            st.rerun()
                    with btn_c2:
                        bm_sym = "🔖" if is_bm else "🤍"
                        if st.button(bm_sym, key=f"btn_bm_{art['id']}", help="Simpan materi ini", use_container_width=True):
                            if is_bm:
                                st.session_state["edu_bookmarks"].discard(art["id"])
                            else:
                                st.session_state["edu_bookmarks"].add(art["id"])
                            st.rerun()

    with tab_koleksi:
        # Search & Category Filter
        f_col1, f_col2 = st.columns([2, 1])
        with f_col1:
            q_search = st.text_input("🔍 Cari Materi Edukasi:", placeholder="Ketik kata kunci (contoh: stunting, ASI, anemia, gizi...)", key="edu_search_box")
        with f_col2:
            kat_pilihan = st.selectbox("📂 Filter Berdasarkan Kategori:", options=KATEGORI_LIST, key="edu_kat_sel")

        filtered = artikel_all
        if kat_pilihan != "Semua":
            filtered = [a for a in filtered if a.get("kategori") == kat_pilihan]
        if q_search.strip():
            kw = q_search.strip().lower()
            filtered = [
                a for a in filtered
                if kw in a.get("judul", "").lower() or kw in a.get("ringkasan", "").lower()
            ]

        _render_cards(filtered)

    with tab_favorit:
        saved_items = [a for a in artikel_all if a["id"] in st.session_state["edu_bookmarks"]]
        if not saved_items:
            st.markdown(
                f"""
                <div style="text-align:center; padding:40px 20px; background:{pal['bg_card']}; border:1px dashed {pal['border_glass']}; border-radius:20px; margin:20px 0;">
                    <span style="font-size:3rem;">🔖</span>
                    <h4 style="color:{pal['text_title']}; margin:12px 0 6px;">Belum Ada Materi Tersimpan</h4>
                    <p style="color:{pal['text_muted']}; font-size:0.88rem; max-width:400px; margin:0 auto;">
                        Klik ikon 🤍 pada materi apa saja untuk menyimpannya di sini agar mudah dibaca kembali sewaktu-waktu.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            _render_cards(saved_items)



# ====================================================================
# MAIN APPLICATION CONTROLLER
# ====================================================================

# ====================================================================
# MAIN APPLICATION CONTROLLER
# ====================================================================
def main():
    if "user" not in st.session_state:
        landing_and_auth_page()
        return

    is_dark = get_current_theme_is_dark()
    inject_custom_css(logged_in=True)
    user = st.session_state["user"]
    role = user.get("role", "Kader")
    logo_src = get_logo_base64()
    db_status = database.get_db_status()
    pal = get_theme_palette(is_dark)

    # Cek Onboarding Biodata
    if not database.has_completed_biodata(user):
        view_onboarding_biodata(user)
        return

    # Sidebar Navigasi Pastel Pink Responsive (Hover Expand/Collapse)
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-header-box">
                <img src="{logo_src}" class="sidebar-logo-img" alt="Logo Posyandu">
                <div class="sidebar-brand-text">
                    <b>Posyandu Digital</b>
                    <small>👤 {user.get('nama', 'Pengguna')}</small><br>
                    <span style="display:inline-block; margin-top:4px; padding:2px 10px; border-radius:99px; background:{pal['primary_light']}; color:{pal['primary']}; font-size:0.72rem; font-weight:700;">{role}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(f"Status DB: **{db_status['mode_label']}**")
        
        # Toggle Light / Dark Mode di Sidebar
        theme_icon = "☀️" if is_dark else "🌙"
        theme_txt = "Mode Terang" if is_dark else "Mode Gelap"
        if st.sidebar.button(f"{theme_icon} {theme_txt}", key="side_theme_toggle", use_container_width=True):
            st.session_state["is_dark_theme"] = not is_dark
            st.rerun()

        st.divider()

        menu_items = MENU.get(role, [])
        if "page" not in st.session_state or st.session_state["page"] not in menu_items:
            st.session_state["page"] = menu_items[0]

        for item in menu_items:
            is_active = (st.session_state["page"] == item)
            btn_type = "primary" if is_active else "secondary"
            if st.sidebar.button(item, key=f"nav_btn_{item}", type=btn_type, use_container_width=True):
                st.session_state["page"] = item
                st.rerun()

        st.divider()

        if st.sidebar.button("🚪 Keluar (Logout)", key="logout_btn", use_container_width=True):
            database.sign_out_user()
            st.session_state.clear()
            st.rerun()

        st.caption("Aplikasi Posyandu Digital &copy; 2026")

    current_page = st.session_state.get("page", menu_items[0])

    if role == "Kader":
        if current_page == "🏠 Dashboard Posyandu":
            view_kader_dashboard()
        elif current_page == "👥 Data Peserta & Riwayat":
            view_kader_peserta()
        elif current_page == "🧒 Pemeriksaan Balita":
            view_kader_balita()
        elif current_page == "🤰 Pemeriksaan Ibu Hamil":
            view_kader_ibu()
        elif current_page == "📊 Laporan Visualisasi Dinamis":
            view_kader_laporan()
        elif current_page == "🗂️ Riwayat Laporan Puskesmas":
            view_kader_riwayat_laporan()
        elif current_page == "📚 Pusat Edukasi Posyandu":
            view_pusat_edukasi()

    elif role == "Ibu Hamil":
        if current_page == "🏠 Dashboard Kehamilan":
            view_ibu_dashboard(user)
        elif current_page == "📖 Buku KIA Digital":
            view_ibu_kia(user)
        elif current_page == "👤 Profil & Biodata Ibu":
            view_ibu_profil(user)
        elif current_page == "📚 Edukasi Kehamilan":
            view_pusat_edukasi()

    elif role == "Orang Tua Balita":
        if current_page == "🏠 Dashboard Tumbuh Kembang":
            view_ortu_dashboard(user)
        elif current_page == "📈 Grafik Z-Score & KMS":
            view_ortu_grafik(user)
        elif current_page == "👶 Data & Tambah Balita":
            view_ortu_tambah_balita(user)
        elif current_page == "📚 Edukasi Gizi & MP-ASI":
            view_pusat_edukasi()


if __name__ == "__main__":
    main()
