# 🌸 Posyandu Digital — Jejak Tumbuh (Redesign & Enhancement v4.0)

Aplikasi Web Healthcare Modern berbasis **Streamlit**, **Supabase (PostgreSQL & Auth)**, serta standar pertumbuhan antropometri **WHO** dan Kementerian Kesehatan RI.

---

## ✨ Fitur & Pembaruan Terbaru (v4.0)

### 1. 🎨 Desain Pastel Pink Clean, Modern & Elegan
- **Tema Pastel Pink Healthcare**: Menggunakan kombinasi soft pink (`#fdf2f8`, `#fce7f3`, `#ec4899`), lavender lembut (`#c084fc`), dan dark navy kontras tinggi.
- **Glassmorphism & Micro-Interactions**: Card transparan elegan dengan backdrop filter blur, border pink glow halus, dan bayangan lembut.
- **Tipografi Profesional**: Menggunakan font modern `Plus Jakarta Sans` dengan kontras tinggi untuk kenyamanan membaca di desktop maupun mobile.

### 2. 🌓 Dual Mode: Light Mode & Dark Mode Interaktif
- **Toggle Mode Instan**: Tombol pergantian tema `☀️ Mode Terang (Light)` / `🌙 Mode Gelap (Dark)` tersedia di navbar atas maupun sidebar.
- **Adaptasi Seluruh Komponen**: Warna background, kartu metrik, form input, tombol, tabel, dan grafik Altair (Z-score & KMS) otomatis beradaptasi saat berpindah mode.
- **Penyimpanan Status Tema**: Preferensi tema disimpan di dalam session state secara konsisten sepanjang sesi penggunaan.

### 3. 🏡 Animasi 2D Cartoon Lingkungan Posyandu yang Hidup
- **Ilustrasi Lingkungan Terpadu**: Gedung Posyandu berbentuk rumah idaman, Dokter/Bidan desa melambaikan tangan (`👋`), Ibu Hamil menyayangi kandungannya, Ibu & Balita bermain ceria dengan bola, pohon rindang, awan berarak, serta matahari bersinar hangat.
- **Animasi Alami & Halus**:
  - Daun pohon dan bunga di taman bergoyang sepoi-sepoi (`flowerBreeze`, `treeSway`).
  - Awan berarak perlahan melintasi langit (`cloudFloat`).
  - Dokter melambaikan tangan menyapa pengunjung (`waveArm`).
  - Balita melompat riang bermain bola (`childPlay`).
  - Efek floating dan glow pada elemen dekoratif.
- **Tooltip Edukasi Interaktif**: Mengarahkan kursor (hover) pada gedung atau setiap karakter akan memunculkan gelembung pesan edukasi kesehatan yang informatif!

### 4. 🎠 Auto-Sliding Carousel Edukasi Interaktif
- **Gerakan Horizontal Otomatis**: Kartu materi edukasi bergerak halus secara horizontal (`autoSlideLeft`).
- **Hover to Pause**: Gerakan carousel otomatis berhenti (jeda) ketika kursor diarahkan ke area kartu agar pengguna dapat membaca ringkasan dengan santai.
- **Informasi Lengkap**: Kartu dilengkapi ikon emoji 3D, badge kategori berwarna, judul materi, ringkasan, dan tips rekomendasi praktis.

### 5. 📚 Pusat Edukasi Posyandu Terintegrasi & Kuis
- **Fitur Pencarian & Filter Cepat**: Filter berdasarkan kategori (*Ibu Hamil*, *Balita*, *Gizi*, *Nutrisi Bayi*, *Imunisasi*, *Pencegahan*).
- **Progress Belajar & Status Membaca**: Indikator persentase materi yang telah selesai dipelajari.
- **Sistem Bookmark**: Simpan materi favorit ke tab *Tersimpan*.
- **Kuis Interaktif**: Kuis pilihan ganda evaluasi pemahaman materi kesehatan dengan penilaian skor langsung.

### 6. 📱 Responsive Sidebar (Hover Expand / Collapse)
- **Compact View**: Sidebar berukuran ringkas (72px) saat cursor menjauh untuk memaksimalkan ruang kerja dashboard.
- **Expanded View**: Sidebar melebar secara halus (290px) dengan transisi mulus saat cursor diarahkan ke sidebar.
- **Menu Lengkap Sesuai Peran**: Navigasi multi-peran untuk **Kader Posyandu**, **Ibu Hamil**, dan **Orang Tua Balita**.

---

## 📁 Struktur Folder Project

```text
POSYANDUDUDU/
├── app.py                      # Main entrypoint Streamlit aplikasi
├── gizi.py                     # Standar antropometri WHO & scoring risiko maternal Kemenkes
├── run.py                      # Runner launcher script
├── requirements.txt            # Dependensi Python
├── assets/
│   └── JEJAK_TUMBUH.jpeg       # Logo resmi Posyandu Digital
├── database/                   # Modul database Supabase & fallback CSV lokal
│   ├── connection.py           # Supabase client & fallback handler
│   ├── users.py                # Autentikasi & manajemen pengguna
│   ├── peserta.py              # CRUD data balita & ibu hamil
│   ├── pemeriksaan.py          # Pencatatan hasil pemeriksaan ANC & balita
│   ├── laporan.py              # Generator & riwayat laporan Puskesmas
│   └── edukasi.py              # Materi edukasi, tips gizi, dan dataset kuis
├── frontend/                   # Modul arsitektur frontend modular
│   ├── styles/
│   │   └── css.py              # Theme engine: Light & Dark pastel pink styling
│   └── components/
│       ├── posyandu_animation.py # SVG Animasi 2D Lingkungan Posyandu + Tooltip
│       ├── edu_carousel.py       # Auto-sliding horizontal carousel
│       ├── headers.py            # Komponen banner & logo formatter
│       └── tables.py             # Tabel interaktif multi-variabel & sorting
└── tests/
    └── test_suite.py           # Test suite otomatis (100% Passed)
```

---

## 🚀 Cara Menjalankan Aplikasi

1. **Pastikan Dependensi Terinstal**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan Aplikasi Streamlit**:
   ```bash
   streamlit run app.py
   ```
   Atau menggunakan python launcher:
   ```bash
   python run.py
   ```

3. **Akses di Browser**:
   Buka URL lokal yang muncul di terminal (biasanya `http://localhost:8501`).

4. **Uji Coba Fitur**:
   - Klik tombol **☀️ Mode Terang** / **🌙 Mode Gelap** untuk melihat adaptasi warna pastel pink.
   - Arahkan kursor ke karakter pada ilustrasi Posyandu untuk membaca tooltip edukasi.
   - Jeda pergerakan Carousel Edukasi dengan meletakkan kursor di atas kartu.
   - Masuk sebagai Kader, Ibu Hamil, atau Orang Tua Balita untuk mengakses dashboard personal terpadu.
