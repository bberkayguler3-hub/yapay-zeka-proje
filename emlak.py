import google.generativeai as genai
import streamlit as st
import pandas as pd

# --- 1. GÜVENLİK VE MODEL AYARI ---
try:
    # Streamlit Cloud "Secrets" panelinde GEMINI_API_KEY tanımlı olmalı
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # En stabil ve hızlı model sürümü
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ API Anahtarı Bulunamadı! Lütfen Streamlit Secrets ayarlarını yapın.")

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Berkay Müteahhitlik ERP", layout="wide", page_icon="🏗️")

# Yan Menü (Sidebar)
st.sidebar.title("🏗️ Yönetim Paneli")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Modül Seçin", ["📊 Finans & Bütçe", "🏠 AI İlan Robotu", "🔍 Malzeme Analizi"])

# --- 3. VERİ SAKLAMA ---
if 'harcamalar' not in st.session_state:
    st.session_state.harcamalar = []

# --- 4. MODÜL: FİNANS & BÜTÇE ---
if menu == "📊 Finans & Bütçe":
    st.title("💰 İnşaat Finans Takip Sistemi")
    
    # Dinamik Bütçe Girişi
    st.sidebar.subheader("⚙️ Proje Ayarları")
    proje_adi = st.sidebar.text_input("Proje Adı", value="Emlak Projesi v1")
    toplam_butce = st.sidebar.number_input("Toplam Hedef Bütçe (TL)", min_value=1, value=20000000, step=1000000)

    st.subheader(f"🏗️ {proje_adi} Finansal Durum")
    
    # Hesaplamalar
    df = pd.DataFrame(st.session_state.harcamalar) if st.session_state.harcamalar else pd.DataFrame(columns=["Kalem", "Tutar"])
    toplam_harcanan = df["Tutar"].sum() if not df.empty else 0
    kalan_para = toplam_butce - toplam_harcanan
    harcama_yuzdesi = (toplam_harcanan / toplam_butce * 100)

    # Özet Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("Hedef Bütçe", f"{toplam_butce:,.0f} TL")
    c2.metric("Harcanan", f"{toplam_harcanan:,.0f} TL", delta=f"{harcama_yuzdesi:.1f}%")
    c3.metric("Kalan Limit", f"{kalan_para:,.0f} TL")

    st.progress(min(harcama_yuzdesi / 100, 1.0))
    st.markdown("---")

    # Masraf Girişi
    st.subheader("➕ Yeni Gider Kaydı")
    col1, col2, col3 = st.columns([2, 2, 1])
    kalem = col1.selectbox("Gider Grubu", ["Arsa", "Beton & Demir", "Hafriyat", "İşçilik", "Tesisat", "Resmi Harçlar", "Pazarlama"])
    tutar = col2.number_input("Tutar (TL)", min_value=0, step=5000)
    
    if col3.button("Sisteme Kaydet"):
        st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
        st.success("Harcama eklendi!")
        st.rerun()

    # Analiz Grafikleri
    if not df.empty:
        g1, g2 = st.columns([3, 2])
        with g1:
            st.subheader("📊 Harcama Dağılımı")
            st.bar_chart(df.groupby("Kalem")["Tutar"].sum())
        with g2:
            st.subheader("📋 Son İşlemler")
            st.dataframe(df, use_container_width=True)
            if st.button("🗑️ Verileri Sıfırla"):
                st.session_state.harcamalar = []
                st.rerun()

# --- 5. MODÜL: AI İLAN ROBOTU ---
elif menu == "🏠 AI İlan Robotu":
    st.title("🏠 AI Satış & Pazarlama")
    st.info("İnşaatını yaptığınız mülkler için yapay zeka ile profesyonel ilanlar yazın.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        konum = st.text_input("Konum", placeholder="Örn: Kadıköy Sahil")
        fiyat = st.text_input("Fiyat", placeholder="10.000.000 TL")
    with col_b:
        # Tırnak hatası (SyntaxError) burada giderildi
        detay = st.text_area("Öne Çıkan Özellikler", "Deprem yönetmeliğine uygun, lüks lobi, geniş balkon, akıllı ev sistemi")
        
    if st.button("✨ İlan Oluştur"):
        if konum and detay:
            with st.spinner('AI metni hazırlıyor...'):
                prompt = f"Bir müteahhit gibi profesyonel, emojili ilan yaz. Konum: {konum}, Fiyat: {fiyat}, Özellikler: {detay}"
                res = model.generate_content(prompt)
                st.markdown("---")
                st.success("İlan Metni Hazır:")
                st.write(res.text)
        else:
            st.warning("Lütfen konum ve özellik kısımlarını doldurun.")

# --- 6. MODÜL: MALZEME ANALİZİ ---
elif menu == "🔍 Malzeme Analizi":
    st.title("🔍 Yapay Zeka Şantiye Şefi")
    st.write("Maliyetler veya teknik sorular için AI'ya danışın.")
    soru = st.text_input("Soru sorun", placeholder="Örn: 500 metrekare inşaat için kaç ton demir gerekir?")
    
    if st.button("Analiz Et"):
        with st.spinner("Analiz ediliyor..."):
            res = model.generate_content(f"Bir inşaat mühendisi gibi detaylı cevap ver: {soru}")
            st.info(res.text)
