# # pages/8_Carreras.py

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.set_page_config(
#     page_title="Análisis de Carreras",
#     page_icon="🏎️",
#     layout="wide",
# )

# st.write("# Análisis de Carreras 🏁")

# st.markdown("""
# Explora los resultados de carreras específicas y visualiza el desempeño de los pilotos en cada vuelta.
# """)

# # Cargar datasets
# lap_times = pd.read_csv('data/lap_times.csv')
# races = pd.read_csv('data/races.csv')
# drivers = pd.read_csv('data/drivers.csv')

# # Selección de año y carrera
# years = races['year'].unique()
# selected_year = st.selectbox("Selecciona un año", sorted(years, reverse=True))

# races_in_year = races[races['year'] == selected_year]
# race_names = races_in_year['name'].unique()
# selected_race = st.selectbox("Selecciona una carrera", race_names)

# # Obtener 'raceId' de la carrera seleccionada
# race_id = races_in_year[races_in_year['name'] == selected_race]['raceId'].values[0]

# # Filtrar datos de 'lap_times'
# lap_times_race = lap_times[lap_times['raceId'] == race_id]

# # Unir con 'drivers' para obtener nombres
# lap_times_race = lap_times_race.merge(drivers[['driverId', 'surname']], on='driverId')

# # Gráfico de posición por vuelta
# st.write("## Posición de Pilotos por Vuelta")

# # Calcular posición por vuelta
# lap_times_race['time_ms'] = lap_times_race['milliseconds']
# lap_times_race = lap_times_race.sort_values(['lap', 'time_ms'])

# lap_times_race['position'] = lap_times_race.groupby('lap').cumcount() + 1

# # Seleccionar pilotos a visualizar
# drivers_in_race = lap_times_race['surname'].unique()
# selected_drivers = st.multiselect("Selecciona pilotos", drivers_in_race, default=drivers_in_race[:5])

# # Filtrar datos
# lap_times_race_filtered = lap_times_race[lap_times_race['surname'].isin(selected_drivers)]

# fig = px.line(lap_times_race_filtered, x='lap', y='position', color='surname',
#               title='Posición de Pilotos por Vuelta', labels={'lap': 'Vuelta', 'position': 'Posición', 'surname': 'Piloto'})
# fig.update_yaxes(autorange="reversed")

# st.plotly_chart(fig)


# pages/9_Carreras.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Análisis de Carreras",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Carreras 🏁")

st.markdown("""
Explora los resultados de las temporadas y visualiza el desempeño de los pilotos y constructores a lo largo del año.
""")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    races = pd.read_csv('data/races.csv')
    driver_standings = pd.read_csv('data/driver_standings.csv')
    drivers = pd.read_csv('data/drivers.csv')
    constructor_standings = pd.read_csv('data/constructor_standings.csv')
    constructors = pd.read_csv('data/constructors.csv')
    return races, driver_standings, drivers, constructor_standings, constructors

races, driver_standings, drivers, constructor_standings, constructors = load_data()

# Opciones para seleccionar entre Pilotos y Constructores
option = st.radio("Selecciona el tipo de análisis", ('Pilotos', 'Constructores'))

# Selección de año
years = sorted(races['year'].unique(), reverse=True)
selected_year = st.selectbox("Selecciona un año", years)

if option == 'Pilotos':
    # Análisis de Pilotos

    # Unir datos para obtener el año y la ronda de cada carrera
    merged_data = pd.merge(driver_standings, races[['raceId', 'year', 'round']], on='raceId')
    merged_data = pd.merge(merged_data, drivers[['driverId', 'surname']], on='driverId')

    # Filtrar para el año seleccionado
    filtered_data = merged_data[merged_data['year'] == selected_year]

    # Crear puntos acumulativos por piloto
    filtered_data = filtered_data.sort_values(by=['driverId', 'round'])
    filtered_data['puntos_acumulados'] = filtered_data.groupby('driverId')['points'].cumsum()

    # Filtrar los mejores 10 pilotos por puntos acumulados
    top_10_pilotos = filtered_data.groupby('surname').tail(1).sort_values(by='puntos_acumulados', ascending=False).head(10)
    top_10_names = top_10_pilotos['surname'].unique()

    # Asignar colores dinámicos usando Plotly Express, basado en los nombres de los pilotos
    colors = px.colors.qualitative.Plotly  # Colores de Plotly por defecto
    color_map = {name: colors[i % len(colors)] for i, name in enumerate(top_10_names)}

    # Crear gráfico lineal de puntos acumulados por piloto
    fig = go.Figure()

    for piloto in top_10_names:
        piloto_data = filtered_data[filtered_data['surname'] == piloto]
        fig.add_trace(go.Scatter(
            x=piloto_data['round'],
            y=piloto_data['puntos_acumulados'],
            mode='lines+markers',
            name=piloto,
            line=dict(color=color_map[piloto])  # Usar colores dinámicos
        ))

    # Configuración del gráfico lineal
    fig.update_layout(
        title=f"Desempeño de los Mejores Pilotos a lo largo de la Temporada ({selected_year})",
        xaxis_title="Rondas de Carrera",
        yaxis_title="Puntos Acumulados",
        legend_title="Pilotos"
    )

    # Mostrar el gráfico
    st.plotly_chart(fig, use_container_width=True)

    # Crear el gráfico de barras con colores correspondientes
    fig_bar = go.Figure()

    for piloto in top_10_names:
        piloto_data = top_10_pilotos[top_10_pilotos['surname'] == piloto]
        fig_bar.add_trace(go.Bar(
            x=[piloto_data['surname'].values[0]],
            y=piloto_data['puntos_acumulados'],
            text=piloto_data['puntos_acumulados'],
            textposition='auto',
            name=piloto,  # Asignar nombre correcto a cada barra en la leyenda
            marker=dict(color=color_map[piloto]),  # Usar el mismo color dinámico
            width=0.7  # Ajustar el ancho de las barras
        ))

    # Configuración del gráfico de barras
    fig_bar.update_layout(
        title=f"Posición Actual de los 10 Mejores Pilotos ({selected_year})",
        xaxis_title="Pilotos",
        yaxis_title="Puntos Totales",
        showlegend=False
    )

    # Mostrar el gráfico de barras
    st.plotly_chart(fig_bar, use_container_width=True)

elif option == 'Constructores':
    # Análisis de Constructores

    # Unir datos para obtener el año y la ronda de cada carrera
    merged_data = pd.merge(constructor_standings, races[['raceId', 'year', 'round']], on='raceId')
    merged_data = pd.merge(merged_data, constructors[['constructorId', 'name']], on='constructorId')

    # Filtrar para el año seleccionado
    filtered_data = merged_data[merged_data['year'] == selected_year]

    # Crear puntos acumulativos por constructor
    filtered_data = filtered_data.sort_values(by=['constructorId', 'round'])
    filtered_data['puntos_acumulados'] = filtered_data.groupby('constructorId')['points'].cumsum()

    # Ordenar los standings actuales
    current_standings = filtered_data.groupby('constructorId').tail(1)
    current_standings = current_standings.sort_values(by='puntos_acumulados', ascending=False)

    # Asignar colores dinámicos usando Plotly Express, basado en los nombres de los constructores
    colors = px.colors.qualitative.Plotly  # Colores de Plotly por defecto
    constructor_names = current_standings['name'].unique()  # Usar los nombres ya ordenados por puntos
    color_map = {name: colors[i % len(colors)] for i, name in enumerate(constructor_names)}

    # Crear gráfico lineal de puntos acumulados por constructor
    fig = go.Figure()

    for constructor in constructor_names:
        constructor_data = filtered_data[filtered_data['name'] == constructor]
        fig.add_trace(go.Scatter(
            x=constructor_data['round'],
            y=constructor_data['puntos_acumulados'],
            mode='lines+markers',
            name=constructor,
            line=dict(color=color_map[constructor])  # Usar colores dinámicos
        ))

    # Configuración del gráfico lineal
    fig.update_layout(
        title=f"Desempeño de los Constructores a lo largo de la Temporada ({selected_year})",
        xaxis_title="Rondas de Carrera",
        yaxis_title="Puntos Acumulados",
        legend_title="Constructores"
    )

    # Mostrar el gráfico de líneas
    st.plotly_chart(fig, use_container_width=True)

    # Crear el gráfico de barras con colores correspondientes y ordenado
    fig_bar = go.Figure()

    for constructor in constructor_names:
        constructor_data = current_standings[current_standings['name'] == constructor]
        fig_bar.add_trace(go.Bar(
            x=[constructor_data['name'].values[0]],
            y=constructor_data['puntos_acumulados'],
            text=constructor_data['puntos_acumulados'],
            textposition='auto',
            marker=dict(color=color_map[constructor]),  # Usar el mismo color dinámico
            width=0.7,  # Ajustar el ancho de las barras
            name=constructor  # Asociar nombre a la leyenda correctamente
        ))

    # Configuración del gráfico de barras
    fig_bar.update_layout(
        title=f"Posición Actual de los Constructores ({selected_year})",
        xaxis_title="Constructores",
        yaxis_title="Puntos Totales",
        showlegend=False
    )

    # Mostrar el gráfico de barras
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.write("Seleccione una opción válida.")
