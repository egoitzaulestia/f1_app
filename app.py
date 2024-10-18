# pages/1_Home.py

import streamlit as st
import base64

st.set_page_config(
    page_title="Home",
    page_icon="🏎️",
    layout="wide",
)

# ---------------------------
# Función para establecer la imagen de fondo
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url(data:image/webp;base64,{encoded_string});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Llamar a la función con la ruta de la imagen
set_background("images/fondoF1_2.jpg")

# ---------------------------
# Estilizar el título con un fondo negro y texto blanco
st.markdown("""
    <br>
    <div style="background-color: rgba(0, 0, 0); padding: 20px; border-radius: 10px;">
        <h1 style="color: white; text-align: center;">
            Bienvenido al Análisis de Datos de Fórmula 1 
        </h1>
        <p style="color: white; text-align: center;">
            Explora diferentes secciones para obtener análisis detallados sobre pilotos, equipos, circuitos y mucho más en el emocionante mundo de la Fórmula 1.
        </p>
    </div>
    <br>
    """, unsafe_allow_html=True)

st.sidebar.success("Selecciona una página arriba.")

# # Descripción adicional (opcional)
# st.markdown("""
#     <div style="background-color: rgba(0, 0, 0, 0.5); padding: 15px; border-radius: 10px;">
#         <p style="color: white; text-align: center;">
#             Explora diferentes secciones para obtener análisis detallados sobre pilotos, equipos, circuitos y mucho más en el emocionante mundo de la Fórmula 1.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)
