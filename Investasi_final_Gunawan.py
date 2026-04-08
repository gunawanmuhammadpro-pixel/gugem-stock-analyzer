import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="GugemStockAnalyzer", 
    page_icon="💹",
    layout="wide"
)

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("💹 GugemStockAnalyzer")
st.write("Solusi Cerdas Pantau Saham & Simulasi Investasi (Trial Version)")

# --- 3. DAFTAR SAHAM ---
daftar_saham = {
    "--- PILIH SAHAM ---": "",
    "🏦 SEKTOR PERBANKAN": "",
    "Bank BCA (BBCA)": "BBCA", "Bank BRI (BBRI)": "BBRI", "Bank Mandiri (BMRI)": "BMRI", "Bank BNI (BBNI)": "BBNI",
    "🔥 SEKTOR ENERGI & TAMBANG": "",
    "Adaro Energy (ADRO)": "ADRO", "Aneka Tambang (ANTM)": "ANTM", "Bukit Asam (PTBA)": "PTBA",
    "🛒 SEKTOR KONSUMER": "",
    "Unilever (UNVR)": "UNVR", "Indofood CBP (ICBP)": "ICBP", "Sido Muncul (SIDO)": "SIDO",
    "🛰️ TELEKOMUNIKASI": "",
    "Telkom Indonesia (TLKM)": "TLKM", "Indosat (ISAT)": "ISAT",
    "🏗️ INFRASTRUKTUR & RETAIL": "",
    "Astra International (ASII)": "ASII", "Ace Hardware (ACES)": "ACES", "Matahari (LPPF)": "LPPF"
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2534/2534135.png", width=80)
    st.header("Gugem Trial Menu")
    
    pilihan_nama = st.selectbox("Pilih Emiten:", list(daftar_saham.keys()))
    kode_pilihan = daftar_saham[pilihan_nama]
    
    kode_manual = st.text_input("Atau Ketik Kode Lain:", "").upper()
    kode_final = kode_manual if kode_manual else kode_pilihan
    
    modal = st.number_input("Modal Simulasi (Rp)", min_value=100000, value=1000000, step=500000)
    
    btn_analisis = st.button("🔍 CEK SEKARANG", use_container_width=True)
    
    st.write("---")
    st.info("💡 **Gugem Pro** Coming Soon! (Fitur Prediksi AI, Laporan PDF, & Real-time Alert)")

# --- 5. LOGIKA UTAMA ---
if btn_analisis and kode_final != "":
    try:
        with st.spinner('Menarik data...'):
            ticker = kode_final + ".JK"
            saham = yf.Ticker(ticker)
            df = saham.history(period="1mo").reset_index()
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            
            info = saham.info
            harga_skrg = info.get("currentPrice", 0)
            nama_pt = info.get("shortName", "Emiten")
            pbv = info.get("priceToBook", 0)

            # Kalkulasi
            harga_per_lot = harga_skrg * 100
            jumlah_lot = int(modal // harga_per_lot) if harga_skrg > 0 else 0
            sisa = modal % harga_per_lot if harga_skrg > 0 else modal

            # GUIDANCE SECTION
            st.divider()
            if 0 < pbv < 2:
                st.success(f"### 💰 ESTIMASI: HARGA WAJAR")
            elif pbv >= 2:
                st.warning(f"### ⚠️ ESTIMASI: HARGA PREMIUM")

            # INFO UTAMA
            st.markdown(f"#### 🏢 {nama_pt} ({kode_final})")
            col1, col2, col3 = st.columns(3)
            col1.metric("Harga/Lembar", f"Rp {harga_skrg:,}")
            col2.metric("Slot Pembelian", f"{jumlah_lot} Lot")
            col3.metric("Saldo Tunai", f"Rp {sisa:,.0f}")

            # GRAFIK AREA
            st.write("---")
            fig = px.area(df, x='Date', y='Close', title=f"Trend Harga {kode_final}")
            fig.update_layout(xaxis_type='category')
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memproses data.")
else:
    st.info("Pilih emiten dan masukkan modal untuk mencoba simulasi Gugem.")

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center;'>GugemStockAnalyzer v1.0 (Trial)<br>By Gunawan</p>", unsafe_allow_html=True)