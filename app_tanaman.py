import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURASI API ---
# Ganti "KODE_API_KAMU" dengan kunci yang kamu dapat dari Google AI Studio
API_KEY = "AIzaSyDxQCr8yQvuxpRBhDUNbzY8sxBb2XH98EA"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI Dokter Tanaman", layout="centered")
st.title("🌿 Dokter Tanaman AI (Online)")
st.write("Gunakan Kamera atau Upload foto untuk diagnosa penyakit tanaman.")

# --- UPLOAD GAMBAR ---
tab1, tab2 = st.tabs(["📸 Ambil Foto (Kamera)", "📁 Upload File (Galeri)"])

image = None

with tab1:
     cam_file = st.camera_input("Klik tombol di bawah untuk ambil foto daun")
     if cam_file:
        image = Image.open(cam_file)

with tab2:
     uploaded_file = st.file_uploader("Pilih foto dari galeri HP...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)

if image is not None:
    st.image(image, caption="Foto yang akan dianalisa", use_container_width=True)

    st.divider()
    st.caption("Aplikasi Dokter Tanaman v2.2 - Powered by Google Gemini AI")
    
    with st.spinner('Sedang menganalisa dengan database online...'):
         try:
            # Menggunakan model Gemini Vision
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            
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

