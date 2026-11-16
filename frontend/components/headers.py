"""
frontend/components/headers.py
Komponen header dan utilitas tanggal/logo.
"""
import base64
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "JEJAK_TUMBUH.jpeg"


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
