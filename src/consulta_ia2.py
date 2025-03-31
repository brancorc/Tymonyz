import os
from dotenv import load_dotenv
from google import genai
from src.logger import get_logger
from src.config import GEMINI_API_KEY, TEXT_IA_PATH

# Funcion  para generar una narracion de una noticia
def narracion_noticia(url):

    logger = get_logger()

    load_dotenv()  # Cargar las variables del archivo .env

    # Verificar API key
    API_KEY = GEMINI_API_KEY

    if not API_KEY:
        logger.error("API key no configurada. Asegúrate de que la variable de entorno GEMINI_API_KEY esté definida.")
        return
    else:
        logger.info("API key cargada correctamente.")

    client = genai.Client(api_key=API_KEY)

    prompt = """
    Te voy a pasar el link de una noticia. Necesito que entres, te fijes todo y lo conviertas en una narración breve pero explicativa, directa y provocadora, perfecta para un video corto de menos de un minuto.   

    Al inicio tenes que decir lo que paso hoy con el titulo de la noticia de una forma muy llamativa, asi la gente se quede con ganas de ver el video. Quiero que el tono sea IRÓNICO, CRÍTICO y con un toque de sarcasmo, como si estuvieras contando la noticia a alguien con total sinceridad y sin filtro. Nada de formalidades, cero títulos como 'Introducción' o 'Conclusión', ni asteriscos, ni emojis. SOLO TEXTO.  

    Resúmelo de forma impactante, haciendo que la gente quiera comentar. No te limites, si hay algo absurdo, destácalo. Si hay algo indignante, exprésalo. Si hay algo gracioso, hazlo notar. Pero sin exageraciones forzadas, que suene natural y directo.  

    Al final, lanza una pregunta que haga reflexionar o genere debate, sin sonar a típico 'call to action'. Quiero que la gente se quede pensando o, mejor aún, discutiendo en los comentarios.  

    Aquí tienes el link de la noticia:  
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt + url,
        )

        # Abrir el archivo en modo escritura ('w' para escribir)
        with open(TEXT_IA_PATH, "w", encoding="utf-8") as file:
            file.write(response.text)  # Agrega un salto de línea antes para separar del contenido previo

        logger.info(f"La respuesta se ha guardado en {TEXT_IA_PATH}.")

    except Exception as e:
        logger.error(f"Error al generar la narración: {e}")
        raise
