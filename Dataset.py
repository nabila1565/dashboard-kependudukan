import streamlit as st
from pathlib import Path

def show_page():
    BASE_DIR = Path(__file__).parent

    datasets = [
        {
        "nama": "Jumlah Penduduk Kabupaten/Kota Jawa Timur",
        "file": BASE_DIR / "Jumlah Penduduk Jatim.csv",
        "deskripsi": "Data jumlah penduduk kabupaten/kota di Provinsi Jawa Timur Tahun 2020-2025",
        "sumber": "https://jatim.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMw==/penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-jawa-timur--2024.html?year=2025"
        },
        {
        "nama": "Laju Pertumbuhan Penduduk Kabupaten/Kota Jawa Timur",
        "file": BASE_DIR / "Laju Pertumbuhan.csv",
        "deskripsi": "Data lajupertumbuhan kabupaten/kota di Provinsi Jawa Timur Tahun 2020-2025",
        "sumber": "https://jatim.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMw==/penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-jawa-timur--2024.html?year=2025"
        },
        {
        "nama": "Kepadatan Penduduk Kabupaten/Kota Jawa Timur",
        "file": BASE_DIR / "Kepadatan.csv",
        "deskripsi": "Data kepadatan penduduk kabupaten/kota di Provinsi Jawa Timur Tahun 2020-2025",
        "sumber": "https://jatim.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMw==/penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-jawa-timur--2024.html?year=2025"
        },
        {
        "nama": "TPAK Kabupaten/Kota Jawa Timur",
        "file": BASE_DIR / "PA Magang - TPAK.csv",
        "deskripsi": "Data TPAK Kabupaten/Kota di Provinsi Jawa Timur Tahun 2020-2025",
        "sumber": "https://jatim.bps.go.id/id/statistics-table/2/Mjc3IzI=/tingkat-partisipasi-angkatan-kerja--tpak--menurut-kabupaten-kota.html"
        },
        {
        "nama": "TPT Kabupaten/Kota Jawa Timur",
        "file": BASE_DIR / "PA Magang - TPT.csv",
        "deskripsi": "Data TPT Kabupaten/Kota di Provinsi Jawa Timur Tahun 2020-2025",
        "sumber": "https://jatim.bps.go.id/id/statistics-table/2/NTQjMg==/tingkat-pengangguran-terbuka-tpt-provinsi-jawa-timur.html"
        },
        {
        "nama": "Jumlah Penduduk Jawa Timur Berdasarkan Kelompok Umur",
        "file": BASE_DIR / "PA Magang-Umur.csv",
        "deskripsi": "Data  Jumlah Penduduk Provinsi Jawa Timur berdasarkan kelompok umur Tahun 2020-2025",
        "sumber": "https://jatim.bps.go.id/id/statistics-table/3/WVc0MGEyMXBkVFUxY25KeE9HdDZkbTQzWkVkb1p6MDkjMw==/jumlah-penduduk-menurut-kelompok-umur-dan-jenis-kelamin--ribu-jiwa--di-provinsi-jawa-timur--2025.html?year=2021"
        },
]

    
    st.markdown("""
    <div style="
        font-size:30px;
        font-weight:900;
        color:#0F172A;
        margin-bottom:8px;
    ">
        Sumber Dataset
    </div>
    <div style="
        font-size:16px;
        color:#64748B;
        line-height:1.6;
    "> Halaman ini memuat data rekap yang digunakan dalam dashboard beserta tautan sumber data.
    </div>
    """, unsafe_allow_html=True)

    for data in datasets:
        with st.container():
            st.markdown(f"""
            <div style="
                    background:white;
                    border:1px solid #DDE7F3;
                    border-radius:18px;
                    padding:20px 22px;
                    margin-bottom:16px;
                    box-shadow:0 8px 22px rgba(15,23,42,0.07);
                ">
                <div style="
                    font-size:20px;
                    font-weight:900;
                    color:#0F172A;
                    margin-bottom:6px;
                    "> {data["nama"]}
                </div>
                <div style="
                    font-size:20px;
                    font-weight:500;
                    color:#0F172A;
                    margin-bottom:6px;
                    "> {data["deskripsi"]}
                </div>
                <div style="
                    font-size:20px;
                    font-weight:900;
                    color:#0F172A;
                    margin-bottom:6px;
                    "> Periode data: <b>2020-2025</b>
                </div>
            </div>
            """, unsafe_allow_html =True)

            
            col1, col2 = st.columns([1, 4])
            if data["file"].exists():
                with open(data["file"], "rb") as file:
                    col1.download_button(
                        label="Download CSV",
                        data=file,
                        file_name=data["file"].name,
                        mime="text/csv",
                        key=f"download_{data['file'].name}"
                    )
            else:
                col1.error("File tidak ditemukan")

            col2.markdown(f"[Lihat sumber data]({data['sumber']})")




            