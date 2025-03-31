import requests
from bs4 import BeautifulSoup

def scraping(url):
    """
    Realiza web scraping de una noticia.
    
    Args:
        url (str): URL de la noticia
        
    Returns:
        str: Contenido de la noticia
        None: Si hay error
    """
    try:
        print(f"Scraping de {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraer contenido
        titles_h1 = [h1.get_text().strip() for h1 in soup.find_all('h1')]
        titles_h2 = [h2.get_text().strip() for h2 in soup.find_all('h2')]
        paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
        
        # Filtrar líneas vacías
        content = [text for text in (titles_h1 + titles_h2 + paragraphs) if text]
        
        if not content:
            print(f"No se encontraron contenidos en {url}")
            return None
            
        article_content = "\n".join(content)
        print(f"Contenido scrapeado: {article_content}")
        return article_content

    except requests.RequestException as e:
        print(f"Error al realizar el scraping: {str(e)}")
        return None
    except Exception as e:
        print(f"Error al realizar el scraping: {str(e)}")
        return None