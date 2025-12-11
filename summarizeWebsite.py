# summarize_website.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# IMPORTANTE: Asumo que 'scraper.py' y 'fetch_website_contents' existen.
# Si 'fetch_website_contents' es una función simple, la puedes copiar aquí también.
# Por ahora, la mantengo como una importación, como en tu código.
from scraper import fetch_website_contents 

# --- CONFIGURACIÓN ---

# Carga las variables de entorno desde el archivo .env
load_dotenv(override=True)

# Inicializa el cliente de OpenAI. La librería OpenAI busca automáticamente 
# la clave en las variables de entorno cargadas.
# Si no usas un API Key, sino Ollama, deberás ajustar esto, pero para OpenAI es estándar.
openai_client = OpenAI()

# Define la variable global para la clave (útil para la comprobación)
api_key = os.getenv('OPENAI_API_KEY')

# Comprobación de la clave (de la celda 5)
if not api_key:
    print("No API key was found - por favor, configura tu archivo .env")
elif not api_key.startswith("sk-proj-"):
    print("La clave de API no empieza por sk-proj-; por favor, verifica la clave")
elif api_key.strip() != api_key:
    print("La clave de API tiene espacios o tabulaciones al inicio o al final; por favor, elimínalos")
else:
    print("API key configurada correctamente para la ejecución.")
    
# --- DEFINICIÓN DE PROMPTS ---

# Define el prompt del sistema
SYSTEM_PROMPT = """
You are a bold, sharp and tenacious investigator assistant that analyzes the contents of a website that contains political news of venezuela,
you extract the most information related to authoritary actions commited by the government towards its citizens, 
specifically focusing on human rights violations, kindnappings under the excuse of political dissidence.
and provides a short, consice,  summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

# Define el prefijo del prompt del usuario
USER_PROMPT_PREFIX = """
Here are the contents of a website.
Provide a summary of this website.
I am looking for structured information, about arbitrary detentions, kidnappings, human rights violations commited by the government of venezuela against its citizens.
Ignore navigation related text.
"""

# --- FUNCIONES AUXILIARES ---

# Función para crear el formato de mensajes de la API (Celda 37)
def messages_for(website_content: str) -> list:
    """Crea la lista de mensajes en el formato que espera la API de OpenAI."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_PREFIX + website_content}
    ]

# Función que llama a la API (Celda 38)
def summarize(url: str, model: str = "gpt-5-nano") -> str:
    """
    Scrapea el contenido de una URL y llama a la API de OpenAI para obtener un resumen.
    """
    print(f"\nScrapeando y resumiendo: {url}...")
    website_content = fetch_website_contents(url)
    
    # Manejo de error si el scrapeo falló (ej. contenido vacío)
    if not website_content:
        return "ERROR: No se pudo obtener contenido del sitio web."

    messages = messages_for(website_content)
    
    # Usamos la variable global openai_client
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content #choices[0] significa la primera respuesta generada.

# Función para mostrar el resultado
def display_summary(url: str):
    """
    Llama a summarize y muestra el resultado.
    En un entorno de script normal, print es mejor que IPython.display.Markdown.
    """
    summary = summarize(url)
    print("="*60)
    print(f"RESUMEN PARA {url}:\n")
    # Imprimimos el resultado directamente, asumiendo que el formato Markdown se verá bien en la consola
    print(summary)
    print("="*60)
    
    
# --- 4. PUNTO DE EJECUCIÓN ---

def main():
    """Ejecuta la lógica principal del script de web scraping y resumen."""
    
    # ⬇️ Nueva línea para pedir la URL al usuario ⬇️
    target_url = input("Ingresa la URL que deseas resumir (ej. https://www.ucab.edu.ve/): ")
    
    if not target_url:
        print("No se ingresó ninguna URL. Usando URL por defecto: https://www.ucab.edu.ve/")
        target_url = "https://www.ucab.edu.ve/"
        
    summary = summarize(target_url)
    
    print("\n" + "="*80)
    print(f"RESUMEN FINAL PARA {target_url}:\n")
    print(summary)
    print("="*80 + "\n")

if __name__ == "__main__":
    main()