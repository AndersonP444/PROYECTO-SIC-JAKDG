# JAKDG

Breve descripción del proyecto.

Este grupo esta conformado por: Anderson, Diego, Jeremy, Kevin y Greymel. Nosotros desarrollaremos los codigos y programas para cumplir con este proyecto y poder plasmarlo en una pagina web y que nuestro trabajo se haga conocido. Con diversas tecnicas lograremos desarrollar un gran programa/pagina web.

## Tabla de contenidos

1. [Nombre](ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FÚTBOL EN ESPAÑA Y ALEMANIA)
2. [Descripción](Este Proyecto se basa en evaluar y ver el progreso del valor de los jugadores de fútbol de la liga de España y Alemania, recopilando datos que muestren el valor de mercado de los jugadores hasta la fecha actual)
3. [Arquitectura]
Las librerías principales que utilizamos en nuestro proyecto son:
* Librería resquests (!pip install requests)(para realizar peticiones HTTP)
* Librería beautifulsoup4 (!pip install beautifulsoup4)(para extraer contenido de archivos HTML y XML, y transformarlo en una lista, matriz o diccionario de Python)
* Libreria pandas (!pip install pandas) (import pandas as pd)(para: 
•	Manipular y analizar estructuras de datos 
•	Generar gráficos de alta calidad con matplotlib )
* Librería matplotlib (!pip install matplotlib) (para crear visualizaciones de datos, como gráficos, histogramas, diagramas de barras, y gráficos de dispersión)
* Librería NumPy (!pip install NumPy) ()
* LibreríaI IPython.display (!pip install IPython) (from IPython.display import display, HTML)(permite mostrar una gran variedad de tipos de gráficos, como gráficos de dispersión, gráficos de barras, gráficos de líneas, entre otros)
* Modulo Datetime (El módulo datetime proporciona clases para manipular fechas y horas)
* Biblioteca base64 (La biblioteca base64 de Python sirve para codificar y decodificar datos binarios en cadenas base64, o viceversa)
* Librería JSON (sirve para codificar y decodificar datos en formato JSON (JavaScript Object Notation).)
* Librería Folium (La librería Folium de Python sirve para visualizar datos geoespaciales en mapas interactivos)

4. [Proceso] 
* Extracción de datos de los jugadores (recopilación de información)
* Filtrar los datos necesarios que vamos a utilizar (procesamiento de datos)
* con los datos de los jugadores listos, creamos un código para crear un archivo csv y guardar la información 
* además también creamos un código que agrega nuevos jugadores manualmente, y los guarda automáticamente en el csv
* utilizamos pandas (pd): para manejar y analizar datos estructurados, como tablas (DataFrames).
* creamos los dataframes y generamos tablas HTML para mostrar los jugadores en tablas 
* usamos el Módulo to_excel: para exportar los datos del DataFrame a un archivo Excel.
* creamos un código para depurar (limpiar) la segunda nacionalidad de los jugadores (los que tenían)
* creamos un código que convierte un valor financiero de texto a un entero o en Euros, Ejemplo: Si el valor contiene "mil €", se elimina esta parte del texto con replace, convirtiendo el número a un flotante y multiplicándolo por 1,000 para obtener euros completos.
Si contiene "mill. €", el proceso es similar, pero se multiplica por 1,000,000.
* importamos los modulos: 
plotly.graph_objects: Se usa para crear gráficos interactivos, en este caso, una gráfica de barras.
datetime y timedelta: Módulos para manejar fechas y horas.
pandas: Biblioteca para trabajar con datos estructurados, como tablas
* creamos la función para graficar el valor de mercado de un jugador: La función toma el nombre del jugador, calcula la evolución de su valor de mercado y genera una gráfica interactiva.
* Creamos un código para enlazar los datos de las tablas y del código con el repositorio del GitHub: 
file_path: Contiene la URL del archivo CSV alojado en un repositorio de GitHub.
pd.read_csv: Carga los datos del CSV en un DataFrame, que es una estructura de datos tabular similar a una hoja de cálculo.
* Función para graficar la evolución:
Solicita al usuario que ingrese el nombre del jugador.
Filtra los datos del jugador correspondiente usando data[data['Nombre'] == nombre_jugador].
* Tambien implementamos un código para añadir datos al csv del GitHub directamente desde el código:
Para añadir datos al archivo CSV en GitHub mediante un script automatizado en Python, usando la API de GitHub. Esto requiere autenticación con un Token Personal de Acceso para acceder y modificar el repositorio.
* también creamos un código para ELIMINAR UNA FILA MEDIANTE SU INDICE (POR SI SE REPITE UN JUGADOR O UN ERROR)
* creamos un código que genera una grafica que compara los valores de mercado iniciales y actuales de dos jugadores seleccionados por el usuario.
* Agregamos un código que permite añadir imágenes a la tabla por su índice (un para cada tabla: LaLiga y Bundesliga) (para mostrar a los jugadores, y saber quienes son)
* Implementamos la creación de un Bot
* Agregamos un código que muestra las coordenadas de la localizacion de los estadios de los equipos de LaLiga y de la Bundesliga (como información extra para saber la ubicación de los estadios donde juega cada jugador con su equipo de su respectiva liga)
* Como función extra creamos un código para una página de Streamlit(APP.PY), para mostrar los datos y las funcionalidades del código en una página Web


5. Funcionalidades:
* visualizar en una tabla los datos de los jugadores de LaLiga y ls Bundesliga
* Ver gráficas del aumento del valor de mercado de los jugadores
* comparación entre el valor de mercado de dos jugadores y su progreso
* Analizar y visualizar el valor de mercado de los jugadores
* Evaluar el incremento porcentual del valor de mercado a lo largo del tiempo
* Identificar patrones y tendencias en la valoración de jugadores
7. Estado del proyecto:
En desarrollo

8. Agradecimientos
Queremos agradecer a nuestros tutores (Prof. Jenny Remolina y Álvaro Arauz) por guíarnos y enseñarnos los principios del lenguaje de programación Python, por su constancia, esfuerzo y dedicación para corregirnos y estar atentos a aclarar nuestras dudas e inquietudes. Agradecer también a nuestros compañeros que han sido parte de nuestro trayecto en esaa primera parte del módulo de python. 

* Nombre del proyecto
ANÁLISIS DE LAS ESTADÍSTICAS QUE TIENEN MAYOR CORRELACIÓN CON EL VALOR DE MERCADO DE LOS JUGADORES DE FUTBOL
* Breve descripción del proyecto -> Alguna imagen o gif que muestre el proyecto

* Arquitectura del proyecto + imagen
1. Librería resquests
2. Librería beautifulsoup4 
3. Libreria pandas 
4. Librería matplotlib 
5. Librería NymPy 
6. LibreríaI IPython.display 
7. Modulo Datetime
8. Biblioteca base64
9. Librería JSON
10. Librería Folium
11. Display HTML
12. Libreria plotly
13. Libreria streamlit
14. Libreria streamlit_lottie
* Proceso de desarrollo:
Primeramente instalamos librerias necesarias la cuales son las mencionadas anteriormente.
Creamos DataFrame y lo mostramos en una tabla html 
-Fuente del dataset

-Limpieza de datos (img que lo valide)

-Manejo excepciones/control errores

-Estadísticos (Valores, gráficos, …)

* Funcionalidades extra:

Ejem 1: Integración del proyecto en una pág web
- Tecnología/Herramientas usadas …
- Arquitectura (img)

Ejem 3: Integración del proyecto en un canal WhatsApp, Discord, Telegram, Correo, …
- Tecnología/Herramientas usadas …
- Arquitectura (img)

Ejem 4: Desarrollo de interfaz gráfica de usuario
- Tecnología/Herramientas usadas …
- Arquitectura (img)

Ejem …: …
- Tecnología/Herramientas usadas …

