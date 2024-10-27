# pages/4_Mapas_Geograficos.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Configuración de la página
st.set_page_config(
    page_title="Mapas Geográficos 3D",
    page_icon="🏎️",
    layout="wide",
)

# Título de la página
st.write("# Mapas Geográficos 🌍")

st.markdown("""
En esta sección, exploramos las ubicaciones de los circuitos de Fórmula 1 a través de mapas interactivos. Puedes visualizar rutas entre circuitos en un año específico, observar la evolución de los circuitos a lo largo de los años y analizar la densidad de circuitos en diferentes regiones.
""")

# ---------------------------
# Cargar los datasets
@st.cache_data
def load_data():
    circuits = pd.read_csv('data/circuits.csv')
    races = pd.read_csv('data/races.csv')
    return circuits, races

circuits, races = load_data()

# Calcular el número de apariciones de cada circuito
circuit_appearances = races['circuitId'].value_counts().reset_index()
circuit_appearances.columns = ['circuitId', 'appearances']
circuits = circuits.merge(circuit_appearances, on='circuitId', how='left')
circuits['appearances'] = circuits['appearances'].fillna(0).astype(int)

# ---------------------------
# Preparar datos para Mapas 2 y 3

# Definir el rango de años desde 1950 hasta 2024
min_year_anim = 1950
max_year_anim = 2024

# Filtrar los años seleccionados
years_selected_anim = list(range(min_year_anim, max_year_anim + 1))
races_years_anim = races[races['year'].isin(years_selected_anim)]

# Crear un DataFrame que contiene los circuitos y el año en que se corrieron
race_circuit_year_anim = races_years_anim.merge(circuits, on='circuitId', how='left')

# Verificar y renombrar columnas si es necesario
if 'name_x' in race_circuit_year_anim.columns and 'name_y' in race_circuit_year_anim.columns:
    race_circuit_year_anim = race_circuit_year_anim.rename(columns={'name_y': 'name'}).drop(columns=['name_x'])
elif 'name' not in race_circuit_year_anim.columns:
    st.error("Error: La columna 'name' no está presente en el DataFrame después del merge. Por favor, verifica los nombres de las columnas.")
    st.stop()

# Seleccionar las columnas necesarias
race_circuit_year_anim = race_circuit_year_anim[['year', 'name', 'location', 'country', 'lat', 'lng']].drop_duplicates()

# ---------------------------
###########
# MAPA 1: Plotly Interactive Map con Rutas entre Circuitos para un Año Seleccionado
###########

st.write("## Mapa 1: Rutas entre Circuitos por Año")

# Crear una lista de años disponibles desde 1950 hasta 2024, invertida
available_years = sorted(races['year'].unique(), reverse=True)
years = [year for year in available_years if 1950 <= year <= 2024]

if 2024 in years:
    default_index = 0  # 2024 está en la posición 0
else:
    default_index = 0  # Si no está 2024, el último año disponible

selected_year = st.selectbox("Selecciona el año", years, index=default_index)

# Filtrar las carreras del año seleccionado y ordenarlas por ronda
races_selected_year = races[(races['year'] == selected_year) & (races['circuitId'].isin(circuits['circuitId']))].sort_values('round')

if races_selected_year.empty:
    st.warning(f"No hay datos disponibles para el año {selected_year}.")
else:
    # Obtener los circuitos del año seleccionado en orden de carreras
    circuit_ids_ordered = races_selected_year['circuitId'].tolist()
    circuit_data_ordered = circuits[circuits['circuitId'].isin(circuit_ids_ordered)].set_index('circuitId')

    # Asegurarse de que los circuitos están en el orden de las carreras
    try:
        circuit_data_ordered = circuit_data_ordered.loc[circuit_ids_ordered].reset_index()
    except KeyError as e:
        st.error(f"Error al ordenar los circuitos: {e}")
        st.stop()

    # Crear las aristas (conexiones entre los circuitos en el orden de las carreras)
    edges_lon = []
    edges_lat = []
    for i in range(len(circuit_ids_ordered) - 1):
        circuito_1 = circuit_data_ordered.iloc[i]
        circuito_2 = circuit_data_ordered.iloc[i + 1]

        # Coordenadas de los dos circuitos
        loc1 = (circuito_1['lat'], circuito_1['lng'])
        loc2 = (circuito_2['lat'], circuito_2['lng'])

        # Añadir las coordenadas para las aristas
        edges_lon.extend([loc1[1], loc2[1], None])  # Longitudes (x)
        edges_lat.extend([loc1[0], loc2[0], None])  # Latitudes (y)

    # Obtener las posiciones de los nodos (coordenadas geográficas)
    lon_coords = circuit_data_ordered['lng'].tolist()
    lat_coords = circuit_data_ordered['lat'].tolist()

    # Crear información adicional para los popups
    circuit_data_ordered['text'] = circuit_data_ordered['name']  # Solo el nombre

    # Datos para hover
    circuit_data_ordered['hover_text'] = '<b>' + circuit_data_ordered['name'] + '</b><br>Localización: ' + circuit_data_ordered['location'] + ', ' + circuit_data_ordered['country']

    # Crear los nodos (circuitos)
    node_trace = go.Scattergeo(
        lon=lon_coords,
        lat=lat_coords,
        text=circuit_data_ordered['text'],
        mode='markers+text',
        marker=dict(
            size=8,
            color='blue',
            line_width=1,
        ),
        hovertext=circuit_data_ordered['hover_text'],
        hoverinfo='text',
        name='Circuitos',
        textfont=dict(
            color='black',
        ),
        textposition="top center",
        showlegend=False
    )

    # Crear las aristas (conexiones)
    edge_trace = go.Scattergeo(
        lon=edges_lon,
        lat=edges_lat,
        mode='lines',
        line=dict(width=2, color='orange'),
        hoverinfo='none',
        name='Rutas',
        showlegend=False
    )

    # Actualizar el diseño del mapa
    fig = go.Figure(data=[edge_trace, node_trace])

    fig.update_layout(
        title_text=f'Rutas de Circuitos F1 en {selected_year}',
        showlegend=False,
        geo=dict(
            projection_type='orthographic',
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue',
            showcountries=True,
            countrycolor='gray',
            showcoastlines=True,
            coastlinecolor='gray',
            showframe=False,
            bgcolor='rgba(0,0,0,0)',
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        width=1200,
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    Este mapa muestra los circuitos de Fórmula 1 para el año seleccionado. Las líneas naranjas representan las rutas entre los circuitos en el orden de las carreras. Los puntos azules indican la ubicación de cada circuito.
    """)

# ---------------------------
###########
# MAPA 2: Evolución de los Circuitos a lo Largo de los Años
###########

st.write("## Mapa 2: Evolución de los Circuitos a lo Largo de los Años")

# Ordenar los años correctamente
race_circuit_year_anim['year'] = race_circuit_year_anim['year'].astype(int)
race_circuit_year_anim = race_circuit_year_anim.sort_values('year')

# Crear la animación con Plotly Express
fig_anim = px.scatter_geo(
    race_circuit_year_anim,
    lon='lng',
    lat='lat',
    text='name',
    hover_name='name',
    hover_data={'location': True, 'country': True, 'lat': False, 'lng': False},
    animation_frame='year',
    projection='orthographic',
    title='Evolución de los Circuitos de Fórmula 1',
    category_orders={'year': sorted(race_circuit_year_anim['year'].unique())}
)

# Configurar todos los nodos con el mismo color y añadir nombres de circuitos
fig_anim.update_traces(
    marker=dict(color='blue', size=8, line=dict(width=1)),
    textposition='top center',
    textfont=dict(color='black'),
)

# Ocultar la barra de colores
fig_anim.update_coloraxes(showscale=False)

# Actualizar el diseño
fig_anim.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    showlegend=False,
    width=1200,
    height=800,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    geo=dict(
        showland=True,
        landcolor='lightgray',
        showocean=True,
        oceancolor='lightblue',
        showcountries=True,
        countrycolor='gray',
        showcoastlines=True,
        coastlinecolor='gray',
        showframe=False,
        bgcolor='rgba(0,0,0,0)',
    ),
)

st.plotly_chart(fig_anim, use_container_width=True)

st.markdown("""
Este mapa animado muestra cómo los circuitos de Fórmula 1 han evolucionado desde 1950 hasta 2024. Observa cómo se han agregado nuevos circuitos y cómo la distribución geográfica ha cambiado a lo largo de las décadas.
""")

# ---------------------------
###########
# MAPA 3: Densidad de Circuitos de Fórmula 1 con Información Adicional
###########

st.write("## Mapa 3: Densidad de Circuitos de Fórmula 1 con Información Adicional")

# Crear un mapa de Folium para el heatmap
heatmap_map = folium.Map(location=[20, 0], zoom_start=2)

# Preparar los datos para el heatmap con información adicional
heat_data = race_circuit_year_anim[['lat', 'lng']].values.tolist()

# Añadir el HeatMap
HeatMap(heat_data, radius=20, blur=15, max_zoom=1).add_to(heatmap_map)

# Añadir marcadores individuales con popups o tooltips que muestren más información
for i, row in race_circuit_year_anim.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=1,  # Tamaño del marcador
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.1,
        tooltip=f"{row['name']} - {row['location']}, {row['country']}"
    ).add_to(heatmap_map)

# Mostrar el mapa de calor en Streamlit
st_folium(heatmap_map, width=None, height=600)

st.markdown("""
Este mapa de calor muestra la densidad de circuitos de Fórmula 1 en diferentes regiones del mundo. Los puntos también incluyen información adicional sobre cada circuito, como su nombre y ubicación, al pasar el ratón por encima de ellos.
""")

# ---------------------------
###########
# MAPA 4: Folium Map con Marcadores de todos los Circuitos de la Historia de la Fórmula 1
###########

st.write("## Mapa 4: Ubicaciones de todos los Circuitos de la Historia de la Fórmula 1")

# Crear el mapa de Folium
m = folium.Map(location=[20, 0], zoom_start=2)

# Añadir marcadores
for index, row in circuits.iterrows():
    folium.Marker(
        location=[row['lat'], row['lng']],
        popup=folium.Popup(html=f"<b>{row['name']}</b><br>Localización: {row['location']}, {row['country']}<br>Número de Carreras: {row['appearances']}", max_width=300),
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(m)

# Mostrar el mapa en Streamlit
st_folium(m, width=None, height=500)

st.markdown("""
Este mapa muestra la ubicación geográfica de todos los circuitos de Fórmula 1. Al hacer clic en un marcador, puedes ver el nombre, la localización y el número de carreras realizadas en ese circuito.
""")
