import streamlit as st
import numpy as np
import cv2
from PIL import Image
from google.cloud import vision
from crop_utils import create_threshold_image, ignore_small_contours, crop_image
from features.gcp_crop_hints import create_bounding_box, calculate_bounding_box_coords

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
    print(type(uploaded_file))
    image_bytes = uploaded_file.read()
    vertices, confidence, importance_fraction = create_bounding_box(image_bytes, aspect_ratio=16/9)
    start_x, start_y, width, height = calculate_bounding_box_coords(vertices)



    image = Image.open(uploaded_file)
    image_array = np.asarray(image)
        # crop the image based on the bounding rectangle
    cropped_image = image_array[start_y:start_y+height,  start_x:start_x+width]
        # draw the rectangle on the original image
    start_vertex = (start_x, start_y)
    end_vertex = (start_x+width, start_y+height)
    colour = (238, 40, 103)
    thickness = int(0.02*min(image_array.shape[0], image_array.shape[1]))
    rectangle_image = cv2.rectangle(image_array, start_vertex, end_vertex, colour, thickness)

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



