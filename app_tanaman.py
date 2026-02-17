import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURASI API ---
# Ganti "KODE_API_KAMU" dengan kunci yang kamu dapat dari Google AI Studio
API_KEY = "KODE_API_KAMU" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI Dokter Tanaman Online", layout="centered")
st.title("🌿 Dokter Tanaman AI (Online Mode)")
st.write("Foto tanamanmu, dan biarkan AI menganalisa penyakit serta solusinya secara real-time.")

# --- UPLOAD GAMBAR ---
uploaded_file = st.file_uploader("Upload foto daun yang sakit...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Foto Tanaman Kamu", use_container_width=True)
    
    with st.spinner('Sedang menganalisa dengan database online...'):
        try:
            # Menggunakan model Gemini Vision
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Perintah untuk AI (Prompt)
            prompt = """
            Kamu adalah pakar tanaman profesional. Lihat foto ini dan berikan:
            1. Nama penyakit tanaman tersebut.
            2. Gejala yang terlihat.
            3. Solusi pengobatan yang efektif dan aman.
            Jawab dalam Bahasa Indonesia yang mudah dimengerti petani.
            """
            
            # Kirim gambar ke AI
            response = model.generate_content([prompt, image])
            
            # Tampilkan Hasil
            st.success("### Hasil Analisa:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Waduh, ada kendala koneksi: {e}")

st.divider()
st.info("Aplikasi ini terhubung langsung dengan database AI Google secara online.")