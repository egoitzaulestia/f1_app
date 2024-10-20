# pages/3_Analisis_Preliminar.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np  # Importar numpy para cálculos numéricos
import json  # Para cargar el JSON de circuit_lengths

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
driver_standings = pd.read_csv('data/driver_standings.csv')
circuits = pd.read_csv('data/circuits.csv')

# Cargar circuit_lengths desde el JSON
with open('data/circuit_lengths.json', 'r') as f:
    circuit_lengths = json.load(f)

# Asignar longitudes de circuitos mapeando por 'name'
circuits['circuit_length'] = circuits['name'].map(circuit_lengths)

# Verificar si hay circuitos sin longitud asignada
missing_lengths = circuits[circuits['circuit_length'].isnull()]
if not missing_lengths.empty:
    st.write("Los siguientes circuitos no tienen longitud asignada:")
    st.write(missing_lengths[['circuitId', 'name']].drop_duplicates())

# Hacemos un merge entre 'results' y 'races' para obtener el año asociado a cada carrera
results_with_year = results.merge(races[['raceId', 'year', 'circuitId']], on='raceId', how='left')

# Unir 'results_with_year' con 'circuits' para obtener la longitud del circuito
results_with_year = results_with_year.merge(circuits[['circuitId', 'circuit_length']], on='circuitId', how='left')

# Análisis 1: Distribución de Pilotos por Nacionalidad
st.write("## Distribución de Pilotos por Nacionalidad")

nationality_counts = drivers['nationality'].value_counts().reset_index()
nationality_counts.columns = ['nationality', 'count']

fig1 = px.bar(nationality_counts.head(10), x='nationality', y='count',
              title='Top 10 Nacionalidades de Pilotos (desde el año 1950 al 2024)',
              labels={'count': 'Número de Pilotos', 'nationality': 'Nacionalidad'},
              text='count')  # Añadimos el número encima de cada barra

fig1.update_traces(textposition='outside')  # Posicionamos el texto encima de las barras
fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
Esta gráfica muestra las nacionalidades más comunes entre los pilotos de Fórmula 1 desde 1950 hasta 2024. Observamos cuáles países han aportado más pilotos a lo largo de la historia.
""")

# Análisis 2: Distribución de Constructores por Nacionalidad
st.write("## Distribución de Constructores por Nacionalidad")

constructor_nationality_counts = constructors['nationality'].value_counts().reset_index()
constructor_nationality_counts.columns = ['nationality', 'count']

fig2 = px.bar(constructor_nationality_counts.head(10), x='nationality', y='count',
              title='Top 10 Nacionalidades de Constructores (desde el año 1950 al 2024)',
              labels={'count': 'Número de Constructores', 'nationality': 'Nacionalidad'},
              text='count')  # Añadimos el número encima de cada barra

fig2.update_traces(textposition='outside')  # Posicionamos el texto encima de las barras
fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
Esta gráfica muestra las nacionalidades más comunes entre los constructores de Fórmula 1 desde 1950 hasta 2024. Permite identificar los países con mayor presencia en la fabricación de vehículos para la competencia.
""")

# Análisis 3: Número de Carreras por Año y Número de Victorias por el Campeón
st.write("## Número de Carreras por Año y Victorias del Campeón")

# Número de carreras por año
races_per_year = races['year'].value_counts().reset_index()
races_per_year.columns = ['year', 'race_count']
races_per_year = races_per_year.sort_values('year')

# Obtener el último raceId de cada año
last_race_per_year = races.groupby('year')['raceId'].max().reset_index()

# Obtener los driver standings del último raceId de cada año
driver_standings_last_race = driver_standings.merge(last_race_per_year, on='raceId')

# Filtrar los campeones (posición 1)
champion_wins = driver_standings_last_race[driver_standings_last_race['position'] == 1][['year', 'driverId']]

# Obtener el número de victorias por piloto por año
wins_by_driver = results_with_year[results_with_year['positionOrder'] == 1].groupby(['year', 'driverId']).size().reset_index(name='win_count')

# Combinar datos para obtener las victorias del campeón
champion_wins = champion_wins.merge(wins_by_driver, on=['year', 'driverId'], how='left')

# Combinar número de carreras por año con victorias del campeón
combined_data = races_per_year.merge(champion_wins[['year', 'win_count']], on='year', how='left')

# Reemplazar NaN en 'win_count' por 0
combined_data['win_count'] = combined_data['win_count'].fillna(0)

# Eliminar el año 2024 del gráfico
combined_data = combined_data[combined_data['year'] != 2024]

# Crear el gráfico de líneas con dos líneas: una para el número de carreras y otra para las victorias del campeón
fig3 = go.Figure()

# Línea para el número de carreras por año
fig3.add_trace(go.Scatter(
    x=combined_data['year'], y=combined_data['race_count'],
    mode='lines', name='Número de Carreras',
    line=dict(color='blue'),
    hovertemplate='Año: %{x}<br>Número de Carreras: %{y}'
))

# Línea para el número de victorias del campeón por año
fig3.add_trace(go.Scatter(
    x=combined_data['year'], y=combined_data['win_count'],
    mode='lines', name='Victorias del Campeón',
    line=dict(color='red'),
    hovertemplate='Año: %{x}<br>Victorias del Campeón: %{y}'
))

# Ajustes adicionales del gráfico
fig3.update_layout(
    title='Número de Carreras por Año y Victorias del Campeón',
    xaxis_title='Año',
    yaxis_title='Número',
    legend_title='Líneas',
    hovermode='x unified',
    width=None,  # Hacemos el ancho del gráfico adaptativo
    height=500,
    legend=dict(
        x=0.01,  # Posición horizontal de la leyenda (izquierda)
        y=0.99,  # Posición vertical de la leyenda (arriba)
        bgcolor='rgba(255,255,255,0.5)',  # Fondo semi-transparente para la leyenda
        bordercolor='black',
        borderwidth=1
    )
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
En este gráfico observamos la evolución del número de carreras por año en la Fórmula 1 y cómo se relaciona con el número de victorias del campeón en cada temporada. Nos permite analizar si un mayor número de carreras influye en las victorias del campeón.
""")

# Análisis 4: Boxplot de las posiciones del campeón en cada carrera por año
st.write("## Distribución de las Posiciones del Campeón por Año")

# Obtener las posiciones del campeón en cada carrera
champion_positions = results_with_year.merge(champion_wins[['year', 'driverId']], on=['year', 'driverId'])
champion_positions = champion_positions[['year', 'positionOrder']]

# Eliminar posiciones nulas o no terminadas (si es necesario)
champion_positions = champion_positions[champion_positions['positionOrder'].notna()]

# Eliminar el año 2024 si está presente
champion_positions = champion_positions[champion_positions['year'] != 2024]

# Convertir 'year' a numérico si no lo es
champion_positions['year'] = champion_positions['year'].astype(int)

# Calcular la media de posiciones por año
mean_positions = champion_positions.groupby('year')['positionOrder'].mean().reset_index()
mean_positions = mean_positions.sort_values('year')

# Realizar regresión lineal sobre la media de posiciones
x = mean_positions['year']
y = mean_positions['positionOrder']
coefficients = np.polyfit(x, y, 1)
poly = np.poly1d(coefficients)
trendline = poly(x)

# Crear el gráfico
fig4 = go.Figure()

# Añadir boxplots
for year in sorted(champion_positions['year'].unique()):
    data = champion_positions[champion_positions['year'] == year]['positionOrder']
    fig4.add_trace(go.Box(
        y=data,
        x=[year]*len(data),
        name=str(year),
        boxmean=False,
        marker_color='lightblue',
        line=dict(color='blue'),
        showlegend=False
    ))

# Añadir la media de posiciones por año
fig4.add_trace(go.Scatter(
    x=mean_positions['year'],
    y=mean_positions['positionOrder'],
    mode='lines',
    name='Media de Posiciones',
    line=dict(color='red'),
    marker=dict(color='red'),
    hovertemplate='Año: %{x}<br>Media de Posición: %{y:.2f}'
))

# Añadir la línea de tendencia
fig4.add_trace(go.Scatter(
    x=mean_positions['year'],
    y=trendline,
    mode='lines',
    name='Tendencia',
    line=dict(color='skyblue', dash='dash'),
    hovertemplate='Año: %{x}<br>Tendencia: %{y:.2f}'
))

# Invertir el eje Y para que la posición 1 esté arriba
fig4.update_yaxes(autorange="reversed")

# Ajustar el diseño
fig4.update_layout(
    title='Distribución de las Posiciones del Campeón por Año',
    xaxis_title='Año',
    yaxis_title='Posición en Carrera',
    width=None,
    height=500,
    legend_title='Leyenda',
    hovermode='x unified'
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
Este gráfico muestra la distribución de las posiciones obtenidas por el campeón en cada carrera de cada año. Los boxplots permiten visualizar la variabilidad y consistencia en el desempeño de los campeones a lo largo de las temporadas.
""")

# Análisis 5: Velocidad Promedio de Pilotos en Carreras de F1 a lo largo de los años
st.write("## Velocidad Promedio de Pilotos en Carreras de F1 (1950-2023)")

# Preparar los datos
# Convertir columnas a tipos numéricos
numeric_columns_results = ['laps', 'milliseconds']
for col in numeric_columns_results:
    results_with_year[col] = pd.to_numeric(results_with_year[col], errors='coerce')

# Calcular la distancia total recorrida por cada piloto en cada carrera
results_with_year['distance'] = results_with_year['laps'] * results_with_year['circuit_length']  # Distancia en km

# Calcular el tiempo total en horas
results_with_year['time_hours'] = results_with_year['milliseconds'] / (1000 * 60 * 60)

# Calcular la velocidad promedio (km/h)
results_with_year['average_speed'] = results_with_year['distance'] / results_with_year['time_hours']

# Eliminar resultados inválidos
results_with_year = results_with_year[
    (results_with_year['average_speed'].notnull()) &
    (results_with_year['average_speed'] > 0) &
    (results_with_year['average_speed'] <= 300)
]

# Seleccionar el rango de años que deseas analizar
start_year = 1950
end_year = 2023

# Filtrar los datos por el rango de años
data_filtered = results_with_year[(results_with_year['year'] >= start_year) & (results_with_year['year'] <= end_year)].copy()

# Convertir 'year' a tipo entero
data_filtered['year'] = data_filtered['year'].astype(int)

# Crear una lista de años ordenados
years_order = sorted(data_filtered['year'].unique())

# Calcular la mediana de la velocidad promedio por año
median_speed_per_year = data_filtered.groupby('year')['average_speed'].median().reset_index()

# Realizar regresión lineal sobre la mediana de velocidades
x = median_speed_per_year['year']
y = median_speed_per_year['average_speed']
coefficients = np.polyfit(x, y, 1)
poly = np.poly1d(coefficients)
trendline = poly(median_speed_per_year['year'])

# Crear el boxplot con Plotly
fig5 = go.Figure()

# Añadir boxplots por año
for year in years_order:
    year_data = data_filtered[data_filtered['year'] == year]['average_speed']
    fig5.add_trace(go.Box(
        y=year_data,
        x=[year]*len(year_data),
        name=str(year),
        boxmean=False,
        marker_color='lightblue',
        line=dict(color='blue'),
        showlegend=False
    ))

# Añadir la mediana de la velocidad promedio por año
fig5.add_trace(go.Scatter(
    x=median_speed_per_year['year'],
    y=median_speed_per_year['average_speed'],
    mode='lines+markers',
    name='Mediana',
    line=dict(color='red'),
    marker=dict(color='red'),
    hovertemplate='Año: %{x}<br>Mediana Velocidad: %{y:.2f} km/h'
))

# Añadir la línea de tendencia
fig5.add_trace(go.Scatter(
    x=median_speed_per_year['year'],
    y=trendline,
    mode='lines',
    name='Tendencia',
    line=dict(color='yellow', dash='dash'),
    hovertemplate='Año: %{x}<br>Tendencia: %{y:.2f} km/h'
))

# Ajustar etiquetas y diseño
fig5.update_layout(
    title='Velocidad Promedio de Pilotos en Carreras de F1 ({}-{})'.format(start_year, end_year),
    xaxis_title='Año',
    yaxis_title='Velocidad Promedio (km/h)',
    width=None,
    height=500,
    legend_title='Leyenda',
    hovermode='x unified',
    xaxis=dict(
        tickmode='linear',
        dtick=5  # Mostrar etiqueta de año cada 5 años
    )
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
Este gráfico muestra la evolución de la velocidad promedio de los pilotos en las carreras de Fórmula 1 desde 1950 hasta 2023. Los boxplots por año permiten visualizar la dispersión de las velocidades, mientras que la línea roja representa la mediana anual y la línea amarilla punteada indica la tendencia a lo largo del tiempo.
""")

st.markdown("""
Estos análisis nos permiten tener una visión general de la evolución y distribución de la Fórmula 1 a lo largo de los años.
""")
