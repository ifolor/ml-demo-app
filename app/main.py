import streamlit as st
import numpy as np
import cv2
from PIL import Image
from google.cloud import vision
from crop_utils import create_threshold_image, ignore_small_contours, crop_image
from features.gcp_crop_hints import *

st.set_page_config(layout="wide")
st.write('<style>div.block-container{padding-top:-20rem;}</style>', unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


st.title("👋 Hello")
st.subheader("Please select which feature you want to test.")

uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
if uploaded_file is not None:
    image_bytes = uploaded_file.read()
    image = Image.open(uploaded_file)
    vertices, confidence, importance_fraction = create_bounding_box(image_bytes, aspect_ratio=16/9)
    start_x, start_y, width, height = calculate_bounding_box_coords(vertices)
    cropped_image = create_cropped_image(image, start_x, start_y, width, height)
    rectangle_image = create_rectangle_image(image, start_x, start_y, width, height)


    col_1, col_2, col_3, col_4, col_5 = st.columns(np.ones(5)*0.2)
    with col_1:
     
 
        st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
        st.image(image, channels="BGR") 
        with col_4:
            st.markdown('<p style="text-align: center;">Crop hints</p>',unsafe_allow_html=True)
            st.image(rectangle_image, channels="RGB")      

        with col_5:
            st.markdown('<p style="text-align: center;">Cropped image</p>',unsafe_allow_html=True)
            st.image(cropped_image, channels="RGB") 



