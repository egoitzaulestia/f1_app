# pages/11_Acerca_de.py

import streamlit as st

st.set_page_config(
    page_title="Acerca del Proyecto",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Acerca del Proyecto ℹ️")

st.markdown("""
**Nombre del Proyecto:** Análisis de Datos de Fórmula 1

**Autor:** Egoitz Aulestia Padilla 

**Curso:** Inteligencia Artificial y Big Data 2023-2025
            
**Centro Escolar:** CEBANC

**Descripción:**

Este proyecto tiene como objetivo analizar y visualizar datos históricos de Fórmula 1, 
proporcionando insights sobre pilotos, equipos, circuitos y más. Utiliza Python y Streamlit 
para crear una aplicación web interactiva que permite a los usuarios explorar los datos de manera intuitiva.

**Contacto:**

- **Email:** egoitzaulestia@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/egoitz-aulestia/

**Agradecimientos:**

- Agradezco a Vopani por proporcionar los datasets [ https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020 ] utilizados en este proyecto.

""")
