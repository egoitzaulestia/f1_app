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


# pages/9_Correlaciones.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Análisis de Correlaciones",
    page_icon="🏎️",
    layout="wide",
)

st.write("# Análisis de Correlaciones 📊")

st.markdown("""
Explora las correlaciones entre diferentes variables en los datos de Fórmula 1.
""")

# Cargar datasets
results = pd.read_csv('data/results.csv')

# Reemplazar valores no numéricos como '\\N' con NaN
results.replace('\\N', np.nan, inplace=True)

# Convertir las columnas numéricas a tipo numérico (si contienen algún valor no convertible a float)
numeric_cols = ['grid', 'positionOrder', 'points', 'laps', 'milliseconds']
results[numeric_cols] = results[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Crear matriz de correlación, eliminando valores NaN
corr_matrix = results[numeric_cols].corr()

# Mostrar la matriz de correlación
st.write("## Matriz de Correlación")

fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Análisis adicional
st.markdown("""
Podemos observar que existe una correlación negativa entre la posición de salida ('grid') y la posición final ('positionOrder'), lo que indica que los pilotos que empiezan en posiciones delanteras tienden a terminar en mejores posiciones.
""")
