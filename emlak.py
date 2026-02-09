import google.generativeai as genai
import streamlit as st
import pandas as pd

# --- 1. GÜVENLİK VE MODEL AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Hata almamak için tam yol belirledik: 'models/gemini-1.5-flash'
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Sistem Hatası: {e}")

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Berkay Müteahhitlik ERP", layout="wide", page_icon="🏗️")

st.sidebar.title("🏗️ Yönetim Paneli")
menu = st.sidebar.radio("Modül Seçin", ["📊 Finans & Bütçe", "🏠 AI İlan Robotu", "🔍 Malzeme Analizi"])

if 'harcamalar' not in st.session_state:
    st.session_state.harcamalar = []

# --- 3. MODÜL: FİNANS & BÜTÇE ---
if menu == "📊 Finans & Bütçe":
    st.title("💰 İnşaat Finans Takip Sistemi")
    
    st.sidebar.subheader("⚙️ Proje Ayarları")
    proje_adi = st.sidebar.text_input("Proje Adı", value="Berkay Towers")
    toplam_butce = st.sidebar.number_input("Toplam Hedef Bütçe (TL)", min_value=1, value=20000000, step=1000000)

    df = pd.DataFrame(st.session_state.harcamalar) if st.session_state.harcamalar else pd.DataFrame(columns=["Kalem", "Tutar"])
    toplam_harcanan = df["Tutar"].sum() if not df.empty else 0
    kalan_para = toplam_butce - toplam_harcanan
    harcama_yuzdesi = (toplam_harcanan / toplam_butce * 100) if toplam_butce > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Hedef Bütçe", f"{toplam_butce:,.0f} TL")
    c2.metric("Harcanan", f"{toplam_harcanan:,.0f} TL", delta=f"{harcama_yuzdesi:.1f}%")
    c3.metric("Kalan Limit", f"{kalan_para:,.0f} TL")

    st.progress(min(harcama_yuzdesi / 100, 1.0))

    st.subheader("➕ Yeni Gider Kaydı")
    col1, col2, col3 = st.columns([2, 2, 1])
    kalem = col1.selectbox("Gider Grubu", ["Arsa", "Beton & Demir", "Hafriyat", "İşçilik", "Tesisat", "Peyzaj", "Resmi Harçlar", "Diğer"])
    tutar = col2.number_input("Tutar (TL)", min_value=0, step=5000)
    
    if col3.button("Kaydet"):
        st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
        st.rerun()

    if not df.empty:
        st.bar_chart(df.groupby("Kalem")["Tutar"].sum())
        st.dataframe(df, use_container_width=True)

# --- 4. MODÜL: AI İLAN ROBOTU ---
elif menu == "🏠 AI İlan Robotu":
    st.title("🏠 AI Satış & Pazarlama")
    konum = st.text_input("Konum")
    detay = st.text_area("Özellikler", "Lüks mutfak, akıllı ev, otopark")
    
    if st.button("✨ İlan Oluştur"):
        if konum and detay:
            with st.spinner('AI yazıyor...'):
                res = model.generate_content(f"Müteahhit ağzıyla ilan yaz. Yer: {konum}, Özellikler: {detay}")
                st.write(res.text)

# --- 5. MODÜL: MALZEME ANALİZİ ---
elif menu == "🔍 Malzeme Analizi":
    st.title("🔍 Yapay Zeka Şantiye Şefi")
    soru = st.text_input("Soru sorun")
    
    if st.button("Analiz Et"):
        if soru:
            with st.spinner('Analiz ediliyor...'):
                # Buradaki model.generate_content artık models/gemini-1.5-flash üzerinden hatasız çalışacak
                res = model.generate_content(f"İnşaat uzmanı olarak yanıtla: {soru}")
                st.info(res.text)
