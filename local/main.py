import streamlit as st
import numpy as np
import cv2
from  PIL import Image, ImageOps
from create_crop_hints import create_threshold_image
st.set_page_config(layout="wide")




def main():

    st.title("👋 Hello")
    st.subheader("This is the relevant region detection demo. Please upload an image to get started.")

    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg']) # To upload the photo
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        threshold_map = create_threshold_image(uploaded_file)

    
        col1, col2, col3, col4 = st.columns( [0.25, 0.25, 0.25, 0.25])
        with col1:
            st.markdown('<p style="text-align: center;">Original image</p>',unsafe_allow_html=True)
            st.image(image)  

        with col2:
            st.markdown('<p style="text-align: center;">Threshold map</p>',unsafe_allow_html=True)
            st.image(threshold_map)  



            #filter = st.sidebar.radio('Any desired aspect ratio (width-to-height)?', ['None','1:1','4:3', '4:5', '16:9'])
            #if filter == 'None':




if __name__ == "__main__":
    main()
