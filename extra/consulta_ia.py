import openai # Importamos la librería openai para interactuar con la API de OpenRouter
from dotenv import load_dotenv # Importamos la función load_dotenv para cargar las variables de entorno desde el archivo .env
import os # Importamos la librería os para interactuar con el sistema operativo
##esta ia le realiza la consula a deepseek
def consulta(contenido):

    load_dotenv()  # Carga las variables del archivo .env
    API_KEY = os.getenv('DEEPSEEK_API_KEY')

    if not API_KEY:
        print("Error: No se encontró la API key. Por favor, verifique el archivo .env y asegúrese de que la clave esté definida.")
        return

    # Configurar el cliente de OpenRouter
    openai.api_key = API_KEY
    openai.api_base = "https://openrouter.ai/api/v1"

    prompt = "quiero que me des toda la informacion del dia de hoy 25/03/2025de la ultima noticia de argentina en economia."
    print("Consulta con DeepSeek...")

    chat = openai.ChatCompletion.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {"role": "system", "content": prompt}, 
            {"role": "user", "content": contenido},
        ]
    )

    # Obtener la respuesta
    respuesta = chat.choices[0].message.content

    print("La respuesta de la IA es:")
    print(respuesta)

    # Guardar la respuesta en un archivo
    with open(r'archivos\texto_ia.txt', "w", encoding="utf-8") as file:
        file.write(respuesta)

    print("La respuesta se ha guardado en 'texto_ia.txt'.")

    if os.path.getsize(r'archivos\texto_ia.txt') == 0: # Comprobar si el archivo está vacío
        print("El archivo está vacío")
        consulta(contenido)

    return 0  # Retornar un código de éxito (0)

consulta("")