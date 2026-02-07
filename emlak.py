import google.generativeai as genai
import streamlit as st
import pandas as pd

# --- 1. GÜVENLİK VE AYARLAR ---
try:
    # Streamlit Cloud'da "Secrets" kısmına GEMINI_API_KEY olarak eklemelisin
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("⚠️ API Anahtarı eksik! Secrets ayarlarını yapana kadar AI çalışmayacaktır.")

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Berkay Emlak & İnşaat Pro", layout="wide")

# Menü Seçenekleri
menu = ["🏠 İlan Oluşturucu (AI)", "🏗️ İnşaat Bütçe Takibi (20M)"]
choice = st.sidebar.selectbox("Modül Seçin", menu)

# --- 3. MODÜL 1: AI İLAN OLUŞTURUCU ---
if choice == "🏠 İlan Oluşturucu (AI)":
    st.title("🏠 Profesyonel İlan Robotu")
    st.info("Emlakçı diliyle etkileyici ilanlar hazırlar.")
    
    col1, col2 = st.columns(2)
    with col1:
        mevki = st.text_input("Konum", placeholder="Örn: Beşiktaş")
        oda = st.selectbox("Oda", ["1+1", "2+1", "3+1", "Villa"])
        fiyat = st.text_input("Satış Fiyatı (TL)")
    with col2:
        ozellikler = st.text_area("Öne Çıkanlar", "Lüks mutfak, yerden ısıtma, akıllı ev...")

    if st.button("✨ İlanı Yazdır"):
        if mevki and ozellikler:
            with st.spinner('Yapay zeka metni dokuyor...'):
                prompt = f"Şu ev için profesyonel ilan yaz: Konum:{mevki}, Oda:{oda}, Fiyat:{fiyat}, Özellikler:{ozellikler}"
                response = model.generate_content(prompt)
                st.success("İlan Hazır!")
                st.write(response.text)
        else:
            st.warning("Lütfen bilgileri eksiksiz girin.")

# --- 4. MODÜL 2: İNŞAAT BÜTÇE TAKİBİ ---
elif choice == "🏗️ İnşaat Bütçe Takibi (20)":
    st.title("🏗️ 20 Milyon TL İnşaat Yönetimi")
    st.markdown("---")
    
    # Sabit Bütçe
    toplam_butce = 20000000
    
    st.subheader("💰 Harcama Girişi")
    c1, c2, c3 = st.columns(3)
    kalem = c1.selectbox("Masraf Kalemi", ["Arsa", "Kaba İnşaat (Demir-Beton)", "İnce İşler", "Ruhsat/Resmi", "Diğer"])
    tutar = c2.number_input("Tutar (TL)", min_value=0, step=10000)
    
    # Basit bir session state ile verileri tutalım (Site açık kaldığı sürece)
    if 'harcamalar' not in st.session_state:
        st.session_state.harcamalar = []

    if c3.button("➕ Harcamayı Ekle"):
        st.session_state.harcamalar.append({"Kalem": kalem, "Tutar": tutar})
        st.toast("Harcama kaydedildi!")

    # Tablo ve Hesaplama
    if st.session_state.harcamalar:
        df = pd.DataFrame(st.session_state.harcamalar)
        toplam_harcanan = df["Tutar"].sum()
        kalan_para = toplam_butce - toplam_harcanan
        
        # Göstergeler
        m1, m2, m3 = st.columns(3)
        m1.metric("Toplam Bütçe", f"{toplam_butce:,.0f} TL")
        m2.metric("Harcanan", f"{toplam_harcanan:,.0f} TL", delta=f"-{toplam_harcanan:,.0f}", delta_color="inverse")
        m3.metric("Kalan Limit", f"{kalan_para:,.0f} TL")
        
        st.progress(min(toplam_harcanan / toplam_butce, 1.0))
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Henüz harcama girilmedi. Bütçen pırıl pırıl 20 milyon TL!")