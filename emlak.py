import google.generativeai as genai
import streamlit as st
import pandas as pd

# --- 1. GÜVENLİK AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("⚠️ API Anahtarı eksik! Lütfen Secrets ayarlarına GEMINI_API_KEY ekleyin.")

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Müteahhit ERP Sistemi", layout="wide", page_icon="🏗️")

st.sidebar.title("🏗️ Şantiye Yönetimi")
menu = st.sidebar.radio("Menü", ["Finans & Bütçe", "AI İlan Yazarı", "Malzeme Analizi"])

# --- 3. VERİ SAKLAMA (Session State) ---
if 'harcamalar' not in st.session_state:
    st.session_state.harcamalar = []

# --- 4. FİNANS & BÜTÇE MODÜLÜ ---
if menu == "Finans & Bütçe":
    st.title("🏗️ Dinamik İnşaat Finans Yönetimi")
    
    # BÜTÇE AYARI - Burayı istediğin gibi değiştirebilirsin
    st.sidebar.subheader("⚙️ Proje Ayarları")
    toplam_butce = st.sidebar.number_input("Toplam Proje Bütçesi (TL)", min_value=0, value=20000000, step=1000000)
    proje_adi = st.sidebar.text_input("Proje Adı", value="Lüks Konut Projesi")

    st.subheader(f"📊 {proje_adi} - Finansal Özet")
    
    # Hesaplamalar
    df = pd.DataFrame(st.session_state.harcamalar) if st.session_state.harcamalar else pd.DataFrame(columns=["Kalem", "Tutar", "Tarih"])
    toplam_harcanan = df["Tutar"].sum() if not df.empty else 0
    kalan_para = toplam_butce - toplam_harcanan
    
    # Yüzde hesaplama (Sıfıra bölünme hatası engellendi)
    harcama_yuzdesi = (toplam_harcanan / toplam_butce * 100) if toplam_butce > 0 else 0

    # Üst Bilgi Kartları
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Hedef Bütçe", f"{toplam_butce:,.0f} TL")
    c2.metric("Toplam Harcanan", f"{toplam_harcanan:,.0f} TL", delta=f"{harcama_yuzdesi:.1f}%")
    c3.metric("Kalan Nakit", f"{kalan_para:,.0f} TL", delta_color="normal")

    st.progress(min(harcama_yuzdesi / 100, 1.0))

    st.markdown("---")

    # Giriş Alanı
    st.subheader("➕ Yeni Gider Kaydı")
    with st.container():
        col1, col2, col3 = st.columns([2, 2, 1])
        kalem = col1.selectbox("Gider Kategorisi", ["Arsa/Arazi", "Hafriyat", "Beton & Demir", "İşçilik", "Tesisat", "Peyzaj", "Resmi Harçlar", "Diğer"])
        tutar = col2.number_input("Tutar (TL)", min_value=0, step=1000)
        
        if col3.button("Sisteme İşle"):
            st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
            st.rerun()

    # Veri Görselleştirme
    if not df.empty:
        col_sol, col_sag = st.columns([3, 2])
        with col_sol:
            st.subheader("📉 Harcama Grafiği")
            st.bar_chart(df.groupby("Kalem")["Tutar"].sum())
        with col_sag:
            st.subheader("📋 Gider Detayları")
            st.dataframe(df, use_container_width=True)
            if st.button("Listeyi Temizle"):
                st.session_state.harcamalar = []
                st.rerun()

# --- 5. AI İLAN YAZARI (ÖNCEKİ KODUN ENTEGRE HALİ) ---
elif menu == "AI İlan Yazarı":
    st.title("🏠 AI Emlak Pazarlama Robotu")
    mevki = st.text_input("Konum", placeholder="Örn: Kadıköy")
    ozellik = st.text_area("Öne Çıkan Özellikler", "Akıllı ev sistemi, geniş teras...")
    
    if st.button("✨ Profesyonel İlan Hazırla"):
        if mevki and ozellik:
            with st.spinner('AI metni hazırlıyor...'):
                res = model.generate_content(f"Müteahhit ağzıyla bir ilan yaz. Yer: {mevki}, Özellikler: {ozellik}")
                st.markdown(res.text)

# --- 6. MALZEME ANALİZİ ---
elif menu == "Malzeme Analizi":
    st.title("📉 Maliyet ve Malzeme Analisti")
    st.write("Müteahhit asistanına piyasa hakkında soru sor.")
    soru = st.text_input("Soru", placeholder="Örn: 100 dairelik proje için ortalama kaç ton demir gider?")
    if st.button("AI'ya Danış"):
        with st.spinner("Hesaplanıyor..."):
            res = model.generate_content(f"Bir inşaat mühendisi gibi cevap ver: {soru}")
            st.info(res.text)