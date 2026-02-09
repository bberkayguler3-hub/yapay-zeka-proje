import google.generativeai as genai
import streamlit as st
import pandas as pd

# --- 1. GÜVENLİK VE YAPAY ZEKA AYARLARI ---
# Bu kısım 404 ve 400 hatalarını bitirmek için güncellendi.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # En stabil ve güncel model: gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ API Anahtarı eksik veya geçersiz! Lütfen Streamlit Secrets ayarlarını kontrol edin.")

# --- 2. SAYFA GENEL TASARIMI ---
st.set_page_config(page_title="Müteahhit ERP Pro", layout="wide", page_icon="🏗️")

# Yan Menü (Sidebar)
st.sidebar.title("🏗️ Şantiye Yönetim Merkezi")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Modül Seçin", ["📈 Finans & Dinamik Bütçe", "🏠 AI İlan Robotu", "📊 Malzeme & Maliyet Analizi"])

# --- 3. VERİ DEPOLAMA (Uygulama açık kaldığı sürece) ---
if 'harcamalar' not in st.session_state:
    st.session_state.harcamalar = []

# --- 4. MODÜL: FİNANS & DİNAMİK BÜTÇE ---
if menu == "📈 Finans & Dinamik Bütçe":
    st.title("💰 Dinamik Finansal Takip Sistemi")
    
    # Dinamik Bütçe Ayarı
    st.sidebar.subheader("⚙️ Proje Parametreleri")
    proje_adi = st.sidebar.text_input("Proje Adı", "Berkay Towers Projesi")
    toplam_butce = st.sidebar.number_input("Hedef Bütçe (TL)", min_value=1, value=20000000, step=1000000)

    # Verileri DataFrame'e dökme
    df = pd.DataFrame(st.session_state.harcamalar) if st.session_state.harcamalar else pd.DataFrame(columns=["Kalem", "Tutar"])
    toplam_harcanan = df["Tutar"].sum() if not df.empty else 0
    kalan_para = toplam_butce - toplam_harcanan
    harcama_yuzdesi = (toplam_harcanan / toplam_butce * 100)
    
    # Üst Gösterge Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Hedef Bütçe", f"{toplam_butce:,.0f} TL")
    c2.metric("Harcanan Toplam", f"{toplam_harcanan:,.0f} TL", delta=f"{harcama_yuzdesi:.1f}%")
    c3.metric("Kalan Nakit Akışı", f"{kalan_para:,.0f} TL")
    
    st.progress(min(harcama_yuzdesi / 100, 1.0))
    st.markdown("---")

    # Harcama Girişi
    st.subheader("📝 Yeni Harcama Kaydı")
    col1, col2, col3 = st.columns([2, 2, 1])
    gider_kalemi = col1.selectbox("Gider Grubu", ["Arsa", "Demir & Beton", "Hafriyat", "İşçilik", "Tesisat", "Resmi Harçlar", "Pazarlama"])
    gider_tutari = col2.number_input("Harcama Tutarı (TL)", min_value=0, step=1000)
    
    if col3.button("➕ Kaydet"):
        st.session_state.harcamalar.append({"Kalem": gider_kalemi, "Tutar": gider_tutari})
        st.rerun()

    # Görsel Analiz
    if not df.empty:
        col_sol, col_sag = st.columns([3, 2])
        with col_sol:
            st.subheader("📊 Harcama Dağılım Grafiği")
            st.bar_chart(df.groupby("Kalem")["Tutar"].sum())
        with col_sag:
            st.subheader("📋 Gider Listesi")
            st.dataframe(df, use_container_width=True)
            if st.button("🗑️ Tüm Verileri Sıfırla"):
                st.session_state.harcamalar = []
                st.rerun()

# --- 5. MODÜL: AI İLAN ROBOTU ---
elif menu == "🏠 AI İlan Robotu":
    st.title("🏠 Profesyonel Emlak Pazarlama")
    st.info("İnşa ettiğiniz projeyi satmak için AI destekli ilan metni hazırlar.")
    
    c1, c2 = st.columns(2)
    with c1:
        mevki = st.text_input("Konum", "Kadıköy / İstanbul")
        fiyat = st.text_input("Satış Fiyatı", "12.500.000 TL")
    with c2:
        ozellikler = st.text_area("Özellikler", "