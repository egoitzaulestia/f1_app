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
circuit_lengths_df = pd.DataFrame.from_dict(data['circuit_lengths'], orient='index', columns=['circuit_length_km'])
circuit_lengths_df.reset_index(inplace=True)
circuit_lengths_df.rename(columns={'index': 'circuitRef'}, inplace=True)
circuit_lengths_df['circuit_length_km'] = pd.to_numeric(circuit_lengths_df['circuit_length_km'], errors='coerce')

# Unir 'circuits' con 'circuit_lengths' a través de 'circuitRef'
circuits = pd.merge(circuits, circuit_lengths_df, on='circuitRef', how='left')

# Unir 'results_races_drivers' con 'circuits' para obtener la longitud del circuito
results_races_drivers = pd.merge(results_races_drivers, circuits[['circuitId', 'circuit_length_km']], on='circuitId', how='left')

# Calcular distancia total recorrida por cada piloto en cada carrera
results_races_drivers['distancia_total_km'] = results_races_drivers['laps'] * results_races_drivers['circuit_length_km']

# Calcular tiempo en horas, evitando división por cero y manejando valores faltantes
results_races_drivers['tiempo_horas'] = results_races_drivers['milliseconds'] / (1000 * 60 * 60)
results_races_drivers['tiempo_horas'].replace(0, np.nan, inplace=True)  # Evitar división por cero

# Calcular velocidad promedio en km/h
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

# Verificar cuántos datos tenemos antes de eliminar filas con NaN
st.write(f"Total de registros antes de eliminar NaNs: {len(corr_data)}")

# Eliminar filas donde todas las variables son NaN
corr_data = corr_data.dropna(how='all')

# Eliminar columnas con todos los valores NaN
corr_data = corr_data.dropna(axis=1, how='all')

# Verificar cuántos datos tenemos después de eliminar filas con NaN
st.write(f"Total de registros después de eliminar NaNs: {len(corr_data)}")

if corr_data.empty:
    st.warning("No hay datos suficientes para generar la matriz de correlación.")
else:
    # ---------------------------
    # Matriz de Correlación General
    st.write("## Matriz de Correlación General")

    corr_matrix = corr_data.corr()

    # Actualizar nombres de columnas a español
    inverse_corr_variables = {v: k for k, v in corr_variables.items()}
    corr_matrix.rename(columns=inverse_corr_variables, inplace=True)
    corr_matrix.rename(index=inverse_corr_variables, inplace=True)

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

    if scatter_data.empty:
        st.warning("No hay datos suficientes para generar el gráfico de dispersión.")
    else:
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

    # Función para generar análisis predefinidos
    def analizar_correlacion(var_x_name, var_y_name):
        x_var = corr_variables[var_x_name]
        y_var = corr_variables[var_y_name]
        data = corr_data[[x_var, y_var]].dropna()
        if data.empty:
            st.write(f"No hay datos suficientes para analizar {var_x_name} vs {var_y_name}.")
            return
        corr_coef = data[x_var].corr(data[y_var])
        st.write(f"**Coeficiente de correlación de Pearson:** {corr_coef:.2f}")
        fig, ax = plt.subplots()
        sns.scatterplot(data=data, x=x_var, y=y_var, alpha=0.5, ax=ax)
        ax.set_xlabel(var_x_name)
        ax.set_ylabel(var_y_name)
        ax.set_title(f'{var_y_name} vs {var_x_name}')
        st.pyplot(fig)
        return corr_coef

    # 1. Correlación entre posición de salida y posición final
    st.write("### 1. Posición de salida vs Posición final")
    corr_gp_fp = analizar_correlacion('Posición de salida (Grid)', 'Posición final')
    st.markdown("""
    Podemos observar una **correlación positiva** entre la posición de salida y la posición final, lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
    """)

    # 2. Correlación entre número de pit stops y posición final
    st.write("### 2. Número de pit stops vs Posición final")
    corr_np_fp = analizar_correlacion('Número de pit stops', 'Posición final')
    st.markdown("""
    Existe una **correlación positiva débil** entre el número de pit stops y la posición final. Esto sugiere que más pit stops pueden estar asociados con posiciones finales más bajas, posiblemente debido al tiempo perdido en paradas adicionales.
    """)

    # 3. Correlación entre edad del piloto y puntos obtenidos
    st.write("### 3. Edad del piloto vs Puntos obtenidos")
    corr_age_points = analizar_correlacion('Edad del piloto', 'Puntos obtenidos')
    st.markdown("""
    La correlación entre la edad del piloto y los puntos obtenidos es **débil**. Esto indica que no hay una relación significativa entre la edad y el rendimiento en términos de puntos en una carrera individual.
    """)

    # 4. Correlación entre posición en clasificación y posición final
    st.write("### 4. Posición en clasificación vs Posición final")
    corr_qp_fp = analizar_correlacion('Posición en clasificación', 'Posición final')
    st.markdown("""
    Existe una **correlación positiva fuerte** entre la posición en clasificación y la posición final. Esto indica que una buena posición en clasificación suele traducirse en una mejor posición al final de la carrera.
    """)
