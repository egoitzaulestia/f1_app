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

**Curso:** Inteligencia Artificial y Big Data
            
**Centro Escolar:** CEBANC

**Descripción:**

Este proyecto tiene como objetivo analizar y visualizar datos históricos de Fórmula 1, 
proporcionando insights sobre pilotos, equipos, circuitos y más. Utiliza Python y Streamlit 
para crear una aplicación web interactiva que permite a los usuarios explorar los datos de manera intuitiva.

**Contacto:**

- **Email:** egoitzaulestia@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/egoitz-aulestia/

**Agradecimientos:**

- Agradezco a [Fuentes de Datos] por proporcionar los datasets utilizados en este proyecto.
- [Otros agradecimientos si aplica]
""")
