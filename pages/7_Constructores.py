# pages/7_Constructores.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análisis de Constructores",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Constructores 🏢")

st.markdown("""
Explora los constructores de Fórmula 1 con más éxito y su desempeño a lo largo de los años.
""")

# Cargar datasets
constructors = pd.read_csv('data/constructors.csv')
results = pd.read_csv('data/results.csv')
races = pd.read_csv('data/races.csv')

# Merge de datos
constructor_results = results.merge(constructors, on='constructorId').merge(races, on='raceId')

# Calcular puntos por constructor
points_by_constructor = constructor_results.groupby(['constructorId', 'name'])['points'].sum().reset_index()

# Top 10 constructores con más puntos
top_teams = points_by_constructor.sort_values(by='points', ascending=False).head(10)

# Gráfico
fig = px.bar(top_teams, x='points', y='name', orientation='h',
             title='Top 10 Equipos con Más Puntos', labels={'points': 'Puntos', 'name': 'Equipo'})
fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig)

# Detalles de un constructor específico
st.write("## Detalles del Constructor")

team_list = constructors['name'].unique()
selected_team = st.selectbox("Selecciona un equipo", team_list)

team_data = constructor_results[constructor_results['name'] == selected_team]

# Estadísticas
total_races = team_data['raceId'].nunique()
total_wins = team_data[team_data['positionOrder'] == 1]['raceId'].nunique()
total_points = team_data['points'].sum()

st.write(f"### Estadísticas de {selected_team}")
st.write(f"**Total de carreras:** {total_races}")
st.write(f"**Total de victorias:** {total_wins}")
st.write(f"**Total de puntos:** {total_points}")

# Gráfico de puntos a lo largo de los años
points_per_year = team_data.groupby('year')['points'].sum().reset_index()

fig2 = px.line(points_per_year, x='year', y='points', title=f'Evolución de Puntos de {selected_team}',
               labels={'year': 'Año', 'points': 'Puntos'})
st.plotly_chart(fig2)
