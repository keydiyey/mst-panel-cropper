import streamlit as st
from utils import *
import pathlib
import io

st.set_page_config(page_title="Batch Image Cropper", layout="wide")

st.title("✂️ Multi-Image Cropper")
st.write("Upload your images.")


with st.sidebar:
    st.header("Upload Zone")
    uploaded_files = st.file_uploader(
        "Choose images...", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
if uploaded_files:
    file_names = [f.name for f in uploaded_files]

    current_file = next(f for f in uploaded_files)
   
    if "cropped_images" not in st.session_state:
        st.session_state.cropped_images = {}

    original_image = st.image(current_file) 


    current_file.seek(0)
    cropped_image = process(current_file)
    st.image(cropped_image, use_container_width=True)
        
        
         
    st.session_state.cropped_images[current_file] = {
        "original": original_image,
        "cropped": cropped_image
    }

    st.success(f"Saved {current_file}!")
   
    if st.session_state.cropped_images:
        st.divider()
        st.header("📊 Before & After Gallery")
        
        for name, data in st.session_state.cropped_images.items():
            with st.expander(f"Results for {name}", expanded=True):
                gc1, gc2 = st.columns(2)
                with gc1:
                    st.caption("Original")
                    st.image(data["original"], use_container_width=True)
                with gc2:
                    st.caption("Cropped")
                    st.image(data["cropped"], use_container_width=True)

else:
    st.warning("Please upload images in the sidebar to begin.")

