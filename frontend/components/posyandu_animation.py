"""
Komponen Animasi Lingkungan Posyandu 2D Pastel yang Hidup:
Menampilkan Gedung Posyandu, Dokter/Kader melambaikan tangan, Ibu Hamil, Ibu dan Balita bermain,
Pohon & Bunga bergoyang sepoi-sepoi, Awan berarak, Matahari bersinar lembut,
dan Tooltip Interaktif untuk edukasi kesehatan.
"""

def get_posyandu_animation_svg(is_dark: bool = False) -> str:
    # Warna pastel sesuai mode
    sky_top = "#1a1226" if is_dark else "#fee2e2"
    sky_bot = "#2a1b3d" if is_dark else "#fdf2f8"
    ground_col = "#2e1a38" if is_dark else "#fbcfe8"
    ground_grad = "#1f1227" if is_dark else "#f472b6"
    wall_col = "#3b224c" if is_dark else "#fff1f2"
    wall_border = "#f472b6" if is_dark else "#f43f5e"
    roof_col = "#be185d" if is_dark else "#fb7185"
    text_col = "#fdf2f8" if is_dark else "#1e1329"

    return f"""
    <div class="posyandu-scenery-container">
    <style>
        .posyandu-scenery-container {{
            width: 100%;
            max-width: 960px;
            margin: 1.5rem auto 2.5rem;
            border-radius: 26px;
            overflow: hidden;
            box-shadow: 0 16px 40px {"rgba(0,0,0,0.4)" if is_dark else "rgba(236,72,153,0.18)"};
            border: 2px solid {"rgba(244,114,182,0.3)" if is_dark else "rgba(244,114,182,0.25)"};
            background: {"#181122" if is_dark else "#fff"};
            position: relative;
        }}

        /* Keyframes Animasi Lembut */
        @keyframes cloudFloatLeft {{
            0% {{ transform: translateX(-40px); }}
            50% {{ transform: translateX(50px); }}
            100% {{ transform: translateX(-40px); }}
        }}
        @keyframes cloudFloatRight {{
            0% {{ transform: translateX(30px); }}
            50% {{ transform: translateX(-40px); }}
            100% {{ transform: translateX(30px); }}
        }}
        @keyframes treeSway {{
            0%, 100% {{ transform: rotate(0deg); }}
            50% {{ transform: rotate(2.5deg); }}
        }}
        @keyframes flowerBreeze {{
            0%, 100% {{ transform: rotate(0deg) translateY(0); }}
            50% {{ transform: rotate(-5deg) translateY(-2px); }}
        }}
        @keyframes sunGlow {{
            0%, 100% {{ transform: scale(1); opacity: 0.95; }}
            50% {{ transform: scale(1.08); opacity: 1; }}
        }}
        @keyframes waveArm {{
            0%, 100% {{ transform: rotate(0deg); }}
            25% {{ transform: rotate(-24deg); }}
            75% {{ transform: rotate(12deg); }}
        }}
        @keyframes childPlay {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-7px) rotate(3deg); }}
        }}
        @keyframes butterflyFly {{
            0% {{ transform: translate(0, 0) rotate(0deg); }}
            25% {{ transform: translate(25px, -18px) rotate(10deg); }}
            50% {{ transform: translate(60px, -6px) rotate(-8deg); }}
            75% {{ transform: translate(35px, 12px) rotate(5deg); }}
            100% {{ transform: translate(0, 0) rotate(0deg); }}
        }}

        .anim-cloud-1 {{ animation: cloudFloatLeft 22s ease-in-out infinite; transform-origin: center; }}
        .anim-cloud-2 {{ animation: cloudFloatRight 28s ease-in-out infinite; transform-origin: center; }}
        .anim-tree {{ animation: treeSway 6s ease-in-out infinite; transform-origin: bottom center; }}
        .anim-flower {{ animation: flowerBreeze 4s ease-in-out infinite; transform-origin: bottom center; }}
        .anim-sun {{ animation: sunGlow 5s ease-in-out infinite; transform-origin: 860px 80px; }}
        .anim-waving-arm {{ animation: waveArm 2.2s ease-in-out infinite; transform-origin: 360px 240px; }}
        .anim-child {{ animation: childPlay 2.8s ease-in-out infinite; transform-origin: bottom center; }}
        .anim-butterfly {{ animation: butterflyFly 8s ease-in-out infinite; }}

        /* Interactive Character & Element Tooltip System */
        .interactive-elem {{
            cursor: pointer;
            transition: transform 0.25s ease, filter 0.25s ease;
        }}
        .interactive-elem:hover {{
            filter: drop-shadow(0 0 10px {"#f472b6" if is_dark else "#ec4899"});
            transform: scale(1.03);
        }}

        .tooltip-bubble {{
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            transform: translateY(8px);
        }}
        .interactive-elem:hover + .tooltip-bubble,
        .interactive-elem:focus + .tooltip-bubble {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>

    <svg viewBox="0 0 960 420" width="100%" height="auto" style="display:block;">
        <defs>
            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="{sky_top}" />
                <stop offset="100%" stop-color="{sky_bot}" />
            </linearGradient>
            <linearGradient id="groundGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="{ground_col}" />
                <stop offset="100%" stop-color="{ground_grad}" />
            </linearGradient>
            <linearGradient id="roofGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="{roof_col}" />
                <stop offset="100%" stop-color="#f43f5e" />
            </linearGradient>
            <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>

        <!-- 1. Langit & Background -->
        <rect width="960" height="420" fill="url(#skyGrad)" />

        <!-- Matahari / Rembulan Lembut -->
        <g class="anim-sun">
            <circle cx="860" cy="80" r="54" fill="{"#fef08a" if not is_dark else "#c084fc"}" opacity="{"0.3" if is_dark else "0.45"}" filter="url(#softGlow)" />
            <circle cx="860" cy="80" r="38" fill="{"#fde047" if not is_dark else "#a855f7"}" />
            {"<!-- Sunbeams -->" if not is_dark else ""}
            <circle cx="860" cy="80" r="28" fill="{"#fef9c3" if not is_dark else "#e9d5ff"}" />
        </g>

        <!-- Awan Berarak -->
        <g class="anim-cloud-1" opacity="{"0.4" if is_dark else "0.75"}">
            <ellipse cx="220" cy="70" rx="45" ry="24" fill="#ffffff" />
            <ellipse cx="255" cy="60" rx="36" ry="26" fill="#ffffff" />
            <ellipse cx="280" cy="72" rx="38" ry="20" fill="#ffffff" />
        </g>
        <g class="anim-cloud-2" opacity="{"0.4" if is_dark else "0.85"}">
            <ellipse cx="640" cy="95" rx="55" ry="26" fill="#ffffff" />
            <ellipse cx="680" cy="85" rx="42" ry="28" fill="#ffffff" />
            <ellipse cx="715" cy="98" rx="40" ry="22" fill="#ffffff" />
        </g>

        <!-- Perbukitan Pastel Belakang -->
        <path d="M-20,330 Q180,240 420,310 T980,280 L980,420 L-20,420 Z" fill="{"#231530" if is_dark else "#fce7f3"}" opacity="0.8" />
        <path d="M-20,340 Q320,270 660,330 T1000,315 L1000,420 L-20,420 Z" fill="{"#1d1127" if is_dark else "#fbcfe8"}" opacity="0.9" />

        <!-- Lapangan Rumput Depan -->
        <rect x="0" y="325" width="960" height="95" fill="url(#groundGrad)" />
        <path d="M0,325 Q240,318 480,325 T960,320 L960,340 Q720,335 480,340 T0,335 Z" fill="{"#4a2152" if is_dark else "#f472b6"}" opacity="0.3" />

        <!-- 2. Gedung Posyandu Rumah Idaman -->
        <g class="interactive-elem" tabindex="0">
            <!-- Bayangan -->
            <ellipse cx="190" cy="355" rx="140" ry="18" fill="rgba(0,0,0,0.14)" />
            <!-- Dinding Rumah -->
            <rect x="75" y="195" width="220" height="150" rx="8" fill="{wall_col}" stroke="{wall_border}" stroke-width="3" />
            <!-- Atap Limas Segitiga Cantik -->
            <polygon points="185,100 50,195 320,195" fill="url(#roofGrad)" />
            <polygon points="185,100 185,195 320,195" fill="rgba(0,0,0,0.08)" />
            <!-- Papan Nama Posyandu -->
            <rect x="110" y="145" width="150" height="36" rx="8" fill="#ffffff" stroke="{wall_border}" stroke-width="2" />
            <text x="185" y="163" font-size="11" font-weight="800" font-family="'Plus Jakarta Sans', sans-serif" fill="#e11d48" text-anchor="middle">🌸 POSYANDU MAWAR</text>
            <text x="185" y="174" font-size="8.5" font-weight="600" font-family="'Plus Jakarta Sans', sans-serif" fill="#64748b" text-anchor="middle">Desa Sehat &bull; Ramah Balita</text>
            <!-- Pintu -->
            <rect x="155" y="255" width="60" height="90" rx="30" fill="{"#4c1d4f" if is_dark else "#fda4af"}" stroke="{wall_border}" stroke-width="2" />
            <circle cx="202" cy="305" r="4.5" fill="#ffffff" />
            <!-- Jendela Kiri -->
            <rect x="95" y="225" width="44" height="48" rx="6" fill="#e0f2fe" stroke="{wall_border}" stroke-width="2" />
            <line x1="117" y1="225" x2="117" y2="273" stroke="{wall_border}" stroke-width="1.5" />
            <line x1="95" y1="249" x2="139" y2="249" stroke="{wall_border}" stroke-width="1.5" />
            <!-- Jendela Kanan -->
            <rect x="230" y="225" width="44" height="48" rx="6" fill="#e0f2fe" stroke="{wall_border}" stroke-width="2" />
            <line x1="252" y1="225" x2="252" y2="273" stroke="{wall_border}" stroke-width="1.5" />
            <line x1="230" y1="249" x2="274" y2="249" stroke="{wall_border}" stroke-width="1.5" />
            <!-- Tanaman Hias Pot Depan Pintu -->
            <rect x="80" y="335" width="22" height="15" rx="3" fill="#fb923c" />
            <circle cx="91" cy="330" r="14" fill="#34d399" />
            <rect x="270" y="335" width="22" height="15" rx="3" fill="#fb923c" />
            <circle cx="281" cy="330" r="14" fill="#34d399" />
        </g>
        <!-- Tooltip Posyandu -->
        <g class="tooltip-bubble">
            <rect x="100" y="70" width="180" height="48" rx="10" fill="{"#1e1329" if is_dark else "#ffffff"}" stroke="#f472b6" stroke-width="1.8" filter="url(#softGlow)" />
            <polygon points="185,118 193,126 177,126" fill="{"#1e1329" if is_dark else "#ffffff"}" />
            <text x="190" y="88" font-size="10.5" font-weight="700" fill="#ec4899" text-anchor="middle">🏥 Pos Pelayanan Terpadu</text>
            <text x="190" y="103" font-size="9" fill="{text_col}" text-anchor="middle">Buka rutin setiap bulan!</text>
        </g>

        <!-- 3. Pohon Rindang Bergoyang (Kiri & Kanan) -->
        <g class="anim-tree" style="transform-origin: 30px 350px;">
            <rect x="22" y="220" width="18" height="130" rx="6" fill="#854d0e" />
            <circle cx="31" cy="190" r="50" fill="#10b981" />
            <circle cx="5" cy="180" r="38" fill="#34d399" />
            <circle cx="55" cy="185" r="42" fill="#059669" />
            <circle cx="31" cy="140" r="40" fill="#6ee7b7" />
        </g>
        <g class="anim-tree" style="transform-origin: 900px 350px;">
            <rect x="890" y="210" width="20" height="140" rx="6" fill="#854d0e" />
            <circle cx="900" cy="180" r="55" fill="#10b981" />
            <circle cx="870" cy="170" r="42" fill="#34d399" />
            <circle cx="930" cy="175" r="45" fill="#059669" />
            <circle cx="900" cy="130" r="44" fill="#a7f3d0" />
        </g>

        <!-- 4. Karakter 1: Bidan / Kader Posyandu (Melambaikan Tangan Ramah) -->
        <g class="interactive-elem" tabindex="0">
            <!-- Bayangan -->
            <ellipse cx="370" cy="358" rx="22" ry="7" fill="rgba(0,0,0,0.18)" />
            <!-- Kaki & Sepatu -->
            <rect x="360" y="325" width="8" height="28" rx="4" fill="#334155" />
            <rect x="372" y="325" width="8" height="28" rx="4" fill="#334155" />
            <!-- Baju Jas Putih Bidan -->
            <path d="M352,240 L388,240 L394,325 L346,325 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
            <!-- Kerudung Pink Pastel / Rambut Rapi -->
            <ellipse cx="370" cy="205" rx="19" ry="24" fill="#f472b6" />
            <!-- Wajah Ramah -->
            <circle cx="370" cy="210" r="14" fill="#fed7aa" />
            <!-- Senyum & Mata -->
            <circle cx="366" cy="207" r="1.8" fill="#475569" />
            <circle cx="374" cy="207" r="1.8" fill="#475569" />
            <path d="M366,215 Q370,220 374,215" stroke="#e11d48" stroke-width="1.8" fill="none" stroke-linecap="round" />
            <!-- Stetoskop Hijau Mint di Leher -->
            <path d="M363,222 Q370,240 377,222" stroke="#059669" stroke-width="2" fill="none" />
            <circle cx="370" cy="242" r="3.5" fill="#059669" />
            <!-- Buku Catatan KMS di Tangan Kiri -->
            <rect x="345" y="260" width="15" height="20" rx="3" fill="#38bdf8" />
            <text x="352" y="274" font-size="8" font-weight="800" fill="#ffffff" text-anchor="middle">KMS</text>
            <!-- Lengan Kanan Melambai (Animasi Wave) -->
            <g class="anim-waving-arm">
                <path d="M386,244 Q405,225 410,205" stroke="#ffffff" stroke-width="9" stroke-linecap="round" fill="none" />
                <circle cx="410" cy="205" r="5.5" fill="#fed7aa" />
                <!-- Emoji Lambaian Tangan -->
                <text x="415" y="200" font-size="12">👋</text>
            </g>
        </g>
        <!-- Tooltip Bidan -->
        <g class="tooltip-bubble">
            <rect x="290" y="130" width="170" height="52" rx="10" fill="{"#1e1329" if is_dark else "#ffffff"}" stroke="#ec4899" stroke-width="1.8" filter="url(#softGlow)" />
            <polygon points="370,182 378,190 362,190" fill="{"#1e1329" if is_dark else "#ffffff"}" />
            <text x="375" y="148" font-size="10.5" font-weight="700" fill="#ec4899" text-anchor="middle">👩‍⚕️ Ibu Bidan & Kader</text>
            <text x="375" y="163" font-size="9" fill="{text_col}" text-anchor="middle">"Yuk timbang dan imunisasi</text>
            <text x="375" y="174" font-size="8.5" font-weight="600" fill="#059669" text-anchor="middle">si kecil setiap bulan!"</text>
        </g>

        <!-- 5. Karakter 2: Ibu Hamil Bahagia (Menjaga Kandungan Sehat) -->
        <g class="interactive-elem" tabindex="0">
            <!-- Bayangan -->
            <ellipse cx="500" cy="358" rx="24" ry="7" fill="rgba(0,0,0,0.18)" />
            <!-- Dress Hamil Lavender Cantik Melengkung -->
            <path d="M485,250 Q525,275 520,328 L475,328 Q470,275 485,250 Z" fill="#c084fc" stroke="#a855f7" stroke-width="1.5" />
            <!-- Tangan Mengelus Perut Sayang -->
            <path d="M488,260 Q515,285 505,295" stroke="#fbcfe8" stroke-width="6" stroke-linecap="round" fill="none" />
            <!-- Kerudung / Rambut Anggun -->
            <ellipse cx="495" cy="210" rx="17" ry="22" fill="#f43f5e" />
            <circle cx="495" cy="213" r="13" fill="#fed7aa" />
            <circle cx="491" cy="210" r="1.6" fill="#475569" />
            <circle cx="498" cy="210" r="1.6" fill="#475569" />
            <path d="M492,217 Q495,221 498,217" stroke="#e11d48" stroke-width="1.6" fill="none" stroke-linecap="round" />
            <!-- Pita Cantik di Baju -->
            <circle cx="490" cy="250" r="4" fill="#fde047" />
        </g>
        <!-- Tooltip Ibu Hamil -->
        <g class="tooltip-bubble">
            <rect x="420" y="140" width="165" height="52" rx="10" fill="{"#1e1329" if is_dark else "#ffffff"}" stroke="#a855f7" stroke-width="1.8" filter="url(#softGlow)" />
            <polygon points="500,192 508,200 492,200" fill="{"#1e1329" if is_dark else "#ffffff"}" />
            <text x="502" y="158" font-size="10.5" font-weight="700" fill="#a855f7" text-anchor="middle">🤰 Pemeriksaan Kehamilan</text>
            <text x="502" y="173" font-size="9" fill="{text_col}" text-anchor="middle">"ANC 10T & Tablet Tambah Darah</text>
            <text x="502" y="184" font-size="8.5" font-weight="600" fill="#e11d48" text-anchor="middle">cegah anemia & KEK!"</text>
        </g>

        <!-- 6. Karakter 3: Ibu & Balita Ceria Bermain Bola -->
        <!-- Ibu Balita -->
        <g class="interactive-elem" tabindex="0">
            <ellipse cx="640" cy="358" rx="20" ry="7" fill="rgba(0,0,0,0.18)" />
            <!-- Rok Hijau Sage & Blus Peach -->
            <path d="M628,245 L652,245 L660,330 L620,330 Z" fill="#34d399" stroke="#10b981" stroke-width="1.5" />
            <ellipse cx="640" cy="245" rx="14" ry="16" fill="#fed7aa" />
            <ellipse cx="640" cy="208" rx="16" ry="21" fill="#fb923c" />
            <circle cx="640" cy="212" r="13" fill="#fed7aa" />
            <circle cx="636" cy="210" r="1.6" fill="#475569" />
            <circle cx="643" cy="210" r="1.6" fill="#475569" />
            <path d="M637,216 Q640,220 643,216" stroke="#e11d48" stroke-width="1.6" fill="none" />
            <!-- Tangan Menunjuk Si Kecil -->
            <path d="M648,250 Q670,270 690,285" stroke="#fed7aa" stroke-width="6" stroke-linecap="round" fill="none" />
        </g>

        <!-- Balita Bermain (Animasi Melompat Riang) -->
        <g class="interactive-elem anim-child" tabindex="0">
            <ellipse cx="715" cy="358" rx="16" ry="5" fill="rgba(0,0,0,0.2)" />
            <!-- Kaos Biru Muda & Celana Pendek -->
            <rect x="706" y="295" width="18" height="24" rx="5" fill="#38bdf8" />
            <rect x="708" y="318" width="6" height="18" rx="3" fill="#f59e0b" />
            <rect x="716" y="318" width="6" height="18" rx="3" fill="#f59e0b" />
            <circle cx="715" cy="280" r="13" fill="#fed7aa" />
            <!-- Topi Balita Lucu -->
            <path d="M702,274 Q715,260 728,274 Z" fill="#ec4899" />
            <circle cx="715" cy="262" r="3" fill="#fde047" />
            <circle cx="711" cy="280" r="1.5" fill="#0f172a" />
            <circle cx="718" cy="280" r="1.5" fill="#0f172a" />
            <path d="M712,286 Q715,290 718,286" stroke="#e11d48" stroke-width="1.8" fill="none" />
            <!-- Bola Mainan Warna-Warni -->
            <circle cx="745" cy="336" r="12" fill="#f43f5e" />
            <path d="M738,330 Q745,336 752,330" stroke="#fde047" stroke-width="3" fill="none" />
            <path d="M738,342 Q745,336 752,342" stroke="#38bdf8" stroke-width="3" fill="none" />
        </g>
        <!-- Tooltip Balita & Ibu -->
        <g class="tooltip-bubble">
            <rect x="620" y="140" width="180" height="52" rx="10" fill="{"#1e1329" if is_dark else "#ffffff"}" stroke="#38bdf8" stroke-width="1.8" filter="url(#softGlow)" />
            <polygon points="705,192 713,200 697,200" fill="{"#1e1329" if is_dark else "#ffffff"}" />
            <text x="710" y="158" font-size="10.5" font-weight="700" fill="#0284c7" text-anchor="middle">👶 Balita Tumbuh Sehat</text>
            <text x="710" y="173" font-size="9" fill="{text_col}" text-anchor="middle">"Pantau kurva KMS & Z-Score</text>
            <text x="710" y="184" font-size="8.5" font-weight="600" fill="#16a34a" text-anchor="middle">bebas risiko stunting!"</text>
        </g>

        <!-- Kupu-Kupu Cantik Terbang -->
        <g class="anim-butterfly" style="transform-origin: 580px 200px;">
            <circle cx="580" cy="200" r="2.5" fill="#1e1b4b" />
            <ellipse cx="575" cy="195" rx="6" ry="4" fill="#f43f5e" />
            <ellipse cx="585" cy="195" rx="6" ry="4" fill="#f43f5e" />
            <ellipse cx="576" cy="204" rx="4" ry="3" fill="#fb923c" />
            <ellipse cx="584" cy="204" rx="4" ry="3" fill="#fb923c" />
        </g>

        <!-- 7. Bunga-Bunga Bergoyang Sepoi-Sepoi di Depan -->
        <g class="anim-flower" style="transform-origin: 320px 360px;">
            <line x1="320" y1="365" x2="320" y2="345" stroke="#16a34a" stroke-width="2.5" />
            <circle cx="320" cy="343" r="6" fill="#fb7185" />
            <circle cx="320" cy="343" r="2.5" fill="#fef08a" />
        </g>
        <g class="anim-flower" style="transform-origin: 440px 360px; animation-delay: 0.8s;">
            <line x1="440" y1="365" x2="440" y2="342" stroke="#16a34a" stroke-width="2.5" />
            <circle cx="440" cy="340" r="7" fill="#c084fc" />
            <circle cx="440" cy="340" r="2.8" fill="#fef08a" />
        </g>
        <g class="anim-flower" style="transform-origin: 560px 360px; animation-delay: 1.4s;">
            <line x1="560" y1="365" x2="560" y2="346" stroke="#16a34a" stroke-width="2.5" />
            <circle cx="560" cy="344" r="6.5" fill="#38bdf8" />
            <circle cx="560" cy="344" r="2.5" fill="#fef08a" />
        </g>
        <g class="anim-flower" style="transform-origin: 790px 360px; animation-delay: 2s;">
            <line x1="790" y1="365" x2="790" y2="344" stroke="#16a34a" stroke-width="2.5" />
            <circle cx="790" cy="342" r="7" fill="#fb7185" />
            <circle cx="790" cy="342" r="2.8" fill="#fef08a" />
        </g>
        <g class="anim-flower" style="transform-origin: 825px 360px; animation-delay: 0.4s;">
            <line x1="825" y1="365" x2="825" y2="348" stroke="#16a34a" stroke-width="2" />
            <circle cx="825" cy="346" r="5.5" fill="#f43f5e" />
            <circle cx="825" cy="346" r="2" fill="#fef08a" />
        </g>
    </svg>
    <div style="text-align:center; padding: 6px 12px; background:{"rgba(255,255,255,0.04)" if is_dark else "rgba(253,242,248,0.7)"}; font-size:0.78rem; color:{"#f472b6" if is_dark else "#be185d"}; font-weight:600;">
        ✨ Arahkan kursor ke gedung atau karakter untuk melihat pesan edukasi interaktif!
    </div>
    </div>
    """
