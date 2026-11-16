"""
====================================================================
MODUL TEMA & CSS: BRIGHT PASTEL PINK HEALTHCARE THEME
Dual Engine: Bright Pastel Pink (Light Mode) & Soft Plum (Dark Mode)
====================================================================
"""
import streamlit as st

def get_theme_palette(is_dark: bool) -> dict:
    if is_dark:
        # Dark Mode yang harmonis dengan nuansa pastel pink lembut (Plum & Rose Dark)
        return {
            "bg_main": "#15101a",
            "bg_gradient": "linear-gradient(135deg, #1b1222 0%, #15101a 50%, #100b16 100%)",
            "bg_card": "rgba(32, 23, 42, 0.85)",
            "bg_card_hover": "rgba(46, 33, 60, 0.95)",
            "bg_sidebar": "linear-gradient(180deg, #1f1429 0%, #160e1d 100%)",
            "border_glass": "rgba(232, 169, 189, 0.25)",
            "border_glow": "rgba(244, 114, 182, 0.55)",
            "text_title": "#fff0f5",
            "text_main": "#fce7f3",
            "text_sub": "#d8b4e2",
            "text_muted": "#b49bb8",
            "primary": "#f472b6",            # Bright pastel rose pink
            "primary_hover": "#ec4899",
            "primary_light": "rgba(244, 114, 182, 0.20)",
            "accent_purple": "#c084fc",
            "accent_green": "#34d399",
            "accent_peach": "#fb923c",
            "accent_red": "#f87171",
            "accent_sky": "#38bdf8",
            "input_bg": "rgba(28, 19, 38, 0.88)",
            "input_border": "rgba(232, 169, 189, 0.35)",
            "chart_grid": "rgba(255, 255, 255, 0.08)",
            "chart_domain": "rgba(255, 255, 255, 0.18)",
            "chart_label": "#e2e8f0",
            "chart_title": "#fff0f5",
            "chart_palette": ["#f472b6", "#34d399", "#c084fc", "#fb923c", "#f87171", "#38bdf8", "#fbbf24"],
            "shadow": "0 10px 30px rgba(0, 0, 0, 0.45)",
            "shadow_glow": "0 0 25px rgba(244, 114, 182, 0.25)"
        }
    else:
        # Light Mode Pastel Pink Cerah & Ceria Sesuai Keinginan User
        return {
            "bg_main": "#fff9fb",
            "bg_gradient": "linear-gradient(135deg, #fff7fa 0%, #fef2f6 50%, #fdf0f7 100%)",
            "bg_card": "rgba(255, 255, 255, 0.94)",
            "bg_card_hover": "#ffffff",
            "bg_sidebar": "linear-gradient(180deg, #fff2f6 0%, #fbe8f0 100%)",
            "border_glass": "rgba(232, 169, 189, 0.40)",
            "border_glow": "rgba(232, 169, 189, 0.75)",
            "text_title": "#2d1b2e",
            "text_main": "#3f2b40",
            "text_sub": "#6e5270",
            "text_muted": "#8f7591",
            "primary": "#e87a9e",            # Pastel pink cerah identitas utama
            "primary_hover": "#d86288",
            "primary_light": "rgba(232, 122, 158, 0.15)",
            "accent_purple": "#a855f7",
            "accent_green": "#10b981",
            "accent_peach": "#f97316",
            "accent_red": "#ef4444",
            "accent_sky": "#0284c7",
            "input_bg": "#ffffff",
            "input_border": "rgba(232, 169, 189, 0.50)",
            "chart_grid": "rgba(180, 140, 165, 0.16)",
            "chart_domain": "rgba(180, 140, 165, 0.32)",
            "chart_label": "#4c385c",
            "chart_title": "#2d1b2e",
            "chart_palette": ["#e87a9e", "#10b981", "#a855f7", "#f97316", "#ef4444", "#0284c7", "#eab308"],
            "shadow": "0 8px 26px rgba(232, 122, 158, 0.12)",
            "shadow_glow": "0 0 22px rgba(232, 122, 158, 0.28)"
        }

def inject_app_css(is_dark: bool = False, is_landing: bool = False):
    p = get_theme_palette(is_dark)
    
    sidebar_css = "" if not is_landing else """
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stMain"], section.main { margin-left: 0 !important; width: 100% !important; }
    """
    
    css = f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    :root {{
        --bg-main: {p["bg_main"]};
        --bg-card: {p["bg_card"]};
        --bg-card-hover: {p["bg_card_hover"]};
        --border-glass: {p["border_glass"]};
        --border-glow: {p["border_glow"]};
        --text-title: {p["text_title"]};
        --text-main: {p["text_main"]};
        --text-sub: {p["text_sub"]};
        --text-muted: {p["text_muted"]};
        --primary: {p["primary"]};
        --primary-hover: {p["primary_hover"]};
        --primary-light: {p["primary_light"]};
        --radius: 18px;
    }}

    .stApp, .stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stCaptionContainer"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: {p["text_main"]};
    }}

    h1, h2, h3, h4, h5, h6, [data-testid="stMetricValue"] {{
        color: {p["text_title"]} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: {p["bg_gradient"]} !important;
        background-attachment: fixed;
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient({p["primary_light"]} 1.3px, transparent 1.3px);
        background-size: 28px 28px;
        pointer-events: none;
        z-index: 0;
    }}

    #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
    }}

    [data-testid="stMainBlockContainer"] {{
        padding-top: 1rem !important;
        max-width: 1260px;
    }}

    /* ─── CARD CONTAINER ─── */
    [data-testid="stForm"], [data-testid="stExpander"], [class*="st-key-card_"] {{
        background: {p["bg_card"]} !important;
        backdrop-filter: blur(18px) !important;
        -webkit-backdrop-filter: blur(18px) !important;
        border: 1px solid {p["border_glass"]} !important;
        border-radius: var(--radius) !important;
        box-shadow: {p["shadow"]} !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    [data-testid="stForm"]:hover, [class*="st-key-card_"]:hover {{
        border-color: {p["border_glow"]} !important;
        box-shadow: {p["shadow_glow"]} !important;
    }}

    /* ─── METRICS / STAT CARDS ─── */
    [data-testid="stMetric"] {{
        background: {p["bg_card"]} !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid {p["border_glass"]} !important;
        border-radius: var(--radius) !important;
        padding: 16px 20px !important;
        box-shadow: {p["shadow"]} !important;
        transition: transform 0.25s ease, border-color 0.25s ease !important;
    }}

    [data-testid="stMetric"]:hover {{
        transform: translateY(-3px);
        border-color: {p["primary"]};
        box-shadow: {p["shadow_glow"]} !important;
    }}

    [data-testid="stMetricLabel"] p {{
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        color: {p["text_muted"]} !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* ─── BUTTONS ─── */
    .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button {{
        border-radius: 14px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.4rem !important;
        border: 1px solid {p["border_glass"]} !important;
        background: {p["bg_card"]} !important;
        color: {p["text_title"]} !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover {{
        transform: translateY(-2px);
        border-color: {p["primary"]} !important;
        box-shadow: 0 6px 20px {p["primary_light"]} !important;
        color: {p["primary"]} !important;
    }}

    button[kind="primary"], button[kind="primaryFormSubmit"] {{
        background: linear-gradient(135deg, {p["primary"]} 0%, {p["accent_purple"]} 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 4px 18px {p["primary_light"]} !important;
    }}

    button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {{
        box-shadow: 0 8px 28px {p["border_glow"]} !important;
        color: #ffffff !important;
    }}

    /* ─── INPUT FIELDS ─── */
    [data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] {{
        background: {p["input_bg"]} !important;
        border: 1px solid {p["input_border"]} !important;
        border-radius: 12px !important;
        color: {p["text_title"]} !important;
    }}

    [data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {{
        border-color: {p["primary"]} !important;
        box-shadow: 0 0 16px {p["primary_light"]} !important;
    }}

    /* ─── TABS ─── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent;
    }}
    [data-testid="stTabs"] [data-baseweb="tab"] {{
        border-radius: 12px 12px 0 0 !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        color: {p["text_muted"]} !important;
        border: none !important;
    }}
    [data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {{
        color: {p["primary"]} !important;
        border-bottom: 3px solid {p["primary"]} !important;
        background: {p["primary_light"]} !important;
    }}

    /* ─── HEADER BANNER ─── */
    .hdr-banner {{
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 20px 26px;
        margin-bottom: 1.4rem;
        border-radius: var(--radius);
        background: {p["bg_card"]};
        backdrop-filter: blur(18px);
        border: 1px solid {p["border_glass"]};
        box-shadow: {p["shadow"]};
    }}

    .hdr-banner .hdr-icon {{
        width: 54px;
        height: 54px;
        flex: none;
        border-radius: 16px;
        background: {p["primary_light"]};
        border: 1px solid {p["border_glass"]};
        display: grid;
        place-items: center;
        font-size: 1.8rem;
    }}

    .hdr-banner h1 {{
        margin: 0 !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        color: {p["text_title"]} !important;
        line-height: 1.25;
    }}

    .hdr-banner p {{
        margin: 4px 0 0 !important;
        color: {p["text_muted"]} !important;
        font-size: 0.92rem;
    }}

    /* ─── RESPONSIVE HOVER SIDEBAR ─── */
    section[data-testid='stSidebar'] {{
        position: fixed !important;
        inset: 0 auto 0 0 !important;
        top: 0 !important;
        height: 100vh !important;
        height: 100dvh !important;
        width: 72px !important;
        min-width: 72px !important;
        max-width: none !important;
        transform: none !important;
        margin: 0 !important;
        visibility: visible !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        z-index: 1000 !important;
        background: {p["bg_sidebar"]} !important;
        border-right: 1px solid {p["border_glass"]} !important;
        transition: width 0.32s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.32s ease !important;
    }}

    section[data-testid='stSidebar']:hover {{
        width: 290px !important;
        box-shadow: 10px 0 35px rgba(0, 0, 0, { "0.55" if is_dark else "0.10" }) !important;
    }}

    section[data-testid='stSidebar'] > div {{
        width: 290px !important;
        height: 100% !important;
        padding-top: 0 !important;
    }}

    section[data-testid='stSidebar'] [data-testid='stSidebarContent'] {{
        padding: 1.1rem 0.7rem !important;
    }}

    [data-testid='stSidebarCollapseButton'], [data-testid='collapsedControl'],
    [data-testid='stSidebarCollapsedControl'], [data-testid='stSidebarHeader'] {{
        display: none !important;
    }}

    [data-testid='stMain'], section.main {{
        margin-left: 72px !important;
        width: calc(100% - 72px) !important;
        transition: margin-left 0.32s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    section[data-testid='stSidebar'] * {{
        white-space: nowrap !important;
    }}

    section[data-testid='stSidebar'] button {{
        justify-content: flex-start !important;
        text-align: left !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        color: {p["text_main"]} !important;
        padding: 0.65rem 0.9rem !important;
        border-radius: 12px !important;
        transition: background 0.2s ease, transform 0.2s ease !important;
    }}

    section[data-testid='stSidebar'] button:hover {{
        background: {p["primary_light"]} !important;
        color: {p["primary"]} !important;
        transform: translateX(4px) !important;
    }}

    section[data-testid='stSidebar'] button[kind='primary'] {{
        background: {p["primary_light"]} !important;
        border-left: 3px solid {p["primary"]} !important;
        font-weight: 700 !important;
        color: {p["primary"]} !important;
    }}

    section[data-testid='stSidebar'] hr {{
        margin: 0.8rem 0 !important;
        border-color: {p["border_glass"]} !important;
    }}

    .sidebar-header-box {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 6px 14px;
    }}

    .sidebar-logo-img {{
        width: 44px;
        height: 44px;
        min-width: 44px;
        border-radius: 14px;
        object-fit: cover;
        box-shadow: 0 4px 14px {p["primary_light"]};
        border: 2px solid {p["border_glass"]};
    }}

    .sidebar-brand-text b {{
        font-size: 1.05rem;
        color: {p["text_title"]};
        display: block;
        line-height: 1.2;
    }}

    .sidebar-brand-text small {{
        color: {p["text_muted"]};
        font-size: 0.82rem;
    }}

    /* ─── THEME TOGGLE PILL ─── */
    .theme-toggle-bar {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.6rem;
    }}

    /* ─── EDUKASI STYLES ─── */
    .edu-hero-banner {{
        background: linear-gradient(135deg, {p["primary_light"]} 0%, rgba(192, 132, 252, 0.12) 100%);
        border: 1px solid {p["border_glow"]};
        border-radius: 20px;
        padding: 24px 30px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: {p["shadow"]};
    }}

    .edu-card-v2 {{
        background: {p["bg_card"]};
        border: 1px solid {p["border_glass"]};
        border-radius: 16px;
        padding: 20px;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        box-shadow: {p["shadow"]};
    }}
    .edu-card-v2:hover {{
        border-color: {p["primary"]};
        box-shadow: {p["shadow_glow"]};
        transform: translateY(-4px);
    }}

    .edu-badge-v2 {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}

    .edu-quiz-card {{
        background: {p["primary_light"]};
        border: 1px solid {p["border_glow"]};
        border-radius: 16px;
        padding: 24px;
        margin-top: 24px;
    }}

    {sidebar_css}
    </style>"""
    st.markdown(css, unsafe_allow_html=True)
