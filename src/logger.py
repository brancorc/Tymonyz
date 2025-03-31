import logging

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Crear un logger
logger = logging.getLogger(__name__)

# Función para obtener el logger configurado
def get_logger():
    return logger
