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
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import json
import reverse_geocoder as rg
import pycountry_convert as pc

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
with open('data/surface_classification.json', 'r') as f:
    surface_classification = json.load(f)

with open('data/permanence_classification.json', 'r') as f:
    permanence_classification = json.load(f)

# Asignar la clasificación de superficies
circuits['surface'] = circuits['name'].map(surface_classification)
surface_numeric_mapping = {'Urbano': 1, 'Mixto': 2, 'Asfalto': 3}
circuits['surface_numeric'] = circuits['surface'].map(surface_numeric_mapping)

# Asignar la clasificación de permanencia
circuits['permanence'] = circuits['name'].map(permanence_classification)
permanence_numeric_mapping = {'Temporal': 1, 'Permanente': 2}
circuits['permanence_numeric'] = circuits['permanence'].map(permanence_numeric_mapping)

# ---------------------------
# Función para obtener el continente a partir de latitud y longitud
def get_continent(lat, lng):
    coordinates = (lat, lng)
    result = rg.search(coordinates)  # Obtener información sobre el país
    country_code = result[0]['cc']

    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_mapping = {
            'AF': 'África',
            'NA': 'América del Norte',
            'SA': 'América del Sur',
            'AS': 'Asia',
            'EU': 'Europa',
            'OC': 'Oceanía'
        }
        return continent_mapping.get(continent_code, 'Desconocido')
    except KeyError:
        return 'Desconocido'

# Aplicar la función para obtener el continente de cada circuito
@st.cache_data
def add_continent_info(df):
    df['continent'] = df.apply(lambda row: get_continent(row['lat'], row['lng']), axis=1)
    return df

circuits = add_continent_info(circuits)

# Mapear los continentes a valores numéricos
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

# Añadir el año al circuito y renombrar columnas
circuits_year = race_circuits[['year', 'circuitId', 'name_x', 'name_y', 'surface', 'permanence', 'continent']]
circuits_year = circuits_year.rename(columns={'name_x': 'race_name', 'name_y': 'circuit_name'})

# ---------------------------
# Crear gráficos de dona interactivos
st.write("## Distribución de Tipos de Circuitos por Año")

# Lista de años desde 2024 hacia atrás
years = sorted(races['year'].unique(), reverse=True)
selected_year = st.selectbox("Selecciona el año para ver la distribución de circuitos", years)

# Filtrar datos para el año seleccionado
circuits_year_selected = circuits_year[circuits_year['year'] == selected_year]

# Datos para los gráficos de dona
# Tipo de Superficie
surface_counts = circuits_year_selected['surface'].value_counts().reset_index()
surface_counts.columns = ['surface', 'count']

# Tipo de Duración
permanence_counts = circuits_year_selected['permanence'].value_counts().reset_index()
permanence_counts.columns = ['permanence', 'count']

# Distribución Geográfica
continent_counts = circuits_year_selected['continent'].value_counts().reset_index()
continent_counts.columns = ['continent', 'count']

# Crear subplots para los gráficos de dona
fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

# Gráfico de dona para Tipo de Superficie
fig.add_trace(go.Pie(
    labels=surface_counts['surface'],
    values=surface_counts['count'],
    name="Tipo de Superficie",
    hole=0.4), 1, 1)

# Gráfico de dona para Tipo de Duración
fig.add_trace(go.Pie(
    labels=permanence_counts['permanence'],
    values=permanence_counts['count'],
    name="Tipo de Duración",
    hole=0.4), 1, 2)

# Gráfico de dona para Distribución Geográfica
fig.add_trace(go.Pie(
    labels=continent_counts['continent'],
    values=continent_counts['count'],
    name="Distribución Geográfica",
    hole=0.4), 1, 3)

# Actualizar títulos y layout
fig.update_layout(
    title_text=f"Distribución de Circuitos en {selected_year}",
    annotations=[
        dict(text='Superficie', x=0.08, y=0.5, font_size=14, showarrow=False),
        dict(text='Duración', x=0.50, y=0.5, font_size=14, showarrow=False),
        dict(text='Geografía', x=0.92, y=0.5, font_size=14, showarrow=False)
    ],
    width=1200,
    height=500,
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Gráfico de los circuitos más utilizados
st.write("## Circuitos con Mayor Número de Carreras")

circuit_counts = race_circuits['name_y'].value_counts().reset_index()
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
