"""
Tymonyz - Generador Automático de Videos de noticias para TikTok

Este paquete contiene las herramientas necesarias para:
- Obtener enlaces de noticias.
- Generar narraciones de las noticias usando IA.
- Crear audios y videos automáticamente.
- Subir videos a TikTok.

"""

from .generador_audio import tts
from .generador_video import video
from .consulta_ia2 import narracion_noticia
from .noticias import obtener_enlaces_noticias
from .logger import get_logger

logger = get_logger()
__version__ = "1.0.0"
__author__ = "Branco"
__all__ = [
    "tts",
    "video",
    "narracion_noticia",
    "obtener_enlaces_noticias",
    "get_logger"
] 