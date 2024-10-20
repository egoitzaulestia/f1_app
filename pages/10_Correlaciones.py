# # pages/9_Correlaciones.py

# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# st.set_page_config(
#     page_title="Análisis de Correlaciones",
#     page_icon="🏎️",
#     layout="wide",
# )

# st.write("# Análisis de Correlaciones 📊")

# st.markdown("""
# Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
# """)

# # Cargar datasets
# results = pd.read_csv('data/results.csv')

# # Seleccionar variables numéricas
# numeric_cols = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds']

# # Crear matriz de correlación
# corr_matrix = results[numeric_cols].corr()

# # Mostrar la matriz de correlación
# st.write("## Matriz de Correlación")

# fig, ax = plt.subplots()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
# st.pyplot(fig)

# # Análisis adicional
# st.markdown("""
# Podemos observar que existe una correlación negativa entre la posición de salida ('grid') y la posición final ('positionOrder'), lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
# """)





# # pages/10_Correlaciones.py

# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np

# st.set_page_config(
#     page_title="Análisis de Correlaciones",
#     page_icon="🏎️",
#     layout="wide",
# )

# st.write("# Análisis de Correlaciones 📊")

# st.markdown("""
# Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
# """)

# # Cargar datasets
# results = pd.read_csv('data/results.csv')

# # Reemplazar valores no numéricos como '\\N' con NaN
# results.replace('\\N', np.nan, inplace=True)

# # Convertir las columnas numéricas a tipo numérico (si contienen algún valor no convertible a float)
# numeric_cols = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds']
# results[numeric_cols] = results[numeric_cols].apply(pd.to_numeric, errors='coerce')

# # Crear matriz de correlación, eliminando valores NaN
# corr_matrix = results[numeric_cols].corr()

# # Mostrar la matriz de correlación
# st.write("## Matriz de Correlación")

# fig, ax = plt.subplots()
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
# st.pyplot(fig)

# # Análisis adicional
# st.markdown("""
# Podemos observar que existe una correlación negativa entre la posición de salida ('grid') y la posición final ('positionOrder'), lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
# """)



# pages/10_Correlaciones.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
    weather = pd.read_csv('data/F1 Weather(2023-2018).csv')

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
        'weather': weather
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

# Unir 'results' con 'races'
results_races = pd.merge(results, races[['raceId', 'year', 'name', 'date', 'circuitId']], on='raceId', how='left')

# Unir con 'drivers'
results_races_drivers = pd.merge(results_races, drivers[['driverId', 'driverRef', 'forename', 'surname', 'dob', 'nationality']], on='driverId', how='left')

# Unir con 'constructors'
results_races_drivers = pd.merge(results_races_drivers, constructors[['constructorId', 'name']], on='constructorId', how='left', suffixes=('', '_constructor'))

# Unir con 'qualifying' para obtener posición de clasificación
qualifying = data['qualifying']
results_races_drivers = pd.merge(results_races_drivers, qualifying[['raceId', 'driverId', 'position']], on=['raceId', 'driverId'], how='left', suffixes=('', '_qualifying'))

# Calcular la edad del piloto en el momento de la carrera
results_races_drivers['dob'] = pd.to_datetime(results_races_drivers['dob'], errors='coerce')
results_races_drivers['date'] = pd.to_datetime(results_races_drivers['date'], errors='coerce')
results_races_drivers['driver_age'] = (results_races_drivers['date'] - results_races_drivers['dob']).dt.days / 365.25

# Calcular el número total de pit stops por piloto en cada carrera
pit_stops_per_driver = data['pit_stops'].groupby(['raceId', 'driverId']).size().reset_index(name='num_pit_stops')

# Unir con el dataset principal
results_races_drivers = pd.merge(results_races_drivers, pit_stops_per_driver, on=['raceId', 'driverId'], how='left')

# Reemplazar NaN en 'num_pit_stops' por 0
results_races_drivers['num_pit_stops'] = results_races_drivers['num_pit_stops'].fillna(0)

# ---------------------------
# Seleccionar variables para el análisis de correlación
corr_variables = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds', 'fastestLapSpeed', 'driver_age', 'num_pit_stops', 'position_qualifying']

# Renombrar 'position' de clasificación a 'position_qualifying' en caso de conflicto
results_races_drivers.rename(columns={'position_qualifying': 'qualifying_position'}, inplace=True)
corr_variables.append('qualifying_position')

# Extraer los datos para las variables seleccionadas
corr_data = results_races_drivers[corr_variables]

# Convertir columnas a numéricas y manejar valores faltantes
corr_data = corr_data.apply(pd.to_numeric, errors='coerce')
corr_data = corr_data.dropna()

# ---------------------------
# Matriz de Correlación General
st.write("## Matriz de Correlación General")

corr_matrix = corr_data.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

st.markdown("""
La matriz de correlación nos muestra las relaciones entre diferentes variables en las carreras de Fórmula 1.
""")

# ---------------------------
# Análisis de Correlaciones Específicas

st.write("## Análisis de Correlaciones Específicas")

# Opciones de variables para el usuario
variable_options = {
    'Posición de salida (Grid)': 'grid',
    'Posición final': 'positionOrder',
    'Puntos obtenidos': 'points',
    'Vueltas completadas': 'laps',
    'Tiempo total de carrera (ms)': 'milliseconds',
    'Velocidad de vuelta más rápida': 'fastestLapSpeed',
    'Edad del piloto': 'driver_age',
    'Número de pit stops': 'num_pit_stops',
    'Posición en clasificación': 'qualifying_position'
}

var_x = st.selectbox('Seleccione la variable en el eje X', list(variable_options.keys()), key='var_x')
var_y = st.selectbox('Seleccione la variable en el eje Y', list(variable_options.keys()), key='var_y')

x = variable_options[var_x]
y = variable_options[var_y]

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

data_gp_fp = corr_data[['grid', 'positionOrder']].dropna()
corr_gp_fp = data_gp_fp['grid'].corr(data_gp_fp['positionOrder'])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_gp_fp:.2f}")

fig_gp_fp, ax_gp_fp = plt.subplots()
sns.scatterplot(data=data_gp_fp, x='grid', y='positionOrder', alpha=0.5, ax=ax_gp_fp)
ax_gp_fp.set_xlabel('Posición de salida (Grid)')
ax_gp_fp.set_ylabel('Posición final')
ax_gp_fp.set_title('Posición final vs Posición de salida')
st.pyplot(fig_gp_fp)

st.markdown("""
Podemos observar una **correlación positiva** entre la posición de salida y la posición final, lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
""")

# 2. Correlación entre número de pit stops y posición final
st.write("### 2. Número de pit stops vs Posición final")

data_np_fp = corr_data[['num_pit_stops', 'positionOrder']].dropna()
corr_np_fp = data_np_fp['num_pit_stops'].corr(data_np_fp['positionOrder'])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_np_fp:.2f}")

fig_np_fp, ax_np_fp = plt.subplots()
sns.scatterplot(data=data_np_fp, x='num_pit_stops', y='positionOrder', alpha=0.5, ax=ax_np_fp)
ax_np_fp.set_xlabel('Número de pit stops')
ax_np_fp.set_ylabel('Posición final')
ax_np_fp.set_title('Posición final vs Número de pit stops')
st.pyplot(fig_np_fp)

st.markdown("""
Existe una **correlación positiva débil** entre el número de pit stops y la posición final. Esto sugiere que más pit stops pueden estar asociados con posiciones finales más bajas, posiblemente debido al tiempo perdido en paradas adicionales.
""")

# 3. Correlación entre edad del piloto y puntos obtenidos
st.write("### 3. Edad del piloto vs Puntos obtenidos")

data_age_points = corr_data[['driver_age', 'points']].dropna()
corr_age_points = data_age_points['driver_age'].corr(data_age_points['points'])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_age_points:.2f}")

fig_age_points, ax_age_points = plt.subplots()
sns.scatterplot(data=data_age_points, x='driver_age', y='points', alpha=0.5, ax=ax_age_points)
ax_age_points.set_xlabel('Edad del piloto')
ax_age_points.set_ylabel('Puntos obtenidos')
ax_age_points.set_title('Puntos obtenidos vs Edad del piloto')
st.pyplot(fig_age_points)

st.markdown("""
La correlación entre la edad del piloto y los puntos obtenidos es **débil**. Esto indica que no hay una relación significativa entre la edad y el rendimiento en términos de puntos en una carrera individual.
""")

# 4. Correlación entre posición en clasificación y posición final
st.write("### 4. Posición en clasificación vs Posición final")

data_qp_fp = corr_data[['qualifying_position', 'positionOrder']].dropna()
corr_qp_fp = data_qp_fp['qualifying_position'].corr(data_qp_fp['positionOrder'])

st.write(f"**Coeficiente de correlación de Pearson:** {corr_qp_fp:.2f}")

fig_qp_fp, ax_qp_fp = plt.subplots()
sns.scatterplot(data=data_qp_fp, x='qualifying_position', y='positionOrder', alpha=0.5, ax=ax_qp_fp)
ax_qp_fp.set_xlabel('Posición en clasificación')
ax_qp_fp.set_ylabel('Posición final')
ax_qp_fp.set_title('Posición final vs Posición en clasificación')
st.pyplot(fig_qp_fp)

st.markdown("""
Existe una **correlación positiva fuerte** entre la posición en clasificación y la posición final. Esto indica que una buena posición en clasificación suele traducirse en una mejor posición al final de la carrera.
""")

# ---------------------------
# Análisis adicional con datos de clima (si están disponibles)
if 'weather' in data:
    st.write("## Análisis con Datos de Clima")

    # Suponiendo que 'weather' contiene información relevante
    weather = data['weather']
    weather.replace('\\N', np.nan, inplace=True)

    # Convertir columnas a tipos apropiados
    weather_cols = ['temperature', 'humidity', 'wind_speed', 'rainfall']
    for col in weather_cols:
        if col in weather.columns:
            weather[col] = pd.to_numeric(weather[col], errors='coerce')

    # Unir 'weather' con 'races' y 'results'
    weather_results = pd.merge(results_races_drivers, weather, on='raceId', how='left')

    # Seleccionar variables para correlación
    weather_corr_vars = ['positionOrder', 'points'] + weather_cols
    weather_data = weather_results[weather_corr_vars].dropna()

    # Mostrar matriz de correlación
    st.write("### Matriz de Correlación con Variables Climáticas")

    weather_corr_matrix = weather_data.corr()

    fig_weather_corr, ax_weather_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(weather_corr_matrix, annot=True, cmap='coolwarm', ax=ax_weather_corr)
    st.pyplot(fig_weather_corr)

    st.markdown("""
    La matriz de correlación incluye variables climáticas como temperatura, humedad, velocidad del viento y precipitación. Esto nos permite explorar cómo las condiciones climáticas pueden afectar el rendimiento en las carreras.
    """)
else:
    st.write("**Datos de clima no disponibles para el análisis.**")

