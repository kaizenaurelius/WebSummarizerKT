# api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Importamos tus herramientas (tal cual como antes)
from scraper import fetch_website_links
from summarizeWebsite import summarize

# Inicializamos la App
app = FastAPI()

# --- CONFIGURACIÓN DE SEGURIDAD (CORS) ---
# Esto es VITAL para que React (puerto 5173) pueda hablar con Python (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, aquí pones tu dominio real. "*" acepta todo.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS DE DATOS ---
# Esto define qué esperamos recibir de React
class RequestModel(BaseModel):
    url: str

# --- TU LÓGICA DE FILTRADO (La movimos aquí) ---
def es_link_de_noticia(url, dominio_base):
    url = url.lower()
    if dominio_base not in url: return False
    
    palabras_prohibidas = [
        "/category/", "/tag/", "login", "registro", "signup", 
        "contacto", "about", "privacidad", "terminos", 
        "facebook", "twitter", "instagram", ".jpg", ".png"
    ]
    
    for p in palabras_prohibidas:
        if p in url: return False

    if len(url) < 35: return False
    
    return True

# --- EL ENDPOINT (EL NUEVO "MAIN") ---
@app.post("/api/analyze")
async def analyze_news(request: RequestModel):
    """
    Esta función reemplaza a tu antiguo 'run_news_bot'.
    React nos manda la URL, y nosotros devolvemos el JSON con las noticias.
    """
    url_principal = request.url
    print(f"📡 Recibida petición para investigar: {url_principal}")
    
    try:
        # 1. Obtener todos los links
        raw_links = fetch_website_links(url_principal)
        
        # 2. Filtrar
        candidatos = [link for link in raw_links if es_link_de_noticia(link, url_principal)]
        print(f"--> Se encontraron {len(candidatos)} noticias potenciales.")
        
        resultados = []
        
        # 3. Procesar (Limitamos a 3 para la demo, luego puedes subirlo)
        # Nota: En una API real, esto puede tardar. React mostrará "Cargando..."
        for link in candidatos[:3]:
            print(f"Analizando: {link}")
            try:
                # Llamamos a tu IA
                resumen_texto = summarize(link)
                
                # Si la IA dice SKIPPED, no lo agregamos
                if "SKIPPED" not in resumen_texto:
                    resultados.append({
                        "url": link,
                        "summary": resumen_texto
                    })
            except Exception as e:
                print(f"Error leyendo {link}: {e}")
                
        # 4. Devolver la respuesta final a React
        return {
            "status": "success",
            "total_found": len(resultados),
            "data": resultados
        }

    except Exception as e:
        print(f"Error critico: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Si ejecutas este archivo directo, arranca el servidor
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor API...")
    uvicorn.run(app, host="127.0.0.1", port=8000)