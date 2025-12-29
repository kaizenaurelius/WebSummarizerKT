from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_website_links(url):
    """
    EL EXPLORADOR (MEJORADO):
    Devuelve todos los links de la web convertidos a rutas absolutas.
    """
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        links = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                # Convierte rutas relativas (/noticia) a absolutas (https://sitio.com/noticia)
                full_url = urljoin(url, href)
                links.append(full_url)
                
        # Eliminamos duplicados y devolvemos la lista
        return list(set(links))
        
    except Exception as e:
        print(f"Error obteniendo links: {e}")
        return []


    
if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBA DE LINKS...")
    
    # Usamos una web que sabemos que tiene muchos links relativos
    url_prueba = "https://www.lapatilla.com" 
    
    print(f"Scrapeando: {url_prueba}")
    links = fetch_website_links(url_prueba)
    
    print(f"\n✅ Se encontraron {len(links)} enlaces en total.")
    print("Mostrando los primeros 10 para verificar:\n")
    
    for i, link in enumerate(links[:10]):
        print(f"[{i+1}] {link}")
        
    # VERIFICACIÓN AUTOMÁTICA
    tiene_relativos = any(not link.startswith("http") for link in links)
    if not tiene_relativos:
        print("\n🎉 ÉXITO: Todos los links son absolutos (tienen http/https).")
    else:
        print("\n⚠️ ALERTA: Todavía hay links rotos o relativos.")