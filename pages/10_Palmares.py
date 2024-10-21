# pages/2_Palmares.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Palmarés",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Palmarés 🥇🥈🥉")

st.markdown("""
A continuación, puedes explorar los datos del palmarés en la historia de la Fórmula 1.
""")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    results = pd.read_csv('data/results.csv', na_values=['\\N', 'NA'])
    races = pd.read_csv('data/races.csv', na_values=['\\N', 'NA'])
    drivers = pd.read_csv('data/drivers.csv', na_values=['\\N', 'NA'])
    return results, races, drivers

results, races, drivers = load_data()

# Unir 'results' con 'races' para obtener el año de cada carrera
results_races = results.merge(races[['raceId', 'year']], on='raceId', how='left')

# Unir con 'drivers' para obtener los nombres de los pilotos
results_races_drivers = results_races.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')

# Identificar apellidos duplicados
surname_counts = drivers['surname'].value_counts()
duplicate_surnames = surname_counts[surname_counts > 1].index.tolist()

# Crear columna 'display_name' que añade la inicial del nombre si el apellido está duplicado
def get_display_name(row):
    if row['surname'] in duplicate_surnames:
        return f"{row['forename'][0]}. {row['surname']}"
    else:
        return row['surname']

# Aplicar la función para crear 'display_name' en 'drivers' y en 'results_races_drivers'
drivers['display_name'] = drivers.apply(get_display_name, axis=1)
results_races_drivers['display_name'] = results_races_drivers.apply(get_display_name, axis=1)

# Filtrar los resultados donde 'positionOrder' es 1 (ganador de la carrera)
winners = results_races_drivers[results_races_drivers['positionOrder'] == 1]

# Crear la tabla pivote
pivot_table = winners.pivot_table(
    index='display_name',
    columns='year',
    values='raceId',
    aggfunc='count',
    fill_value=0
)

# Añadir una columna con el total de victorias
pivot_table['Total'] = pivot_table.sum(axis=1)

# Calcular el año promedio de las victorias de cada piloto
mean_victory_year = winners.groupby('display_name')['year'].mean()

# Añadir el año promedio al pivot_table
pivot_table['mean_year'] = mean_victory_year

# Ordenar la tabla por el año promedio de victorias en orden descendente (pilotos más recientes arriba)
pivot_table = pivot_table.sort_values('mean_year', ascending=False)

# Guardar 'Total' para filtrar después
total_victories = pivot_table['Total']

# Eliminar las columnas 'Total' y 'mean_year' para el heatmap
pivot_table_heatmap = pivot_table.drop(['Total', 'mean_year'], axis=1)

# Selector para el número mínimo de victorias
num_vic = st.slider('Número mínimo de victorias para mostrar en el gráfico', min_value=1, max_value=30, value=5)

# Filtrar los pilotos con al menos 'num_vic' victorias
pivot_table_heatmap_filtered = pivot_table_heatmap[total_victories >= num_vic]

if pivot_table_heatmap_filtered.empty:
    st.warning(f"No hay pilotos con al menos {num_vic} victorias.")
else:
    # Resetear el índice para usar en Plotly
    pivot_table_heatmap_filtered = pivot_table_heatmap_filtered.reset_index()

    # Convertir los datos al formato largo para Plotly
    heatmap_data = pivot_table_heatmap_filtered.melt(id_vars='display_name', var_name='Año', value_name='Victorias')

    # Crear el heatmap con Plotly
    fig = px.imshow(
        pivot_table_heatmap_filtered.set_index('display_name'),
        aspect='auto',
        color_continuous_scale='Blues',
        labels=dict(x="Año", y="Piloto", color="Número de Victorias")
    )

    fig.update_layout(
        title=f'Pilotos con al menos {num_vic} victorias en Fórmula 1 (por año)',
        xaxis_nticks=len(pivot_table_heatmap_filtered.columns) - 1,  # Ajustar número de ticks en el eje x
        yaxis_autorange='reversed'
    )

    # Ajustar tamaño de la figura
    fig.update_layout(height=800)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


st.markdown("""
Este gráfico interactivo muestra un mapa de calor de los pilotos de Fórmula 1 con más victorias, visualizando cuántas veces ganaron en cada año de competición. Los pilotos están ordenados según el promedio del año de sus victorias, destacando a las generaciones más recientes, y permite filtrar por el número mínimo de triunfos, ofreciendo una vista clara de los dominadores históricos de la F1.""")
