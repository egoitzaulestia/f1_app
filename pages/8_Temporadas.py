# pages/8_Temporadas.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Análisis de Temporadas",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Temporadas 🏆")

st.markdown("""
Explora el desempeño de los pilotos y constructores a lo largo de diferentes temporadas de Fórmula 1.
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

# ---------------------------
# Sección 1: Análisis de Desempeño en una Temporada
st.write("## Desempeño en una Temporada")

# Opción para seleccionar entre Pilotos y Constructores
option = st.radio("Selecciona el tipo de análisis", ('Pilotos', 'Constructores'), key='option_desempeno')

# Selección de año
years = sorted(races['year'].unique(), reverse=True)
selected_year = st.selectbox("Selecciona un año", years, key='selected_year')

if option == 'Pilotos':
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
        title=f"Posición Final de los 10 Mejores Pilotos ({selected_year})",
        xaxis_title="Pilotos",
        yaxis_title="Puntos Totales",
        showlegend=False
    )

    # Mostrar el gráfico de barras
    st.plotly_chart(fig_bar, use_container_width=True)

elif option == 'Constructores':
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
        title=f"Posición Final de los Constructores ({selected_year})",
        xaxis_title="Constructores",
        yaxis_title="Puntos Totales",
        showlegend=False
    )

    # Mostrar el gráfico de barras
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.write("Seleccione una opción válida.")

# ---------------------------
# Sección 2: Comparación de Pilotos a través de Temporadas
st.write("## Comparación de Pilotos a través de Temporadas")

# Selección de años para comparación
selected_years = st.multiselect("Selecciona uno o más años para comparar", years, default=years[:2])

if not selected_years:
    st.warning("Por favor, selecciona al menos un año para continuar.")
    st.stop()

# Unir datos para obtener el año y la ronda de cada carrera
merged_data = pd.merge(driver_standings, races[['raceId', 'year', 'round']], on='raceId')
merged_data = pd.merge(merged_data, drivers[['driverId', 'surname']], on='driverId')

# Filtrar para los años seleccionados
filtered_data = merged_data[merged_data['year'].isin(selected_years)]

# Crear puntos acumulados totales por piloto y año
total_points = filtered_data.groupby(['year', 'surname'])['points'].sum().reset_index()

# Seleccionar los top 5 pilotos por año
top_pilotos_list = []
for year in selected_years:
    data_year = total_points[total_points['year'] == year]
    top_pilotos = data_year.sort_values(by='points', ascending=False).head(5)
    top_pilotos_list.append(top_pilotos)

# Concatenar los datos de los top pilotos
top_pilotos_data = pd.concat(top_pilotos_list)
top_pilotos_names = top_pilotos_data['surname'].unique()

# Asignar colores dinámicos
colors = px.colors.qualitative.Plotly  # Colores de Plotly por defecto
color_map = {year: colors[i % len(colors)] for i, year in enumerate(selected_years)}

# Crear gráfico de barras comparativo
fig_bar_comparison = go.Figure()

for year in selected_years:
    top_pilotos_year = top_pilotos_data[top_pilotos_data['year'] == year]
    fig_bar_comparison.add_trace(go.Bar(
        x=top_pilotos_year['surname'],
        y=top_pilotos_year['points'],
        text=top_pilotos_year['points'],
        textposition='auto',
        name=str(year),
        marker=dict(color=color_map[year]),
    ))

# Configuración del gráfico de barras
fig_bar_comparison.update_layout(
    title=f"Comparación de los Mejores Pilotos en las Temporadas Seleccionadas",
    xaxis_title="Pilotos",
    yaxis_title="Puntos Totales",
    barmode='group',
    legend_title="Año"
)

st.plotly_chart(fig_bar_comparison, use_container_width=True)
