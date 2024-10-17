# pages/5_Circuitos.py

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Análisis de Circuitos",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Circuitos 🏟️")

st.markdown("""
Explora las características y estadísticas de los circuitos de Fórmula 1.
""")

# Cargar datasets
circuits = pd.read_csv('data/circuits.csv')
races = pd.read_csv('data/races.csv')

# Unir datasets para obtener información adicional
race_circuits = races.merge(circuits, on='circuitId')

# Número de veces que se ha corrido en cada circuito
circuit_counts = race_circuits['name_y'].value_counts().reset_index()
circuit_counts.columns = ['circuit_name', 'race_count']

# Gráfico de los circuitos más utilizados
st.write("## Circuitos con Mayor Número de Carreras")

fig = px.bar(circuit_counts.head(10), x='race_count', y='circuit_name', orientation='h',
             title='Top 10 Circuitos con Más Carreras', labels={'race_count': 'Número de Carreras', 'circuit_name': 'Circuito'})
fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig)

# Detalles de un circuito específico
st.write("## Detalles de Circuito")

circuit_list = circuits['name'].unique()
selected_circuit = st.selectbox("Selecciona un circuito", circuit_list)

circuit_info = circuits[circuits['name'] == selected_circuit]

st.write(f"### Información de {selected_circuit}")
st.write(circuit_info[['location', 'country', 'lat', 'lng', 'alt']].T)

# Mapa del circuito seleccionado
st.write("### Ubicación del Circuito")

m = folium.Map(location=[circuit_info['lat'].values[0], circuit_info['lng'].values[0]], zoom_start=10)
folium.Marker(
    location=[circuit_info['lat'].values[0], circuit_info['lng'].values[0]],
    popup=selected_circuit,
    icon=folium.Icon(color='red', icon='flag')
).add_to(m)

st_data = st_folium(m, width=700, height=500)
