import os
from dotenv import load_dotenv

# Obtener la ruta absoluta al directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno usando la ruta absoluta al .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Rutas base del proyecto a las carpetas
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIOS_DIR = os.path.join(ASSETS_DIR, "audios")
BACKGROUND_VIDEOS = os.path.join(ASSETS_DIR, "background_videos")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
TEXTS_DIR = os.path.join(ASSETS_DIR, "texts")
TIKTOK_UPLOADER_DIR = os.path.join(BASE_DIR, "src", "TiktokAutoUploader")


# Rutas de archivos específicos #seguir esto
FONT_PATH = os.path.join(FONTS_DIR, "Poppins-Bold.ttf")
AUDIO_IA_PATH = os.path.join(AUDIOS_DIR, "voz_natural.mp3")
TEXT_NOTICIAS_PATH = os.path.join(TEXTS_DIR, "noticias.txt")
TEXT_IA_PATH = os.path.join(TEXTS_DIR, "texto_ia.txt")

# Configuración de APIs y credenciales
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MEDIASTACK_API_KEY = os.getenv("MEDIASTACK_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")

# Configuración de video
TEXT_FONT_SIZE = 95
BACKGROUND_VOLUME = 0.325
VOICE_VOLUME = 0.5