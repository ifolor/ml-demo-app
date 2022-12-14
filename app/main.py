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


@st.experimental_memo
def convert_bytes_to_image(image_bytes):
    image_array = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    image_color = cv2.imdecode(image_array , cv2.IMREAD_COLOR)
    image_color_copy = image_color.copy()
    image_grey = cv2.imdecode(image_array , cv2.IMREAD_GRAYSCALE)
    return image_color, image_color_copy, image_grey

@st.experimental_memo
def show_images(uploaded_file):
    if uploaded_file is not None:
    #for uploaded_file in uploaded_files:
            # Convert the file to an opencv image.
            #print(uploaded_file.read())
            #print(type(uploaded_file.read())) # byte


            # Read bytes as color and greyscale images
        image_color, image_color_copy, image_grey = convert_bytes_to_image(uploaded_file.read())

    
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

@st.experimental_memo      
def get_hints(uploaded_file):
    if uploaded_file is not None:
        image_color, image_color_copy, image_grey = convert_bytes_to_image(uploaded_file.read())
        image_bytes = uploaded_file.read()
        #print(image_bytes)
 
        image = vision.Image(content=image_bytes)
        response = client.crop_hints(image=image)
        hints = response.crop_hints_annotation.crop_hints
        
        for n, hint in enumerate(hints):
            print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in hint.bounding_poly.vertices])

        confidence = hint.confidence
        print(confidence)

        print('bounds: {}'.format(','.join(vertices)))    
        print(vertices) 
        start_x = int(vertices[0].split(",")[0].replace('(', ''))
        start_y = int(vertices[0].split(",")[1].replace(')', ''))
        width = int(vertices[1].split(",")[0].replace('(', '')) - start_x
        height = int(vertices[2].split(",")[1].replace(')', '')) - start_y
        print(start_x, start_y, width, height)

        

        # crop the image based on the bounding rectangle
        cropped_image = image_color[start_y:start_y+height,  start_x:start_x+width]
        # draw the rectangle on the original image
        start_vertex = (start_x, start_y)
        end_vertex = (start_x+width, start_y+height)
        colour = (238, 40, 103)
        thickness = int(0.02*min(image.shape[0], image.shape[1]))
        rectangle_image = cv2.rectangle(image_color, start_vertex, end_vertex, colour, thickness)

        col_1, col_2, col_3, col_4, col_5 = st.columns(np.ones(5)*0.2)
        with col_1:
            st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
            st.image(image_color, channels="BGR") 
        with col_4:
            st.markdown('<p style="text-align: center;">Crop hints</p>',unsafe_allow_html=True)
            st.image(rectangle_image, channels="BGR")      

        with col_5:
            st.markdown('<p style="text-align: center;">Cropped image</p>',unsafe_allow_html=True)
            st.image(cropped_image, channels="BGR") 



st.title("👋 Hello")
st.subheader("Please select which feature you want to test.")

features = ["Crop hints (OpenCV implementation)", 
            "Crop hints (Google Vision API)", 
            "Dominant colors"]
page = st.radio("", features)


if page == "Crop hints (OpenCV implementation)":
    col_1, col_2 = st.columns([1, 1])
    with col_1:
        uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    show_images(uploaded_file)

elif page == "Crop hints (Google Vision API)":
    col_1, col_2 = st.columns([1, 1])
    with col_1:
        uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    get_hints(uploaded_file)

else:
    col_1, col_2 = st.columns([1, 2])
    with col_1:
        number_of_colors = st.select_slider(
        'How many dominant colors do you want to extract from your image?',
    options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
    





   



