import streamlit as st
import numpy as np
import cv2
from  PIL import Image
from crop_utils import create_threshold_image, ignore_small_contours
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

    
        col1, col2, col3, col4, col5 = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])
        with col1:
            st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
            st.image(image)  

        with col2:
            st.markdown('<p style="text-align: center;">Saliency map</p>',unsafe_allow_html=True)
            st.image(saliency_map)  

        with col3:
            st.markdown('<p style="text-align: center;">Saliency map</p>',unsafe_allow_html=True)
            st.image(threshold_map) 

        with col4:
            st.markdown('<p style="text-align: center;">Saliency map</p>',unsafe_allow_html=True)
            st.image(threshold_map_exclude_small_contours)            


            #filter = st.sidebar.radio('Any desired aspect ratio (width-to-height)?', ['None','1:1','4:3', '4:5', '16:9'])
            #if filter == 'None':




if __name__ == "__main__":
    main()
