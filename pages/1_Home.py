# pages/1_Home.py

import streamlit as st
# import base64

st.set_page_config(
    page_title="Home",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Datos de Fórmula 1 🏁")

st.markdown("""
Bienvenido a la aplicación interactiva de análisis de datos de Fórmula 1. Aquí podrás explorar diferentes aspectos de la F1, incluyendo pilotos, equipos, circuitos y más.

Utiliza el menú de navegación para explorar las distintas secciones de la aplicación.
""")

# # Función para establecer la imagen de fondo
# def set_background(image_file):
#     with open(image_file, "rb") as image:
#         encoded_string = base64.b64encode(image.read()).decode()
#     css = f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/png;base64,{encoded_string});
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }}
#     </style>
#     """
#     st.markdown(css, unsafe_allow_html=True)

# # Llamar a la función con la ruta de la imagen
# set_background("images/fondoF1.webp")