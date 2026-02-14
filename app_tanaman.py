import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import os
import tensorflow as tf

# --- 1. SETTING HALAMAN ---
st.set_page_config(page_title="AI Dokter Tanaman", page_icon="🌿")

# --- 2. JUDUL ---
st.title("🌿 AI Dokter Tanaman")

# --- 3. MENU LIST DROP ---
st.write("---")
jenis = st.selectbox(
    "Pilih Jenis Tanaman:",
    ["Padi", "Jagung", "Cabai", "Tomat", "Kedelai"]
)

# --- 4. DUA OPSI DENGAN LOGIKA PINTAR ---
st.write(f"### Masukkan Foto Daun {jenis}:")
tab1, tab2 = st.tabs(["📸 Gunakan Kamera", "📁 Pilih dari Galeri"])

with tab1:
    foto_kamera = st.camera_input("Ambil foto sekarang")

with tab2:
    foto_file = st.file_uploader("Klik untuk cari foto di HP/Laptop", type=["jpg", "png", "jpeg"])

# --- PERBAIKAN DI SINI: Logika Prioritas ---
foto_final = None

# Jika ada foto dari kamera, pakai itu. Jika tidak, cek apakah ada dari galeri.
if foto_kamera is not None:
    foto_final = foto_kamera
elif foto_file is not None:
    foto_final = foto_file

# --- 5. FUNGSI PREDIKSI AI ---
def predict_tflite(img_data):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_model = os.path.join(base_dir, "model_unquant.tflite")
    path_label = os.path.join(base_dir, "labels.txt")

    interpreter = tf.lite.Interpreter(model_path=path_model)
    interpreter.allocate_tensors()
    
    image = img_data.convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    img_array = np.asarray(image).astype(np.float32)
    normalized = (img_array / 127.5) - 1
    data = np.expand_dims(normalized, axis=0)

    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], data)
    interpreter.invoke()
    prediction = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    
    with open(path_label, "r") as f:
        class_names = [line.strip() for line in f.readlines()]
    
    index = np.argmax(prediction[0])
    return class_names[index], prediction[0][index]

# --- 6. LOGIKA TAMPILAN (DIPERBAIKI) ---
if foto_final is not None:
    st.write("---")
    # Tampilkan gambar yang dipilih/difoto
    img = Image.open(foto_final)
    st.image(img, caption="Foto Siap Dianalisa", use_container_width=True)
    
    if st.button(f"🔍 ANALISA {jenis.upper()}", use_container_width=True):
        with st.spinner('Menganalisa...'):
            hasil, skor = predict_tflite(img)
            label_final = hasil.split(' ', 1)[-1] if ' ' in hasil else hasil
            
            st.success(f"### Hasil: {label_final}")
            st.info(f"Keyakinan AI: {np.round(skor*100, 2)}%")
            
    if st.button("🔄 RESET / FOTO ULANG", use_container_width=True):
        st.rerun()

st.write("---")
st.caption("AI Dokter Tanaman V1.7 - Fix Display")