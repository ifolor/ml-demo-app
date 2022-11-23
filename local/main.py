import streamlit as st
import numpy as np
import cv2
from  PIL import Image


#def main():
st.sidebar.markdown('<p class="font">My First Photo Converter App</p>', unsafe_allow_html=True)
with st.sidebar.expander("About the App"):
     st.write("""
        Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect.  \n  \nThis app was created by Sharone Li as a side project to learn Streamlit and computer vision. Hope you enjoy!
     """)



#Create two columns with different width
col1, col2 = st.columns( [0.5, 0.5])
with col1:               # To display the header text using css style
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)


uploaded_file = st.file_uploader("", type=['jpg','png','jpeg']) # To upload the photo
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns( [0.5, 0.5])
    with col1:
        st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
        st.image(image,width=300)  

    with col2:
        st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)


#if __name__ == "__main__":
#    main()
