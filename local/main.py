import streamlit as st
import numpy as np
import cv2
from  PIL import Image
st.set_page_config(layout="wide")


def main():

    st.title("👋 Hello")
    st.subheader("This is the relevant region detection demo")

    st.subheader("Upload your photo")
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg']) # To upload the photo
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
    
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=400)  

        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
            filter = st.sidebar.radio('Any desired aspect ratio (width-to-height)?', ['None','1:1','4:3', '4:5', '16:9'])
            if filter == 'None':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                st.image(gray_scale, width=250)
            elif filter == 'Black and White':
                converted_img = np.array(image.convert('RGB'))
                gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                st.image(blackAndWhiteImage, width=300)


if __name__ == "__main__":
    main()
