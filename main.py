import time
#1 El recolector, o scraper funciona para buscar los Links de noticias en la web
from scraper import fetch_website_links
#2 El analista, la funcion que resume
from summarizeWebsite import summarize

def is_a_news_link(url, base_domain):
    """ Filtrando links qu eno sean del mismo dominio """
    
    
    #1 asseguramos que pertenezcan al mismo sition, ejemplo que no sea facebook.
    if base_domain not in url:
        return False
    
    #2 Palabras que indican que no es una noticia
    
    
    
    ignored_words = ["contact", "login", "registro", "privacidad", "terminos", "category", "tag" ]
    if any(p in url.lower() for p in ignored_words):
        return False
    
    #3 para nombres muy cortos.(noticias suelen tener nombres largos)
    if len(url) < 20:
        return False
    
def run_bot(main_url):
    print(f"Bot initializing in: {main_url}")
    
    
    #A. Asking for Links
    print("Searching links...")
    all_links = fetch_website_links(main_url)
    
    #B. Filtering useful links
    
    qualifies = [link for link in all_links if is_a_news_link(link, main_url) ]
    
    #C. Main Loop
    for i, link in enumerate(qualifies[:3]): #Testing a few links
        print(f"\n[{i+1}] Procesando: {link}")
        
        try:
            #D. Summarizing
            result = summarize(link)
            print("---Summary---")
            print(result)
            print("-------------")
            
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(2)
        
if __name__ == "__main__":
    target_url = input("Ingresa la web de noticias ")
    run_bot(target_url)