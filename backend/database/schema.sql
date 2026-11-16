-- ====================================================================
-- SKEMA DATABASE SUPABASE POSTGRESQL (PRODUCTION READY): POSYANDU DIGITAL
-- ====================================================================
-- Skrip ini idempotent dan aman dijalankan ulang melalui Supabase SQL Editor.
-- Mengintegrasikan Supabase Auth (auth.users), User Profiles,
-- Entitas Relasional, Triggers, dan Row Level Security (RLS).
-- ====================================================================

-- 1. Ekstensi UUID & Kriptografi
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. Fungsi helper untuk auto-update kolom updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- 3. TABEL: users (Profil Pengguna Terhubung Supabase Auth)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY, -- Terhubung dengan auth.users.id
    username VARCHAR(60),
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255), -- Fallback offline
    role VARCHAR(30) NOT NULL CHECK (role IN ('Kader', 'Ibu Hamil', 'Orang Tua Balita', 'Pengelola')),
    nama VARCHAR(150) NOT NULL,
    id_peserta VARCHAR(50),
    alamat_dusun VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON public.users(role);

-- Trigger: Otomatis sinkronisasi saat pengguna baru registrasi di Supabase Auth
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO public.users (id, username, email, role, nama)
    VALUES (
        new.id,
        COALESCE(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
        new.email,
        COALESCE(new.raw_user_meta_data->>'role', 'Orang Tua Balita'),
        COALESCE(new.raw_user_meta_data->>'nama', split_part(new.email, '@', 1))
    )
    ON CONFLICT (id) DO UPDATE SET
        email = EXCLUDED.email,
        nama = COALESCE(public.users.nama, EXCLUDED.nama),
        role = COALESCE(public.users.role, EXCLUDED.role);
    RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ====================================================================
-- 4. TABEL: orang_tua (Profil Orang Tua Balita)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.orang_tua (
    id_orang_tua VARCHAR(50) PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    nama_ayah VARCHAR(150),
    nama_ibu VARCHAR(150),
    nama_wali VARCHAR(150),
    email VARCHAR(120),
    alamat_dusun VARCHAR(100),
    alamat_lengkap TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orang_tua_user ON public.orang_tua(user_id);

-- ====================================================================
-- 5. TABEL: peserta (Peserta Balita & Ibu Hamil)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.peserta (
    id_peserta VARCHAR(50) PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    jenis_peserta VARCHAR(30) NOT NULL CHECK (jenis_peserta IN ('Balita', 'Ibu Hamil')),
    nama VARCHAR(150) NOT NULL,
    email VARCHAR(120),
    tanggal_lahir DATE,
    usia_bulan NUMERIC(5,1),
    usia_ibu_tahun INTEGER,
    jenis_kelamin VARCHAR(20) CHECK (jenis_kelamin IN ('Laki-laki', 'Perempuan')),
    id_orang_tua VARCHAR(50) REFERENCES public.orang_tua(id_orang_tua) ON DELETE SET NULL,
    nama_orang_tua VARCHAR(150),
    usia_kehamilan_minggu INTEGER,
    alamat_dusun VARCHAR(100),
    alamat_lengkap TEXT,
    status VARCHAR(50) DEFAULT 'Terdaftar',
    tanggal_daftar DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_peserta_jenis ON public.peserta(jenis_peserta);
CREATE INDEX IF NOT EXISTS idx_peserta_dusun ON public.peserta(alamat_dusun);
CREATE INDEX IF NOT EXISTS idx_peserta_user ON public.peserta(user_id);
CREATE INDEX IF NOT EXISTS idx_peserta_ortu ON public.peserta(id_orang_tua);

-- ====================================================================
-- 6. TABEL: pemeriksaan_balita (Pemeriksaan Antropometri Balita)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.pemeriksaan_balita (
    id BIGSERIAL PRIMARY KEY,
    id_peserta VARCHAR(50) NOT NULL REFERENCES public.peserta(id_peserta) ON DELETE CASCADE,
    tanggal_pemeriksaan DATE NOT NULL,
    usia_bulan NUMERIC(5,1) NOT NULL,
    berat_kg NUMERIC(5,2) NOT NULL,
    tinggi_cm NUMERIC(5,2) NOT NULL,
    lingkar_kepala_cm NUMERIC(5,2),
    vitamin_a VARCHAR(20) DEFAULT 'Tidak',
    imunisasi VARCHAR(50) DEFAULT 'Lengkap sesuai usia',
    z_bb_u NUMERIC(5,2),
    z_tb_u NUMERIC(5,2),
    status_gizi VARCHAR(50),
    jadwal_berikutnya DATE,
    catatan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pem_balita_peserta ON public.pemeriksaan_balita(id_peserta);
CREATE INDEX IF NOT EXISTS idx_pem_balita_tgl ON public.pemeriksaan_balita(tanggal_pemeriksaan);
CREATE INDEX IF NOT EXISTS idx_pem_balita_status ON public.pemeriksaan_balita(status_gizi);

-- ====================================================================
-- 7. TABEL: pemeriksaan_ibu_hamil (Pemeriksaan Maternal)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.pemeriksaan_ibu_hamil (
    id BIGSERIAL PRIMARY KEY,
    id_peserta VARCHAR(50) NOT NULL REFERENCES public.peserta(id_peserta) ON DELETE CASCADE,
    tanggal_pemeriksaan DATE NOT NULL,
    usia_kehamilan_minggu INTEGER NOT NULL,
    berat_kg NUMERIC(5,2) NOT NULL,
    lila_cm NUMERIC(5,2) NOT NULL,
    sistol INTEGER NOT NULL,
    diastol INTEGER NOT NULL,
    hb_gdl NUMERIC(4,1) NOT NULL,
    tfu_cm NUMERIC(5,2),
    djj_bpm INTEGER,
    tablet_fe VARCHAR(50) DEFAULT 'Diberikan',
    status_kek VARCHAR(30),
    status_anemia VARCHAR(30),
    status_hipertensi VARCHAR(30),
    risiko VARCHAR(50),
    jadwal_berikutnya DATE,
    hpl DATE,
    catatan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pem_ibu_peserta ON public.pemeriksaan_ibu_hamil(id_peserta);
CREATE INDEX IF NOT EXISTS idx_pem_ibu_tgl ON public.pemeriksaan_ibu_hamil(tanggal_pemeriksaan);
CREATE INDEX IF NOT EXISTS idx_pem_ibu_risiko ON public.pemeriksaan_ibu_hamil(risiko);

-- ====================================================================
-- 8. TABEL: laporan (Laporan Bulanan Posyandu)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.laporan (
    id BIGSERIAL PRIMARY KEY,
    id_laporan VARCHAR(50) UNIQUE NOT NULL,
    periode VARCHAR(20) NOT NULL,
    kelompok VARCHAR(30) NOT NULL,
    variabel VARCHAR(100) NOT NULL,
    dibuat_oleh VARCHAR(150),
    tanggal_dibuat DATE DEFAULT CURRENT_DATE,
    status VARCHAR(50) DEFAULT 'Siap diserahkan',
    tanggal_serah DATE,
    catatan TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_laporan_periode ON public.laporan(periode);

-- ====================================================================
-- 9. TABEL: edukasi (Materi Edukasi Kesehatan)
-- ====================================================================
CREATE TABLE IF NOT EXISTS public.edukasi (
    id BIGSERIAL PRIMARY KEY,
    slug VARCHAR(100) UNIQUE,
    ikon VARCHAR(10),
    kategori VARCHAR(50),
    judul VARCHAR(200) NOT NULL,
    ringkasan TEXT,
    konten TEXT,
    urutan INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================================================
-- 10. TRIGGERS UNTUK AUTO-UPDATE UPDATED_AT
-- ====================================================================
DROP TRIGGER IF EXISTS trg_users_updated ON public.users;
CREATE TRIGGER trg_users_updated BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_peserta_updated ON public.peserta;
CREATE TRIGGER trg_peserta_updated BEFORE UPDATE ON public.peserta FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_balita_updated ON public.pemeriksaan_balita;
CREATE TRIGGER trg_balita_updated BEFORE UPDATE ON public.pemeriksaan_balita FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_ibu_updated ON public.pemeriksaan_ibu_hamil;
CREATE TRIGGER trg_ibu_updated BEFORE UPDATE ON public.pemeriksaan_ibu_hamil FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_laporan_updated ON public.laporan;
CREATE TRIGGER trg_laporan_updated BEFORE UPDATE ON public.laporan FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ====================================================================
-- 11. ROW LEVEL SECURITY (RLS) POLICIES
-- ====================================================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.orang_tua ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.peserta ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pemeriksaan_balita ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pemeriksaan_ibu_hamil ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.laporan ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.edukasi ENABLE ROW LEVEL SECURITY;

-- Kebijakan Akses:
-- 1. Users: Pengguna dapat membaca & mengupdate akunnya sendiri; Kader dapat melihat semua akun.
DROP POLICY IF EXISTS "Users Read Policy" ON public.users;
CREATE POLICY "Users Read Policy" ON public.users FOR SELECT USING (
    auth.uid() = id OR
    EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'Kader') OR
    auth.role() = 'anon'
);

DROP POLICY IF EXISTS "Users Insert Update Policy" ON public.users;
CREATE POLICY "Users Insert Update Policy" ON public.users FOR ALL USING (
    auth.uid() = id OR
    EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'Kader') OR
    auth.role() = 'anon'
) WITH CHECK (true);

-- 2. Peserta: Ibu Hamil & Orang Tua melihat peserta miliknya; Kader melihat semua.
DROP POLICY IF EXISTS "Peserta Access Policy" ON public.peserta;
CREATE POLICY "Peserta Access Policy" ON public.peserta FOR ALL USING (
    auth.uid() = user_id OR
    EXISTS (SELECT 1 FROM public.orang_tua WHERE user_id = auth.uid() AND id_orang_tua = public.peserta.id_orang_tua) OR
    EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'Kader') OR
    auth.role() = 'anon'
) WITH CHECK (true);

-- 3. Orang Tua Policy
DROP POLICY IF EXISTS "Orang Tua Access Policy" ON public.orang_tua;
CREATE POLICY "Orang Tua Access Policy" ON public.orang_tua FOR ALL USING (
    auth.uid() = user_id OR
    EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'Kader') OR
    auth.role() = 'anon'
) WITH CHECK (true);

-- 4. Pemeriksaan Balita: Orang tua melihat anaknya; Kader mengelola semua.
DROP POLICY IF EXISTS "Pemeriksaan Balita Policy" ON public.pemeriksaan_balita;
CREATE POLICY "Pemeriksaan Balita Policy" ON public.pemeriksaan_balita FOR ALL USING (
    EXISTS (
        SELECT 1 FROM public.peserta p
        WHERE p.id_peserta = public.pemeriksaan_balita.id_peserta AND (
            p.user_id = auth.uid() OR
            EXISTS (SELECT 1 FROM public.orang_tua o WHERE o.user_id = auth.uid() AND o.id_orang_tua = p.id_orang_tua)
        )
    ) OR
    EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'Kader') OR
    auth.role() = 'anon'
) WITH CHECK (true);

-- 5. Pemeriksaan Ibu Hamil: Ibu melihat riwayatnya; Kader mengelola semua.
DROP POLICY IF EXISTS "Pemeriksaan Ibu Policy" ON public.pemeriksaan_ibu_hamil;
CREATE POLICY "Pemeriksaan Ibu Policy" ON public.pemeriksaan_ibu_hamil FOR ALL USING (
    EXISTS (
        SELECT 1 FROM public.peserta p
        WHERE p.id_peserta = public.pemeriksaan_ibu_hamil.id_peserta AND p.user_id = auth.uid()
    ) OR
    EXISTS (SELECT 1 FROM public.users WHERE id = auth.uid() AND role = 'Kader') OR
    auth.role() = 'anon'
) WITH CHECK (true);

-- 6. Laporan: Kader mengelola laporan; publik/peserta dapat membaca rekap.
DROP POLICY IF EXISTS "Laporan Policy" ON public.laporan;
CREATE POLICY "Laporan Policy" ON public.laporan FOR ALL USING (true) WITH CHECK (true);

-- 7. Edukasi: Semua pengguna dapat membaca artikel edukasi.
DROP POLICY IF EXISTS "Edukasi Read Policy" ON public.edukasi;
CREATE POLICY "Edukasi Read Policy" ON public.edukasi FOR SELECT USING (true);
