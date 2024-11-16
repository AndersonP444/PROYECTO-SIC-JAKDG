# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import requests
from streamlit_lottie import st_lottie

# Función para cargar animaciones Lottie desde una URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Configuración de la página
st.title("ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA.")
st.write("Exploración interactiva de las estadísticas de jugadores basada en sus valores de mercado.")

# Carga y muestra una animación Lottie
lottie_url = "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
lottie_coding = load_lottieurl(lottie_url)
if lottie_coding:
    st_lottie(lottie_coding, height=200, width=300)

# Cargar el archivo CSV desde GitHub
file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados.csv'
data = pd.read_csv(file_path)

# Función para convertir los valores de mercado a euros completos (enteros)
def convertir_valor(valor):
    if isinstance(valor, str):
        if "mil €" in valor:
            return int(float(valor.replace(" mil €", "").replace(",", ".")) * 1_000)
        elif "mill. €" in valor:
            return int(float(valor.replace(" mill. €", "").replace(",", ".")) * 1_000_000)
    return None

# Verificar y convertir las columnas de valores de mercado
if 'Valor de Mercado en 01/01/2024' in data.columns and 'Valor de Mercado Actual' in data.columns:
    data["Valor de Mercado en 01/01/2024"] = data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
    data["Valor de Mercado Actual"] = data["Valor de Mercado Actual"].apply(convertir_valor)

# Fecha de inicio y fecha actual
fecha_inicio = datetime(2024, 1, 1)
fecha_hoy = datetime.today()

# Contenedor para mostrar la tabla
with st.container():
    st.subheader("Datos de Jugadores")
    st.write("Tabla de datos de los valores de mercado de los jugadores.")
    st.dataframe(data)  # Mostrar el DataFrame en un contenedor separado

# Contenedor para seleccionar un jugador y mostrar su gráfica
with st.container():
    st.subheader("Evolución del Valor de Mercado de un Jugador")
    nombre_jugador = st.selectbox("Selecciona un jugador:", data['Nombre'].unique())

    # Función para graficar el crecimiento en valor de mercado de un jugador
    def graficar_jugador(nombre_jugador):
        jugador = data[data['Nombre'] == nombre_jugador]
        if not jugador.empty:
            valor_inicial = jugador['Valor de Mercado en 01/01/2024'].values[0]
            valor_actual = jugador['Valor de Mercado Actual'].values[0]
            fechas = pd.date_range(fecha_inicio, fecha_hoy, freq='MS')
            valores = [valor_inicial + (valor_actual - valor_inicial) * (i / (len(fechas) - 1)) for i in range(len(fechas))]
            fig = go.Figure(data=go.Bar(x=fechas, y=valores))
            fig.update_layout(title=f'Evolución del Valor de Mercado de {nombre_jugador}',
                              xaxis_title='Fecha',
                              yaxis_title='Valor de Mercado (€)',
                              xaxis=dict(tickformat="%Y-%m"))
            return fig
        else:
            st.write("Jugador no encontrado.")
            return None

    fig = graficar_jugador(nombre_jugador)
    if fig:
        st.plotly_chart(fig)

# Contenedor para la gráfica de todos los jugadores
with st.container():
    st.subheader("Evolución del Porcentaje de Mercado de Todos los Jugadores")
    def graficar_todos_los_jugadores():
        fig = go.Figure()
        fechas = pd.date_range(fecha_inicio, fecha_hoy, freq='MS')
        for _, jugador in data.iterrows():
            nombre_jugador = jugador['Nombre']
            valor_inicial = jugador['Valor de Mercado en 01/01/2024']
            valor_actual = jugador['Valor de Mercado Actual']
            valores = [valor_inicial + (valor_actual - valor_inicial) * (i / (len(fechas) - 1)) for i in range(len(fechas))]
            fig.add_trace(go.Scatter(x=fechas, y=valores, mode='lines', name=nombre_jugador))
        fig.update_layout(title='Evolución del Porcentaje de Mercado de Todos los Jugadores',
                          xaxis_title='Fecha',
                          yaxis_title='Valor de Mercado (€)',
                          xaxis=dict(tickformat="%Y-%m"))
        return fig

    fig_todos = graficar_todos_los_jugadores()
    st.plotly_chart(fig_todos)


# Contenedor para la gráfica de todos los jugadores
with st.container():
    st.subheader("Evolución del Valor de Mercado de Todos los Jugadores")
    
    def graficar_todos_los_jugadores():
        fig = go.Figure()
        fechas = pd.date_range(fecha_inicio, fecha_hoy, freq='MS')
        
        for _, jugador in data.iterrows():
            nombre_jugador = jugador['Nombre']
            valor_inicial = jugador['Valor de Mercado en 01/01/2024']
            valor_actual = jugador['Valor de Mercado Actual']
            valores = [valor_inicial + (valor_actual - valor_inicial) * (i / (len(fechas) - 1)) for i in range(len(fechas))]
            fig.add_trace(go.Bar(x=fechas, y=valores, name=nombre_jugador))
        
        fig.update_layout(title='Evolución del Valor de Mercado de Todos los Jugadores',
                          xaxis_title='Fecha',
                          yaxis_title='Valor de Mercado (€)',
                          barmode='stack',
                          xaxis=dict(tickformat="%Y-%m"))
        
        return fig

    fig_todos = graficar_todos_los_jugadores()
    st.plotly_chart(fig_todos)

# Enlace directo al archivo raw en GitHub
file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
data = pd.read_csv(file_path)

# Función para convertir URLs en imágenes en cualquier columna
def convertir_urls_a_imagenes(df):
    # Crear una copia para no modificar el DataFrame original
    df_copy = df.copy()
    
    # Identificar columnas que contienen URLs y convertirlas en HTML de imágenes
    for col in df_copy.columns:
        # Comprobar si la columna contiene URLs (esto asume que todas las filas de la columna contienen URLs si la primera fila lo tiene)
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    
    return df_copy

# Convertir las URLs en imágenes para la tabla
data_con_imagenes = convertir_urls_a_imagenes(data)

# Mostrar la tabla en Streamlit con las imágenes renderizadas
with st.container():
    st.subheader("Datos de Jugadores")
    st.write("Tabla completa con imágenes de los jugadores y valores de mercado.")
    # Renderizar la tabla con HTML para mostrar las imágenes
    st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)
