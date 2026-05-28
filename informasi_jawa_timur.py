import streamlit as st
import base64
import pandas as pd
import plotly.express as px
import textwrap
from pathlib import Path


#Fungsi membaca gambar
def get_base64_image(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        return None
    with open(image_path,"rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded
#CSS Halamam Informasi Jawa Timur
def load_informasi_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #f6f8fc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* NAVBAR */
    .top-navbar {
        width: 100%;
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-bottom: 28px;
    }

    .nav-item {
        display: inline-block;
        background: none;
        color: #111844  !important;
        text-decoration: none;
        font-weight: 700;
        padding: 10px 24px;
        border-radius: 999px;
        font-size: 15px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
        border: 1px solid #e5e7eb;
        transition: 0.2s ease;
    }

    .nav-item:hover {
        color: #4f46e5 !important;
        border-color: #4f46e5;
        transform: translateY(-2px);
    }

    .nav-item.active {
        background: #4f46e5;
        color: white !important;
    }

    /* HERO IMAGE */
    .hero {
        position: relative;
        border-radius: 15px;
        padding: 0;
        min-height: 260px;
        max-width: 88%;
        margin-top:100px;
        margin-left:auto;
        margin-right:auto;
        color: white;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        box-shadow: 0 20px 100px rgba(50, 80, 50, 0.25);
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 780px;
    }

    .hero h1 {
        font-size: 48px;
        line-height: 1.15;
        font-weight: 900;
        margin-bottom: 16px;
        letter-spacing: -0.5px;
    }

    .hero p {
        font-size: 17px;
        line-height: 1.7;
        color: #e5e7eb;
        margin-bottom: 26px;
    }

    /* WELCOME BOX */
    .welcome-box {
        display: inline-block;
        background: #FBF5DD;
        border-radius: 999px;
        padding: 6px 20px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
        margin-bottom: 10px;
        margin-top:20px
    }

    .welcome-box h1 {
        color: black;
        font-size: 20px;
        font-weight: 900;
        margin: 0;
        line-height: 1.2;
    }

    /* BADGE */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.95);
        color: white;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 18px;
    }

    /* TITLE SECTION */
    .section-title {
        font-size: 26px;
        font-weight: 900;
        color: #0f172a;
        margin-top: 36px;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 18px;
    }

    /* CARD */
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        min-height: 190px;
        height: 190px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        text-align: center;
        justify-content: center;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.10);
    }

    .metric-row {
        display: flex;
        align-items: center;
        gap: 14px;
        justify-content: center;
    }

    .metric-icon {
        width: 46px;
        height: 46px;
        min-width: 46px;
        border-radius: 14px;
        background: #eef2ff;
        color: #4f46e5;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
    }

    .metric-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .metric-label {
        font-size: 18px;
        color: black;
        margin-bottom: 12px;
        line-height: 1.45;
        font-weight: 650;
    }

    .metric-value {
        font-size: 40px;
        font-weight: 900;
        color: darkblue;
        margin-bottom: 4px;
        line-height: 1.2;
    }

    .metric-desc {
        font-size: 18px;
        color: black;
        margin-top: 6px;
    }
    .main-title {
        color: #0D530E !important;
        font-size: 45px !important;
        font-weight: 1000 !important;
        line-height: 1.15;
        margin-top: 18px;
        margin-bottom: 16px;
    }
    .custom-card {
        background: white;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        height: 100%;
        transition: 0.2s ease;
    }

    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.10);
    }

    .custom-card h3 {
        font-size: 20px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .custom-card p {
        font-size: 18px;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 0px;
    }

    .footer {
        margin-top: 40px;
        padding: 20px;
        text-align: center;
        color: #64748b;
        font-size: 14px;
    }
    .profil-section {
        width: 100%;
        margin-top: 36px;
    }

    .profil-section h1 {
        color: #0b5d16;
        font-size: 48px;
        font-weight: 900;
        line-height: 1.2;
        margin-bottom: 20px;
    }

    .profil-section p {
        color: #111827;
        font-size: 18px;
        line-height: 1.8;
        max-width: 100%;
    }
    .stats-section {
    width: 100%;
    margin-top: 48px;
    margin-bottom: 48px;
    padding: 28px 20px;
    background: transparent;
    }

    .stats-row {
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        gap: 18px;
        width: 100%;
    }

    .stats-item {
        flex: 1;
        text-align: center;
        padding: 18px 10px;
        border-radius: 18px;
        background: transparent;
        border: none;
    }

    .stats-value {
        font-size: 34px;
        font-weight: 900;
        color: #0b5d16;
        line-height: 1.1;
        margin-bottom: 10px;
    }

    .stats-label {
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        line-height: 1.35;
    }

    .stats-title {
        text-align: center;
        margin-top: 36px;
    }

    .stats-title h2 {
        color: #0b5d16;
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .stats-title p {
        color: #64748b;
        font-size: 15px;
        margin: 0;
    }

    @media screen and (max-width: 900px) {
        .stats-row {
            flex-wrap: wrap;
        }

        .stats-item {
            min-width: 160px;
        }
        .stats-value {
            font-size: 28px;
        }
    }
        </style>
        """, unsafe_allow_html=True)

def show_informasi_jawa_timur():
    load_informasi_css()

    col_home, col_info = st.columns(2)
    with col_home:
        st.markdown("""
                    <div class ="welcome-box">
                    <h1> Selamat Datang</h1>
                    </div>
                    """, unsafe_allow_html=True
                    )
        st.markdown ("""
                    <div id="home" class="hero-content">
                        <h1 class="main-title">Dashboard Kependudukan Provinsi Jawa Timur</h1>
                        <p> Laman ini memuat informasi terkini mengenai kondisi kependudukan, dashboard kependudukan, serta analisis clustering  wilayah di Provinsi Jawa Timur.
                        Dibuat untuk mendukung tugas akhir magang pada Dinas Komunikasi dan Informatika Provinsi Jawa Timur.
                        </p>
                    </div>

                    """, unsafe_allow_html=True)
    with col_info:
        
        image_base64 = get_base64_image("sejarah-jawa-timur.jpg")

        if image_base64:
                hero_background = f"""
                    background-image: url("data:image/png;base64,{image_base64}");
                """
        else:
                hero_background = """
                    background: #94a3b8;
                """

        st.markdown(
                f"""
                <div class="hero" style='{hero_background}'>
                </div>
                """,
                unsafe_allow_html=True)

    #tentang Jatim
    st.markdown ("""
    <div id="tentang-jatim" class="profil-section">
            <h1 class="main-title">Informasi Singkat Tentang Jawa Timur</h1>
            <p>   Provinsi Jawa Timur terletak di bagian timur Pulau Jawa dan salah satu provinsi dengan peran stategis dalam perekonomian nasional.
            Jawa Timur memiliki potensi besar di beragam sektor seperti industri, perdagangan, pendidikan, dan pariwisata.
            Dengan keberagaman geografis dan budaya, Jawa Timur senantiasa berkembang menjadi potensi yang maju dan sejahtera.
            </p>
        </div>""", unsafe_allow_html=True)
    
    # Path Data
    BASE_DIR = Path(__file__).parent

    JUMLAH_PENDUDUK_PATH = BASE_DIR / "Jumlah Penduduk Jatim.csv"
    LAJU_PATH = BASE_DIR / "Laju Pertumbuhan.csv"
    KEPADATAN_PATH = BASE_DIR / "Kepadatan.csv"
    TPAK_PATH = BASE_DIR / "PA Magang - TPAK.csv"
    TPT_PATH = BASE_DIR / "PA Magang - TPT.csv"

    file_paths = {
        "Jumlah Penduduk Jatim": JUMLAH_PENDUDUK_PATH,
        "Laju Pertumbuhan": LAJU_PATH,
        "Kepadatan": KEPADATAN_PATH,
        "TPAK": TPAK_PATH,
        "TPT": TPT_PATH,

    }

    for nama_file, path_file in file_paths.items():
        if not path_file.exists():
            st.error(f"File {nama_file} tidak ditemukan: {path_file}")
            st.stop()

    # Load Data
    df_jumlahpenduduk = pd.read_csv(JUMLAH_PENDUDUK_PATH)
    df_lajupertumbuhan = pd.read_csv(LAJU_PATH)
    df_kepadatan = pd.read_csv(KEPADATAN_PATH)
    df_TPAK = pd.read_csv(TPAK_PATH)
    df_TPT = pd.read_csv(TPT_PATH)

    # Ambil Nilai Jawa Timur Tahun 2025
    jumlah_penduduk_jatim_2025 = df_jumlahpenduduk.loc[
        df_jumlahpenduduk["Kabupaten/Kota"].str.strip().str.lower() == "jawa timur",
        "2025"
    ].iloc[0]

    jumlah_penduduk_jatim_2025 = int(jumlah_penduduk_jatim_2025)
    jumlah_penduduk_format = f"{jumlah_penduduk_jatim_2025:,}".replace(",", ".") +  "Jiwa"

    laju_pertumbuhan_jatim_2025 = df_lajupertumbuhan.loc[
        df_lajupertumbuhan["Kabupaten/Kota"].str.strip().str.lower() == "jawa timur",
        "2025"
    ].iloc[0]

    kepadatan_jatim_2025 = df_kepadatan.loc[
        df_kepadatan["Kabupaten/Kota"].str.strip().str.lower() == "jawa timur",
        "2025"
    ].iloc[0]

    kepadatan_penduduk = int(kepadatan_jatim_2025)
    kepadatan_penduduk_format = f"{kepadatan_penduduk:,}".replace(",", ".") + " jiwa/km²"
   
    tpak_jatim_2025 = df_TPAK.loc[
        df_TPAK["Kabupaten/Kota"].str.strip().str.lower() == "jawa timur",
        "2025"
    ].iloc[0]

    tpt_jatim_2025 = df_TPT.loc[
        df_TPT["Kabupaten/Kota"].str.strip().str.lower() == "jawa timur",
        "2025"
    ].iloc[0]

    # Statistik 5 item sejajar 1 baris
    stats_html = f"""
    <style>
    .stats-section {{
        width: 100%;
        margin-top: 48px;
        margin-bottom: 48px;
        padding: 28px 20px;
        background: transparent;
    }}

    .stats-row {{
        display: flex;
        justify-content: space-between;
        align-items: stretch;
        gap: 18px;
        width: 100%;
    }}

    .stats-item {{
        flex: 1;
        text-align: center;
        padding: 18px 10px;
        border-radius: 18px;
        background: transparent;
        border: none;
    }}

    .stats-value {{
        font-size: 34px;
        font-weight: 900;
        color: #0b5d16;
        line-height: 1.1;
        margin-bottom: 10px;
    }}

    .stats-label {{
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        line-height: 1.35;
    }}

    .stats-title {{
        text-align: center;
        margin-top: 36px;
    }}

    .stats-title h2 {{
        color: #0b5d16;
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 8px;
    }}

    .stats-title p {{
        color: #64748b;
        font-size: 15px;
        margin: 0;
    }}
    </style>

    <div class="stats-section">
        <div class="stats-row">
            <div class="stats-item">
                <div class="stats-value">{jumlah_penduduk_format}</div>
                <div class="stats-label">Jumlah Penduduk</div>
            </div>

            <div class="stats-item">
                <div class="stats-value">{laju_pertumbuhan_jatim_2025}%</div>
                <div class="stats-label">Laju Pertumbuhan<br>Penduduk</div>
            </div>

            <div class="stats-item">
                <div class="stats-value">{kepadatan_penduduk_format}</div>
                <div class="stats-label">Kepadatan Penduduk</div>
            </div>

            <div class="stats-item">
                <div class="stats-value">{tpak_jatim_2025}%</div>
                <div class="stats-label">TPAK<br>Tahun 2025</div>
            </div>

            <div class="stats-item">
                <div class="stats-value">{tpt_jatim_2025}%</div>
                <div class="stats-label">TPT<br>Tahun 2025</div>
            </div>
        </div>

        <div class="stats-title">
            <p>Ringkasan indikator utama Provinsi Jawa Timur Tahun 2025</p>
        </div>
    </div>
    """

    st.html(stats_html)