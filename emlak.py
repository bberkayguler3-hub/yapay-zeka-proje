import google.generativeai as genai
import streamlit as st
import pandas as pd

# --- 1. MODEL AYARI (HATA ALMAYAN VERSİYON) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # 404 hatasını önlemek için en stabil model ismi:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"⚠️ Kurulum Hatası: {e}")

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Berkay Müteahhitlik ERP", layout="wide", page_icon="🏗️")

st.sidebar.title("🏗️ Yönetim Paneli")
menu = st.sidebar.radio("Modül Seçin", ["📊 Finans & Bütçe", "🏠 AI İlan Robotu", "🔍 Malzeme Analizi"])

if 'harcamalar' not in st.session_state:
    st.session_state.harcamalar = []

# --- 3. MODÜL: FİNANS & BÜTÇE ---
if menu == "📊 Finans & Bütçe":
    st.title("💰 İnşaat Finans Takip Sistemi")
    toplam_butce = st.sidebar.number_input("Hedef Bütçe (TL)", min_value=1, value=20000000)
    
    df = pd.DataFrame(st.session_state.harcamalar) if st.session_state.harcamalar else pd.DataFrame(columns=["Kalem", "Tutar"])
    toplam_harcanan = df["Tutar"].sum() if not df.empty else 0
    kalan_para = toplam_butce - toplam_harcanan

    c1, c2, c3 = st.columns(3)
    c1.metric("Hedef Bütçe", f"{toplam_butce:,.0f} TL")
    c2.metric("Harcanan", f"{toplam_harcanan:,.0f} TL")
    c3.metric("Kalan", f"{kalan_para:,.0f} TL")

    st.subheader("➕ Yeni Gider Kaydı")
    col1, col2, col3 = st.columns([2, 2, 1])
    kalem = col1.selectbox("Gider", ["Arsa", "Demir-Beton", "İşçilik", "Diğer"])
    tutar = col2.number_input("Tutar (TL)", min_value=0)
    
    if col3.button("Kaydet"):
        st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
        st.rerun()

    if not df.empty:
        st.bar_chart(df.groupby("Kalem")["Tutar"].sum())

# --- 4. MODÜL: AI İLAN ROBOTU ---
elif menu == "🏠 AI İlan Robotu":
    st.title("🏠 AI İlan Hazırlayıcı")
    konum = st.text_input("Konum")
    ozellik = st.text_area("Özellikler")
    
    if st.button("✨ Oluştur"):
        if konum and ozellik:
            with st.spinner('AI Yanıtlıyor...'):
                try:
                    # 'models/' takısı eklemeden, doğrudan ismiyle çağırıyoruz
                    res = model.generate_content(f"Müteahhit ağzıyla ilan yaz. Yer: {konum}, Özellikler: {ozellik}")
                    st.write(res.text)
                except Exception as e:
                    st.error(f"Yapay zeka hatası: {e}")

# --- 5. MODÜL: MALZEME ANALİZİ ---
elif menu == "🔍 Malzeme Analizi":
    st.title("🔍 Yapay Zeka Şantiye Şefi")
    soru = st.text_input("Soru sorun")
    
    if st.button("Analiz Et"):
        if soru:
            with st.spinner('Analiz ediliyor...'):
                try:
                    res = model.generate_content(f"İnşaat uzmanı olarak yanıtla: {soru}")
                    st.info(res.text)
                except Exception as e:
                    st.error(f"Analiz başarısız: {e}")
