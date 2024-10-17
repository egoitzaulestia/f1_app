# pages/8_Carreras.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análisis de Carreras",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Carreras 🏁")

st.markdown("""
Explora los resultados de carreras específicas y visualiza el desempeño de los pilotos en cada vuelta.
""")

# Cargar datasets
lap_times = pd.read_csv('data/lap_times.csv')
races = pd.read_csv('data/races.csv')
drivers = pd.read_csv('data/drivers.csv')

# Selección de año y carrera
years = races['year'].unique()
selected_year = st.selectbox("Selecciona un año", sorted(years, reverse=True))

races_in_year = races[races['year'] == selected_year]
race_names = races_in_year['name'].unique()
selected_race = st.selectbox("Selecciona una carrera", race_names)

# Obtener 'raceId' de la carrera seleccionada
race_id = races_in_year[races_in_year['name'] == selected_race]['raceId'].values[0]

# Filtrar datos de 'lap_times'
lap_times_race = lap_times[lap_times['raceId'] == race_id]

# Unir con 'drivers' para obtener nombres
lap_times_race = lap_times_race.merge(drivers[['driverId', 'surname']], on='driverId')

# Gráfico de posición por vuelta
st.write("## Posición de Pilotos por Vuelta")

# Calcular posición por vuelta
lap_times_race['time_ms'] = lap_times_race['milliseconds']
lap_times_race = lap_times_race.sort_values(['lap', 'time_ms'])

lap_times_race['position'] = lap_times_race.groupby('lap').cumcount() + 1

# Seleccionar pilotos a visualizar
drivers_in_race = lap_times_race['surname'].unique()
selected_drivers = st.multiselect("Selecciona pilotos", drivers_in_race, default=drivers_in_race[:5])

# Filtrar datos
lap_times_race_filtered = lap_times_race[lap_times_race['surname'].isin(selected_drivers)]

fig = px.line(lap_times_race_filtered, x='lap', y='position', color='surname',
              title='Posición de Pilotos por Vuelta', labels={'lap': 'Vuelta', 'position': 'Posición', 'surname': 'Piloto'})
fig.update_yaxes(autorange="reversed")

st.plotly_chart(fig)
