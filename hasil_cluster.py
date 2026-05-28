import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from pathlib import Path
from streamlit_folium import st_folium
import streamlit.components.v1 as components




def show_page():
    BASE_DIR = Path(__file__).parent
    HASIL_CLUSTER_PATH = BASE_DIR / "hasil_cluster_jatim.csv"

    if not HASIL_CLUSTER_PATH.exists():
        st.error(f"File hasil cluster tidak ditemukan: {HASIL_CLUSTER_PATH}")
        st.stop()

    df_cluster = pd.read_csv(HASIL_CLUSTER_PATH)

    # =========================
    # JUDUL HALAMAN
    # =========================
    st.markdown("""
    <div style="margin-bottom:24px;">
        <div style="
            font-size:34px;
            font-weight:900;
            color:black;
            margin-bottom:8px;
        ">
            Hasil Cluster Kabupaten/Kota di Jawa Timur Tahun 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # RINGKASAN HASIL CLUSTER
    # =========================
    st.markdown("""
    <div style="
        margin-top: 22px;
        margin-bottom: 12px;
        padding-left: 12px;
        border-left: 15px solid #4C763B;
    ">
        <div style="
            font-size: 22px;
            font-weight: 900;
            color: #0F172A;
        ">
            Ringkasan Hasil Cluster
        </div>
        <div style="
            font-size: 14px;
            color: #0F172A;
            margin-top: 4px;
        ">
            Ringkasan jumlah cluster dan metode yang digunakan dalam analisis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background:white;
            border-radius:18px;
            padding:22px;
            border:1px solid #E5E7EB;
            box-shadow:0 8px 24px rgba(15,23,42,0.06);
            text-align:center;
        ">
            <div style="font-size:16px; color:black; font-weight:700; margin-bottom:8px;">
                Jumlah Cluster
            </div>
            <div style="font-size:38px; color:#4C763B; font-weight:900;">
                3
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background:white;
            border-radius:18px;
            padding:22px;
            border:1px solid #E5E7EB;
            box-shadow:0 8px 24px rgba(15,23,42,0.06);
            text-align:center;
        ">
            <div style="font-size:16px; color:black; font-weight:700; margin-bottom:8px;">
                Metode
            </div>
            <div style="font-size:30px; color:#4C763B; font-weight:900;">
                Ward
            </div>
            <div style="font-size:16px; color:black;">
                Hierarchical Clustering
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background:white;
            border-radius:18px;
            padding:22px;
            border:1px solid #E5E7EB;
            box-shadow:0 8px 24px rgba(15,23,42,0.06);
            text-align:center;
        ">
            <div style="font-size:16px; color:black; font-weight:700; margin-bottom:8px;">
               Hasil Silhouette Score
            </div>
            <div style="font-size:38px; color:#4C763B; font-weight:900;">
                0,529
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # TABEL HASIL CLUSTER
    # =========================
    st.markdown("""
    <div style="
        margin-top: 32px;
        margin-bottom: 12px;
        padding-left: 12px;
        border-left: 15px solid #4C763B;
    ">
        <div style="
            font-size: 22px;
            font-weight: 900;
            color: #0F172A;
        ">
            Tabel Hasil Cluster
        </div>
        <div style="
            font-size: 14px;
            color: black;
            margin-top: 4px;
        ">
            Data hasil pengelompokan kabupaten/kota berdasarkan indikator yang digunakan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df_cluster.head(38), use_container_width=True)

    
    # =========================
    # PETA CLUSTER
    # =========================

    st.markdown("""
    <div style="
        margin-top: 32px;
        margin-bottom: 14px;
        padding-left: 12px;
        border-left: 15px solid #4C763B;
    ">
        <div style="
            font-size: 22px;
            font-weight: 900;
            color: #0F172A;
        ">
            Peta Sebaran Cluster Kabupaten/Kota
        </div>
        <div style="
            font-size: 14px;
            color: black;
            margin-top: 4px;
        ">
            Warna pada peta menunjukkan cluster masing-masing kabupaten/kota di Jawa Timur.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fungsi untuk menyamakan nama daerah antara CSV dan GeoJSON
    def nama_daerah(nama):
        nama = str(nama).lower()
        nama = nama.replace("kab.", "kabupaten ")
        nama = nama.replace("kota.", "kota ")
        nama = nama.replace("kab ", "kabupaten ")
        nama = nama.replace(".", " ")
        nama = " ".join(nama.split())
        return nama

    # Ambil kolom yang dibutuhkan untuk peta
    df_peta = df_cluster[["Kabupaten/Kota", "Cluster"]].copy()
    df_peta["nama_bersih"] = df_peta["Kabupaten/Kota"].apply(nama_daerah)

    # Ambil GeoJSON kabupaten/kota Indonesia
    url_geojson = "https://raw.githubusercontent.com/AlfianAliM/Indonesia-GeoJSON/master/kab_kota.geojson"
    gdf_indonesia = gpd.read_file(url_geojson)

    # Filter hanya Provinsi Jawa Timur
    # Kode provinsi Jawa Timur = 35
    gdf_jatim = gdf_indonesia[
        gdf_indonesia["code"].astype(str).str.startswith("35")
    ].copy()

    gdf_jatim["nama_bersih"] = gdf_jatim["name"].apply(nama_daerah)

    # Gabungkan data GeoJSON dengan hasil cluster
    gdf_cluster = gdf_jatim.merge(
        df_peta,
        on="nama_bersih",
        how="left"
    )

    gdf_cluster["Cluster"] = pd.to_numeric(gdf_cluster["Cluster"], errors="coerce")
    gdf_cluster_plot = gdf_cluster.dropna(subset=["Cluster"]).copy()
    gdf_cluster_plot["Cluster"] = gdf_cluster_plot["Cluster"].astype(int)

    # Warna cluster
    colors = {
        0: "#2563EB",  # Biru
        1: "#EF4444",  # Merah
        2: "#10B981"   # Hijau
    }

    # Membuat peta
    m = folium.Map(
        location=[-7.55, 112.55],
        zoom_start=8,
        tiles="cartodbpositron"
    )

    def style_function(feature):
        cluster = feature["properties"]["Cluster"]

        if cluster is None:
            return {
                "fillColor": "#D1D5DB",
                "color": "black",
                "weight": 0.8,
                "fillOpacity": 0.5,
            }

        cluster = int(cluster)

        return {
            "fillColor": colors.get(cluster, "#9CA3AF"),
            "color": "black",
            "weight": 0.8,
            "fillOpacity": 0.8,
        }

    folium.GeoJson(
        gdf_cluster_plot,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["name", "Cluster"],
            aliases=["Daerah:", "Cluster:"],
            localize=True
        )
    ).add_to(m)

    # Tampilkan peta
    st_folium(m, width=1000, height=520)

   
    # =========================
    # INTERPRETASI SETIAP CLUSTER
    # =========================
    st.markdown("""
    <div style="
        margin-top: 32px;
        margin-bottom: 14px;
        padding-left: 12px;
        border-left: 15px solid #4C763B;
    ">
        <div style="
            font-size: 22px;
            font-weight: 900;
            color: #0F172A;
        ">
            Interpretasi Setiap Cluster
        </div>
        <div style="
            font-size: 14px;
            color: black;
            margin-top: 4px;
        ">
            Ringkasan karakteristik masing-masing cluster berdasarkan indikator demografi dan ketenagakerjaan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
        <div style="
            background: #F9F5F0;
            border: 1px solid #BFDBFE;
            border-radius: 22px;
            padding: 22px;
            min-height: 470px;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        ">
            <div style="
                width: 58px;
                height: 58px;
                border-radius: 18px;
                background: #4C763B;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                font-weight: 900;
                margin-bottom: 16px;
            ">
                1
            </div>

            <div style="
                font-size: 22px;
                font-weight: 900;
                color: #0F172A;
                margin-bottom: 6px;
            ">
                Cluster 1
            </div>
            
            
            <div style="
                background: #B0CE88;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            ">
                <b>Daftar Daerah:</b><br>
                Kab.Bangkalan, Kab.Banyuwangi, Kab.Blitar, Kab.Bojonegoro, Kab.Bondowoso
                , Kab.Gresik, Kab.Jember, Kab.Jombang, Kab.Kediri, Kab.Lamongan, Kab.Lumajang
                , Kab.Madiun, Kab.Magetan, Kab.Malang, Kab.Mojokerto, Kab.Nganjuk, Kab.Ngawi, Kab.Pacitan
                , Kab.Pamekasan, Kab.Pasuruan, Kab.Ponorogo, Kab.Probolinggo, Kab.Sampang
                , Kab.Situbondo, Kab.Sumenep, Kab.Trenggalek, Kab.Tuban
                , Kab.Tulungagung, Kota Batu
                
            </div>
                        
               <div style="
                background: #EFF5D2;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            ">
                <div style="
                font-size: 16px;
                color: #black;
                line-height: 1.6;
                ">
                <b>Hasil Cluster:</b><br>
                </div>
                        
                <div style="
                font-size: 14px;
                color: #black;
                line-height: 1.6;
                ">
                Jumlah Penduduk (Minimal) = 225.120 Jiwa<br>
                Jumlah Penduduk (Maximal) = 2.755.438 Jiwa<br> 
                Laju Pertumbuhan (Median) = 0.65% <br>  
                Kepadatan Penduduk (Median) = 791 jiwa/km²<br>   
                TPAK (Mean) = 75,28% <br>
                TPT (Mean) = 3,48% <br>
                </div>
               
            </div>
      
           <div style="
                background: #B0CE88;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            "> <b>Ciri Utama:</b><br>
            Cluster 1 dengan 29 daerah memiliki ciri utama berupa jumlah penduduk, laju pertumbuhan tertinggi, TPAK yang tergolong tinggi dibandingkan cluster lainnya.
            Serta, Laju Pertumbuhan Penduduk dan TPT yang tergolong rendah dibandingkan cluster lainnya.
            </div>
        </div>
        """, height=1000, scrolling=False)
    

    
    components.html("""
        <div style="
            background: #F9F5F0;
            border: 1px solid #BFDBFE;
            border-radius: 22px;
            padding: 22px;
            min-height: 470px;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        ">
            <div style="
                width: 58px;
                height: 58px;
                border-radius: 18px;
                background: #4C763B;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                font-weight: 900;
                margin-bottom: 16px;
            ">
                2
            </div>

            <div style="
                font-size: 22px;
                font-weight: 900;
                color: #0F172A;
                margin-bottom: 6px;
            ">
                Cluster 2
            </div>
            
            
            <div style="
                background: #B0CE88;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            ">
                <b>Daftar Daerah:</b><br>
            Kab.Sidoarjo, Kota Malang, Kota Surabaya
                
            </div>
                        
               <div style="
                background: #EFF5D2;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            ">
                <div style="
                font-size: 16px;
                color: #black;
                line-height: 1.6;
                ">
                <b>Hasil Cluster:</b><br>
                </div>
                        
                <div style="
                font-size: 14px;
                color: #black;
                line-height: 1.6;
                ">
                Jumlah Penduduk (Minimal) = 879.873 Jiwa<br>
                Jumlah Penduduk (Maximal) = 2.931.611 Jiwa<br> 
                Laju Pertumbuhan (Median) = 0,88% <br>  
                Kepadatan Penduduk (Median) = 7.921 jiwa/km²<br>   
                TPAK (Mean) = 69,99% <br>
                TPT (Mean) = 5,43% <br>
                </div>
               
            </div>
      
           <div style="
                background: #B0CE88;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            "> <b>Ciri Utama:</b><br>
            Cluster 2 dengan 3 daerah memiliki ciri utama berupa kepadatan penduduk dan TPT tergolong tertinggi dibandingkan dengan cluster lainnya.
            Serta, Laju Pertumbuhan Penduduk dan TPAK yang tergolong rendah dibandingkan cluster lainnya.
            </div>
        </div>
        """, height=1000, scrolling=False)
    
    components.html("""
        <div style="
            background: #F9F5F0;
            border: 1px solid #BFDBFE;
            border-radius: 22px;
            padding: 22px;
            min-height: 470px;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        ">
            <div style="
                width: 58px;
                height: 58px;
                border-radius: 18px;
                background: #4C763B;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                font-weight: 900;
                margin-bottom: 16px;
            ">
                3
            </div>

            <div style="
                font-size: 22px;
                font-weight: 900;
                color: #0F172A;
                margin-bottom: 6px;
            ">
                Cluster 3
            </div>
            
            
            <div style="
                background: #B0CE88;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            ">
                <b>Daftar Daerah:</b><br>
           Kota Blitar, Kota Kediri, Kota Madiun, Kota Mojokerto, Kota Pasuruan, Kota Probolinggo
            </div>
                        
               <div style="
                background: #EFF5D2;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            ">
                <div style="
                font-size: 16px;
                color: #black;
                line-height: 1.6;
                ">
                <b>Hasil Cluster:</b><br>
                </div>
                        
                <div style="
                font-size: 14px;
                color: #black;
                line-height: 1.6;
                ">
                Jumlah Penduduk (Minimal) = 138.613 Jiwa<br>
                Jumlah Penduduk (Maximal) = 301.202 Jiwa<br> 
                Laju Pertumbuhan (Median) = 1,02% <br>  
                Kepadatan Penduduk (Median) = 5.171,5 jiwa/km²<br>   
                TPAK (Mean) = 71,98% <br>
                TPT (Mean) = 4,42% <br>
                </div>
               
            </div>
      
           <div style="
                background: #B0CE88;
                border-radius: 14px;
                padding: 12px;
                margin-top: 14px;
                font-size: 14px;
                color: #black;
                line-height: 1.6;
            "> <b>Ciri Utama:</b><br>
            Cluster 3 dengan 6 daerah memiliki ciri utama berupa laju pertumbuhan penduduk yang tergolong tertinggi dibandingkan dengan cluster lainnya.
            Serta, Jumlah Penduduk yang tergolong rendah dibandingkan cluster lainnya.
            </div>
        </div>
        """, height=1000, scrolling=False)

   

   

if __name__ == "__main__":
    show_page()