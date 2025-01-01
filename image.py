import streamlit as st

def display_image(image_path):
    st.image(image_path, caption='Kilometer', use_column_width=True)

from PIL import Image
def display_image(image_path):
    image = Image.open('kilometer_listrik.png')
    image = image.resize((100, int(image.height * (100 / image.width))))  

    st.image(image, caption='Konsumsi Energi')  
    
   