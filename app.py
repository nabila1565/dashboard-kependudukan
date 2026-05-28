import streamlit as st
from informasi_jawa_timur import show_informasi_jawa_timur

st.set_page_config(
    page_title="Dashboard Demografi Jawa Timur",
    page_icon="🗺️",
    layout="wide"
)

st.markdown("""
<style>
/* Background utama aplikasi */
.stApp {
    background-color: #FFFFFF;
}

/* Header atas Streamlit */
[data-testid="stHeader"] {
    background-color: #FFFFFF;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #306D29
}

/* Judul/label sidebar */
[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

/* Radio menu KHUSUS di sidebar */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: none;
    border: 1.5px solid white !important;
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    transition: 0.3s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

/* Hover radio menu KHUSUS sidebar */
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: rgba(77,166,255,0.35) !important;
    transform: translateX(4px);
}

/* Teks radio menu KHUSUS sidebar */
[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: white !important;
    font-size: 16px;
    font-weight: 600;
}

/* Pastikan area utama tidak ikut putih */
section.main p,
section.main h1,
section.main h2,
section.main h3,
section.main h4,
section.main h5,
section.main h6,
section.main label,
section.main span {
    color: inherit;
}
</style>
""", unsafe_allow_html=True)


menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Informasi Jawa Timur",
        "Dashboard",
        "Dataset",
        "Hasil Cluster Tahun 2025"
    ]
)

if menu == "Informasi Jawa Timur":
    show_informasi_jawa_timur()

elif menu == "Dashboard":
    from dashboard import show_page
    show_page()
elif menu == "Dataset":
    from Dataset import show_page
    show_page()
elif menu == "Hasil Cluster Tahun 2025":
    from hasil_cluster import show_page
    show_page()