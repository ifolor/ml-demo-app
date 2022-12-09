import streamlit as st
import numpy as np
import cv2
from  PIL import Image
from crop_utils import create_threshold_image, ignore_small_contours, crop_image
st.set_page_config(layout="wide")

st.write('<style>div.block-container{padding-top:-20rem;}</style>', unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)



def show_images():
    col_1, col_2 = st.columns([1, 1])
    with col_1:
        uploaded_files = st.file_uploader("", type=['jpg','png','jpeg'], accept_multiple_files=True)

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
        # Convert the file to an opencv image.
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            image_copy = image.copy()
            image_grey = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

        
            saliency_map, threshold_map = create_threshold_image(image_grey)
            threshold_map_exclude_small_contours = ignore_small_contours(threshold_map)
            rectangle_image, cropped_image = crop_image(image_copy, threshold_map_exclude_small_contours)

    
            col_1, col_2, col_3, col_4, col_5 = st.columns(np.ones(5)*0.2)
            with col_1:
                st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
                st.image(image, channels="BGR")  

            with col_2:
                st.markdown('<p style="text-align: center;">Saliency map</p>',unsafe_allow_html=True)
                st.image(saliency_map)  

            with col_3:
                st.markdown('<p style="text-align: center;">Threshold map</p>',unsafe_allow_html=True)
                st.image(threshold_map) 

            with col_4:
                st.markdown('<p style="text-align: center;">Crop hints</p>',unsafe_allow_html=True)
                st.image(rectangle_image, channels="BGR")      

            with col_5:
                st.markdown('<p style="text-align: center;">Cropped image</p>',unsafe_allow_html=True)
                st.image(cropped_image, channels="BGR") 
      



st.title("👋 Hello")
st.subheader("Please select which feature you want to test.")

features = ["Crop hints", "Dominant colors"]
page = st.radio("", features)


if page == "Crop hints":
    show_images()
elif page == "Dominant colors":
    col_1, col_2 = st.columns([1, 2])
    with col_1:
        number_of_colors = st.select_slider(
        'How many dominant colors do you want to extract from your image?',
    options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    





   


            #filter = st.sidebar.radio('Any desired aspect ratio (width-to-height)?', ['None','1:1','4:3', '4:5', '16:9'])
            #if filter == 'None':

