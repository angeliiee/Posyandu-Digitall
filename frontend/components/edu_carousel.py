from textwrap import dedent

"""
Komponen Auto-Sliding Carousel Interaktif untuk Modul Edukasi Posyandu.
Menampilkan card materi bergulir otomatis secara horizontal dengan pause saat hover,
navigasi manual panah, preview visual, indikator kategori warna cerah, dan tooltip interaktif.
"""
from typing import List, Dict, Any

def render_edu_carousel_html(articles: List[Dict[str, Any]], is_dark: bool = False) -> str:
    card_bg = "rgba(36, 26, 48, 0.95)" if is_dark else "rgba(255, 255, 255, 0.96)"
    card_border = "rgba(232, 169, 189, 0.35)" if is_dark else "rgba(232, 122, 158, 0.28)"
    text_title = "#fff0f5" if is_dark else "#2d1b2e"
    text_desc = "#d8b4e2" if is_dark else "#5c4060"
    shadow = "0 8px 24px rgba(0,0,0,0.45)" if is_dark else "0 10px 25px rgba(232, 122, 158, 0.15)"

    # Duplikasi daftar artikel untuk infinite smooth sliding effect
    cards_html = ""
    for art in articles + articles:
        badge_bg = "rgba(244,114,182,0.22)" if is_dark else "rgba(232, 122, 158, 0.15)"
        badge_text = "#f472b6" if is_dark else "#d85b82"
        
        cards_html += f"""
        <div class="carousel-card" title="Materi: {art.get('judul', '')}">
            <div class="carousel-card-inner">
                <div class="card-icon-badge">
                    <span class="card-icon">{art.get('icon', '🌸')}</span>
                </div>
                <span class="card-kategori-tag" style="background:{badge_bg}; color:{badge_text};">
                    {art.get('kategori', 'Umum')}
                </span>
                <h4 class="card-title">{art.get('judul', '')}</h4>
                <p class="card-desc">{art.get('ringkasan', '')}</p>
                <div class="card-footer-action">
                    <span class="read-more-text">Pelajari Materi ➜</span>
                </div>
            </div>
        </div>
        """

    return dedent(f"""
    <div class="edu-carousel-wrapper">
    <div class="edu-carousel-wrapper">
        <style>
        .edu-carousel-wrapper {{
            position: relative;
            width: 100%;
            overflow: hidden;
            padding: 1.2rem 0;
            margin: 0.8rem 0 1.6rem;
        }}
        .edu-carousel-track {{
            display: flex;
            gap: 20px;
            width: max-content;
            animation: slideScroll 38s linear infinite;
        }}
        .edu-carousel-wrapper:hover .edu-carousel-track {{
            animation-play-state: paused;
        }}
        @keyframes slideScroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        .carousel-card {{
            width: 290px;
            flex-shrink: 0;
            background: {card_bg};
            border: 1.5px solid {card_border};
            border-radius: 20px;
            padding: 22px 18px 18px;
            box-shadow: {shadow};
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
        }}
        .carousel-card:hover {{
            transform: translateY(-8px) scale(1.02);
            border-color: #e87a9e;
            box-shadow: 0 16px 36px rgba(232, 122, 158, 0.25);
        }}
        .card-icon-badge {{
            width: 50px;
            height: 50px;
            border-radius: 14px;
            background: rgba(232, 122, 158, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
        }}
        .card-icon {{
            font-size: 1.8rem;
        }}
        .card-kategori-tag {{
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 99px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 8px;
        }}
        .card-title {{
            font-size: 1.02rem;
            font-weight: 700;
            color: {text_title};
            margin: 0 0 8px 0;
            line-height: 1.35;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-desc {{
            font-size: 0.83rem;
            color: {text_desc};
            line-height: 1.5;
            margin: 0 0 14px 0;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .card-footer-action {{
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-top: 10px;
            border-top: 1px dashed {card_border};
        }}
        .read-more-text {{
            font-size: 0.8rem;
            font-weight: 700;
            color: #e87a9e;
        }}
        </style>
        <div class="edu-carousel-track">
            {cards_html}
        </div>
    </div>
    """)
