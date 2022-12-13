import streamlit as st
import numpy as np
import cv2
import os
from google.cloud import vision
from crop_utils import create_threshold_image, ignore_small_contours, crop_image
st.set_page_config(layout="wide")
st.write('<style>div.block-container{padding-top:-20rem;}</style>', unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "369410-4d30b4b7a194.json"
client = vision.ImageAnnotatorClient()


def calculate_crop_hints():
    uploaded_files = st.file_uploader("", type=['jpg','png','jpeg'], accept_multiple_files=True, key="3")
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:

            image_bytes = uploaded_file.read()
            image_g = vision.Image(content=image_bytes)
            response = client.crop_hints(image=image_g)
            hints = response.crop_hints_annotation.crop_hints
            print(hints)


def show_images():
    col_1, col_2 = st.columns([1, 1])
    with col_1:
        uploaded_files = st.file_uploader("", type=['jpg','png','jpeg'], accept_multiple_files=True, key="4")

    if uploaded_files is not None:
        for uploaded_file in uploaded_files:

            # Convert the file to an opencv image.
            #print(uploaded_file.read())
            #print(type(uploaded_file.read())) # byte

            #image_bytes = uploaded_file.read()
            #image_g = vision.Image(content=image_bytes)
            #response = client.crop_hints(image=image_g)
            #hints = response.crop_hints_annotation.crop_hints
            #print(hints)

            # Read bytes as color and greyscale images
            image_array = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image_color = cv2.imdecode(image_array , cv2.IMREAD_COLOR)
            image_color_copy = image_color.copy()
            image_grey = cv2.imdecode(image_array , cv2.IMREAD_GRAYSCALE)

    
            saliency_map, threshold_map = create_threshold_image(image_grey)
            threshold_map_exclude_small_contours = ignore_small_contours(threshold_map)
            rectangle_image, cropped_image = crop_image(image_color_copy, threshold_map_exclude_small_contours)

    
            col_1, col_2, col_3, col_4, col_5 = st.columns(np.ones(5)*0.2)
            with col_1:
                st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
                st.image(image_color, channels="BGR")  

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
    calculate_crop_hints()
elif page == "Dominant colors":
    col_1, col_2 = st.columns([1, 2])
    with col_1:
        number_of_colors = st.select_slider(
        'How many dominant colors do you want to extract from your image?',
    options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    





   


            #filter = st.sidebar.radio('Any desired aspect ratio (width-to-height)?', ['None','1:1','4:3', '4:5', '16:9'])
            #if filter == 'None':

