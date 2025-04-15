import random
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip
import whisper
from mutagen.mp3 import MP3  # Importar la clase MP3 de mutagen para obtener la duración del archivo MP3
from src.config import FONT_PATH, AUDIO_IA_PATH, BACKGROUND_VIDEOS, BACKGROUND_VOLUME, VOICE_VOLUME, TEXT_FONT_SIZE
from src.logger import get_logger

fuente = FONT_PATH

def video(video_fondo, salida_video_path, texto_miniatura): #recibe un video de fondo y la salida del video generado (video_generado.mp4)

    logger = get_logger()


    audio_clip = MP3(AUDIO_IA_PATH)  # Utilizar la librería Mutagen para leer el archivo MP3
    duracion_audio = audio_clip.info.length  # Obtener la duración en segundos del archivo MP3

    # Cargar el video original
    video_clip = VideoFileClip(video_fondo)

    # Obtener la duración del video original
    video_duration = video_clip.duration

    # Asegurarse de que el video es lo suficientemente largo
    if video_duration <= duracion_audio:
        print("El video original es demasiado corto.")
        nuevo_video_fondo = BACKGROUND_VIDEOS + "/v" + str(random.randint(0, 6)) + ".mp4" #direccion de un video de fondo (debe ser random)
        video(nuevo_video_fondo, salida_video_path, texto_miniatura) #llamar a la función video para generar el video con subtítulos y audio de voz. (llamado video_generado.mp4)
    else:

        logger.info("Generando video...")

        # Generar un inicio aleatorio para el recorte
        start_time = random.uniform(0, video_duration - duracion_audio)
        
        # Cortar el video desde start_time hasta start_time + duracion_audio
        final_clip = video_clip.subclipped(start_time, start_time + duracion_audio)
        
        # Cargar el audio de voz
        audio_clip = AudioFileClip(AUDIO_IA_PATH)

        # Asegurarse de que el audio de voz tenga la duración adecuada
        audio_clip = audio_clip.with_duration(duracion_audio)

        # Obtener el audio original del video
        original_audio = final_clip.audio

        # Bajar el volumen del audio original (por ejemplo, a la mitad)
        original_audio = original_audio.with_volume_scaled(BACKGROUND_VOLUME)  # Cambia 0.325 a cualquier otro valor para ajustar el volumen

        # Mezclar el audio original y el audio de fondo
        mixed_audio = CompositeAudioClip([original_audio, audio_clip.with_volume_scaled(VOICE_VOLUME)])  # Ajustar el volumen del audio de voz si es necesario

        # Establecer el audio mezclado al video
        final_clip = final_clip.with_audio(mixed_audio)
        
        # Transcribir el audio para obtener las palabras y tiempos
        model = whisper.load_model("base")
        result = model.transcribe(AUDIO_IA_PATH, word_timestamps=True)

        # Extraer palabras y sus tiempos
        words = []
        if 'segments' in result:
            for segment in result['segments']:
                if 'words' in segment:
                    for word_info in segment['words']:
                        words.append((word_info['word'], word_info['start'], word_info['end']))

        # Crear una lista de clips para combinar
        clips = []

        for word, start, end in words:
            # Crear un clip de texto para la palabra
            text_clip = TextClip(text = word, font_size=TEXT_FONT_SIZE, color='black', bg_color = "yellow", font=fuente) 
            
            # Obtener las dimensiones del texto
            text_width, text_height = text_clip.size
            
             # Fondo amarillo con un pequeño margen alrededor del texto
            bg_margin = 35  # Margen extra alrededor del texto
            text_clip = TextClip(text = word, font_size=TEXT_FONT_SIZE, color='black', bg_color = "yellow", font=fuente, size=(text_width + 3 * bg_margin, text_height + 3 * bg_margin))

            #txt_bg = TextClip(text = " " * len(word), font_size=80, color='black', bg_color='yellow', font=fuente, size=(text_width + 3 * bg_margin, text_height + 3 * bg_margin))
            
             # Centrar el fondo y el texto en la parte inferior
            #txt_bg = txt_bg.with_position(('center', 'center')).with_start(start).with_duration(end - start)
            text_clip = text_clip.with_position(('center', 'center')).with_start(start).with_duration(end - start)
            
             # Añadir el clip de texto y su fondo amarillo a la lista
            #clips.append(txt_bg)  # Fondo
            clips.append(text_clip)  # Texto

        # Cargar el texto de la portada
        portada = TextClip(text = texto_miniatura, font_size=TEXT_FONT_SIZE, color='black', bg_color='orange', font=fuente, size=(1920, 1080))
        portada = portada.with_position(("center", "center")).with_duration(0.01)  # Dura 0.01 segundo
    
        # Crear un CompositeVideoClip con el video original y los subtítulos
        video_with_subtitles = CompositeVideoClip([final_clip] + clips + [portada])
    
        # Escribir el video generado con audio y subtítulos
        video_with_subtitles.write_videofile(salida_video_path, codec="libx264", audio_codec="aac")
        
        print(f"Video generado con audio y subtítulos: {salida_video_path}")

        # Cerrar los clips
        video_clip.close()
        audio_clip.close()

#video_fondo = r"C:\Users\branc\Escritorio\tymonyz\videos_fondo\v" + str(random.randint(0, 6)) + ".mp4"
#path_video_generado = r"C:\Users\branc\Escritorio\tymonyz\TiktokAutoUploader\VideosDirPath\video_generado" + str(0) + ".mp4"
                
#video(video_fondo, path_video_generado, "hola esta es una miniatura de ejemplo")