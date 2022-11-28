import streamlit as st
import numpy as np
import cv2
from  PIL import Image
from crop_utils import create_threshold_image, ignore_small_contours, crop_image
st.set_page_config(layout="wide")



def main():

    st.title("👋 Hello")
    st.subheader("This is the relevant region detection demo. Please upload an image to get started.")

    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg']) # To upload the photo
    if uploaded_file is not None:
        print(uploaded_file)
        image = Image.open(uploaded_file)
        saliency_map, threshold_map = create_threshold_image(image)
        threshold_map_exclude_small_contours = ignore_small_contours(threshold_map)
        rectangle_image, cropped_image = crop_image(image, threshold_map_exclude_small_contours)

    
        col_1, col_2, col_3, col_4, col_5 = st.columns(np.ones(5)*0.2)
        with col_1:
            st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
            st.image(image)  

        with col_2:
            st.markdown('<p style="text-align: center;">Saliency map</p>',unsafe_allow_html=True)
            st.image(saliency_map)  

        with col_3:
            st.markdown('<p style="text-align: center;">Threshold map</p>',unsafe_allow_html=True)
            st.image(threshold_map) 

        with col_4:
            st.markdown('<p style="text-align: center;">Crop hints</p>',unsafe_allow_html=True)
            st.image(rectangle_image)      

        with col_5:
            st.markdown('<p style="text-align: center;">Cropped image</p>',unsafe_allow_html=True)
            st.image(cropped_image)       


            #filter = st.sidebar.radio('Any desired aspect ratio (width-to-height)?', ['None','1:1','4:3', '4:5', '16:9'])
            #if filter == 'None':




if __name__ == "__main__":
    main()
