import google.generativeai as genai
import streamlit as st

# --- 1. YAPAY ZEKA VE API AYARLARI ---
# Senin verdiğin anahtarı buraya hatasız yerleştirdim
API_KEY = st.secrets["GEMINI_API_KEY"]

try:
    genai.configure(api_key=API_KEY)
    # 404 hatasını bitirmek için mevcut ve güncel bir model seçtik
    # 429 hatasını (kota) aşmak için farklı bir model deniyoruz
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error(f"Başlatma Hatası: {e}")

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Emlak AI -  İlan Sihirbazı", layout="wide", page_icon="🏠")

st.title("🏠 Emlak AI - Profesyonel İlan Robotu")
st.write("Verileri girin ve yapay zekanın ilanınızı yazmasını izleyin.")

# --- 3. GİRİŞ ALANLARI (Sol Panel) ---
with st.sidebar:
    st.header("🏢 Gayrimenkul Bilgileri")
    mevki = st.text_input("Konum / Semt", placeholder="Örn: Kadıköy, İstanbul")
    oda_sayisi = st.selectbox("Oda Sayısı", ["1+0", "1+1", "2+1", "3+1", "4+1", "Villa"])
    metrekare = st.number_input("Metrekare (m²)", min_value=10, value=100)
    bina_yasi = st.slider("Bina Yaşı", 0, 50, 5)
    fiyat = st.text_input("Fiyat (TL)", placeholder="Örn: 8.500.000")
    
    st.divider()
    st.info("Berkay için Antigravity hızında hazırlandı.")

# --- 4. ANA EKRAN (Detaylar ve Sonuç) ---
st.subheader("📝 Evin Öne Çıkan Özellikleri")
ekstra = st.text_area("Detaylar", placeholder="Deniz manzaralı, geniş balkonlu, site içerisinde, otoparklı...", height=150)

if st.button("✨ Profesyonel İlan Oluştur"):
    if mevki and ekstra:
        with st.spinner('🤖 Yapay zeka ilan metnini dokuyor...'):
            # Profesyonel Emlakçı Komutu (Prompt)
            prompt = f"""
            Bir profesyonel gayrimenkul danışmanı gibi davran. 
            Aşağıdaki bilgilere sahip taşınmaz için dikkat çekici, satış odaklı bir ilan yaz:
            
            Konum: {mevki}
            Oda Sayısı: {oda_sayisi}
            Metrekare: {metrekare} m2
            Bina Yaşı: {bina_yasi}
            Fiyat: {fiyat} TL
            Özellikler: {ekstra}
            
            İlanın içinde etkileyici bir başlık olsun, emojiler kullan ve özelliklerini madde madde belirt.
            """
            
            try:
                # Yapay zekadan yanıt alıyoruz
                response = model.generate_content(prompt)
                st.success("✅ İlanınız Başarıyla Hazırlandı!")
                st.divider()
                st.markdown(response.text) # AI yanıtı buraya yazılır
            except Exception as e:
                st.error(f"Hata detayı: {e}")
                st.warning("⚠️ ÖNEMLİ: Eğer hala 404 veya 400 hatası alıyorsan, lütfen Opera VPN'i kapatıp sayfayı yenile.")
    else:
        st.warning("Lütfen Konum ve Detaylar kısımlarını doldurun.")