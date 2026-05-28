import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px
from pathlib import Path


def show_page():
   
    # KONFIGURASI PATH
    BASE_DIR = Path(__file__).parent

    DATA_PATH = BASE_DIR / "jumlah penduduk-prov.csv"
    JUMLAH_PENDUDUK_PATH = BASE_DIR / "Jumlah Penduduk Jatim.csv"
    LAJU_PATH = BASE_DIR / "Laju Pertumbuhan.csv"
    KEPADATAN_PATH = BASE_DIR / "Kepadatan.csv"
    TPAK_PATH = BASE_DIR / "PA Magang - TPAK.csv"
    TPT_PATH = BASE_DIR / "PA Magang - TPT.csv"

    file_paths = {
        "Data Penduduk Provinsi": DATA_PATH,
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

    # =========================
    # LOAD DATA
    # =========================
    df_kependudukanprov = pd.read_csv(DATA_PATH)
    df_jumlahpenduduk = pd.read_csv(JUMLAH_PENDUDUK_PATH)
    df_lajupertumbuhan = pd.read_csv(LAJU_PATH)
    df_kepadatan = pd.read_csv(KEPADATAN_PATH)
    df_TPAK = pd.read_csv(TPAK_PATH)
    df_TPT = pd.read_csv(TPT_PATH)

    tahun_cols = ["2020", "2021", "2022", "2023", "2024", "2025"]

    # =========================
    # STYLE GLOBAL
    # =========================
    st.markdown("""
    <style>
        .main-title h1 {
            font-size: 36px;
            font-weight: 900;
            margin: 0;
            line-height: 1.25;
        }

        .main-title p {
            font-size: 16px;
            margin-top: 10px;
            color: #DBEAFE;
        }

        .section-title {
            background: transparent;
            color: #0F172A;
            padding: 0 0 0 14px;
            border-left: 10px solid green;
            border-radius: 0;
            margin: 26px 0 16px 0;
            box-shadow: none;
        }

        .section-title h2 {
            font-size: 22px;
            font-weight: 900;
            margin: 0;
            line-height: 1.25;
        }

        .section-title p {
            margin: 5px 0 0 0;
            color: #64748B;
            font-size: 14px;
            line-height: 1.4;
        }
        .small-heading {
            color: #0F172A;
            font-size: 20px;
            font-weight: 900;
            line-height: 1.3;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    # JUDUL DASHBOARD
    st.markdown("""
    <div class="main-title">
        <h1>Dashboard Kependudukan dan Ketenagakerjaan Provinsi Jawa Timur</h1>
    </div>
    """, unsafe_allow_html=True)

    # FUNGSI BANTU
   
    def bersihkan_angka_indonesia(df, tahun_cols):
        df.columns = df.columns.str.strip()

        for col in tahun_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    def format_indo(x, desimal=1):
        return f"{x:,.{desimal}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def format_angka(nilai, satuan=""):
        if pd.isna(nilai):
            return "-"

        if satuan == "%":
            return f"{nilai:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
        elif satuan == "jiwa":
            return f"{nilai:,.0f} jiwa".replace(",", ".")
        elif satuan == "jiwa/km²":
            return f"{nilai:,.0f} jiwa/km²".replace(",", ".")
        else:
            return f"{nilai:,.0f}".replace(",", ".")

    def grafik(df_filter, tahun_cols, nama_indikator, pilihan_kabkota, satuan="", label_y=None):
        df_grafik = df_filter.melt(
            id_vars="Kabupaten/Kota",
            value_vars=tahun_cols,
            var_name="Tahun",
            value_name=nama_indikator
        )

        if label_y is None:
            label_y = nama_indikator

        fig = px.line(
            df_grafik,
            x="Tahun",
            y=nama_indikator,
            text=nama_indikator,
            markers=True,
            title=f"{nama_indikator} {pilihan_kabkota}"
        )

        fig.update_yaxes(
            title_text=f"<b>{label_y}</b>",
            title_font=dict(size=13, color="black", family="Arial Black"),
            tickfont=dict(size=11, color="black"),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7",
            tickformat=","
        )

        return fig

    def hitung_insight(df_filter, tahun_cols, nama_kolom):
        df_long = df_filter.melt(
            id_vars="Kabupaten/Kota",
            value_vars=tahun_cols,
            var_name="Tahun",
            value_name=nama_kolom
        )

        mean_val = df_long[nama_kolom].mean()
        max_val = df_long[nama_kolom].max()
        min_val = df_long[nama_kolom].min()

        return mean_val, max_val, min_val

    # CLEANING DATA PROVINSI
    df_kependudukanprov.columns = df_kependudukanprov.columns.str.strip()
    df_kependudukanprov = df_kependudukanprov.loc[
        :, ~df_kependudukanprov.columns.str.contains("^Unnamed")
    ]

    df_kependudukanprov["Provinsi"] = (
        df_kependudukanprov["Provinsi"]
        .astype(str)
        .str.strip()
    )

    df_kependudukanprov = bersihkan_angka_indonesia(df_kependudukanprov, tahun_cols)

    df_kependudukanprov = df_kependudukanprov[
        df_kependudukanprov["Provinsi"] != "Indonesia"
    ]

    # =========================
    # SECTION PROVINSI
    # =========================
    st.markdown("""
    <div class="section-title">
        <h2>Jumlah Penduduk Berdasarkan Provinsi di Indonesia Tahun 2020-2025</h2>
    </div>
    """, unsafe_allow_html=True)

    tahun_pilihan = st.selectbox(
        "Pilih Tahun",
        tahun_cols,
        key="filter_tahun_provinsi"
    )

    df_tahun = df_kependudukanprov.sort_values(
        by=tahun_pilihan,
        ascending=False
    ).reset_index(drop=True)

    top5 = df_tahun.head(5)

    data_jatim = df_kependudukanprov[
        df_kependudukanprov["Provinsi"] == "Jawa Timur"
    ].iloc[0]

    nilai_jatim = data_jatim[tahun_pilihan]
    peringkat_jatim = df_tahun[df_tahun["Provinsi"] == "Jawa Timur"].index[0] + 1

    prov_pertama = df_tahun.iloc[0]["Provinsi"]
    nilai_pertama = df_tahun.iloc[0][tahun_pilihan]
    selisih_jatim = nilai_pertama - nilai_jatim

    # =========================
    # CARD INSIGHT PROVINSI
    # =========================
    card1, card2, card3 = st.columns(3)

    with card1:
        components.html(f"""
        <div style="
            background:#0D530E;
            padding:20px;
            border-radius:20px;
            margin-bottom:18px;
            min-height:100px;
            box-shadow:0 10px 26px rgba(15,23,42,0.22);
            font-family:Arial, sans-serif;
            text-align:center;
            color:white;
        ">
            <div style="font-size:16px; font-weight:900; margin-bottom:10px;">
                Jawa Timur Tahun {tahun_pilihan}
            </div>
            <div style="color:#FFEF91; font-size:42px; font-weight:900;">
                {format_indo(nilai_jatim, 1)}
            </div>
            <div style="font-size:15px; font-weight:700; margin-top:8px;">
                Ribu Jiwa
            </div>
        </div>
        """, height=210, scrolling=False)

    with card2:
        components.html(f"""
        <div style="
            background:#0D530E;
            padding:20px;
            border-radius:20px;
            min-height:100px;
            box-shadow:0 10px 26px rgba(15,23,42,0.22);
            font-family:Arial, sans-serif;
            text-align:center;
            color:white;
        ">
            <div style="font-size:16px; font-weight:900; margin-bottom:10px;">
                Peringkat Jawa Timur
            </div>
            <div style="color:#FFEF91; font-size:42px; font-weight:900;">
                {peringkat_jatim}
            </div>
            <div style="font-size:15px; font-weight:700; margin-top:8px;">
                dari 34 provinsi
            </div>
        </div>
        """, height=210, scrolling=False)

    with card3:
        components.html(f"""
        <div style="
            background:#0D530E;
            padding:20px;
            border-radius:20px;
            min-height:100px;
            box-shadow:0 10px 26px rgba(15,23,42,0.22);
            font-family:Arial, sans-serif;
            text-align:center;
            color:white;
        ">
            <div style="font-size:16px; font-weight:900; margin-bottom:10px;">
                Selisih dengan {prov_pertama}
            </div>
            <div style="color:#FFEF91; font-size:42px; font-weight:900;">
                {format_indo(selisih_jatim, 1)}
            </div>
            <div style="font-size:15px; font-weight:700; margin-top:8px;">
                Ribu Jiwa
            </div>
        </div>
        """, height=210, scrolling=False)

    # =========================
    # GRAFIK PROVINSI
    # =========================
    palette_jatim = ["#132A13", "#31572C", "#4F772D", "#90A955", "#C1CF2A"]
    col_prov1, col_prov2 = st.columns(2)

    with col_prov1:
        st.markdown(
            f'<div class="small-heading">5 Provinsi dengan Jumlah Penduduk Tertinggi Tahun {tahun_pilihan}</div>',
            unsafe_allow_html=True
        )
        fig_bar = px.bar(
            top5,
            x="Provinsi",
            y=tahun_pilihan,
            text=tahun_pilihan
        )

        fig_bar.update_layout(
            height=430,
            xaxis_title="<b>Provinsi</b>",
            yaxis_title="<b>Jumlah Penduduk (Ribu Jiwa)</b>",
            font=dict(color="black", size=13),
            xaxis=dict(
                title_font=dict(color="black", size=14),
                tickfont=dict(color="black", size=11)
            ),
            yaxis=dict(
                title_font=dict(color="black", size=14),
                tickfont=dict(color="black", size=11),
                gridcolor="#EEF2F7"
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=40, b=60, l=60, r=30)
        )

        fig_bar.update_traces(
            marker_color = palette_jatim,
            texttemplate="%{text:,.1f}",
            textfont=dict(color="white", size=11),
            textposition="inside"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col_prov2:
        st.markdown(
            '<div class="small-heading">Tren Jumlah Penduduk Provinsi Jawa Timur Tahun 2020–2025</div>',
            unsafe_allow_html=True
        )

        df_tren_jatim = pd.DataFrame({
            "Tahun": tahun_cols,
            "Jumlah Penduduk": [data_jatim[tahun] for tahun in tahun_cols]
        })

        fig_line = px.line(
            df_tren_jatim,
            x="Tahun",
            y="Jumlah Penduduk",
            markers=True,
            text="Jumlah Penduduk",

        )

        fig_line.update_layout(
            height=430,
            hovermode="x unified",
            font=dict(color="black", size=13),
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=40, b=60, l=60, r=30)
        )

        fig_line.update_traces(
            texttemplate="%{text:,.1f}",
            textposition="top center",
            textfont=dict(size=11, color="black"),
            marker=dict(size=9, color="#306D29", line=dict(width=2, color="white")),
            line=dict(width=4, color="#306D29"),
            cliponaxis=False
        )

        fig_line.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"
        )

        fig_line.update_yaxes(
            title_text="<b>Jumlah Penduduk (Ribu Jiwa)</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"
        )

        st.plotly_chart(fig_line, use_container_width=True)
        st.caption("Sumber: BPS Indonesia, 2020–2025")

    # =========================
    # CLEANING DATA KAB/KOTA
    # =========================
    for df in [df_jumlahpenduduk, df_lajupertumbuhan, df_kepadatan, df_TPAK, df_TPT]:
        df.columns = df.columns.str.strip()
        df["Kabupaten/Kota"] = df["Kabupaten/Kota"].astype(str).str.strip()

        for col in tahun_cols:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df_jumlahpenduduk = df_jumlahpenduduk[
        df_jumlahpenduduk["Kabupaten/Kota"] != "Jawa Timur"
    ]

    df_lajupertumbuhan = df_lajupertumbuhan[
        df_lajupertumbuhan["Kabupaten/Kota"] != "Jawa Timur"
    ]

    df_kepadatan = df_kepadatan[
        df_kepadatan["Kabupaten/Kota"] != "Jawa Timur"
    ]

    df_TPAK = df_TPAK[
        df_TPAK["Kabupaten/Kota"] != "Jawa Timur"
    ]

    df_TPT = df_TPT[
        df_TPT["Kabupaten/Kota"] != "Jawa Timur"
    ]

    # =========================
    # SECTION KAB/KOTA
    # =========================
    st.markdown("""
    <div class="section-title">
        <h2>Kondisi Kependudukan dan Ketenagakerjaan Berdasarkan Kabupaten/Kota</h2>

    </div>
    """, unsafe_allow_html=True)

    # Pastikan tahun urut
    tahun_cols = ["2020", "2021", "2022", "2023", "2024", "2025"]
    tahun_cols = sorted(tahun_cols, key=lambda x: int(x))
    #pilih kota dan tahun
    pilihan_kabkota = st.selectbox(
        "Pilih Kabupaten/Kota",
        df_jumlahpenduduk["Kabupaten/Kota"].unique(),
        key="Filter_utama_kabkota"
    )
    pilihan_tahun_kabkota = st.multiselect(
        "Pilih Tahun",
        tahun_cols,
        default=tahun_cols,
        key="Filter_tahun_kabkota"
    )
    if not pilihan_tahun_kabkota:
        st.warning("Pilih minimal satu tahun untuk menampilkan grafik.")
        st.stop()
   
        # sistem akan otomatis mengurutkan menjadi 2022, 2024, 2025
        pilihan_tahun_kabkota = sorted(
            pilihan_tahun_kabkota,
            key=lambda x: int(x)
        )

        # Teks tahun untuk caption dan insight
    if len(pilihan_tahun_kabkota) == len(tahun_cols):
        teks_tahun_kabkota = f"{tahun_cols[0]}–{tahun_cols[-1]}"
    elif len(pilihan_tahun_kabkota) == 1:
            teks_tahun_kabkota = pilihan_tahun_kabkota[0]
    else:
            teks_tahun_kabkota = ", ".join(pilihan_tahun_kabkota)
    #cleaning
    df_filter_jp = df_jumlahpenduduk[
        df_jumlahpenduduk["Kabupaten/Kota"] == pilihan_kabkota
    ]

    df_filter_lp = df_lajupertumbuhan[
        df_lajupertumbuhan["Kabupaten/Kota"] == pilihan_kabkota
    ]

    df_filter_kepadatan = df_kepadatan[
        df_kepadatan["Kabupaten/Kota"] == pilihan_kabkota
    ]

    df_filter_TPAK = df_TPAK[
        df_TPAK["Kabupaten/Kota"] == pilihan_kabkota
    ]

    df_filter_TPT = df_TPT[
        df_TPT["Kabupaten/Kota"] == pilihan_kabkota
    ]

    # =========================
    # FUNGSI GRAFIK GARIS
    # =========================
    def grafik(df_filter, tahun_cols, nama_indikator, pilihan_kabkota, satuan="", label_y=None):
        # Pastikan tahun selalu urut walaupun user pilih acak
        tahun_cols = sorted(tahun_cols, key=lambda x: int(x))

        df_grafik = df_filter.melt(
            id_vars="Kabupaten/Kota",
            value_vars=tahun_cols,
            var_name="Tahun",
            value_name=nama_indikator
        )

        # Paksa urutan tahun di sumbu X
        df_grafik["Tahun"] = pd.Categorical(
            df_grafik["Tahun"],
            categories=tahun_cols,
            ordered=True
        )

        df_grafik = df_grafik.sort_values("Tahun")

        if label_y is None:
            label_y = nama_indikator

        fig = px.line(
            df_grafik,
            x="Tahun",
            y=nama_indikator,
            text=nama_indikator,
            markers=True,
            title=f"{nama_indikator} {pilihan_kabkota}"
        )

        fig.update_layout(
            height=430,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=70, b=60, l=60, r=30),
            font=dict(color="#132A13", size=13),
            title=dict(
                text=f"<b>{nama_indikator} {pilihan_kabkota}</b>",
                x=0.02,
                font=dict(size=20, color="#132A13", family="Arial Black")
            )
        )

        fig.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="#132A13", size=14, family="Arial Black"),
            tickfont=dict(color="#132A13", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7",
            categoryorder="array",
            categoryarray=tahun_cols
        )

        fig.update_yaxes(
            title_text=f"<b>{label_y}</b>",
            title_font=dict(size=13, color="#132A13", family="Arial Black"),
            tickfont=dict(size=11, color="#132A13"),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7",
            tickformat=","
        )

        if satuan == "%":
            fig.update_traces(
                line=dict(color="#306D29", width=4),
                marker=dict(color="#306D29", size=9),
                texttemplate="%{text:.2f}%",
                textposition="top center",
                textfont=dict(size=11, color="black"),
                cliponaxis=False
            )
        else:
            fig.update_traces(
                line=dict(color="#306D29", width=4),
                marker=dict(color="#306D29", size=9),
                texttemplate="%{text:,.0f}",
                textposition="top center",
                textfont=dict(size=11, color="black"),
                cliponaxis=False
            )

        return fig
    # GRAFIK KAB/KOTA
    col1, col2 = st.columns(2)
    with col1:
        fig_jp = grafik(
            df_filter_jp,
            pilihan_tahun_kabkota,
            "Jumlah Penduduk",
            pilihan_kabkota,
            label_y="Jumlah Penduduk (Ribu jiwa)"
        )
        fig_jp.update_traces(
            textfont=dict(size=11, color="black"),
            line=dict(color="#306D29", width=4),
            marker=dict(color="#306D29", size=9)
        )
        
        fig_jp.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"

        )
        st.plotly_chart(fig_jp, use_container_width=True)

    with col2:
        fig_lp = grafik(
            df_filter_lp,
            pilihan_tahun_kabkota,
            "Laju Pertumbuhan",
            pilihan_kabkota,
            satuan="%",
            label_y="Laju Pertumbuhan (%)"
        )
        fig_lp.update_traces(
            textfont=dict(size=11, color="black"),
            line=dict(color="#306D29", width=4),
            marker=dict(color="#306D29", size=9)
        )
        
        fig_lp.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"

        )
        st.plotly_chart(fig_lp, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig_kp = grafik(
            df_filter_kepadatan,
            pilihan_tahun_kabkota,
            "Kepadatan Penduduk",
            pilihan_kabkota,
            label_y="Kepadatan Penduduk (km²)"
        )
        fig_kp.update_traces(
            textfont=dict(size=11, color="black"),
            line=dict(color="#306D29", width=4),
            marker=dict(color="#306D29", size=9)
        )
        
        fig_kp.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"

        )
        st.plotly_chart(fig_kp, use_container_width=True)

    with col4:
        fig_tpak = grafik(
            df_filter_TPAK,
            pilihan_tahun_kabkota,
            "TPAK",
            pilihan_kabkota,
            satuan="%",
            label_y="Nilai TPAK (%)"
        )
        fig_tpak.update_traces(
            textfont=dict(size=11, color="black"),
            line=dict(color="#306D29", width=4),
            marker=dict(color="#306D29", size=9)
        )
        
        fig_tpak.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"

        )
        st.plotly_chart(fig_tpak, use_container_width=True)

    fig_tpt = grafik(
        df_filter_TPT,
        pilihan_tahun_kabkota,
        "TPT",
        pilihan_kabkota,
        satuan="%",
        label_y="Nilai TPT (%)"
    )
    fig_tpt.update_traces(
            textfont=dict(size=11, color="black"),
            line=dict(color="#306D29", width=4),
            marker=dict(color="#306D29", size=9)
        )
        
    fig_tpt.update_xaxes(
            title_text="<b>Tahun</b>",
            title_font=dict(color="black", size=14, family="Arial Black"),
            tickfont=dict(color="black", size=11),
            showline=True,
            linecolor="#CBD5E1",
            gridcolor="#EEF2F7"

        )
    st.plotly_chart(fig_tpt, use_container_width=True)

    st.caption("Sumber: BPS Provinsi Jawa Timur, 2020–2025")

    # =========================
    # INSIGHT KAB/KOTA
    # =========================
    mean_jp, max_jp, min_jp = hitung_insight(
        df_filter_jp,
        pilihan_tahun_kabkota,
        "Jumlah Penduduk"
    )

    mean_lp, max_lp, min_lp = hitung_insight(
        df_filter_lp,
        pilihan_tahun_kabkota,
        "Laju Pertumbuhan"
    )

    mean_kepadatan, max_kepadatan, min_kepadatan = hitung_insight(
        df_filter_kepadatan,
        pilihan_tahun_kabkota,
        "Kepadatan Penduduk"
    )

    mean_tpak, max_tpak, min_tpak = hitung_insight(
        df_filter_TPAK,
        pilihan_tahun_kabkota,
        "TPAK"
    )

    mean_tpt, max_tpt, min_tpt = hitung_insight(
        df_filter_TPT,
        pilihan_tahun_kabkota,
        "TPT"
    )

    components.html(f"""
    <div style="
        background: none;
        border:1px solid #D8E3F0;
        border-radius:28px;
        padding:34px 38px;
        box-shadow:0 16px 40px rgba(15,23,42,0.12);
        font-family:Arial, sans-serif;
    ">

        <div style="display:flex; align-items:center; gap:18px; margin-bottom:30px;">
            <div>
                <div style="
                    font-size:30px;
                    font-weight:900;
                    color:#0F172A;
                    margin-bottom:6px;
                ">
                    Insight Kabupaten/Kota
                </div>
                <div style="
                    font-size:16px;
                    color:#306D29;
                    font-width:500px;
                ">
                    Ringkasan rata-rata, nilai maksimum, dan minimum untuk {pilihan_kabkota}
                </div>
            </div>
        </div>

        <div style="
            display:grid;
            grid-template-columns:repeat(3, 1fr);
            gap:24px;
            margin-bottom:24px;
        ">

            <div class="insight-card">
                <div class="card-title">Jumlah Penduduk</div>
                <div class="row"><span>Rata-rata</span><b>{format_angka(mean_jp, "jiwa")}</b></div>
                <div class="row"><span>Max</span><b>{format_angka(max_jp, "jiwa")}</b></div>
                <div class="row"><span>Min</span><b>{format_angka(min_jp, "jiwa")}</b></div>
            </div>

            <div class="insight-card">
                <div class="card-title">Laju Pertumbuhan</div>
                <div class="row"><span>Rata-rata</span><b>{format_angka(mean_lp, "%")}</b></div>
                <div class="row"><span>Max</span><b>{format_angka(max_lp, "%")}</b></div>
                <div class="row"><span>Min</span><b>{format_angka(min_lp, "%")}</b></div>
            </div>

            <div class="insight-card">
                <div class="card-title"> Kepadatan Penduduk</div>
                <div class="row"><span>Rata-rata</span><b>{format_angka(mean_kepadatan, "jiwa/km²")}</b></div>
                <div class="row"><span>Max</span><b>{format_angka(max_kepadatan, "jiwa/km²")}</b></div>
                <div class="row"><span>Min</span><b>{format_angka(min_kepadatan, "jiwa/km²")}</b></div>
            </div>
        </div>

        <div style="
            display:grid;
            grid-template-columns:repeat(2, 1fr);
            gap:24px;
            width:70%;
            margin:0 auto;
        ">
            <div class="insight-card">
                <div class="card-title">TPAK</div>
                <div class="row"><span>Rata-rata</span><b>{format_angka(mean_tpak, "%")}</b></div>
                <div class="row"><span>Max</span><b>{format_angka(max_tpak, "%")}</b></div>
                <div class="row"><span>Min</span><b>{format_angka(min_tpak, "%")}</b></div>
            </div>

            <div class="insight-card">
                <div class="card-title"> TPT</div>
                <div class="row"><span>Rata-rata</span><b>{format_angka(mean_tpt, "%")}</b></div>
                <div class="row"><span>Max</span><b>{format_angka(max_tpt, "%")}</b></div>
                <div class="row"><span>Min</span><b>{format_angka(min_tpt, "%")}</b></div>
            </div>
        </div>
    </div>

    <style>
    .insight-card {{
        background:white;
        border:1px solid #DDE7F3;
        border-radius:22px;
        padding:22px;
        box-shadow:0 10px 26px rgba(15,23,42,0.10);
    }}

    .card-title {{
        font-size:19px;
        font-weight:900;
        color:#0F172A;
        margin-bottom:18px;
    }}

    .row {{
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:13px 0;
        border-bottom:1px solid #E5EAF2;
        font-size:15px;
        color:black;
    }}

    .row:last-child {{
        border-bottom:none;
    }}

    .row b {{
        color:#306D29;
        font-size:16px;
        font-weight:900;
    }}
    </style>
    """, height=780, scrolling=False)



    # =========================
    # SECTION TOP 5 KAB/KOTA
    # =========================
    st.markdown("""
    <div class="section-title">
        <h2>Peringkat 5 Kabupaten/Kota Tertinggi Berdasarkan Indikator Kependudukan dan Ketenagakerjaan</h2>
        <p>Pilih tahun untuk menampilkan 5 Kabupaten/Kota dengan nilai tertinggi pada setiap indikator</p>
    </div>
    """, unsafe_allow_html=True)

    # Pastikan tahun urut
    tahun_cols = ["2020", "2021", "2022", "2023", "2024", "2025"]
    tahun_cols = sorted(tahun_cols, key=lambda x: int(x))

    # Untuk Top 5 cukup pilih 1 tahun
    tahun_pilihan_top5 = st.selectbox(
        "Pilih Tahun Top 5",
        tahun_cols,
        index=len(tahun_cols) - 1,
        key="filter_tahun_top5"
    )

    # Palette warna
    palette_jatim = ["#132A13", "#31572C", "#4F772D", "#90A955", "#ECF39E"]


    def grafik_bar_top5(df, tahun_pilihan, judul, label_y, satuan=""):
        top5 = (
            df.sort_values(by=tahun_pilihan, ascending=False)
            .head(5)
            .copy()
        )

        urutan_kabkota = top5["Kabupaten/Kota"].tolist()

        fig = px.bar(
            top5,
            x="Kabupaten/Kota",
            y=tahun_pilihan,
            text=tahun_pilihan,
            title=f"{judul} Tahun {tahun_pilihan}",
            category_orders={"Kabupaten/Kota": urutan_kabkota}
        )

        fig.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=70, b=80, l=65, r=35),
            title=dict(
                text=f"<b>{judul} Tahun {tahun_pilihan}</b>",
                x=0.02,
                font=dict(size=17, color="#132A13", family="Arial Black")
            ),
            font=dict(color="#132A13", family="Arial")
        )

        fig.update_xaxes(
            title_text="<b>Kabupaten/Kota</b>",
            title_font=dict(size=13, color="#132A13", family="Arial Black"),
            tickfont=dict(size=10, color="#132A13"),
            tickangle=-25,
            categoryorder="array",
            categoryarray=urutan_kabkota
        )

        fig.update_yaxes(
            title_text=f"<b>{label_y}</b>",
            title_font=dict(size=13, color="#132A13", family="Arial Black"),
            tickfont=dict(size=11, color="#132A13"),
            gridcolor="#ECF39E",
            tickformat=","
        )

        if satuan == "%":
            fig.update_traces(
                marker_color=palette_jatim,
                texttemplate="%{text:.2f}%",
                textposition="outside",
                textfont=dict(size=11, color="#132A13"),
                cliponaxis=False
            )
        else:
            fig.update_traces(
                marker_color=palette_jatim,
                texttemplate="%{text:,.0f}",
                textposition="outside",
                textfont=dict(size=11, color="#132A13"),
                cliponaxis=False
            )

        return fig


    # =========================
    # DATA TOP 5 BAR CHART
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        fig_top5_jp = grafik_bar_top5(
            df_jumlahpenduduk,
            tahun_pilihan_top5,
            "Top 5 Jumlah Penduduk",
            "Jumlah Penduduk (Jiwa)"
        )
        st.plotly_chart(fig_top5_jp, use_container_width=True)
        st.caption(f"Sumber: BPS Jatim, {tahun_pilihan_top5}")

    with col2:
        fig_top5_lp = grafik_bar_top5(
            df_lajupertumbuhan,
            tahun_pilihan_top5,
            "Top 5 Laju Pertumbuhan",
            "Laju Pertumbuhan (%)",
            satuan="%"
        )
        st.plotly_chart(fig_top5_lp, use_container_width=True)
        st.caption(f"Sumber: BPS Jatim, {tahun_pilihan_top5}")

    col3, col4 = st.columns(2)

    with col3:
        fig_top5_kp = grafik_bar_top5(
            df_kepadatan,
            tahun_pilihan_top5,
            "Top 5 Kepadatan Penduduk",
            "Kepadatan Penduduk (Jiwa/km²)"
        )
        st.plotly_chart(fig_top5_kp, use_container_width=True)
        st.caption(f"Sumber: BPS Jatim, {tahun_pilihan_top5}")

    with col4:
        fig_top5_tpak = grafik_bar_top5(
            df_TPAK,
            tahun_pilihan_top5,
            "Top 5 TPAK",
            "TPAK (%)",
            satuan="%"
        )
        st.plotly_chart(fig_top5_tpak, use_container_width=True)
        st.caption(f"Sumber: BPS Jatim, {tahun_pilihan_top5}")

    fig_top5_tpt = grafik_bar_top5(
        df_TPT,
        tahun_pilihan_top5,
        "Top 5 TPT",
        "TPT (%)",
        satuan="%"
    )

    st.plotly_chart(fig_top5_tpt, use_container_width=True)
    st.caption(f"Sumber: BPS Jatim, {tahun_pilihan_top5}")


  




    #statistik insight
    #Jumlah Penduduk Tertinggi
    idx_jp = df_jumlahpenduduk[tahun_pilihan].idxmax()
    daerah_jp = df_jumlahpenduduk.loc[idx_jp, "Kabupaten/Kota"]
    nilai_jp = df_jumlahpenduduk.loc[idx_jp, tahun_pilihan]
    #Laju Pertumbuhan Tertinggi
    idx_lp = df_lajupertumbuhan[tahun_pilihan].idxmax()
    daerah_lp = df_lajupertumbuhan.loc[idx_jp, "Kabupaten/Kota"]
    nilai_lp = df_lajupertumbuhan.loc[idx_jp, tahun_pilihan]
    #Kepadatan Penduduk
    idx_kp = df_kepadatan[tahun_pilihan].idxmax()
    daerah_kp = df_kepadatan.loc[idx_jp, "Kabupaten/Kota"]
    nilai_kp = df_kepadatan.loc[idx_jp, tahun_pilihan]
    #TPAK
    idx_TPAK = df_TPAK[tahun_pilihan].idxmax()
    daerah_TPAK = df_TPAK.loc[idx_jp, "Kabupaten/Kota"]
    nilai_TPAK = df_TPAK.loc[idx_jp, tahun_pilihan]
    #TPT
    #Kepadatan Penduduk
    idx_TPT = df_TPT[tahun_pilihan].idxmax()
    daerah_TPT = df_TPT.loc[idx_jp, "Kabupaten/Kota"]
    nilai_TPT = df_TPT.loc[idx_jp, tahun_pilihan]


    def ambil_tertinggi(df, tahun_pilihan):
        idx = df[tahun_pilihan].idxmax()
        daerah = df.loc[idx, "Kabupaten/Kota"]
        nilai = df.loc[idx, tahun_pilihan]
        return daerah, nilai

    daerah_jp, nilai_jp = ambil_tertinggi(df_jumlahpenduduk, tahun_pilihan)
    daerah_lp, nilai_lp = ambil_tertinggi(df_lajupertumbuhan, tahun_pilihan)
    daerah_kp, nilai_kp = ambil_tertinggi(df_kepadatan, tahun_pilihan)
    daerah_tpak, nilai_tpak = ambil_tertinggi(df_TPAK, tahun_pilihan)
    daerah_tpt, nilai_tpt = ambil_tertinggi(df_TPT, tahun_pilihan)
    #FORMAT ANGKA
    def format_card(nilai, satuan=""):
        if satuan == "%":
            return f"{nilai:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
        elif satuan == "jiwa":
            return f"{nilai:,.0f} jiwa".replace(",", ".")
        elif satuan == "jiwa/km²":
            return f"{nilai:,.0f} jiwa/km²".replace(",", ".")
        else:
            return f"{nilai:,.0f}".replace(",", ".")
#CARD
    st.markdown(f"""
        <div class="section-title">
            <h2>Insight Nilai Tertinggi Kabupaten/Kota Tahun {tahun_pilihan_top5}</h2>
            <p>Ringkasan Wilayah dengan nilai tertinggi pada setiap indikator kependudukan dan ketenagakerjaan</p>
        </div>
        """, unsafe_allow_html=True)
    def card_tertinggi(judul, nilai, daerah):
        html_card = f"""
        <div style="
            background: #0D530E;
            border-radius: 20px;
            padding: 20px;
            min-height: 180px;
            text-align: center;
            font-family: Arial, sans-serif;
            box-sizing: border-box;
        ">
            <div style="
                font-size: 16px;
                color:white;
                font-weight: 900;
                margin-bottom: 16px;
            ">
                {judul}
            </div>

            <div style="
                font-size: 25px;
                color: #E7E1B1;
                font-weight: 900;
                margin-bottom: 16px;
            ">
                {nilai}
            </div>
            <div style="
                font-size: 20px;
                color: #FFFFFF;
                font-weight: 900;
                line-height: 1.25;
                margin-bottom: 12px;
            ">
                {daerah}
            </div>

        </div>
        """
        components.html(html_card, height=230, scrolling=False)

    col1, col2, col3 = st.columns(3)
    with col1:
            card_tertinggi(
                "Jumlah Penduduk Tertinggi",
                format_card(nilai_jp, "jiwa"),
                daerah_jp
            )

    with col2:
            card_tertinggi(
                "Laju Pertumbuhan Tertinggi",
                format_card(nilai_lp, "%"),
                daerah_lp
            )

    with col3:
            card_tertinggi(
                "Kepadatan Penduduk Tertinggi",
                format_card(nilai_kp, "jiwa/km²"),
                daerah_kp
            )

    col4, col5 = st.columns(2)

    with col4:
            card_tertinggi(
                "TPAK Tertinggi",
                format_card(nilai_tpak, "%"),
                daerah_tpak
            )

    with col5:
            card_tertinggi(
                "TPT Tertinggi",
                format_card(nilai_tpt, "%"),
                daerah_tpt,
            )