"""
frontend/components/tables.py
Komponen tabel interaktif dengan dropdown variabel, pencarian, dan pengurutan.
"""
from typing import List, Optional

import numpy as np
import pandas as pd
import streamlit as st


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
