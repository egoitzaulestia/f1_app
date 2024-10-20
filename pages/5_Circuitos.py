# # pages/5_Circuitos.py

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import folium
# from streamlit_folium import st_folium

# st.set_page_config(
#     page_title="Análisis de Circuitos",
#     page_icon="🏎️",
#     layout="wide",
# )

# st.write("# Análisis de Circuitos 🏟️")

# st.markdown("""
# Explora las características y estadísticas de los circuitos de Fórmula 1.
# """)

# # Cargar datasets
# circuits = pd.read_csv('data/circuits.csv')
# races = pd.read_csv('data/races.csv')

# # Unir datasets para obtener información adicional
# race_circuits = races.merge(circuits, on='circuitId')

# # Número de veces que se ha corrido en cada circuito
# circuit_counts = race_circuits['name_y'].value_counts().reset_index()
# circuit_counts.columns = ['circuit_name', 'race_count']

# # Gráfico de los circuitos más utilizados
# st.write("## Circuitos con Mayor Número de Carreras")

# fig = px.bar(circuit_counts.head(10), x='race_count', y='circuit_name', orientation='h',
#              title='Top 10 Circuitos con Más Carreras', labels={'race_count': 'Número de Carreras', 'circuit_name': 'Circuito'})
# fig.update_layout(yaxis=dict(autorange="reversed"))

# st.plotly_chart(fig)

# # Detalles de un circuito específico
# st.write("## Detalles de Circuito")

# circuit_list = circuits['name'].unique()
# selected_circuit = st.selectbox("Selecciona un circuito", circuit_list)

# circuit_info = circuits[circuits['name'] == selected_circuit]

# st.write(f"### Información de {selected_circuit}")
# st.write(circuit_info[['location', 'country', 'lat', 'lng', 'alt']].T)

# # Mapa del circuito seleccionado
# st.write("### Ubicación del Circuito")

# m = folium.Map(location=[circuit_info['lat'].values[0], circuit_info['lng'].values[0]], zoom_start=10)
# folium.Marker(
#     location=[circuit_info['lat'].values[0], circuit_info['lng'].values[0]],
#     popup=selected_circuit,
#     icon=folium.Icon(color='red', icon='flag')
# ).add_to(m)

# st_data = st_folium(m, width=700, height=500)


# pages/5_Circuitos.py

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(
    page_title="Análisis de Circuitos",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Circuitos 🏟️")

st.markdown("""
Explora las características y estadísticas de los circuitos de Fórmula 1.
""")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    circuits = pd.read_csv('data/circuits.csv')
    races = pd.read_csv('data/races.csv')
    return circuits, races

circuits, races = load_data()

# ---------------------------
# Leer los archivos JSON
with open('data/surface_classification.json', 'r', encoding='utf-8') as f:
    surface_classification = json.load(f)

with open('data/permanence_classification.json', 'r', encoding='utf-8') as f:
    permanence_classification = json.load(f)

with open('data/continent_classification.json', 'r', encoding='utf-8') as f:
    continent_classification = json.load(f)

# Asignar la clasificación de superficies
circuits['surface'] = circuits['name'].map(surface_classification)
surface_numeric_mapping = {'Urbano': 1, 'Mixto': 2, 'Asfalto': 3}
circuits['surface_numeric'] = circuits['surface'].map(surface_numeric_mapping)

# Asignar la clasificación de permanencia
circuits['permanence'] = circuits['name'].map(permanence_classification)
permanence_numeric_mapping = {'Temporal': 1, 'Permanente': 2}
circuits['permanence_numeric'] = circuits['permanence'].map(permanence_numeric_mapping)

# Asignar la clasificación de continentes
circuits['continent'] = circuits['name'].map(continent_classification)
continent_numeric_mapping = {
    'África': 1,
    'América del Norte': 2,
    'América del Sur': 3,
    'Asia': 4,
    'Europa': 5,
    'Oceanía': 6
}
circuits['continent_numeric'] = circuits['continent'].map(continent_numeric_mapping)

# ---------------------------
# Unir datasets para obtener información adicional
race_circuits = races.merge(circuits, on='circuitId')

# Renombrar columnas en race_circuits para tener 'circuit_name'
race_circuits.rename(columns={'name_x': 'race_name', 'name_y': 'circuit_name'}, inplace=True)

# ---------------------------
# Gráfico de los circuitos más utilizados
st.write("## Circuitos con Mayor Número de Carreras")

circuit_counts = race_circuits['circuit_name'].value_counts().reset_index()
circuit_counts.columns = ['circuit_name', 'race_count']

fig = px.bar(
    circuit_counts.head(10),
    x='race_count',
    y='circuit_name',
    orientation='h',
    title='Top 10 Circuitos con Más Carreras',
    labels={'race_count': 'Número de Carreras', 'circuit_name': 'Circuito'}
)
fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Detalles de un circuito específico
st.write("## Detalles de Circuito")

circuit_list = circuits['name'].unique()
selected_circuit = st.selectbox("Selecciona un circuito", circuit_list)

circuit_info = circuits[circuits['name'] == selected_circuit]

st.write(f"### Información de {selected_circuit}")
st.write(circuit_info[['location', 'country', 'lat', 'lng', 'alt', 'surface', 'permanence', 'continent']].T)

# ---------------------------
# Mapa del circuito seleccionado
st.write("### Ubicación del Circuito")

m = folium.Map(location=[circuit_info['lat'].values[0], circuit_info['lng'].values[0]], zoom_start=10)
folium.Marker(
    location=[circuit_info['lat'].values[0], circuit_info['lng'].values[0]],
    popup=selected_circuit,
    icon=folium.Icon(color='red', icon='flag')
).add_to(m)

st_data = st_folium(m, width=700, height=500)
