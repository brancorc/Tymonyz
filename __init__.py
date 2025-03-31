"""
Tymonyz - Generador Automático de Videos de noticias para TikTok

Este paquete proporciona una solución completa para:
- Obtener noticias de fuentes web
- Generar narraciones usando IA
- Crear videos automáticamente
- Subir contenido a TikTok
"""

from src.noticias import obtener_enlaces_noticias, narracion_noticia
from src.generador_audio import tts
from src.generador_video import video
from src.logger import get_logger
from src.config import (
    TEXT_NOTICIAS_PATH,
    TEXT_IA_PATH,
    AUDIO_IA_PATH,
    BACKGROUND_VIDEOS,
    TIKTOK_UPLOADER_DIR
)

__version__ = "1.0.0"
__author__ = "Branco"
__all__ = [
    "obtener_enlaces_noticias",
    "narracion_noticia",
    "tts",
    "video",
    "get_logger",
    "TEXT_NOTICIAS_PATH",
    "TEXT_IA_PATH",
    "AUDIO_IA_PATH",
    "BACKGROUND_VIDEOS",
    "TIKTOK_UPLOADER_DIR"
] 