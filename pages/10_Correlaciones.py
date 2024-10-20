# # # pages/9_Correlaciones.py

# # import streamlit as st
# # import pandas as pd
# # import seaborn as sns
# # import matplotlib.pyplot as plt

# # st.set_page_config(
# #     page_title="Análisis de Correlaciones",
# #     page_icon="🏎️",
# #     layout="wide",
# # )

# # st.write("# Análisis de Correlaciones 📊")

# # st.markdown("""
# # Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
# # """)

# # # Cargar datasets
# # results = pd.read_csv('data/results.csv')

# # # Seleccionar variables numéricas
# # numeric_cols = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds']

# # # Crear matriz de correlación
# # corr_matrix = results[numeric_cols].corr()

# # # Mostrar la matriz de correlación
# # st.write("## Matriz de Correlación")

# # fig, ax = plt.subplots()
# # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
# # st.pyplot(fig)

# # # Análisis adicional
# # st.markdown("""
# # Podemos observar que existe una correlación negativa entre la posición de salida ('grid') y la posición final ('positionOrder'), lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
# # """)





# # # pages/10_Correlaciones.py

# # import streamlit as st
# # import pandas as pd
# # import seaborn as sns
# # import matplotlib.pyplot as plt
# # import numpy as np

# # st.set_page_config(
# #     page_title="Análisis de Correlaciones",
# #     page_icon="🏎️",
# #     layout="wide",
# # )

# # st.write("# Análisis de Correlaciones 📊")

# # st.markdown("""
# # Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
# # """)

# # # Cargar datasets
# # results = pd.read_csv('data/results.csv')

# # # Reemplazar valores no numéricos como '\\N' con NaN
# # results.replace('\\N', np.nan, inplace=True)

# # # Convertir las columnas numéricas a tipo numérico (si contienen algún valor no convertible a float)
# # numeric_cols = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds']
# # results[numeric_cols] = results[numeric_cols].apply(pd.to_numeric, errors='coerce')

# # # Crear matriz de correlación, eliminando valores NaN
# # corr_matrix = results[numeric_cols].corr()

# # # Mostrar la matriz de correlación
# # st.write("## Matriz de Correlación")

# # fig, ax = plt.subplots()
# # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
# # st.pyplot(fig)

# # # Análisis adicional
# # st.markdown("""
# # Podemos observar que existe una correlación negativa entre la posición de salida ('grid') y la posición final ('positionOrder'), lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
# # """)



# # pages/10_Correlaciones.py

# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np

# st.set_page_config(
#     page_title="Análisis de Correlaciones",
#     page_icon="📊",
#     layout="wide",
# )

# st.write("# Análisis de Correlaciones 📊")

# st.markdown("""
# Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
# """)

# # ---------------------------
# # Cargar datasets
# @st.cache_data
# def load_data():
#     drivers = pd.read_csv('data/drivers.csv')
#     constructors = pd.read_csv('data/constructors.csv')
#     results = pd.read_csv('data/results.csv')
#     races = pd.read_csv('data/races.csv')
#     circuits = pd.read_csv('data/circuits.csv')
#     lap_times = pd.read_csv('data/lap_times.csv')
#     pit_stops = pd.read_csv('data/pit_stops.csv')
#     qualifying = pd.read_csv('data/qualifying.csv')
#     seasons = pd.read_csv('data/seasons.csv')
#     driver_standings = pd.read_csv('data/driver_standings.csv')
#     constructor_standings = pd.read_csv('data/constructor_standings.csv')
#     constructor_results = pd.read_csv('data/constructor_results.csv')
#     sprint_results = pd.read_csv('data/sprint_results.csv')
#     status = pd.read_csv('data/status.csv')
#     weather = pd.read_csv('data/F1 Weather(2023-2018).csv')

#     return {
#         'drivers': drivers,
#         'constructors': constructors,
#         'results': results,
#         'races': races,
#         'circuits': circuits,
#         'lap_times': lap_times,
#         'pit_stops': pit_stops,
#         'qualifying': qualifying,
#         'seasons': seasons,
#         'driver_standings': driver_standings,
#         'constructor_standings': constructor_standings,
#         'constructor_results': constructor_results,
#         'sprint_results': sprint_results,
#         'status': status,
#         'weather': weather
#     }

# data = load_data()

# # ---------------------------
# # Preparar los datos para el análisis

# # Reemplazar valores no numéricos
# for df_name in ['results', 'qualifying', 'lap_times', 'pit_stops']:
#     data[df_name].replace('\\N', np.nan, inplace=True)

# # Convertir columnas numéricas a tipos apropiados
# numeric_cols_results = ['grid', 'positionOrder', 'position', 'points', 'laps', 'milliseconds', 'fastestLapSpeed']
# data['results'][numeric_cols_results] = data['results'][numeric_cols_results].apply(pd.to_numeric, errors='coerce')

# numeric_cols_qualifying = ['position', 'q1', 'q2', 'q3']
# data['qualifying'][numeric_cols_qualifying] = data['qualifying'][numeric_cols_qualifying].apply(pd.to_numeric, errors='coerce')

# # Merge de datasets relevantes
# results = data['results']
# races = data['races']
# drivers = data['drivers']
# constructors = data['constructors']
# pit_stops = data['pit_stops']

# # Unir 'results' con 'races'
# results_races = pd.merge(results, races[['raceId', 'year', 'name', 'date', 'circuitId']], on='raceId', how='left')

# # Unir con 'drivers'
# results_races_drivers = pd.merge(results_races, drivers[['driverId', 'driverRef', 'forename', 'surname', 'dob', 'nationality']], on='driverId', how='left')

# # Unir con 'constructors'
# results_races_drivers = pd.merge(results_races_drivers, constructors[['constructorId', 'name']], on='constructorId', how='left', suffixes=('', '_constructor'))

# # Unir con 'qualifying' para obtener posición de clasificación
# qualifying = data['qualifying']
# results_races_drivers = pd.merge(results_races_drivers, qualifying[['raceId', 'driverId', 'position']], on=['raceId', 'driverId'], how='left', suffixes=('', '_qualifying'))

# # Renombrar 'position' de clasificación a 'qualifying_position'
# results_races_drivers.rename(columns={'position_qualifying': 'qualifying_position'}, inplace=True)

# # Calcular la edad del piloto en el momento de la carrera
# results_races_drivers['dob'] = pd.to_datetime(results_races_drivers['dob'], errors='coerce')
# results_races_drivers['date'] = pd.to_datetime(results_races_drivers['date'], errors='coerce')
# results_races_drivers['driver_age'] = (results_races_drivers['date'] - results_races_drivers['dob']).dt.days / 365.25

# # Calcular el número total de pit stops por piloto en cada carrera
# pit_stops_per_driver = data['pit_stops'].groupby(['raceId', 'driverId']).size().reset_index(name='num_pit_stops')

# # Unir con el dataset principal
# results_races_drivers = pd.merge(results_races_drivers, pit_stops_per_driver, on=['raceId', 'driverId'], how='left')

# # Reemplazar NaN en 'num_pit_stops' por 0
# results_races_drivers['num_pit_stops'] = results_races_drivers['num_pit_stops'].fillna(0)

# # ---------------------------
# # Seleccionar variables para el análisis de correlación
# corr_variables = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds', 'fastestLapSpeed', 'driver_age', 'num_pit_stops', 'qualifying_position']

# # Extraer los datos para las variables seleccionadas
# corr_data = results_races_drivers[corr_variables]

# # Convertir columnas a numéricas y manejar valores faltantes
# corr_data = corr_data.apply(pd.to_numeric, errors='coerce')
# corr_data = corr_data.dropna()

# # ---------------------------
# # Matriz de Correlación General
# st.write("## Matriz de Correlación General")

# corr_matrix = corr_data.corr()

# fig, ax = plt.subplots(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
# st.pyplot(fig)

# st.markdown("""
# La matriz de correlación nos muestra las relaciones entre diferentes variables en las carreras de Fórmula 1.
# """)

# # ---------------------------
# # Análisis de Correlaciones Específicas

# st.write("## Análisis de Correlaciones Específicas")

# # Opciones de variables para el usuario
# variable_options = {
#     'Posición de salida (Grid)': 'grid',
#     'Posición final': 'positionOrder',
#     'Puntos obtenidos': 'points',
#     'Vueltas completadas': 'laps',
#     'Tiempo total de carrera (ms)': 'milliseconds',
#     'Velocidad de vuelta más rápida': 'fastestLapSpeed',
#     'Edad del piloto': 'driver_age',
#     'Número de pit stops': 'num_pit_stops',
#     'Posición en clasificación': 'qualifying_position'
# }

# var_x = st.selectbox('Seleccione la variable en el eje X', list(variable_options.keys()), key='var_x')
# var_y = st.selectbox('Seleccione la variable en el eje Y', list(variable_options.keys()), key='var_y')

# x = variable_options[var_x]
# y = variable_options[var_y]

# # Preparar datos para el scatter plot
# scatter_data = corr_data[[x, y]].dropna()

# # Crear scatter plot
# fig_scatter, ax_scatter = plt.subplots()
# sns.scatterplot(data=scatter_data, x=x, y=y, ax=ax_scatter)
# ax_scatter.set_xlabel(var_x)
# ax_scatter.set_ylabel(var_y)
# ax_scatter.set_title(f'{var_y} vs {var_x}')
# st.pyplot(fig_scatter)

# # Calcular coeficiente de correlación
# corr_coef = scatter_data[x].corr(scatter_data[y])
# st.write(f"**Coeficiente de correlación de Pearson entre {var_x} y {var_y}: {corr_coef:.2f}**")

# # Interpretación básica
# if corr_coef > 0.5:
#     st.write("Existe una **correlación positiva fuerte** entre las variables seleccionadas.")
# elif corr_coef > 0.3:
#     st.write("Existe una **correlación positiva moderada** entre las variables seleccionadas.")
# elif corr_coef > 0.1:
#     st.write("Existe una **correlación positiva débil** entre las variables seleccionadas.")
# elif corr_coef < -0.5:
#     st.write("Existe una **correlación negativa fuerte** entre las variables seleccionadas.")
# elif corr_coef < -0.3:
#     st.write("Existe una **correlación negativa moderada** entre las variables seleccionadas.")
# elif corr_coef < -0.1:
#     st.write("Existe una **correlación negativa débil** entre las variables seleccionadas.")
# else:
#     st.write("No existe una correlación significativa entre las variables seleccionadas.")

# # ---------------------------
# # Análisis Predefinidos

# st.write("## Análisis Predefinidos")

# # 1. Correlación entre posición de salida y posición final
# st.write("### 1. Posición de salida vs Posición final")

# data_gp_fp = corr_data[['grid', 'positionOrder']].dropna()
# corr_gp_fp = data_gp_fp['grid'].corr(data_gp_fp['positionOrder'])

# st.write(f"**Coeficiente de correlación de Pearson:** {corr_gp_fp:.2f}")

# fig_gp_fp, ax_gp_fp = plt.subplots()
# sns.scatterplot(data=data_gp_fp, x='grid', y='positionOrder', alpha=0.5, ax=ax_gp_fp)
# ax_gp_fp.set_xlabel('Posición de salida (Grid)')
# ax_gp_fp.set_ylabel('Posición final')
# ax_gp_fp.set_title('Posición final vs Posición de salida')
# st.pyplot(fig_gp_fp)

# st.markdown("""
# Podemos observar una **correlación positiva** entre la posición de salida y la posición final, lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
# """)

# # 2. Correlación entre número de pit stops y posición final
# st.write("### 2. Número de pit stops vs Posición final")

# data_np_fp = corr_data[['num_pit_stops', 'positionOrder']].dropna()
# corr_np_fp = data_np_fp['num_pit_stops'].corr(data_np_fp['positionOrder'])

# st.write(f"**Coeficiente de correlación de Pearson:** {corr_np_fp:.2f}")

# fig_np_fp, ax_np_fp = plt.subplots()
# sns.scatterplot(data=data_np_fp, x='num_pit_stops', y='positionOrder', alpha=0.5, ax=ax_np_fp)
# ax_np_fp.set_xlabel('Número de pit stops')
# ax_np_fp.set_ylabel('Posición final')
# ax_np_fp.set_title('Posición final vs Número de pit stops')
# st.pyplot(fig_np_fp)

# st.markdown("""
# Existe una **correlación positiva débil** entre el número de pit stops y la posición final. Esto sugiere que más pit stops pueden estar asociados con posiciones finales más bajas, posiblemente debido al tiempo perdido en paradas adicionales.
# """)

# # 3. Correlación entre edad del piloto y puntos obtenidos
# st.write("### 3. Edad del piloto vs Puntos obtenidos")

# data_age_points = corr_data[['driver_age', 'points']].dropna()
# corr_age_points = data_age_points['driver_age'].corr(data_age_points['points'])

# st.write(f"**Coeficiente de correlación de Pearson:** {corr_age_points:.2f}")

# fig_age_points, ax_age_points = plt.subplots()
# sns.scatterplot(data=data_age_points, x='driver_age', y='points', alpha=0.5, ax=ax_age_points)
# ax_age_points.set_xlabel('Edad del piloto')
# ax_age_points.set_ylabel('Puntos obtenidos')
# ax_age_points.set_title('Puntos obtenidos vs Edad del piloto')
# st.pyplot(fig_age_points)

# st.markdown("""
# La correlación entre la edad del piloto y los puntos obtenidos es **débil**. Esto indica que no hay una relación significativa entre la edad y el rendimiento en términos de puntos en una carrera individual.
# """)

# # 4. Correlación entre posición en clasificación y posición final
# st.write("### 4. Posición en clasificación vs Posición final")

# data_qp_fp = corr_data[['qualifying_position', 'positionOrder']].dropna()
# corr_qp_fp = data_qp_fp['qualifying_position'].corr(data_qp_fp['positionOrder'])

# st.write(f"**Coeficiente de correlación de Pearson:** {corr_qp_fp:.2f}")

# fig_qp_fp, ax_qp_fp = plt.subplots()
# sns.scatterplot(data=data_qp_fp, x='qualifying_position', y='positionOrder', alpha=0.5, ax=ax_qp_fp)
# ax_qp_fp.set_xlabel('Posición en clasificación')
# ax_qp_fp.set_ylabel('Posición final')
# ax_qp_fp.set_title('Posición final vs Posición en clasificación')
# st.pyplot(fig_qp_fp)

# st.markdown("""
# Existe una **correlación positiva fuerte** entre la posición en clasificación y la posición final. Esto indica que una buena posición en clasificación suele traducirse en una mejor posición al final de la carrera.
# """)

# # ---------------------------
# # Análisis adicional con datos de clima (si están disponibles)
# if 'weather' in data:
#     st.write("## Análisis con Datos de Clima")

#     # Suponiendo que 'weather' contiene información relevante
#     weather = data['weather']
#     weather.replace('\\N', np.nan, inplace=True)

#     # Convertir columnas a tipos apropiados
#     weather_cols = ['temperature', 'humidity', 'wind_speed', 'rainfall']
#     for col in weather_cols:
#         if col in weather.columns:
#             weather[col] = pd.to_numeric(weather[col], errors='coerce')

#     # Unir 'weather' con 'races' y 'results'
#     weather_results = pd.merge(results_races_drivers, weather, on='raceId', how='left')

#     # Seleccionar variables para correlación
#     weather_corr_vars = ['positionOrder', 'points'] + weather_cols
#     weather_data = weather_results[weather_corr_vars].dropna()

#     if not weather_data.empty:
#         # Mostrar matriz de correlación
#         st.write("### Matriz de Correlación con Variables Climáticas")

#         weather_corr_matrix = weather_data.corr()

#         fig_weather_corr, ax_weather_corr = plt.subplots(figsize=(10, 8))
#         sns.heatmap(weather_corr_matrix, annot=True, cmap='coolwarm', ax=ax_weather_corr)
#         st.pyplot(fig_weather_corr)

#         st.markdown("""
#         La matriz de correlación incluye variables climáticas como temperatura, humedad, velocidad del viento y precipitación. Esto nos permite explorar cómo las condiciones climáticas pueden afectar el rendimiento en las carreras.
#         """)
#     else:
#         st.write("**No hay datos suficientes para realizar el análisis con variables climáticas.**")
# else:
#     st.write("**Datos de clima no disponibles para el análisis.**")



# pages/10_Correlaciones.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json

st.set_page_config(
    page_title="Análisis de Correlaciones",
    page_icon="📊",
    layout="wide",
)

st.write("# Análisis de Correlaciones 📊")

st.markdown("""
Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
""")

# ---------------------------
# Cargar datasets
@st.cache_data
def load_data():
    drivers = pd.read_csv('data/drivers.csv')
    constructors = pd.read_csv('data/constructors.csv')
    results = pd.read_csv('data/results.csv')
    races = pd.read_csv('data/races.csv')
    circuits = pd.read_csv('data/circuits.csv')
    lap_times = pd.read_csv('data/lap_times.csv')
    pit_stops = pd.read_csv('data/pit_stops.csv')
    qualifying = pd.read_csv('data/qualifying.csv')
    seasons = pd.read_csv('data/seasons.csv')
    driver_standings = pd.read_csv('data/driver_standings.csv')
    constructor_standings = pd.read_csv('data/constructor_standings.csv')
    constructor_results = pd.read_csv('data/constructor_results.csv')
    sprint_results = pd.read_csv('data/sprint_results.csv')
    status = pd.read_csv('data/status.csv')
    # No cargamos weather data

    # Cargar datos desde los archivos JSON
    with open('data/surface_classification.json', 'r') as f:
        surface_classification = json.load(f)

    with open('data/permanence_classification.json', 'r') as f:
        permanence_classification = json.load(f)

    with open('data/continent_classification.json', 'r') as f:
        continent_classification = json.load(f)

    with open('data/circuit_lengths.json', 'r') as f:
        circuit_lengths = json.load(f)

    return {
        'drivers': drivers,
        'constructors': constructors,
        'results': results,
        'races': races,
        'circuits': circuits,
        'lap_times': lap_times,
        'pit_stops': pit_stops,
        'qualifying': qualifying,
        'seasons': seasons,
        'driver_standings': driver_standings,
        'constructor_standings': constructor_standings,
        'constructor_results': constructor_results,
        'sprint_results': sprint_results,
        'status': status,
        'surface_classification': surface_classification,
        'permanence_classification': permanence_classification,
        'continent_classification': continent_classification,
        'circuit_lengths': circuit_lengths
    }

data = load_data()

# ---------------------------
# Preparar los datos para el análisis

# Reemplazar valores no numéricos
for df_name in ['results', 'qualifying', 'lap_times', 'pit_stops']:
    data[df_name].replace('\\N', np.nan, inplace=True)

# Convertir columnas numéricas a tipos apropiados
numeric_cols_results = ['grid', 'positionOrder', 'position', 'points', 'laps', 'milliseconds', 'fastestLapSpeed']
data['results'][numeric_cols_results] = data['results'][numeric_cols_results].apply(pd.to_numeric, errors='coerce')

numeric_cols_qualifying = ['position', 'q1', 'q2', 'q3']
data['qualifying'][numeric_cols_qualifying] = data['qualifying'][numeric_cols_qualifying].apply(pd.to_numeric, errors='coerce')

# Merge de datasets relevantes
results = data['results']
races = data['races']
drivers = data['drivers']
constructors = data['constructors']
pit_stops = data['pit_stops']
circuits = data['circuits']

# Unir 'results' con 'races'
results_races = pd.merge(results, races[['raceId', 'year', 'name', 'date', 'circuitId']], on='raceId', how='left')

# Unir con 'drivers'
results_races_drivers = pd.merge(results_races, drivers[['driverId', 'driverRef', 'forename', 'surname', 'dob', 'nationality']], on='driverId', how='left')

# Unir con 'constructors'
results_races_drivers = pd.merge(results_races_drivers, constructors[['constructorId', 'name']], on='constructorId', how='left', suffixes=('', '_constructor'))

# Unir con 'qualifying' para obtener posición de clasificación
qualifying = data['qualifying']
results_races_drivers = pd.merge(results_races_drivers, qualifying[['raceId', 'driverId', 'position']], on=['raceId', 'driverId'], how='left', suffixes=('', '_qualifying'))

# Renombrar 'position' de clasificación a 'posicion_clasificacion'
results_races_drivers.rename(columns={'position_qualifying': 'posicion_clasificacion'}, inplace=True)

# Calcular la edad del piloto en el momento de la carrera
results_races_drivers['dob'] = pd.to_datetime(results_races_drivers['dob'], errors='coerce')
results_races_drivers['date'] = pd.to_datetime(results_races_drivers['date'], errors='coerce')
results_races_drivers['edad_piloto'] = (results_races_drivers['date'] - results_races_drivers['dob']).dt.days / 365.25

# Calcular el número total de pit stops por piloto en cada carrera
pit_stops_per_driver = data['pit_stops'].groupby(['raceId', 'driverId']).size().reset_index(name='num_pit_stops')

# Unir con el dataset principal
results_races_drivers = pd.merge(results_races_drivers, pit_stops_per_driver, on=['raceId', 'driverId'], how='left')

# Reemplazar NaN en 'num_pit_stops' por 0
results_races_drivers['num_pit_stops'] = results_races_drivers['num_pit_stops'].fillna(0)

# Añadir información de circuitos
# Añadir longitud del circuito desde 'circuit_lengths'
# Convertir 'circuit_lengths' de JSON a DataFrame
circuit_lengths = pd.DataFrame.from_dict(data['circuit_lengths'], orient='index', columns=['circuit_length_km'])
circuit_lengths.reset_index(inplace=True)
circuit_lengths.rename(columns={'index': 'circuitRef'}, inplace=True)

# Unir 'circuits' con 'circuit_lengths' a través de 'circuitRef'
circuits = pd.merge(circuits, circuit_lengths, on='circuitRef', how='left')

# Unir 'results_races_drivers' con 'circuits' para obtener la longitud del circuito
results_races_drivers = pd.merge(results_races_drivers, circuits[['circuitId', 'circuit_length_km']], on='circuitId', how='left')

# Calcular distancia total recorrida por cada piloto en cada carrera
results_races_drivers['distancia_total_km'] = results_races_drivers['laps'] * results_races_drivers['circuit_length_km']

# Calcular velocidad promedio en km/h
# Convertir 'milliseconds' a horas
results_races_drivers['tiempo_horas'] = results_races_drivers['milliseconds'] / (1000 * 60 * 60)
results_races_drivers['velocidad_promedio_kmh'] = results_races_drivers['distancia_total_km'] / results_races_drivers['tiempo_horas']

# ---------------------------
# Seleccionar variables para el análisis de correlación
corr_variables = {
    'Posición de salida (Grid)': 'grid',
    'Posición final': 'positionOrder',
    'Puntos obtenidos': 'points',
    'Vueltas completadas': 'laps',
    'Tiempo total de carrera (ms)': 'milliseconds',
    'Velocidad de vuelta más rápida': 'fastestLapSpeed',
    'Edad del piloto': 'edad_piloto',
    'Número de pit stops': 'num_pit_stops',
    'Posición en clasificación': 'posicion_clasificacion',
    'Distancia total recorrida (km)': 'distancia_total_km',
    'Velocidad promedio (km/h)': 'velocidad_promedio_kmh'
}

# Extraer los datos para las variables seleccionadas
corr_data = results_races_drivers[list(corr_variables.values())]

# Convertir columnas a numéricas y manejar valores faltantes
corr_data = corr_data.apply(pd.to_numeric, errors='coerce')
corr_data = corr_data.dropna()

# ---------------------------
# Matriz de Correlación General
st.write("## Matriz de Correlación General")

corr_matrix = corr_data.corr()

# Actualizar nombres de columnas a español
corr_matrix.rename(columns={v: k for k, v in corr_variables.items()}, inplace=True)
corr_matrix.rename(index={v: k for k, v in corr_variables.items()}, inplace=True)

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.markdown("""
La matriz de correlación nos muestra las relaciones entre diferentes variables en las carreras de Fórmula 1.
""")

# ---------------------------
# Análisis de Correlaciones Específicas

st.write("## Análisis de Correlaciones Específicas")

# Opciones de variables para el usuario
variable_options = list(corr_variables.keys())

var_x = st.selectbox('Seleccione la variable en el eje X', variable_options, key='var_x')

# Excluir la variable seleccionada en var_x de las opciones en var_y
var_y_options = [option for option in variable_options if option != var_x]

var_y = st.selectbox('Seleccione la variable en el eje Y', var_y_options, key='var_y')

x = corr_variables[var_x]
y = corr_variables[var_y]

# Preparar datos para el scatter plot
scatter_data = corr_data[[x, y]].dropna()

# Crear scatter plot
fig_scatter, ax_scatter = plt.subplots()
sns.scatterplot(data=scatter_data, x=x, y=y, ax=ax_scatter)
ax_scatter.set_xlabel(var_x)
ax_scatter.set_ylabel(var_y)
ax_scatter.set_title(f'{var_y} vs {var_x}')
st.pyplot(fig_scatter)

# Calcular coeficiente de correlación
corr_coef = scatter_data[x].corr(scatter_data[y])
st.write(f"**Coeficiente de correlación de Pearson entre {var_x} y {var_y}: {corr_coef:.2f}**")

# Interpretación básica
if corr_coef > 0.5:
    st.write("Existe una **correlación positiva fuerte** entre las variables seleccionadas.")
elif corr_coef > 0.3:
    st.write("Existe una **correlación positiva moderada** entre las variables seleccionadas.")
elif corr_coef > 0.1:
    st.write("Existe una **correlación positiva débil** entre las variables seleccionadas.")
elif corr_coef < -0.5:
    st.write("Existe una **correlación negativa fuerte** entre las variables seleccionadas.")
elif corr_coef < -0.3:
    st.write("Existe una **correlación negativa moderada** entre las variables seleccionadas.")
elif corr_coef < -0.1:
    st.write("Existe una **correlación negativa débil** entre las variables seleccionadas.")
else:
    st.write("No existe una correlación significativa entre las variables seleccionadas.")

# ---------------------------
# Análisis Predefinidos

st.write("## Análisis Predefinidos")

# 1. Correlación entre posición de salida y posición final
st.write("### 1. Posición de salida vs Posición final")

data_gp_fp = corr_data[[corr_variables['Posición de salida (Grid)'], corr_variables['Posición final']]].dropna()
corr_gp_fp = data_gp_fp[corr_variables['Posición de salida (Grid)']].corr(data_gp_fp[corr_variables['Posición final']])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_gp_fp:.2f}")

fig_gp_fp, ax_gp_fp = plt.subplots()
sns.scatterplot(data=data_gp_fp, x=corr_variables['Posición de salida (Grid)'], y=corr_variables['Posición final'], alpha=0.5, ax=ax_gp_fp)
ax_gp_fp.set_xlabel('Posición de salida (Grid)')
ax_gp_fp.set_ylabel('Posición final')
ax_gp_fp.set_title('Posición final vs Posición de salida')
st.pyplot(fig_gp_fp)

st.markdown("""
Podemos observar una **correlación positiva** entre la posición de salida y la posición final, lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
""")

# 2. Correlación entre número de pit stops y posición final
st.write("### 2. Número de pit stops vs Posición final")

data_np_fp = corr_data[[corr_variables['Número de pit stops'], corr_variables['Posición final']]].dropna()
corr_np_fp = data_np_fp[corr_variables['Número de pit stops']].corr(data_np_fp[corr_variables['Posición final']])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_np_fp:.2f}")

fig_np_fp, ax_np_fp = plt.subplots()
sns.scatterplot(data=data_np_fp, x=corr_variables['Número de pit stops'], y=corr_variables['Posición final'], alpha=0.5, ax=ax_np_fp)
ax_np_fp.set_xlabel('Número de pit stops')
ax_np_fp.set_ylabel('Posición final')
ax_np_fp.set_title('Posición final vs Número de pit stops')
st.pyplot(fig_np_fp)

st.markdown("""
Existe una **correlación positiva débil** entre el número de pit stops y la posición final. Esto sugiere que más pit stops pueden estar asociados con posiciones finales más bajas, posiblemente debido al tiempo perdido en paradas adicionales.
""")

# 3. Correlación entre edad del piloto y puntos obtenidos
st.write("### 3. Edad del piloto vs Puntos obtenidos")

data_age_points = corr_data[[corr_variables['Edad del piloto'], corr_variables['Puntos obtenidos']]].dropna()
corr_age_points = data_age_points[corr_variables['Edad del piloto']].corr(data_age_points[corr_variables['Puntos obtenidos']])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_age_points:.2f}")

fig_age_points, ax_age_points = plt.subplots()
sns.scatterplot(data=data_age_points, x=corr_variables['Edad del piloto'], y=corr_variables['Puntos obtenidos'], alpha=0.5, ax=ax_age_points)
ax_age_points.set_xlabel('Edad del piloto')
ax_age_points.set_ylabel('Puntos obtenidos')
ax_age_points.set_title('Puntos obtenidos vs Edad del piloto')
st.pyplot(fig_age_points)

st.markdown("""
La correlación entre la edad del piloto y los puntos obtenidos es **débil**. Esto indica que no hay una relación significativa entre la edad y el rendimiento en términos de puntos en una carrera individual.
""")

# 4. Correlación entre posición en clasificación y posición final
st.write("### 4. Posición en clasificación vs Posición final")

data_qp_fp = corr_data[[corr_variables['Posición en clasificación'], corr_variables['Posición final']]].dropna()
corr_qp_fp = data_qp_fp[corr_variables['Posición en clasificación']].corr(data_qp_fp[corr_variables['Posición final']])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_qp_fp:.2f}")

fig_qp_fp, ax_qp_fp = plt.subplots()
sns.scatterplot(data=data_qp_fp, x=corr_variables['Posición en clasificación'], y=corr_variables['Posición final'], alpha=0.5, ax=ax_qp_fp)
ax_qp_fp.set_xlabel('Posición en clasificación')
ax_qp_fp.set_ylabel('Posición final')
ax_qp_fp.set_title('Posición final vs Posición en clasificación')
st.pyplot(fig_qp_fp)

st.markdown("""
Existe una **correlación positiva fuerte** entre la posición en clasificación y la posición final. Esto indica que una buena posición en clasificación suele traducirse en una mejor posición al final de la carrera.
""")
