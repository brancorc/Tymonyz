import os
from google.cloud import texttospeech
from src.logger import get_logger
from dotenv import load_dotenv
from src.config import GOOGLE_APPLICATION_CREDENTIALS

logger = get_logger()

def tts(text, output_filename):

    load_dotenv()  # Cargar las variables del archivo .env

    logger.info("Generando audio...")

    # Configurar las credenciales de Google Cloud 
    google_credentials = GOOGLE_APPLICATION_CREDENTIALS

    if not google_credentials:
        logger.error("No se encuentran las credenciales de Google Cloud en las variables de entorno.")
        return


    try:
        # Inicializar el cliente de Text-to-Speech
        client = texttospeech.TextToSpeechClient()

        # Configurar la solicitud de síntesis
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Configurar la voz correcta (es-ES-Studio-F)
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-ES",
            name="es-ES-Studio-F",  # Voz masculina, debido al error anterior
            ssml_gender=texttospeech.SsmlVoiceGender.MALE  # Género masculino
        )

        # Configurar el tipo de audio de salida
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Realizar la solicitud a la API
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        # Guardar el audio en el archivo de salida
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        
        logger.info("Audio guardado como %s", output_filename)
    
    except Exception as e:
        logger.error(f"Error al generar el audio: {e}")