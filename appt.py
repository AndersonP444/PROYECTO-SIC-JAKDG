import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from streamlit_lottie import st_lottie

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis Futbolístico",
    page_icon="⚽",
    layout="wide"
)

# Función para cargar animaciones Lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cargar datos
@st.cache_data
def load_data():
    file_path = 'https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/valores_mercado_actualizados%20(3).csv'
    return pd.read_csv(file_path)

# Función para convertir valores de mercado
def convertir_valor(valor):
    if isinstance(valor, str):
        if "mil €" in valor:
            return int(float(valor.replace(" mil €", "").replace(",", ".")) * 1_000)
        elif "mill. €" in valor:
            return int(float(valor.replace(" mill. €", "").replace(",", ".")) * 1_000_000)
    return None

# Función para convertir URLs a imágenes en cualquier columna
def convertir_urls_a_imagenes(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    return df_copy

# Función para generar valores mensuales interpolados
def generar_valores_mensuales(valor_inicial, valor_final):
    fecha_inicio = datetime(2024, 1, 1)
    fecha_actual = datetime.now()
    meses = []
    valores = []
    
    # Generar lista de meses
    fecha_actual = fecha_actual.replace(day=1)
    fecha = fecha_inicio
    while fecha <= fecha_actual:
        meses.append(fecha.strftime('%B %Y'))
        fecha += timedelta(days=32)
        fecha = fecha.replace(day=1)
    
    # Calcular valores interpolados
    num_meses = len(meses)
    for i in range(num_meses):
        valor = valor_inicial + (valor_final - valor_inicial) * (i / (num_meses - 1))
        valores.append(valor)
    
    return meses, valores

# Cargar y preparar datos
data = load_data()
data["Valor de Mercado en 01/01/2024"] = data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
data["Valor de Mercado Actual"] = data["Valor de Mercado Actual"].apply(convertir_valor)

# Convertir las URLs en imágenes para la tabla
data_con_imagenes = convertir_urls_a_imagenes(data)

# Sidebar con menú principal
st.sidebar.title("Menú Principal")
menu_principal = st.sidebar.radio(
    "Seleccione una sección:",
    ["Introducción", "Objetivos", "Metodología", "Herramientas", "Resultados", "Conclusiones"]
)

if menu_principal == "Introducción":
    st.title("Introducción")
    st.write("""
    La industria del fútbol ha evolucionado significativamente, convirtiéndose en un mercado 
    donde el valor de los jugadores es un indicador crucial de su desempeño y potencial.
    """)
    
    lottie_url = "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
    lottie_coding = load_lottieurl(lottie_url)
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)
    
    # Formatear valores de mercado con símbolo de euro
    data["Valor de Mercado en 01/01/2024"] = data["Valor de Mercado en 01/01/2024"].apply(lambda x: f"€{int(x):,}" if pd.notnull(x) else "N/A")
    data["Valor de Mercado Actual"] = data["Valor de Mercado Actual"].apply(lambda x: f"€{int(x):,}" if pd.notnull(x) else "N/A")

    # Convertir las URLs en imágenes para la tabla
    data_con_imagenes = convertir_urls_a_imagenes(data)

    # Mostrar la tabla con imágenes de los jugadores
    with st.container():
        st.subheader("Datos de Jugadores")
        st.write("Tabla con imágenes de los jugadores y valores de mercado.")
        st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)


elif menu_principal == "Metodología":
    st.title("Metodología")
    
    visualizacion = st.selectbox(
        "Seleccione tipo de visualización:",
        ["Evolución Individual", "Comparación entre Jugadores", "Tendencias Generales"]
    )
    
    if visualizacion == "Evolución Individual":
        st.subheader("Evolución Individual del Valor de Mercado")
        nombre_jugador = st.selectbox("Selecciona un jugador:", data['Nombre'].unique())
        
        jugador = data[data['Nombre'] == nombre_jugador]
        if not jugador.empty:
            valor_inicial = jugador['Valor de Mercado en 01/01/2024'].iloc[0]
            valor_final = jugador['Valor de Mercado Actual'].iloc[0]
            
            meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=meses,
                y=valores,
                mode='lines+markers',
                name=nombre_jugador,
                line=dict(width=3),
                marker=dict(size=10)
            ))
            
            fig.update_layout(
                title=f'Evolución Mensual del Valor de Mercado de {nombre_jugador}',
                xaxis_title='Mes',
                yaxis_title='Valor de Mercado (€)',
                hovermode='x unified',
                showlegend=True
            )
            st.plotly_chart(fig)
            
            # Mostrar tabla de valores mensuales
            df_mensual = pd.DataFrame({
                'Mes': meses,
                'Valor de Mercado (€)': [f"€{int(v):,}" for v in valores]
            })
            st.write("Valores mensuales:")
            st.dataframe(df_mensual)
            
    elif visualizacion == "Comparación entre Jugadores":
        st.subheader("Comparación entre Jugadores")
        col1, col2 = st.columns(2)
        with col1:
            jugador1 = st.selectbox("Primer jugador:", data['Nombre'].unique())
        with col2:
            jugador2 = st.selectbox("Segundo jugador:", data['Nombre'].unique())
        
        if jugador1 and jugador2:
            fig = go.Figure()
            
            for jugador in [jugador1, jugador2]:
                datos_jugador = data[data['Nombre'] == jugador]
                valor_inicial = datos_jugador['Valor de Mercado en 01/01/2024'].iloc[0]
                valor_final = datos_jugador['Valor de Mercado Actual'].iloc[0]
                
                meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
                
                fig.add_trace(go.Scatter(
                    x=meses,
                    y=valores,
                    mode='lines+markers',
                    name=jugador,
                    line=dict(width=3),
                    marker=dict(size=10)
                ))
            
            fig.update_layout(
                title='Comparación de Evolución Mensual del Valor de Mercado',
                xaxis_title='Mes',
                yaxis_title='Valor de Mercado (€)',
                hovermode='x unified',
                showlegend=True
            )
            st.plotly_chart(fig)
    
    elif visualizacion == "Tendencias Generales":
        st.subheader("Tendencias Generales del Mercado")
        
        fig = go.Figure()
        for _, jugador in data.iterrows():
            valor_inicial = jugador['Valor de Mercado en 01/01/2024']
            valor_final = jugador['Valor de Mercado Actual']
            
            meses, valores = generar_valores_mensuales(valor_inicial, valor_final)
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=valores,
                mode='lines',
                name=jugador['Nombre'],
                opacity=0.5
            ))
        
        fig.update_layout(
            title='Tendencias Generales del Valor de Mercado',
            xaxis_title='Mes',
            yaxis_title='Valor de Mercado (€)',
            hovermode='x unified',
            showlegend=True
        )
        st.plotly_chart(fig)

elif menu_principal == "Objetivos":
    st.title("Objetivos del Proyecto")
    st.write("""
    ### Objetivos Principales:
    - Analizar y visualizar el valor de mercado de los jugadores
    - Evaluar el incremento porcentual del valor de mercado a lo largo del tiempo
    - Identificar patrones y tendencias en la valoración de jugadores
    """)

elif menu_principal == "Herramientas":
    st.title("Herramientas y Tecnologías")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Tecnologías Principales")
        st.write("""
        - Python
        - Pandas
        - Streamlit
        - Plotly
        - Google Colab
        - Jupiter Notebook
        """)
    
    with col2:
        st.header("Bibliotecas Adicionales")
        st.write("""
        - Matplotlib
        - Seaborn
        - Streamlit-Lottie
        """)

elif menu_principal == "Resultados":
    st.title("Resultados")
    
    tab1, tab2, tab3 = st.tabs(["Estadísticas Generales", "Análisis de Tendencias", "Recomendaciones"])
    
    with tab1:
        st.header("Estadísticas Generales")
        st.write("Estadísticas descriptivas de los valores de mercado:")
        st.dataframe(data[['Valor de Mercado en 01/01/2024', 'Valor de Mercado Actual']].describe())
        
    with tab2:
        st.header("Análisis de Tendencias")
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=data['Valor de Mercado en 01/01/2024'],
            name='Enero 2024'
        ))
        fig.add_trace(go.Box(
            y=data['Valor de Mercado Actual'],
            name='Actual'
        ))
        fig.update_layout(
            title='Distribución de Valores de Mercado',
            yaxis_title='Valor de Mercado (€)'
        )
        st.plotly_chart(fig)
        
    with tab3:
        st.header("Recomendaciones")
        st.write("""
        Basadas en el análisis de datos:
        - Recomendaciones para clubes
        - Estrategias de inversión
        - Oportunidades de mercado
        """)

else:  # Conclusiones
    st.title("Conclusiones")
    st.write("""
    ### Principales Hallazgos:
    - El análisis de datos en el fútbol ofrece insights valiosos para la toma de decisiones
    - Las tendencias del mercado muestran patrones significativos en la valoración de jugadores
    - La gestión basada en datos puede mejorar significativamente las estrategias de los equipos
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA")
