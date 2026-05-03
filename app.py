import streamlit as st
from utils import *
from PIL import Image
import io


st.set_page_config(page_title="Batch Image Cropper", layout="wide")


def compress_image(file, quality=70, max_size=(1920, 1920)):
    img = Image.open(file)
    img.thumbnail(max_size)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    return buffer

with st.sidebar:
    st.header("Upload Panels Here")
    uploaded_files = st.file_uploader(
        "Choose images...", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
  
if uploaded_files:
    if "cropped_images" not in st.session_state:
        st.session_state.cropped_images = {}
    
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state.cropped_images:
            imagefile = compress_image(uploaded_file)
            
            cropped_result = process(imagefile)
            
            st.session_state.cropped_images[uploaded_file.name] = {
                "original": uploaded_file,
                "cropped": cropped_result
            }

        data = st.session_state.cropped_images[uploaded_file.name]
        
        with st.expander(f"Results: {uploaded_file.name}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.caption("Original")
                st.image(data["original"])
            
            with col2:
                st.caption("Cropped & Rotated")
                if data["cropped"] is not None:
                    st.image(data["cropped"], channels="BGR", width=450)
                    
else:
    st.warning("Please upload images in the sidebar to begin.")

