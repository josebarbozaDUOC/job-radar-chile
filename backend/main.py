# backend/main.py

"""
JobRadar Chile - Main Scraper
Extrae ofertas de trabajo por categorías de GetOnBoard Chile
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
from dateutil.relativedelta import relativedelta
from datetime import datetime
import os
import time

# URL de portal de empleos
NAME_PORTAL = "getonbrd.com"
URL_WEB = "https://www."+NAME_PORTAL+"/jobs/"
URL_WEB_CATEGORY = "programming"

# DB SQLite ruta y nombre
SQLITE_PATH = "data/"
SQLITE_DB_JOBS = "jobs.db"

# Esquema para crear tabla job_urls
SCHEMA_JOBS_URLS = """CREATE TABLE IF NOT EXISTS job_urls (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    posted_date TEXT,
    portal TEXT,
    category TEXT,
    scraped_at TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
    );"""

SCHEMA_JOBS_URLS_INSERT = """INSERT OR IGNORE INTO job_urls 
    (url, posted_date, portal, category, scraped_at, processed) 
    VALUES (?, ?, ?, ?, ?, ?)"""

# Headers para requests https://developer.mozilla.org/en-US/docs/Glossary/Request_header
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
}

# Configuración de scraping
TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 1


# Crear y armar db estructura tabla empleos en sqlite, en data/
def create_table():
    os.makedirs(SQLITE_PATH, exist_ok=True)
    con = sqlite3.connect(SQLITE_PATH + SQLITE_DB_JOBS)
    cur = con.cursor()
    cur.execute(SCHEMA_JOBS_URLS)
    con.commit()
    con.close()


# Validar fecha de publicación de cada empleo
def is_recent_job(date_text):
    """Valida si la fecha está ENTRE hace un mes y hoy"""
    if not date_text:
        return True
    
    try:
        # Parsear fecha
        month_str, day_str = date_text.lower().split()
        months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        
        job_month = months.index(month_str) + 1
        job_day = int(day_str)
        job_date = datetime(2025, job_month, job_day)
        
        # Rango: hace un mes hasta hoy
        one_month_ago = datetime.now() - relativedelta(months=1)
        today = datetime.now()
        
        # ENTRE las dos fechas
        return one_month_ago <= job_date <= today
        
    except:
        return False

# Scrap y guardar todas las url de empleos en db
def scrap_base_urls():
    """WebScraping para obtener todas las urls de empleos"""
    url = URL_WEB + URL_WEB_CATEGORY

    print(f"Scrapeando categoría: {URL_WEB_CATEGORY}")
    print(f"URL: {url}")
   
    try:
        # Request con timeout configurado
        response = requests.get(
            url, 
            headers=HEADERS, 
            timeout=TIMEOUT
        )
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        
        # Parsear HTML https://beautiful-soup-4.readthedocs.io/en/latest/#quick-start
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ver que hay en la web
        os.makedirs('data/raw', exist_ok=True)
        filename_soup = f"data/raw/soup.txt"
        with open(filename_soup, 'w', encoding='utf-8') as f:
            f.write(f"{soup}")

        # Buscar trabajos con selector específico
        job_items = soup.find_all('a', class_='gb-results-list__item')
        print(f"Trabajos encontrados totales: {len(job_items)}")

        filename_jobs_items = f"data/raw/job_items.txt"
        with open(filename_jobs_items, 'w', encoding='utf-8') as f:
            f.write(f"{job_items}")


        # Procesar cada trabajo
        jobs_data = []  # Lista de tuplas (url, date)
        for job_item in job_items:
            """
            filtrar por ofertas del último mes
            las fechas vienen como 'jul 02', 'Jul 18', 'ago 09'
            dentro de: <div class="opacity-half size0">jul 02</div>
            asumir que se guardarán ofertas de hace un año, filtrar en detalle en scrap_jobs_detail()
            """

            job_url = job_item.get('href', '')
            
            # Extraer fecha
            date_element = job_item.select_one('.opacity-half.size0')
            date_text = date_element.get_text(strip=True) if date_element else ""
            
            # Solo agregar si es reciente
            if is_recent_job(date_text):
                jobs_data.append((job_url, date_text))

        # guardar job urls en txt
        print(f"Trabajos encontrados filtrados: {len(jobs_data)}")
        filename_jobs_urls = f"data/raw/job_urls.txt"
        with open(filename_jobs_urls, 'w', encoding='utf-8') as f:
            for url, date in jobs_data:
                f.write(f"{url} | {date}\n")
        print(f"Guardado: {filename_jobs_urls}")

        # Insertar en DB (ignore si ya existe)
        try:
            # Un solo batch insert
            con = sqlite3.connect(SQLITE_PATH + SQLITE_DB_JOBS)
            cur = con.cursor()

            # Preparar datos para executemany
            insert_data = [
                (url, date, NAME_PORTAL, URL_WEB_CATEGORY, datetime.now(), False) 
                for url, date in jobs_data]

            # https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.executemany
            cur.executemany(SCHEMA_JOBS_URLS_INSERT, insert_data)
            con.commit()
            con.close()
            print(f"Insertados {len(insert_data)} registros en DB")

        except Exception as e:
            print(f"Error insertando URLs: {e}")

    except Exception as e:
        print(f"Error scrapeando {URL_WEB_CATEGORY}: {e}")
        return

# Loop for url in job_urls, obtiene el job, scrap, guarda en db table jobs
def scrap_jobs_detail():
    return

# Run
def main():
    create_table()
    scrap_base_urls()

if __name__ == "__main__":
   main()