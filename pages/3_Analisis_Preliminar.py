# pages/3_Analisis_Preliminar.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análisis Preliminar",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis Preliminar 🔍")

st.markdown("""
En esta sección, presentamos algunos análisis y visualizaciones preliminares para entender mejor los datos de Fórmula 1.
""")

# Cargar datasets
drivers = pd.read_csv('data/drivers.csv')
constructors = pd.read_csv('data/constructors.csv')
results = pd.read_csv('data/results.csv')
races = pd.read_csv('data/races.csv')

# Análisis 1: Distribución de Pilotos por Nacionalidad
st.write("## Distribución de Pilotos por Nacionalidad")

nationality_counts = drivers['nationality'].value_counts().reset_index()
nationality_counts.columns = ['nationality', 'count']

fig1 = px.bar(nationality_counts.head(10), x='nationality', y='count', 
              title='Top 10 Nacionalidades de Pilotos', labels={'count': 'Número de Pilotos', 'nationality': 'Nacionalidad'})
st.plotly_chart(fig1)

# Análisis 2: Número de Carreras por Año
st.write("## Número de Carreras por Año")

races_per_year = races['year'].value_counts().reset_index()
races_per_year.columns = ['year', 'race_count']
races_per_year = races_per_year.sort_values('year')

fig2 = px.line(races_per_year, x='year', y='race_count', 
               title='Número de Carreras por Año', labels={'year': 'Año', 'race_count': 'Número de Carreras'})
st.plotly_chart(fig2)

# Análisis 3: Evolución de Velocidad Promedio a lo Largo de los Años
st.write("## Evolución de la Velocidad Promedio de los Pilotos")

# Cargar datos adicionales si es necesario y realizar el análisis (similar a los códigos anteriores)
# [Incluye aquí el análisis de velocidad promedio si lo deseas]

st.markdown("""
Estos análisis nos permiten tener una visión general de la evolución y distribución de la Fórmula 1 a lo largo de los años.
""")
