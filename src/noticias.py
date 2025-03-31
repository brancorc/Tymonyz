import requests
import os
from dotenv import load_dotenv
from google import genai
from src.logger import get_logger
from src.config import NEWSDATA_API_KEY, TEXT_NOTICIAS_PATH, GEMINI_API_KEY

logger = get_logger()

#Función para obtener enlaces de noticias mediante la api de newsdata
def obtener_enlaces_noticias():    

    load_dotenv()  # Cargar las variables del archivo .env

    API_KEY = NEWSDATA_API_KEY # Cargar la clave API desde el config.py con las variables de entorno .evn

    if not API_KEY:
        logger.error("Falta la clave API en las variables de entorno.")
        return
    else:
        logger.info("API key de newsdatacargada correctamente.")

    url = 'https://newsdata.io/api/1/latest' # URL de la API de Newsdata para obtener las ultimas noticias

    params = {
        'apikey': API_KEY,
        'country': 'ar',
        'language': 'es'
    }

    try:
        response = requests.get(url, params=params) ## Envío de la petición a la API
        response.raise_for_status()  # Lanza un error si la respuesta no es 200 (exitosa)

        data = response.json()
        articles = data.get('results', [])

        if not articles:
            logger.warning("No se encontraron noticias.")
            return

        with open(TEXT_NOTICIAS_PATH, 'w', encoding='utf-8') as file: #guarda los links y titulos de las noticias en archivos/noticias.txt 
            for article in articles:
                file.write(f"{article['link']} {article['title']}\n")

        logger.info(f"Las noticias han sido guardadas en {TEXT_NOTICIAS_PATH}.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener las noticias: {e}")

    elegir_mejores_noticias()

# Función para elegir las mejores noticias con ia y modificar el titulo
def elegir_mejores_noticias(archivo=TEXT_NOTICIAS_PATH):

    load_dotenv()  # Cargar las variables del archivo .env

    API_KEY = GEMINI_API_KEY # Cargar la clave API desde el archivo config.py con las variables de entorno .evn

    if not API_KEY:
        logger.error("API key no configurada. Asegúrate de que la variable de entorno GEMINI_API_KEY esté definida.")
        return
    else:
        logger.info("API key de gemini cargada correctamente.")

    client = genai.Client(api_key=API_KEY)

    # Leer el archivo de texto
    with open(TEXT_NOTICIAS_PATH, "r", encoding="utf-8") as file:
        contenido = file.read()

    prompt = "hola, te voy a pasar un par de links de noticias junto con su titulo al lado. quiero que me devuelvas las 5 noticias que consideres más interesantes. la respuesta que me tenes que devolver tiene que ser asi: url1 titulo1 \n url2 titulo2 \n url3 titulo3... Respondeme solo con eso que te pido, no me digas ni una otra palabra. solo las url y los titulos, pero los titulos quiero que los hagas vos lo mas interesante posible y con pocas palabras"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt + contenido,
    )

    # Abrir el archivo en modo escritura y guardar el contenido
    with open(TEXT_NOTICIAS_PATH, "w", encoding="utf-8") as file:
        file.write(response.text)  # Agrega un salto de línea antes para separar del contenido previo

    logger.info(f"Contenido seleccionado por ia guardado en {TEXT_NOTICIAS_PATH}")

if __name__ == "__main__":
    obtener_enlaces_noticias()
