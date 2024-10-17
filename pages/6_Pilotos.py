import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.colors import LinearSegmentedColormap

st.set_page_config(
    page_title="Análisis de Pilotos",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Pilotos 🏆")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    drivers = pd.read_csv('data/drivers.csv')
    results = pd.read_csv('data/results.csv')
    races = pd.read_csv('data/races.csv')
    return drivers, results, races

drivers, results, races = load_data()

# Verificar si 'points' está presente en results
if 'points' not in results.columns:
    st.error("El dataset 'results.csv' no contiene la columna 'points'. No se pueden calcular las posiciones finales en el campeonato correctamente.")
    st.stop()

# ---------------------------
# Crear 'display_name' para los pilotos
drivers['initial'] = drivers['forename'].str[0]
surname_counts = drivers['surname'].value_counts()
drivers['display_name'] = drivers.apply(
    lambda row: f"{row['initial']}. {row['surname']}" if surname_counts[row['surname']] > 1 else row['surname'],
    axis=1
)

# Merge de datos con display_name
driver_results = results.merge(drivers, on='driverId').merge(races, on='raceId')

# Calcular victorias por piloto
wins = driver_results[driver_results['positionOrder'] == 1]
wins_by_driver = wins.groupby(['driverId', 'display_name'])['raceId'].count().reset_index()
wins_by_driver = wins_by_driver.rename(columns={'raceId': 'wins'})

# Top 10 pilotos con más victorias
top_winners = wins_by_driver.sort_values(by='wins', ascending=False).head(10)

# Gráfico de Top 10 Pilotos
fig = px.bar(
    top_winners,
    x='wins',
    y='display_name',
    orientation='h',
    title='Top 10 Pilotos con Más Victorias',
    labels={'wins': 'Victorias', 'display_name': 'Piloto'},
    color='wins',
    color_continuous_scale='Blues'
)
fig.update_layout(yaxis=dict(autorange="reversed"))

st.plotly_chart(fig)

st.write("## Detalles del Piloto")

# Lista de pilotos únicos con display_name
pilots_list = drivers['display_name'].unique()
selected_pilot = st.selectbox("Selecciona un piloto", pilots_list)

# Filtrar datos del piloto seleccionado
pilot_data = driver_results[driver_results['display_name'] == selected_pilot]

# Mostrar estadísticas
st.write(f"### Estadísticas de {selected_pilot}")

# Total de carreras
total_races = pilot_data['raceId'].nunique()
st.write(f"**Total de carreras:** {total_races}")

# Total de victorias
total_wins = pilot_data[pilot_data['positionOrder'] == 1]['raceId'].nunique()
st.write(f"**Total de victorias:** {total_wins}")

# ---------------------------
# Calcular posición en el campeonato basado en puntos
championship_points = driver_results.groupby(['year', 'display_name'])['points'].sum().reset_index()

# Calcular la posición en el campeonato por año
championship_points['championship_position'] = championship_points.groupby('year')['points'].rank(method='dense', ascending=False).astype(int)

# Filtrar para el piloto seleccionado
pilot_championship = championship_points[championship_points['display_name'] == selected_pilot]

# Añadir una columna que marque si fue campeón
pilot_championship['champion'] = pilot_championship['championship_position'].apply(lambda x: 'Champion' if x == 1 else '')

# Crear el gráfico de líneas para posición en el campeonato
fig_championship = px.line(
    pilot_championship,
    x='year',
    y='championship_position',
    title=f'Posición Final de {selected_pilot} en el Campeonato',
    labels={'year': 'Año', 'championship_position': 'Posición'},
    markers=True
)

# Filtrar los años en los que fue campeón
champion_years = pilot_championship[pilot_championship['champion'] == 'Champion']

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

# # ---------------------------
# # Gráfico 2: Heatmap de posiciones por carrera y año
# # Crear una tabla pivote con los resultados de las carreras por circuito y año
# heatmap_data = pilot_data.pivot_table(index='name', columns='year', values='positionOrder', aggfunc='min')

# # Configurar el estilo de Seaborn
# sns.set(style='white')

# # Crear la figura y ajustar el tamaño
# plt.figure(figsize=(20, 10))

# # Definir una paleta personalizada de blanco y negro para el heatmap
# black_white_cmap = LinearSegmentedColormap.from_list('black_white', ['black', 'white'])

# # Crear el heatmap
# sns.heatmap(
#     heatmap_data,
#     cmap=black_white_cmap,
#     linewidths=0.5,
#     linecolor='lightgrey',
#     cbar_kws={'label': 'Posición en la Carrera'},
#     annot=True, fmt='.0f'
# )

# # Ajustar las etiquetas y título
# plt.title(f'Posiciones de {selected_pilot} en las Carreras (por año)', fontsize=18)
# plt.xlabel('Año', fontsize=14)
# plt.ylabel('Circuito', fontsize=14)

# # Mejorar la legibilidad de las etiquetas del eje X
# plt.xticks(rotation=90)

# # Ajustar el gráfico
# plt.tight_layout()

# # Mostrar el gráfico en Streamlit
# st.pyplot(plt)



# ---------------------------
# Función para crear la escala de colores

def get_custom_color_scale():
    """
    Crear una escala de colores que asigna un color oscuro al primer puesto (1),
    y va aclarando progresivamente hacia el último puesto.
    Las celdas vacías (carreras no corridas) tendrán el mismo color que el último puesto.
    """
    color_scale = [
        [0, "lightgray"],  # Vacío (no participado) será gris claro (igual que el último puesto)
        [0.1, "lightblue"],  # Colores claros para posiciones más altas (peores resultados)
        [0.5, "blue"],  # Posiciones medias
        [1, "darkblue"]  # El color más oscuro para el primer puesto (victoria)
    ]
    return color_scale

# ---------------------------
# Gráfico 2: Heatmap de posiciones por carrera y año usando Plotly Graph Objects

# Crear una tabla pivote con los resultados de las carreras por circuito y año
heatmap_data = pilot_data.pivot_table(index='name', columns='year', values='positionOrder', aggfunc='min')

# Obtener el máximo puesto en los datos
max_position = pilot_data['positionOrder'].max()

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
    # Utilizamos una escala de colores secuencial de Blues invertida
    # para que 1 sea el más oscuro y posiciones más altas sean más claras
    return px.colors.sequential.Blues[::-1]

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
    showscale=True
    
))

# Configurar el layout
fig_heatmap.update_layout(
    title=f'Posiciones de {selected_pilot} en las Carreras (por año)',
    xaxis_title='Año',
    yaxis_title='Circuito',
    width=1200,
    height=800
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown(f"""
Este heatmap muestra las posiciones de {selected_pilot} en las carreras a lo largo de los años. Las celdas vacías representan las carreras no corridas (color igual al último puesto). Las áreas más oscuras indican mejores posiciones (1), mientras que las más claras representan posiciones más altas.
""")