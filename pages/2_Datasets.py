# pages/2_Datasets.py

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Datasets",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Datasets Utilizados 📂")

st.markdown("A continuación, puedes explorar los distintos datasets utilizados en este proyecto.")

# Lista de datasets
datasets = {
    "Pilotos": "data/drivers.csv",
    "Constructores": "data/constructors.csv",
    "Resultados": "data/results.csv",
    "Circuitos": "data/circuits.csv",
    "Resultados de Constructores": "data/constructor_results.csv",
    "Clasificación de Constructores": "data/constructor_standings.csv",
    "Clasificación de Pilotos": "data/driver_standings.csv",
    "Tiempor se Vuelta": "data/lap_times.csv",
    "Pit Stops": "data/pit_stops.csv",
    "Clasificación": "data/qualifying.csv",
    "Temporada": "data/seasons.csv",
    "Resultados de Sprints": "data/sprint_results.csv",
    "Estado": "data/status.csv",
    "F1 Weather (2023-2018)": "data/F1 Weather(2023-2018).csv"
}

# Selección de dataset
dataset_name = st.selectbox("Selecciona un dataset", list(datasets.keys()))
data = pd.read_csv(datasets[dataset_name])

st.write(f"## {dataset_name} Dataset")

# Muestra de datos
st.write("### Muestra de Datos:")
st.dataframe(data.head(21))

# Descripción estadística mejorada
st.write("### Descripción Estadística Completa:")

# Crear la descripción estadística extendida
descripcion = data.describe(include="all").T  # Transponer la tabla para mayor legibilidad
descripcion["Tipo de Dato"] = data.dtypes  # Añadir la columna de tipos de datos
descripcion["Valores_únicos"] = data.nunique()  # Número de valores únicos por columna
descripcion["Valores_Nulos"] = data.isnull().sum()  # Número de valores nulos por columna
descripcion["Valores_Nulos_%"] = (descripcion["Valores_Nulos"] / data.shape[0]) * 100  # Porcentaje de valores nulos

st.dataframe(descripcion)

# # Información adicional de columnas
# st.write("### Información de Columnas:")
# col_info = pd.DataFrame({
#     "Columna": data.columns,
#     "Tipo de Dato": data.dtypes,
#     "Valores Nulos": data.isnull().sum(),
#     "Valores Únicos": data.nunique()
# })
# st.dataframe(col_info)
