import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
    spain_data = pd.read_csv('https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/CSV%20DESPUES%20DEL%20PROCESAMIENTO%20DE%20DATOS/valores_mercado_actualizados_con_estadisticas.csv')
    bundesliga_data = pd.read_csv('https://raw.githubusercontent.com/AndersonP444/PROYECTO-SIC-JAKDG/main/CSV%20DESPUES%20DEL%20PROCESAMIENTO%20DE%20DATOS/valores_mercado_bundesliga_con_estadisticas.csv')
    return spain_data, bundesliga_data

# Función para convertir valores de mercado
def convertir_valor(valor):
    if isinstance(valor, str):
        if "mil €" in valor:
            return int(float(valor.replace(" mil €", "").replace(",", ".")) * 1_000)
        elif "mill. €" in valor:
            return int(float(valor.replace(" mill. €", "").replace(",", ".")) * 1_000_000)
    return None

# Función para convertir URLs a imágenes
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
    
    fecha_actual = fecha_actual.replace(day=1)
    fecha = fecha_inicio
    while fecha <= fecha_actual:
        meses.append(fecha.strftime('%B %Y'))
        fecha += timedelta(days=32)
        fecha = fecha.replace(day=1)
    
    num_meses = len(meses)
    for i in range(num_meses):
        valor = valor_inicial + (valor_final - valor_inicial) * (i / (num_meses - 1))
        valores.append(valor)
    
    return meses, valores

# Cargar datos
spain_data, bundesliga_data = load_data()

# Procesar datos de España
spain_data["Valor de Mercado en 01/01/2024"] = spain_data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
spain_data["Valor de Mercado Actual"] = spain_data["Valor de Mercado Actual"].apply(convertir_valor)

# Procesar datos de Bundesliga
bundesliga_data["Valor de Mercado en 01/01/2024"] = bundesliga_data["Valor de Mercado en 01/01/2024"].apply(convertir_valor)
bundesliga_data["Valor de Mercado Actual"] = bundesliga_data["Valor de Mercado Actual"].apply(convertir_valor)

# Sidebar con menú principal
st.sidebar.title("Menú Principal")
menu_principal = st.sidebar.radio(
    "Seleccione una sección:",
    ["Introducción", "Objetivos", "Metodología", "Herramientas", "Resultados", "Conclusiones"]
)

# Selector de liga
liga_seleccionada = st.sidebar.selectbox(
    "Seleccione la liga:",
    ["LaLiga", "Bundesliga", "Comparativa"]
)

# Función para convertir URLs a imágenes
def convertir_urls_a_imagenes(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    return df_copy

# Función para convertir URLs a imágenes
def convertir_urls_a_imagenes(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        if df_copy[col].astype(str).str.startswith('http').any():
            df_copy[col] = df_copy[col].apply(lambda url: f'<img src="{url}" width="50">' if isinstance(url, str) and url.startswith('http') else url)
    return df_copy

# Código principal
if menu_principal == "Introducción":
    st.title("Introducción")
    st.write("""
    La industria del fútbol ha evolucionado significativamente, convirtiéndose en un mercado 
    donde el valor de los jugadores es un indicador crucial de su desempeño y potencial.
    """)

    # Cargar animación Lottie
    lottie_url = "https://lottie.host/embed/3d48d4b9-51ad-4b7d-9d28-5e248cace11/Rz3QtSCq3.json"
    lottie_coding = load_lottieurl(lottie_url)
    if lottie_coding:
        st_lottie(lottie_coding, height=200, width=300)

    # Mostrar datos según la liga seleccionada
    if liga_seleccionada == "LaLiga":
        data_to_show = spain_data
        title = "Datos de Jugadores de LaLiga"
    elif liga_seleccionada == "Bundesliga":
        data_to_show = bundesliga_data
        title = "Datos de Jugadores de Bundesliga"
    else:
        st.subheader("Comparativa entre LaLiga y Bundesliga")
        
        # Mostrar tablas en Comparativa
        def generar_tabla_html(data):
            data_con_imagenes = convertir_urls_a_imagenes(data)
            return data_con_imagenes.to_html(escape=False, index=False)

        # Tabla de LaLiga
        st.write("### LaLiga")
        tabla_laliga_html = generar_tabla_html(spain_data)
        st.markdown(tabla_laliga_html, unsafe_allow_html=True)

        # Tabla de Bundesliga
        st.write("### Bundesliga")
        tabla_bundesliga_html = generar_tabla_html(bundesliga_data)
        st.markdown(tabla_bundesliga_html, unsafe_allow_html=True)

    # Mostrar tabla individual con imágenes (si no es Comparativa)
    if liga_seleccionada != "Comparativa":
        with st.container():
            st.subheader(title)
            data_con_imagenes = convertir_urls_a_imagenes(data_to_show)
            st.markdown(data_con_imagenes.to_html(escape=False), unsafe_allow_html=True)

if menu_principal == "Metodología":
    st.title("Metodología")
    
    if liga_seleccionada == "Comparativa":
        st.subheader("Análisis Comparativo: LaLiga vs Bundesliga")
        
        # 1. Gráfica de violín
        st.subheader("1. Distribución General de Valores de Mercado")
        fig_violin = go.Figure()

        fig_violin.add_trace(go.Violin(
            y=spain_data['Valor de Mercado Actual'],
            name='LaLiga',
            box_visible=True,
            meanline_visible=True,
            line_color='blue',
            fillcolor='rgba(0, 0, 255, 0.3)',
            opacity=0.7
        ))

        fig_violin.add_trace(go.Violin(
            y=bundesliga_data['Valor de Mercado Actual'],
            name='Bundesliga',
            box_visible=True,
            meanline_visible=True,
            line_color='green',
            fillcolor='rgba(0, 255, 0, 0.3)',
            opacity=0.7
        ))

        fig_violin.update_layout(
            title="Distribución de Valores de Mercado por Liga",
            yaxis_title="Valor de Mercado (€)",
            xaxis_title="Ligas",
            violingap=0.5,
            violingroupgap=0.3,
            showlegend=True
        )

        st.plotly_chart(fig_violin)

        # 2. Gráfica de dispersión
        st.subheader("2. Relación Edad vs Valor de Mercado")
        fig_scatter = go.Figure()

        fig_scatter.add_trace(go.Scatter(
            x=spain_data['Edad'],
            y=spain_data['Valor de Mercado Actual'],
            mode='markers',
            name='LaLiga',
            marker=dict(
                size=10,
                color='blue',
                opacity=0.6
            )
        ))

        fig_scatter.add_trace(go.Scatter(
            x=bundesliga_data['Edad'],
            y=bundesliga_data['Valor de Mercado Actual'],
            mode='markers',
            name='Bundesliga',
            marker=dict(
                size=10,
                color='green',
                opacity=0.6
            )
        ))

        fig_scatter.update_layout(
            title="Relación entre Edad y Valor de Mercado",
            xaxis_title="Edad",
            yaxis_title="Valor de Mercado (€)",
            showlegend=True
        )

        st.plotly_chart(fig_scatter)

        # 3. Comparativa Individual
        st.subheader("3. Comparativa Individual de Jugadores")
        col1, col2 = st.columns(2)
        with col1:
            jugador_laliga = st.selectbox("Selecciona un jugador de LaLiga:", spain_data['Nombre'].unique())
        with col2:
            jugador_bundesliga = st.selectbox("Selecciona un jugador de Bundesliga:", bundesliga_data['Nombre'].unique())

        datos_laliga = spain_data[spain_data['Nombre'] == jugador_laliga].iloc[0]
        datos_bundesliga = bundesliga_data[bundesliga_data['Nombre'] == jugador_bundesliga].iloc[0]

        # 3.1 Gráfica de evolución temporal
        meses_laliga, valores_laliga = generar_valores_mensuales(
            datos_laliga['Valor de Mercado en 01/01/2024'],
            datos_laliga['Valor de Mercado Actual']
        )
        meses_bundesliga, valores_bundesliga = generar_valores_mensuales(
            datos_bundesliga['Valor de Mercado en 01/01/2024'],
            datos_bundesliga['Valor de Mercado Actual']
        )

        fig_evolucion = go.Figure()

        fig_evolucion.add_trace(go.Scatter(
            x=meses_laliga,
            y=valores_laliga,
            mode='lines+markers',
            name=f"{jugador_laliga} (LaLiga)",
            line=dict(color='red', width=3),
            marker=dict(size=10)
        ))

        fig_evolucion.add_trace(go.Scatter(
            x=meses_bundesliga,
            y=valores_bundesliga,
            mode='lines+markers',
            name=f"{jugador_bundesliga} (Bundesliga)",
            line=dict(color='blue', width=3),
            marker=dict(size=10)
        ))

        fig_evolucion.update_layout(
            title='Evolución Mensual del Valor de Mercado',
            xaxis_title='Mes',
            yaxis_title='Valor de Mercado (€)',
            hovermode='x unified',
            showlegend=True
        )

        st.plotly_chart(fig_evolucion)

        # 3.2 Gráfica de barras comparativa
        fig_barras = go.Figure(data=[
            go.Bar(name='Valor Inicial', 
                  x=['LaLiga', 'Bundesliga'], 
                  y=[datos_laliga['Valor de Mercado en 01/01/2024'], 
                     datos_bundesliga['Valor de Mercado en 01/01/2024']],
                  marker_color=['rgba(255, 0, 0, 0.7)', 'rgba(0, 0, 255, 0.7)']),
            go.Bar(name='Valor Actual', 
                  x=['LaLiga', 'Bundesliga'], 
                  y=[datos_laliga['Valor de Mercado Actual'], 
                     datos_bundesliga['Valor de Mercado Actual']],
                  marker_color=['rgba(255, 0, 0, 0.9)', 'rgba(0, 0, 255, 0.9)'])
        ])

        fig_barras.update_layout(
            title=f'Comparación de Valores: {jugador_laliga} vs {jugador_bundesliga}',
            barmode='group',
            yaxis_title='Valor de Mercado (€)'
        )

        st.plotly_chart(fig_barras)

        # 4. Análisis de Variación Porcentual
        variacion_laliga = ((datos_laliga['Valor de Mercado Actual'] - 
                            datos_laliga['Valor de Mercado en 01/01/2024']) / 
                            datos_laliga['Valor de Mercado en 01/01/2024'] * 100)
        
        variacion_bundesliga = ((datos_bundesliga['Valor de Mercado Actual'] - 
                                datos_bundesliga['Valor de Mercado en 01/01/2024']) / 
                                datos_bundesliga['Valor de Mercado en 01/01/2024'] * 100)

        # Gráfica de variación porcentual
        fig_variacion = go.Figure(data=[
            go.Bar(
                x=['LaLiga', 'Bundesliga'],
                y=[variacion_laliga, variacion_bundesliga],
                marker_color=['red', 'blue'],
                text=[f"{variacion_laliga:.1f}%", f"{variacion_bundesliga:.1f}%"],
                textposition='auto',
            )
        ])

        fig_variacion.update_layout(
            title='Variación Porcentual del Valor de Mercado',
            yaxis_title='Variación (%)',
            showlegend=False
        )

        st.plotly_chart(fig_variacion)

        # Análisis detallado
        st.write(f"""
        ### Análisis Comparativo Detallado

        #### 1. Distribución General (Gráfica de Violín)
        - Muestra la concentración de valores en diferentes rangos
        - Permite identificar patrones de valoración en cada liga
        - Revela la dispersión y simetría de los valores

        #### 2. Relación Edad-Valor (Gráfica de Dispersión)
        - Visualiza la correlación entre edad y valor de mercado
        - Identifica tendencias de valoración por edad
        - Permite comparar políticas de valoración entre ligas

        #### 3. Análisis Individual

        **{jugador_laliga} (LaLiga)**
        - Valor inicial (Enero 2024): €{datos_laliga['Valor de Mercado en 01/01/2024']:,}
        - Valor actual: €{datos_laliga['Valor de Mercado Actual']:,}
        - Variación porcentual: {variacion_laliga:.2f}%
        - Tendencia: {'Positiva ↑' if variacion_laliga > 0 else 'Negativa ↓' if variacion_laliga < 0 else 'Estable →'}

        **{jugador_bundesliga} (Bundesliga)**
        - Valor inicial (Enero 2024): €{datos_bundesliga['Valor de Mercado en 01/01/2024']:,}
        - Valor actual: €{datos_bundesliga['Valor de Mercado Actual']:,}
        - Variación porcentual: {variacion_bundesliga:.2f}%
        - Tendencia: {'Positiva ↑' if variacion_bundesliga > 0 else 'Negativa ↓' if variacion_bundesliga < 0 else 'Estable →'}

        #### 4. Factores Influyentes
        
        **Rendimiento Deportivo**
        - Participación en competiciones
        - Estadísticas individuales
        - Impacto en resultados del equipo
        
        **Factores Externos**
        - Lesiones o tiempo de inactividad
        - Situación contractual
        - Edad y potencial de desarrollo
        - Demanda en el mercado
        
        #### 5. Conclusiones del Análisis
        - {'El jugador de LaLiga muestra una tendencia más pronunciada' if abs(variacion_laliga) > abs(variacion_bundesliga) else 'El jugador de Bundesliga muestra una tendencia más pronunciada'}
        - Diferencias entre ligas: {'Los valores sugieren una valoración más alta en LaLiga' if datos_laliga['Valor de Mercado Actual'] > datos_bundesliga['Valor de Mercado Actual'] else 'Los valores sugieren una valoración más alta en Bundesliga'}
        - Oportunidades de mercado: {'Potencial de inversión en crecimiento' if variacion_laliga > 0 or variacion_bundesliga > 0 else 'Momento de cautela en inversiones'}
        """)
    
    else:
        # Para las otras visualizaciones (Evolución Individual, Comparación entre Jugadores, etc.)
        visualizacion = st.selectbox(
            "Seleccione tipo de visualización:",
            ["Evolución Individual", "Comparación entre Jugadores"]
        )

        # Selección de datos según la liga
        if liga_seleccionada == "LaLiga":
            data = spain_data
        elif liga_seleccionada == "Bundesliga":
            data = bundesliga_data
        
        # Visualización: Evolución Individual
        if visualizacion == "Evolución Individual":
            st.subheader(f"Evolución Individual del Valor de Mercado - {liga_seleccionada}")
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
                
                df_mensual = pd.DataFrame({
                    'Mes': meses,
                    'Valor de Mercado (€)': [f"€{int(v):,}" for v in valores]
                })
                st.write("Valores mensuales:")
                st.dataframe(df_mensual)

        # Visualización: Comparación entre Jugadores
        elif visualizacion == "Comparación entre Jugadores":
            if liga_seleccionada == "Comparativa":
                st.subheader("Comparación entre Jugadores de LaLiga y Bundesliga")
                col1, col2 = st.columns(2)
                with col1:
                    jugador1 = st.selectbox("Jugador de LaLiga:", spain_data['Nombre'].unique())
                with col2:
                    jugador2 = st.selectbox("Jugador de Bundesliga:", bundesliga_data['Nombre'].unique())

                if jugador1 and jugador2:
                    fig = go.Figure()

                    # Datos LaLiga
                    datos_jugador1 = spain_data[spain_data['Nombre'] == jugador1]
                    valor_inicial1 = datos_jugador1['Valor de Mercado en 01/01/2024'].iloc[0]
                    valor_final1 = datos_jugador1['Valor de Mercado Actual'].iloc[0]
                    meses1, valores1 = generar_valores_mensuales(valor_inicial1, valor_final1)

                    # Datos Bundesliga
                    datos_jugador2 = bundesliga_data[bundesliga_data['Nombre'] == jugador2]
                    valor_inicial2 = datos_jugador2['Valor de Mercado en 01/01/2024'].iloc[0]
                    valor_final2 = datos_jugador2['Valor de Mercado Actual'].iloc[0]
                    meses2, valores2 = generar_valores_mensuales(valor_inicial2, valor_final2)

                    fig.add_trace(go.Scatter(
                        x=meses1,
                        y=valores1,
                        mode='lines+markers',
                        name=f"{jugador1} (LaLiga)",
                        line=dict(width=3),
                        marker=dict(size=10)
                    ))

                    fig.add_trace(go.Scatter(
                        x=meses2,
                        y=valores2,
                        mode='lines+markers',
                        name=f"{jugador2} (Bundesliga)",
                        line=dict(width=3),
                        marker=dict(size=10)
                    ))

                    fig.update_layout(
                        title='Comparación de Valores de Mercado entre Ligas',
                        xaxis_title='Mes',
                        yaxis_title='Valor de Mercado (€)',
                        hovermode='x unified',
                        showlegend=True
                    )
                    st.plotly_chart(fig)

                    # Análisis
                    st.write(f"""
                    ### Análisis de la Comparación:
                    - **{jugador1} (LaLiga)**:
                        - Valor Inicial: €{int(valor_inicial1):,}
                        - Valor Actual: €{int(valor_final1):,}
                    - **{jugador2} (Bundesliga)**:
                        - Valor Inicial: €{int(valor_inicial2):,}
                        - Valor Actual: €{int(valor_final2):,}

                    Este análisis resalta las diferencias en las trayectorias de los jugadores seleccionados, 
                    permitiendo observar cómo han evolucionado sus valores de mercado a lo largo del tiempo.
                    """)
            else:
                st.subheader(f"Comparación entre Jugadores - {liga_seleccionada}")
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
                        title=f'Comparación de Valores de Mercado - {liga_seleccionada}',
                        xaxis_title='Mes',
                        yaxis_title='Valor de Mercado (€)',
                        hovermode='x unified',
                        showlegend=True
                    )
                    st.plotly_chart(fig)

                    # Análisis
                    st.write(f"""
                    ### Análisis de la Comparación:
                    Comparando los valores de mercado de **{jugador1}** y **{jugador2}** en la misma liga, 
                    es posible observar diferencias significativas en sus trayectorias.
                    
                    Estos patrones pueden estar relacionados con:
                    - **Rendimiento reciente**.
                    - **Impacto en sus equipos**.
                    - **Expectativas futuras en el mercado de fichajes**.
                    """)



elif menu_principal == "Objetivos":
    st.title("Objetivos del Proyecto")
    st.write("""
    ### Objetivos Principales:
    - Analizar y visualizar el valor de mercado de los jugadores en LaLiga y Bundesliga
    - Evaluar el incremento porcentual del valor de mercado a lo largo del tiempo
    - Identificar patrones y tendencias en la valoración de jugadores
    - Comparar las valoraciones entre las diferentes ligas
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
    
    if liga_seleccionada == "Comparativa":
        tab1, tab2, tab3 = st.tabs(["Estadísticas Generales", "Análisis Comparativo", "Recomendaciones"])
        
        with tab1:
            st.header("Estadísticas Generales")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("LaLiga")
                st.dataframe(spain_data[['Valor de Mercado en 01/01/2024', 'Valor de Mercado Actual']].describe())
            
            with col2:
                st.subheader("Bundesliga")
                st.dataframe(bundesliga_data[['Valor de Mercado en 01/01/2024', 'Valor de Mercado Actual']].describe())
        
        with tab2:
            st.header("Análisis Comparativo")
            fig = go.Figure()
            
            fig.add_trace(go.Box(
                y=spain_data['Valor de Mercado Actual'],
                name='LaLiga'
            ))
            
            fig.add_trace(go.Box(
                y=bundesliga_data['Valor de Mercado Actual'],
                name='Bundesliga'
            ))
            
            fig.update_layout(
                title='Distribución de Valores de Mercado por Liga',
                yaxis_title='Valor de Mercado (€)'
            )
            st.plotly_chart(fig)
        
        with tab3:
            st.header("Recomendaciones")
            st.write("""
            Basadas en el análisis comparativo:
            - Recomendaciones para clubes de ambas ligas
            - Estrategias de inversión considerando diferencias entre mercados
            - Oportunidades de mercado en ambas ligas
            """)
    else:
        tab1, tab2, tab3 = st.tabs(["Estadísticas Generales", "Análisis de Tendencias", "Recomendaciones"])
        
        with tab1:
            st.header("Estadísticas Generales")
            if liga_seleccionada == "LaLiga":
                st.dataframe(spain_data[['Valor de Mercado en 01/01/2024', 'Valor de Mercado Actual']].describe())
            else:
                st.dataframe(bundesliga_data[['Valor de Mercado en 01/01/2024', 'Valor de Mercado Actual']].describe())
        
        with tab2:
            st.header("Análisis de Tendencias")
            fig = go.Figure()
            
            if liga_seleccionada == "LaLiga":
                fig.add_trace(go.Box(
                    y=spain_data['Valor de Mercado en 01/01/2024'],
                    name='Enero 2024'
                ))
                fig.add_trace(go.Box(
                    y=spain_data['Valor de Mercado Actual'],
                    name='Actual'
                ))
            else:
                fig.add_trace(go.Box(
                    y=bundesliga_data['Valor de Mercado en 01/01/2024'],
                    name='Enero 2024'
                ))
                fig.add_trace(go.Box(
                    y=bundesliga_data['Valor de Mercado Actual'],
                    name='Actual'
                ))
            
            fig.update_layout(
                title=f'Distribución de Valores de Mercado - {liga_seleccionada}',
                yaxis_title='Valor de Mercado (€)'
            )
            st.plotly_chart(fig)
        
        with tab3:
            st.header("Recomendaciones")
            st.write(f"""
            Basadas en el análisis de datos de {liga_seleccionada}:
            - Recomendaciones para clubes
            - Estrategias de inversión
            - Oportunidades de mercado
            """)

else:  # Conclusiones
    st.title("Conclusiones")
    if liga_seleccionada == "Comparativa":
        st.write("""
        ### Principales Hallazgos:
        - Comparativa entre LaLiga y Bundesliga muestra patrones interesantes en la valoración de jugadores
        - Las diferencias entre mercados ofrecen oportunidades únicas de inversión
        - La gestión basada en datos puede mejorar significativamente las estrategias de los equipos en ambas ligas
        """)
    else:
        st.write(f"""
        ### Principales Hallazgos en {liga_seleccionada}:
        - El análisis de datos en el fútbol ofrece insights valiosos para la toma de decisiones
        - Las tendencias del mercado muestran patrones significativos en la valoración de jugadores
        - La gestión basada en datos puede mejorar significativamente las estrategias de los equipos
        """)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL EN ESPAÑA Y ALEMANIA")



