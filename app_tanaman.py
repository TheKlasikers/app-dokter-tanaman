import streamlit as st
import requests
import base64
from PIL import Image
import io

KUNCI_API = "AIzaSyDxQCr8yQvuxpRBhDUNbzY8sxBb2XH98EA"
URL_API = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={KUNCI_API}"

st.set_page_config(page_title="Dokter Tanaman AI", layout="centered")
st.title("🌿 Dokter Tanaman AI (Final Fix)")

st.write("---")
klik_analisa = st.button("2. KLIK INI UNTUK ANALISA")
st.write("---")

file_gambar = st.file_uploader("Upload foto daun...", type=["jpg", "png", "jpeg"])
if file_gambar:
    img = Image.open(file_gambar)
    st.image(img, caption="Foto Berhasil Diupload", use_container_width=True)
elif klik_analisa and not file_gambar:
    st.warning("Waduh Bro, fotonya di-upload dulu baru klik tombolnya!")
   
st.divider()
st.caption("Versi 6.1 - Anti 404 & Anti Ghosting")
