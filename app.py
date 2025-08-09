# app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io

st.set_page_config(page_title="Advanced Cartoonify", page_icon="🎨", layout="wide")

st.title("🎨 Advanced Cartoonify App")
st.write("Upload an image or use your camera — choose a style, tweak sliders, preview and download.")

# -----------------------
# Utility image helpers
# -----------------------
def to_cv2(img_pil):
    arr = np.array(img_pil)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

def to_pil(cv2_img):
    rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def read_image_from_streamlit(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    return image

def save_image_bytes(pil_img, fmt="PNG"):
    buf = io.BytesIO()
    pil_img.save(buf, format=fmt)
    return buf.getvalue()

# -----------------------
# Filter functions
# -----------------------
def adjust_brightness_contrast(pil_img, brightness=1.0, contrast=1.0):
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(brightness)
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(contrast)
    return pil_img

def pencil_sketch_cv(cv_img, ksize=7):
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (ksize, ksize), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    sketch_color = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    return sketch_color

def oil_painting_effect(cv_img, diameter=7, sigma_space=75, sigma_color=75):
    tmp = cv_img.copy()
    for _ in range(2):
        tmp = cv2.bilateralFilter(tmp, diameter, sigma_color, sigma_space)
    try:
        stylized = cv2.stylization(tmp, sigma_s=60, sigma_r=0.6)
    except Exception:
        stylized = tmp
    return stylized

def sepia_cv(cv_img):
    img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB).astype(np.float32)
    tr = img[:,:,0]*0.393 + img[:,:,1]*0.769 + img[:,:,2]*0.189
    tg = img[:,:,0]*0.349 + img[:,:,1]*0.686 + img[:,:,2]*0.168
    tb = img[:,:,0]*0.272 + img[:,:,1]*0.534 + img[:,:,2]*0.131
    sep = np.stack([tr, tg, tb], axis=2)
    sep = np.clip(sep, 0, 255).astype(np.uint8)
    return cv2.cvtColor(sep, cv2.COLOR_RGB2BGR)

def cartoonify_cv(cv_img, num_down=2, num_bilateral=7, edge_block_size=9, edge_C=2):
    img = cv_img.copy()
    for _ in range(num_down):
        img = cv2.pyrDown(img)
    for _ in range(num_bilateral):
        img = cv2.bilateralFilter(img, d=9, sigmaColor=9, sigmaSpace=7)
    for _ in range(num_down):
        img = cv2.pyrUp(img)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, edge_block_size, edge_C)
    edges_col = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    edges_col = cv2.resize(edges_col, (img.shape[1], img.shape[0]))  # FIX: match sizes
    cartoon = cv2.bitwise_and(img, edges_col)
    return cartoon

# -----------------------
# Sidebar controls
# -----------------------
st.sidebar.header("Input options")
mode = st.sidebar.radio("Source", ("Upload Image", "Use Camera"))

st.sidebar.header("Effects & Style")
style = st.sidebar.selectbox("Choose Style",
                             ("Cartoon (default)", "Pencil Sketch", "Oil Painting", "Sepia", "Grayscale"))

st.sidebar.subheader("Cartoon Parameters")
num_down = st.sidebar.slider("Downsampling steps", 0, 3, 2)
num_bilateral = st.sidebar.slider("Bilateral filter passes", 1, 10, 7)
edge_block = st.sidebar.slider("Edge block size (odd)", 3, 15, 9, step=2)
edge_C = st.sidebar.slider("Edge sensitivity (C)", 1, 10, 2)

st.sidebar.subheader("Adjustments")
brightness = st.sidebar.slider("Brightness", 0.5, 1.5, 1.0, 0.05)
contrast = st.sidebar.slider("Contrast", 0.5, 1.5, 1.0, 0.05)

# -----------------------
# Main UI
# -----------------------
col1, col2 = st.columns([1,1])

input_image = None
if mode == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])
    if uploaded_file is not None:
        input_image = read_image_from_streamlit(uploaded_file)
else:
    camera_file = st.camera_input("Take a photo with your camera")
    if camera_file is not None:
        input_image = read_image_from_streamlit(camera_file)

if input_image is None:
    st.info("Please upload an image or take a photo with the camera.")
    st.stop()

adjusted = adjust_brightness_contrast(input_image, brightness=brightness, contrast=contrast)
cv_img = to_cv2(adjusted)

if style == "Cartoon (default)":
    result_cv = cartoonify_cv(cv_img, num_down=num_down, num_bilateral=num_bilateral,
                              edge_block_size=edge_block, edge_C=edge_C)
elif style == "Pencil Sketch":
    result_cv = pencil_sketch_cv(cv_img, ksize=7)
elif style == "Oil Painting":
    result_cv = oil_painting_effect(cv_img, diameter=9, sigma_space=75, sigma_color=75)
elif style == "Sepia":
    result_cv = sepia_cv(cv_img)
elif style == "Grayscale":
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    result_cv = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
else:
    result_cv = cartoonify_cv(cv_img, num_down=num_down, num_bilateral=num_bilateral,
                              edge_block_size=edge_block, edge_C=edge_C)

result_pil = to_pil(result_cv)
orig_pil = input_image

with col1:
    st.subheader("Original")
    st.image(orig_pil, use_column_width=True)
with col2:
    st.subheader(f"Result — {style}")
    st.image(result_pil, use_column_width=True)

buf = io.BytesIO()
result_pil.save(buf, format="PNG")
byte_im = buf.getvalue()

st.download_button("💾 Download Result", data=byte_im, file_name="cartoonified.png", mime="image/png")

st.markdown("---")
st.write("**Tips:** Try changing 'Bilateral filter passes' (smoothing) and 'Edge sensitivity (C)' to get thicker or thinner outlines.")
