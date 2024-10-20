# # pages/7_Constructores.py

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# st.set_page_config(
#     page_title="Análisis de Constructores",
#     page_icon="🏎️",
#     layout="wide",
# )

# st.write("# Análisis de Constructores 🏆")

# # ---------------------------
# # Cargar datasets
# @st.cache_data
# def load_data():
#     constructors = pd.read_csv('data/constructors.csv')
#     results = pd.read_csv('data/results.csv')
#     races = pd.read_csv('data/races.csv')
#     return constructors, results, races

# constructors, results, races = load_data()

# # Verificar si 'points' está presente en results
# if 'points' not in results.columns:
#     st.error("El dataset 'results.csv' no contiene la columna 'points'. No se pueden calcular las posiciones finales en el campeonato correctamente.")
#     st.stop()

# # ---------------------------
# # Crear 'display_name' para los constructores
# constructor_counts = constructors['name'].value_counts()
# constructors['display_name'] = constructors.apply(
#     lambda row: f"{row['name']} ({row['nationality']})" if constructor_counts[row['name']] > 1 else row['name'],
#     axis=1
# )

# # Merge de datos con display_name
# constructor_results = results.merge(constructors[['constructorId', 'display_name']], on='constructorId').merge(races, on='raceId')

# # Calcular victorias por constructor
# wins = constructor_results[constructor_results['positionOrder'] == 1]
# wins_by_constructor = wins.groupby(['constructorId', 'display_name'])['raceId'].count().reset_index()
# wins_by_constructor = wins_by_constructor.rename(columns={'raceId': 'wins'})

# # Top 10 constructores con más victorias
# top_winners = wins_by_constructor.sort_values(by='wins', ascending=False).head(10)

# # Gráfico de Top 10 Constructores
# fig = px.bar(
#     top_winners,
#     x='wins',
#     y='display_name',
#     orientation='h',
#     title='Top 10 Constructores con Más Victorias',
#     labels={'wins': 'Victorias', 'display_name': 'Constructor'},
#     color='wins',
#     color_continuous_scale='Blues'
# )
# fig.update_layout(yaxis=dict(autorange="reversed"))

# st.plotly_chart(fig, use_container_width=True)

# st.write("## Detalles del Constructor")

# # Lista de constructores únicos con display_name
# constructors_list = constructors['display_name'].unique()
# selected_constructor = st.selectbox("Selecciona un constructor", constructors_list)

# # Filtrar datos del constructor seleccionado
# constructor_data = constructor_results[constructor_results['display_name'] == selected_constructor]

# # Mostrar estadísticas
# st.write(f"### Estadísticas de {selected_constructor}")

# # Total de carreras
# total_races = constructor_data['raceId'].nunique()
# st.write(f"**Total de carreras:** {total_races}")

# # Total de victorias
# total_wins = constructor_data[constructor_data['positionOrder'] == 1]['raceId'].nunique()
# st.write(f"**Total de victorias:** {total_wins}")

# # Total de puntos
# total_points = constructor_data['points'].sum()
# st.write(f"**Total de puntos:** {total_points}")

# # ---------------------------
# # Calcular posición en el campeonato basado en puntos
# championship_points = constructor_results.groupby(['year', 'display_name'])['points'].sum().reset_index()

# # Calcular la posición en el campeonato por año
# championship_points['championship_position'] = championship_points.groupby('year')['points'].rank(method='dense', ascending=False).astype(int)

# # Filtrar para el constructor seleccionado
# constructor_championship = championship_points[championship_points['display_name'] == selected_constructor]

# # Añadir una columna que marque si fue campeón
# constructor_championship['champion'] = constructor_championship['championship_position'].apply(lambda x: 'Champion' if x == 1 else '')

# # Crear el gráfico de líneas para posición en el campeonato
# fig_championship = px.line(
#     constructor_championship,
#     x='year',
#     y='championship_position',
#     title=f'Posición Final de {selected_constructor} en el Campeonato',
#     labels={'year': 'Año', 'championship_position': 'Posición'},
#     markers=False
# )

# # Filtrar los años en los que fue campeón
# champion_years = constructor_championship[constructor_championship['champion'] == 'Champion']

# # Añadir estrellas para cuando fue campeón
# if not champion_years.empty:
#     fig_championship.add_trace(
#         go.Scatter(
#             x=champion_years['year'],
#             y=champion_years['championship_position'],
#             mode='markers',
#             marker=dict(size=15, color='yellow', symbol='star'),
#             name='Campeón'
#         )
#     )

# # Invertir el eje Y para que 1 esté en la parte superior
# fig_championship.update_yaxes(autorange="reversed")

# # Añadir leyenda manual
# fig_championship.update_layout(
#     legend=dict(
#         title="Leyenda",
#         itemsizing='constant'
#     )
# )

# st.plotly_chart(fig_championship, use_container_width=True)

# # ---------------------------
# # Gráfico: Heatmap de posiciones por carrera y año usando Plotly Graph Objects

# # Crear una tabla pivote con los resultados de las carreras por circuito y año
# heatmap_data = constructor_data.pivot_table(index='name', columns='year', values='positionOrder', aggfunc='min')

# # Obtener el máximo puesto en los datos
# max_position = constructor_data['positionOrder'].max()

# # Reemplazar NaN con max_position +1 para indicar carreras no corridas
# heatmap_data = heatmap_data.fillna(max_position + 1)

# # Crear una matriz de texto donde las celdas con max_position +1 tienen ''
# text_matrix = heatmap_data.applymap(lambda x: '' if x == (max_position + 1) else str(int(x)))

# # Definir una escala de colores personalizada
# def get_custom_color_scale():
#     """
#     Crear una escala de colores que asigna un color oscuro al primer puesto (1),
#     y va aclarando progresivamente hacia el último puesto.
#     Las celdas vacías (carreras no corridas) tendrán el mismo color que el último puesto.
#     """
#     return px.colors.sequential.Blues

# # Crear el heatmap con Plotly Graph Objects
# fig_heatmap = go.Figure(data=go.Heatmap(
#     z=heatmap_data.values,
#     x=heatmap_data.columns,
#     y=heatmap_data.index,
#     colorscale=get_custom_color_scale(),
#     colorbar=dict(title='Posición'),
#     text=text_matrix.values,
#     hoverinfo='text',
#     texttemplate='%{text}',
#     showscale=True,
#     line=dict(width=1, color='black')  # Añadir líneas de recuadro
# ))

# # Configurar el layout
# fig_heatmap.update_layout(
#     title=f'Posiciones de {selected_constructor} en las Carreras (por año)',
#     xaxis_title='Año',
#     yaxis_title='Circuito',
#     width=1200,
#     height=800
# )

# st.plotly_chart(fig_heatmap, use_container_width=True)

# st.markdown(f"""
# Este heatmap muestra las posiciones de {selected_constructor} en las carreras a lo largo de los años. Las celdas vacías representan las carreras no corridas (mismo color que el último puesto). Las áreas más oscuras indican mejores posiciones (1), mientras que las más claras representan posiciones más altas.
# """)


# pages/7_Constructores.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Análisis de Constructores",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Constructores 🏆")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    constructors = pd.read_csv('data/constructors.csv')
    results = pd.read_csv('data/results.csv')
    races = pd.read_csv('data/races.csv')
    return constructors, results, races

constructors, results, races = load_data()

# Verificar si 'points' está presente en results
if 'points' not in results.columns:
    st.error("El dataset 'results.csv' no contiene la columna 'points'. No se pueden calcular las posiciones finales en el campeonato correctamente.")
    st.stop()

# ---------------------------
# Crear 'display_name' para los constructores
constructor_counts = constructors['name'].value_counts()
constructors['display_name'] = constructors.apply(
    lambda row: f"{row['name']} ({row['nationality']})" if constructor_counts[row['name']] > 1 else row['name'],
    axis=1
)

# Merge de datos con display_name
constructor_results = results.merge(constructors[['constructorId', 'display_name']], on='constructorId').merge(races[['raceId', 'year', 'name']], on='raceId')

# Renombrar 'name' de 'races' a 'race_name'
constructor_results = constructor_results.rename(columns={'name': 'race_name'})

# Calcular victorias por constructor
wins = constructor_results[constructor_results['positionOrder'] == 1]
wins_by_constructor = wins.groupby(['constructorId', 'display_name'])['raceId'].count().reset_index()
wins_by_constructor = wins_by_constructor.rename(columns={'raceId': 'wins'})

# Top 10 constructores con más victorias
top_winners = wins_by_constructor.sort_values(by='wins', ascending=False).head(10)

# Gráfico de Top 10 Constructores
fig = px.bar(
    top_winners,
    x='wins',
    y='display_name',
    orientation='h',
    title='Top 10 Constructores con Más Victorias',
    labels={'wins': 'Victorias', 'display_name': 'Constructor'},
    color='wins',
    color_continuous_scale='Blues'
)
fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig, use_container_width=True)

st.write("## Detalles del Constructor")

# Lista de constructores únicos con display_name
constructors_list = constructors['display_name'].unique()
selected_constructor = st.selectbox("Selecciona un constructor", constructors_list)

# Filtrar datos del constructor seleccionado
constructor_data = constructor_results[constructor_results['display_name'] == selected_constructor]

# Mostrar estadísticas
st.write(f"### Estadísticas de {selected_constructor}")

# Total de carreras
total_races = constructor_data['raceId'].nunique()
st.write(f"**Total de carreras:** {total_races}")

# Total de victorias
total_wins = constructor_data[constructor_data['positionOrder'] == 1]['raceId'].nunique()
st.write(f"**Total de victorias:** {total_wins}")

# Total de puntos
total_points = constructor_data['points'].sum()
st.write(f"**Total de puntos:** {total_points}")

# ---------------------------
# Calcular posición en el campeonato basado en puntos
championship_points = constructor_results.groupby(['year', 'display_name'])['points'].sum().reset_index()

# Calcular la posición en el campeonato por año
championship_points['championship_position'] = championship_points.groupby('year')['points'].rank(method='dense', ascending=False).astype(int)

# Filtrar para el constructor seleccionado
constructor_championship = championship_points[championship_points['display_name'] == selected_constructor]

# Añadir una columna que marque si fue campeón
constructor_championship['champion'] = constructor_championship['championship_position'].apply(lambda x: 'Champion' if x == 1 else '')

# Crear el gráfico de líneas para posición en el campeonato
fig_championship = px.line(
    constructor_championship,
    x='year',
    y='championship_position',
    title=f'Posición Final de {selected_constructor} en el Campeonato',
    labels={'year': 'Año', 'championship_position': 'Posición'},
    markers=True
)

# Filtrar los años en los que fue campeón
champion_years = constructor_championship[constructor_championship['champion'] == 'Champion']

# Añadir estrellas para cuando fue campeón
if not champion_years.empty:
    fig_championship.add_trace(
        go.Scatter(
            x=champion_years['year'],
            y=champion_years['championship_position'],
            mode='markers',
            marker=dict(size=15, color='yellow', symbol='star'),
            name='Campeón'
        )
    )

# Invertir el eje Y para que 1 esté en la parte superior
fig_championship.update_yaxes(autorange="reversed")

# Añadir leyenda manual
fig_championship.update_layout(
    legend=dict(
        title="Leyenda",
        itemsizing='constant'
    )
)

st.plotly_chart(fig_championship, use_container_width=True)

# ---------------------------
# Gráfico: Heatmap de posiciones por carrera y año usando Plotly Graph Objects

# Crear una tabla pivote con los resultados de las carreras por circuito y año
heatmap_data = constructor_data.pivot_table(index='race_name', columns='year', values='positionOrder', aggfunc='min')

# Obtener el máximo puesto en los datos
max_position = constructor_data['positionOrder'].max()

# Reemplazar NaN con max_position +1 para indicar carreras no corridas
heatmap_data = heatmap_data.fillna(max_position + 1)

# Crear una matriz de texto donde las celdas con max_position +1 tienen ''
text_matrix = heatmap_data.applymap(lambda x: '' if x == (max_position + 1) else str(int(x)))

# Definir una escala de colores personalizada
def get_custom_color_scale():
    """
    Crear una escala de colores que asigna un color oscuro al primer puesto (1),
    y va aclarando progresivamente hacia el último puesto.
    Las celdas vacías (carreras no corridas) tendrán el mismo color que el último puesto.
    """
    return px.colors.sequential.Blues

# Crear el heatmap con Plotly Graph Objects
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale=get_custom_color_scale(),
    colorbar=dict(title='Posición'),
    text=text_matrix.values,
    hoverinfo='text',
    texttemplate='%{text}',
    showscale=True,
    line=dict(width=1, color='black')  # Añadir líneas de recuadro
))

# Configurar el layout
fig_heatmap.update_layout(
    title=f'Posiciones de {selected_constructor} en las Carreras (por año)',
    xaxis_title='Año',
    yaxis_title='Carrera',
    width=1200,
    height=800
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown(f"""
Este heatmap muestra las posiciones de {selected_constructor} en las carreras a lo largo de los años. Las celdas vacías representan las carreras no corridas (mismo color que el último puesto). Las áreas más oscuras indican mejores posiciones (1), mientras que las más claras representan posiciones más altas.
""")
