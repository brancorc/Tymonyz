from src.noticias import obtener_enlaces_noticias
from src.generador_audio import tts
from src.generador_video import video
from src.logger import get_logger
from src.consulta_ia2 import narracion_noticia
from src.config import TEXT_NOTICIAS_PATH, TEXT_IA_PATH, AUDIO_IA_PATH, BACKGROUND_VIDEOS, TIKTOK_UPLOADER_DIR
import random
import subprocess
from datetime import datetime

logger = get_logger()

def wrap_text(text, max_chars=23):
    """
    Agrega saltos de línea al texto sin cortar palabras a la mitad. (para la miniatura del video)
    
    Args:
        text (str): El texto de entrada
        max_chars (int): Máximo de caracteres por línea antes de intentar un salto de línea
        
    Returns:
        str: Texto con saltos de línea
    """
    try:
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 > max_chars:
                lines.append(current_line)
                current_line = word
            else:
                current_line += (" " if current_line else "") + word
        
        if current_line:
            lines.append(current_line)
            
        lines.append(datetime.now().strftime("%d/%m/%Y"))
        
        return "\n".join(lines)
    except Exception as e:
        print(f"Error al envolver el texto: {str(e)}")
        raise

def main():
    
    """
    Función principal que ejecuta el proceso completo de generación y subida de videos.
    """

    try:

        i = 0
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        
        logger.info("Iniciando proceso de generación de videos")
        
        logger.info("Obteniendo enlaces de noticias")
        
        obtener_enlaces_noticias()
        
        # Leer enlaces y titulos de las noticias
        with open(TEXT_NOTICIAS_PATH, "r", encoding="utf-8") as file:
            enlaces = file.readlines()
            
        logger.info(f"Se encontraron {len(enlaces)} noticias para procesar")
        
        # Procesar cada noticia
        for enlace in enlaces:
            try: #empieza a procesar cada noticia, generando la narracion, el video, y la subida a tiktok
                enlace = enlace.strip()
                url, titulo = enlace.split(' ', 1)
                
                logger.info(f"Procesando noticia: {titulo}, url: {url}")

                narracion_noticia(url)

                # Leer texto generado y lo guarda en la variable texto
                with open(TEXT_IA_PATH, "r", encoding="utf-8") as file:
                    texto = file.read()
                    
                # Generar audio con el texto generado por la IA
                tts(texto, AUDIO_IA_PATH)

                # Generar video
                video_fondo = BACKGROUND_VIDEOS + "/v" + str(random.randint(0, 6)) + ".mp4"
                path_video_generado = r"C:\Users\branc\Escritorio\tymonyz\src\TiktokAutoUploader\VideosDirPath\video_generado" + str(i) + ".mp4"
                
                texto_miniatura = wrap_text(titulo) # Agregar saltos de línea al texto para la miniatura
                
                video(video_fondo, path_video_generado, texto_miniatura)
                
                logger.info(f"Video generado: {path_video_generado}, subiendo a tiktok...")

                comando = [
                    "python", "cli.py", "upload",
                    "--user", "argnewsia",
                    "-v", path_video_generado,
                    "-t", f"{titulo}. {fecha_hoy}"
                ]
                
                subprocess.run(comando, cwd=TIKTOK_UPLOADER_DIR)
                
                logger.info("Video subido exitosamente")
                
                i += 1
                
            except Exception as e:
                print(f"Error procesando noticia: {str(e)}")
                raise
                
        logger.info("Proceso completado exitosamente")
        
    except Exception as e:
        print(f"Error en el proceso principal: {str(e)}")
        raise

if __name__ == "__main__": 
    main() #ejecuta todo el proceso