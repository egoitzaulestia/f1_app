# pages/8_Temporadas.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Análisis de Temporadas",
    page_icon="🏆",
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

# Selección de años para comparación
years = sorted(races['year'].unique(), reverse=True)
selected_years = st.multiselect("Selecciona uno o más años para comparar", years, default=years[:2])

if not selected_years:
    st.warning("Por favor, selecciona al menos un año para continuar.")
    st.stop()

# Opciones para seleccionar entre Pilotos y Constructores
option = st.radio("Selecciona el tipo de análisis", ('Pilotos', 'Constructores'))

if option == 'Pilotos':
    # Análisis de Pilotos

    # Unir datos para obtener el año y la ronda de cada carrera
    merged_data = pd.merge(driver_standings, races[['raceId', 'year', 'round']], on='raceId')
    merged_data = pd.merge(merged_data, drivers[['driverId', 'surname']], on='driverId')

    # Filtrar para los años seleccionados
    filtered_data = merged_data[merged_data['year'].isin(selected_years)]

    # Crear puntos acumulativos por piloto y año
    filtered_data = filtered_data.sort_values(by=['year', 'driverId', 'round'])
    filtered_data['puntos_acumulados'] = filtered_data.groupby(['year', 'driverId'])['points'].cumsum()

    # Seleccionar los top 5 pilotos por año
    top_pilotos_list = []
    for year in selected_years:
        data_year = filtered_data[filtered_data['year'] == year]
        top_pilotos = data_year.groupby('surname').tail(1).sort_values(by='puntos_acumulados', ascending=False).head(5)
        top_pilotos_list.append(top_pilotos)

    # Concatenar los datos de los top pilotos
    top_pilotos_data = pd.concat(top_pilotos_list)
    top_pilotos_names = top_pilotos_data['surname'].unique()

    # Asignar colores dinámicos
    colors = px.colors.qualitative.Plotly  # Colores de Plotly por defecto
    color_map = {name: colors[i % len(colors)] for i, name in enumerate(top_pilotos_names)}

    # Crear gráfico lineal de puntos acumulados por piloto
    fig = go.Figure()

    for year in selected_years:
        data_year = filtered_data[filtered_data['year'] == year]
        for piloto in top_pilotos_names:
            piloto_data = data_year[data_year['surname'] == piloto]
            if not piloto_data.empty:
                fig.add_trace(go.Scatter(
                    x=piloto_data['round'],
                    y=piloto_data['puntos_acumulados'],
                    mode='lines+markers',
                    name=f"{piloto} ({year})",
                    line=dict(color=color_map[piloto]),
                    legendgroup=piloto,
                    showlegend=True
                ))

    # Configuración del gráfico lineal
    fig.update_layout(
        title=f"Desempeño de los Mejores Pilotos en las Temporadas Seleccionadas",
        xaxis_title="Rondas de Carrera",
        yaxis_title="Puntos Acumulados",
        legend_title="Pilotos",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Crear gráfico de barras comparativo
    fig_bar = go.Figure()

    for year in selected_years:
        top_pilotos_year = top_pilotos_data[top_pilotos_data['year'] == year]
        fig_bar.add_trace(go.Bar(
            x=top_pilotos_year['surname'],
            y=top_pilotos_year['puntos_acumulados'],
            text=top_pilotos_year['puntos_acumulados'],
            textposition='auto',
            name=str(year),
            marker=dict(color=colors[selected_years.index(year) % len(colors)]),
        ))

    # Configuración del gráfico de barras
    fig_bar.update_layout(
        title=f"Comparación de los Mejores Pilotos en las Temporadas Seleccionadas",
        xaxis_title="Pilotos",
        yaxis_title="Puntos Totales",
        barmode='group',
        legend_title="Año"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

elif option == 'Constructores':
    # Análisis de Constructores

    # Unir datos para obtener el año y la ronda de cada carrera
    merged_data = pd.merge(constructor_standings, races[['raceId', 'year', 'round']], on='raceId')
    merged_data = pd.merge(merged_data, constructors[['constructorId', 'name']], on='constructorId')

    # Filtrar para los años seleccionados
    filtered_data = merged_data[merged_data['year'].isin(selected_years)]

    # Crear puntos acumulativos por constructor y año
    filtered_data = filtered_data.sort_values(by=['year', 'constructorId', 'round'])
    filtered_data['puntos_acumulados'] = filtered_data.groupby(['year', 'constructorId'])['points'].cumsum()

    # Seleccionar los top 5 constructores por año
    top_constructors_list = []
    for year in selected_years:
        data_year = filtered_data[filtered_data['year'] == year]
        top_constructors = data_year.groupby('name').tail(1).sort_values(by='puntos_acumulados', ascending=False).head(5)
        top_constructors_list.append(top_constructors)

    # Concatenar los datos de los top constructores
    top_constructors_data = pd.concat(top_constructors_list)
    top_constructors_names = top_constructors_data['name'].unique()

    # Asignar colores dinámicos
    colors = px.colors.qualitative.Plotly  # Colores de Plotly por defecto
    color_map = {name: colors[i % len(colors)] for i, name in enumerate(top_constructors_names)}

    # Crear gráfico lineal de puntos acumulados por constructor
    fig = go.Figure()

    for year in selected_years:
        data_year = filtered_data[filtered_data['year'] == year]
        for constructor in top_constructors_names:
            constructor_data = data_year[data_year['name'] == constructor]
            if not constructor_data.empty:
                fig.add_trace(go.Scatter(
                    x=constructor_data['round'],
                    y=constructor_data['puntos_acumulados'],
                    mode='lines+markers',
                    name=f"{constructor} ({year})",
                    line=dict(color=color_map[constructor]),
                    legendgroup=constructor,
                    showlegend=True
                ))

    # Configuración del gráfico lineal
    fig.update_layout(
        title=f"Desempeño de los Mejores Constructores en las Temporadas Seleccionadas",
        xaxis_title="Rondas de Carrera",
        yaxis_title="Puntos Acumulados",
        legend_title="Constructores",
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Crear gráfico de barras comparativo
    fig_bar = go.Figure()

    for year in selected_years:
        top_constructors_year = top_constructors_data[top_constructors_data['year'] == year]
        fig_bar.add_trace(go.Bar(
            x=top_constructors_year['name'],
            y=top_constructors_year['puntos_acumulados'],
            text=top_constructors_year['puntos_acumulados'],
            textposition='auto',
            name=str(year),
            marker=dict(color=colors[selected_years.index(year) % len(colors)]),
        ))

    # Configuración del gráfico de barras
    fig_bar.update_layout(
        title=f"Comparación de los Mejores Constructores en las Temporadas Seleccionadas",
        xaxis_title="Constructores",
        yaxis_title="Puntos Totales",
        barmode='group',
        legend_title="Año"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.write("Seleccione una opción válida.")
