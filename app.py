import streamlit as st

st.set_page_config(
    page_title="Dashboard Demografi Jawa Timur",
    page_icon="🗺️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #FFFFFF;
}

[data-testid="stHeader"] {
    background-color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background: #556B2F;
}

[data-testid="stSidebar"] label {
    color: white !important;
    font-weight: 600;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #111844 !important;
    border: 1.5px solid #5DADE2 !important;
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    transition: 0.3s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: none !important;
    transform: translateX(4px);
}

[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: white !important;
    font-size: 16px;
    font-weight: 600;
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
    from informasi_jawa_timur import show_informasi_jawa_timur
    show_informasi_jawa_timur()

elif menu == "Dashboard":
    from dashboard import show_page
    show_page()

elif menu == "Dataset":
    from Dataset import show_page
    show_page()

elif menu == "Hasil Cluster Tahun 2025":
    try:
        from hasil_cluster import show_page
        show_page()
    except Exception as e:
        st.error("Halaman Hasil Cluster belum bisa ditampilkan.")
        st.write("Detail error:", e)
