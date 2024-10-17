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
    page_title="Mapas Geográficos",
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
###########
# MAPA 1: Folium Map con Marcadores de Circuitos
###########

st.write("## Mapa 1: Ubicaciones de los Circuitos de Fórmula 1")

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
st_folium(m, width=1200, height=500)

st.markdown("""
Este mapa muestra la ubicación geográfica de todos los circuitos de Fórmula 1. Al hacer clic en un marcador, puedes ver el nombre, la localización y el número de carreras realizadas en ese circuito.
""")

# ---------------------------
###########
# MAPA 2: Plotly Interactive Map con Rutas entre Circuitos para un Año Seleccionado
###########

st.write("## Mapa 2: Rutas entre Circuitos por Año")

# Crear una lista de años disponibles desde 1950 hasta 2024
available_years = sorted(races['year'].unique())
years = [year for year in available_years if 1950 <= year <= 2024]
selected_year = st.selectbox("Selecciona el año", years)

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
    edges_x = []
    edges_y = []
    for i in range(len(circuit_ids_ordered) - 1):
        circuito_1 = circuit_data_ordered.iloc[i]
        circuito_2 = circuit_data_ordered.iloc[i + 1]

        # Coordenadas de los dos circuitos
        loc1 = (circuito_1['lat'], circuito_1['lng'])
        loc2 = (circuito_2['lat'], circuito_2['lng'])

        # Añadir las coordenadas para las aristas
        edges_x.extend([loc1[1], loc2[1], None])  # Longitudes (x)
        edges_y.extend([loc1[0], loc2[0], None])  # Latitudes (y)

    # Obtener las posiciones de los nodos (coordenadas geográficas)
    x_coords = circuit_data_ordered['lng'].tolist()
    y_coords = circuit_data_ordered['lat'].tolist()

    # Crear información adicional para los popups
    circuit_data_ordered['text'] = circuit_data_ordered['name'] + '<br>' + \
        'Localización: ' + circuit_data_ordered['location'] + ', ' + circuit_data_ordered['country']

    # Crear los nodos (circuitos) con mismo color
    node_trace = go.Scattergeo(
        lon=x_coords,
        lat=y_coords,
        text=circuit_data_ordered['text'],
        mode='markers',
        marker=dict(
            size=8,
            color='blue',  # Mismo color para todos los nodos
            line_width=1,
        ),
        hoverinfo='text',
        name='Circuitos'
    )

    # Crear las aristas (conexiones)
    edge_trace = go.Scattergeo(
        lon=edges_x,
        lat=edges_y,
        mode='lines',
        line=dict(width=2, color='orange'),
        hoverinfo='none',
        name='Rutas'
    )

    # Crear la figura con nodos y aristas
    fig = go.Figure(data=[edge_trace, node_trace])

    # Añadir leyenda manual
    fig.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode='markers',
            marker=dict(
                size=8,
                color='blue',
                line_width=1,
            ),
            name='Circuitos'
        )
    )
    fig.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode='lines',
            line=dict(width=2, color='orange'),
            name='Rutas'
        )
    )

    # Actualizar el diseño del mapa
    fig.update_layout(
        title_text=f'Rutas de Circuitos F1 en {selected_year}',
        showlegend=True,
        width=800,
        height=600,
        geo=dict(
            projection_type='equirectangular',  # Proyección más plana para evitar distorsiones
            showland=True,
            landcolor='rgb(243, 243, 243)',
            showocean=True,
            oceancolor='rgb(230, 245, 255)',
            coastlinecolor='gray',
            countrycolor='gray',
        ),
        margin=dict(l=0, r=0, t=50, b=0),
    )

    # Mostrar el mapa en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    Este mapa muestra los circuitos de Fórmula 1 para el año seleccionado. Las líneas naranjas representan las rutas entre los circuitos en el orden de las carreras. Los puntos azules indican la ubicación de cada circuito.
    """)

# ---------------------------
###########
# MAPA 3: Plotly Animated Map mostrando la Evolución de los Circuitos a lo Largo de los Años
###########

st.write("## Mapa 3: Evolución de los Circuitos a lo Largo de los Años")

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

# Verificar si 'name' está presente
if 'name' not in race_circuit_year_anim.columns:
    st.error("Error: La columna 'name' no está presente en el DataFrame. Verifica los nombres de las columnas después del merge.")
else:
    # Crear la animación con Plotly Express
    fig_anim = px.scatter_geo(
        race_circuit_year_anim,
        lon='lng',
        lat='lat',
        color='name',
        hover_name='name',
        hover_data={'location': True, 'country': True, 'lat': False, 'lng': False},
        animation_frame='year',
        projection='natural earth',
        title='Evolución de los Circuitos de Fórmula 1',
    )

    # Configurar todos los nodos con el mismo color
    fig_anim.update_traces(marker=dict(color='green', size=8, line=dict(width=1)))

    # Añadir leyenda manual
    fig_anim.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode='markers',
            marker=dict(
                size=8,
                color='green',
                line_width=1,
            ),
            name='Circuitos'
        )
    )

    fig_anim.update_layout(
        width=800,
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=True,
    )

    # Mostrar la animación en Streamlit
    st.plotly_chart(fig_anim, use_container_width=True)

    st.markdown("""
    Este mapa animado muestra cómo los circuitos de Fórmula 1 han evolucionado desde 1950 hasta 2024. Observa cómo se han agregado nuevos circuitos y cómo la distribución geográfica ha cambiado a lo largo de las décadas.
    """)

# ---------------------------
###########
# MAPA 4: Folium Heatmap de la Densidad de Circuitos con Información Adicional
###########

st.write("## Mapa 4: Densidad de Circuitos de Fórmula 1 con Información Adicional")

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

# Mostrar el mapa de calor en Streamlit con mayor ancho
st_folium(heatmap_map, width=1200, height=600)  # Ajuste del ancho a 1200

st.markdown("""
Este mapa de calor muestra la densidad de circuitos de Fórmula 1 en diferentes regiones del mundo. Los puntos también incluyen información adicional sobre cada circuito, como su nombre y ubicación, al pasar el ratón por encima de ellos.
""")
