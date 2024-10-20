# pages/8_Carreras.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Análisis de Carreras",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Carreras 🏁")

st.markdown("""
Explora los resultados detallados de carreras individuales y visualiza el desempeño de los pilotos en cada vuelta.
""")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    races = pd.read_csv('data/races.csv')
    results = pd.read_csv('data/results.csv')
    lap_times = pd.read_csv('data/lap_times.csv')
    drivers = pd.read_csv('data/drivers.csv')
    constructors = pd.read_csv('data/constructors.csv')
    return races, results, lap_times, drivers, constructors

races, results, lap_times, drivers, constructors = load_data()

# Selección de año y carrera
years = sorted(races['year'].unique(), reverse=True)
selected_year = st.selectbox("Selecciona un año", years)

races_in_year = races[races['year'] == selected_year]
race_names = races_in_year['name'].unique()
selected_race = st.selectbox("Selecciona una carrera", race_names)

# Obtener 'raceId' de la carrera seleccionada
race_id = races_in_year[races_in_year['name'] == selected_race]['raceId'].values[0]

st.write(f"## Resultados de la Carrera: {selected_race} ({selected_year})")

# Filtrar resultados de la carrera seleccionada
race_results = results[results['raceId'] == race_id]

# Unir con 'drivers' y 'constructors' para obtener nombres
race_results = race_results.merge(drivers[['driverId', 'surname', 'forename']], on='driverId')
race_results = race_results.merge(constructors[['constructorId', 'name']], on='constructorId')

# Ordenar por posición final
race_results = race_results.sort_values(by='positionOrder')

# Seleccionar columnas relevantes
race_results = race_results[['positionOrder', 'forename', 'surname', 'name', 'laps', 'time', 'milliseconds', 'points']]

# Renombrar columnas para mejor presentación
race_results.columns = ['Posición', 'Nombre', 'Apellido', 'Constructor', 'Vueltas', 'Tiempo', 'Milisegundos', 'Puntos']

# Mostrar tabla de resultados como una tabla gráfica adaptada al modo oscuro
st.write("### Tabla de Resultados")

# Preparar los datos para la tabla
table_data = race_results.reset_index(drop=True)

# Crear una lista de colores para las filas alternadas
fill_colors = []
for i in range(len(table_data)):
    if i % 2 == 0:
        # Filas pares
        fill_colors.append('rgba(50, 50, 50, 0.5)')
    else:
        # Filas impares
        fill_colors.append('rgba(0, 0, 0, 0)')  # Transparente

# Crear una matriz de colores para las celdas
cell_fill_colors = []
for col in table_data.columns:
    cell_fill_colors.append(fill_colors)

# Crear una tabla de Plotly adaptada al modo oscuro
fig_table = go.Figure(data=[go.Table(
    header=dict(
        values=list(table_data.columns),
        fill_color='rgb(30, 30, 30)',  # Fondo oscuro para el encabezado
        align='left',
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[table_data[col] for col in table_data.columns],
        fill_color=cell_fill_colors,
        align='left',
        font=dict(color='white', size=11)
    )
)])

# Ajustar el layout de la tabla
fig_table.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
    plot_bgcolor='rgba(0,0,0,0)'    # Fondo transparente
)

# Mostrar la tabla en Streamlit
st.plotly_chart(fig_table, use_container_width=True)

# Gráfico de posiciones por vuelta
st.write("## Posición de Pilotos por Vuelta")

# Filtrar datos de 'lap_times'
lap_times_race = lap_times[lap_times['raceId'] == race_id]

if lap_times_race.empty:
    st.warning("No hay datos de tiempos de vuelta disponibles para esta carrera.")
else:
    # Unir con 'drivers' para obtener nombres
    lap_times_race = lap_times_race.merge(drivers[['driverId', 'surname']], on='driverId')

    # Calcular posición por vuelta
    lap_times_race['time_ms'] = lap_times_race['milliseconds']
    lap_times_race = lap_times_race.sort_values(['lap', 'time_ms'])

    lap_times_race['position'] = lap_times_race.groupby('lap').cumcount() + 1

    # Seleccionar pilotos a visualizar
    drivers_in_race = lap_times_race['surname'].unique()
    selected_drivers = st.multiselect("Selecciona pilotos para visualizar", drivers_in_race, default=drivers_in_race[:5])

    # Filtrar datos
    lap_times_race_filtered = lap_times_race[lap_times_race['surname'].isin(selected_drivers)]

    fig = px.line(lap_times_race_filtered, x='lap', y='position', color='surname',
                  title='Posición de Pilotos por Vuelta', labels={'lap': 'Vuelta', 'position': 'Posición', 'surname': 'Piloto'})
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(hovermode='x unified')

    st.plotly_chart(fig, use_container_width=True)

    # Estadísticas específicas de la carrera
    st.write("## Estadísticas de la Carrera")

    # Número total de vueltas
    total_laps = lap_times_race['lap'].max()
    st.write(f"**Total de vueltas:** {total_laps}")

    # Piloto con vuelta más rápida
    fastest_lap = lap_times_race.loc[lap_times_race['milliseconds'].idxmin()]
    fastest_driver = fastest_lap['surname']
    fastest_lap_number = fastest_lap['lap']
    fastest_time_ms = fastest_lap['milliseconds']
    # Convertir tiempo de milisegundos a formato mm:ss.SSS
    fastest_time_formatted = pd.to_timedelta(fastest_time_ms, unit='ms')
    fastest_time_formatted = str(fastest_time_formatted)[10:]  # Obtener solo minutos, segundos y milisegundos
    st.write(f"**Vuelta más rápida:** Vuelta {fastest_lap_number} por {fastest_driver} con un tiempo de {fastest_time_formatted}")

    # Gráfico de tiempos de vuelta
    st.write("### Tiempos de Vuelta por Piloto")

    # Convertir milisegundos a segundos para una mejor interpretación
    lap_times_race_filtered['time_seconds'] = lap_times_race_filtered['milliseconds'] / 1000

    fig_times = px.line(lap_times_race_filtered, x='lap', y='time_seconds', color='surname',
                        title='Tiempos de Vuelta por Piloto', labels={'lap': 'Vuelta', 'time_seconds': 'Tiempo (segundos)', 'surname': 'Piloto'})

    fig_times.update_layout(hovermode='x unified')

    st.plotly_chart(fig_times, use_container_width=True)
