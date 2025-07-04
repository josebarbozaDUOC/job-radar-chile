# backend/main.py

"""
JobRadar Chile - Script principal
Orquesta el proceso de scraping y almacenamiento
"""

import sys
import time
from datetime import datetime
import random
from config import GETONBOARD_CATEGORIES
from database import create_tables, insert_job_urls, get_job_count_by_portal
from database import get_job_urls_full, insert_job_offer, mark_job_as_processed
from scrapers.getonbrd import GetOnBoardScraper


def scrape_getonboard(categories: list = None):
    """
    Ejecutar scraping de GetOnBoard
    Args: categories: Lista de categorías a scrapear. Si es None, usa 'programming'
    """
    if categories is None:
        categories = ['programming']
    
    scraper = GetOnBoardScraper()
    
    for category in categories:
        print(f"\n{'='*50}")
        print(f"Procesando categoría: {category}")
        print(f"{'='*50}")
        
        # Obtener trabajos
        jobs = scraper.scrape_job_listings(category)
        
        if jobs:
            # Guardar en base de datos
            inserted = insert_job_urls(
                jobs_data=jobs,
                portal=scraper.portal_name,
                category=category
            )
            print(f"✓ Categoría {category} completada: {inserted} nuevos trabajos")
        else:
            print(f"✗ No se encontraron trabajos para {category}")


def scrape_job_details(limit: int = None, test_mode: bool = False):
    """
    Scrapear detalles de cada oferta de trabajo desde las URLs guardadas
    Args:
        limit: Número máximo de URLs a procesar (None = todas)
        test_mode: Si True, solo procesa 3 URLs para testing
    """
    print(f"\n{'='*50}")
    print("SCRAPING DETALLES DE OFERTAS")
    print(f"{'='*50}")
    
    # Obtener URLs no procesadas
    job_urls = get_job_urls_full(processed=False, limit=limit)
    
    if not job_urls:
        print("No hay URLs pendientes de procesar")
        return
    
    total_urls = len(job_urls)
    print(f"URLs a procesar: {total_urls}")
    
    if test_mode:
        job_urls = job_urls[:3]
        print("Modo TEST: procesando solo 3 URLs")
    
    scraper = GetOnBoardScraper()
    processed = 0
    errors = 0
    
    for idx, job_url_row in enumerate(job_urls, 1):
        url = job_url_row['url']
        job_id = job_url_row['id']
        
        print(f"\n[{idx}/{len(job_urls)}] Procesando: {url}")
        
        try:
            # Scrapear detalles
            job_details = scraper.scrape_job_detail(url)
            
            if job_details:
                # Insertar en job_offers
                if insert_job_offer(job_details):
                    print(f"✓ Guardado en job_offers")
                    mark_job_as_processed(job_id)
                    processed += 1
                else:
                    print(f"⚠ Ya existe en job_offers")
                    mark_job_as_processed(job_id)  # Marcar como procesado igual
            else:
                print(f"✗ No se pudieron obtener detalles")
                errors += 1
                
        except Exception as e:
            print(f"✗ Error: {e}")
            errors += 1
        
        # Delay entre requests
        if idx < len(job_urls):  # No delay después del último
            delay = random.uniform(1, 3)
            print(f"Esperando {delay:.1f} segundos...")
            time.sleep(delay)
            
            # Pausa larga cada 50 registros
            if idx % 50 == 0:
                long_delay = random.uniform(10, 20)
                print(f"\n⏸ Pausa larga: {long_delay:.1f} segundos (cada 50 registros)")
                time.sleep(long_delay)
    
    # Resumen
    print(f"\n{'='*50}")
    print(f"RESUMEN SCRAPING DETALLES")
    print(f"{'='*50}")
    print(f"Total procesados: {processed}/{total_urls}")
    print(f"Errores: {errors}")
    print(f"✓ Scraping de detalles completado")


def show_stats():
    """Mostrar estadísticas de la base de datos"""
    print(f"\n{'='*50}")
    print("ESTADÍSTICAS")
    print(f"{'='*50}")
    
    stats = get_job_count_by_portal()
    for portal, count in stats:
        print(f"{portal}: {count} trabajos")

        
def main():
    """Función principal"""
    print("👀 JobRadar Chile - Iniciando...")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Crear/verificar tablas
    create_tables()
    
    # Ejecutar scraping
    # Solo categoría 'programming'
    # scrape_getonboard(GETONBOARD_CATEGORIES)  # Todas las categorías
    scrape_getonboard(['programming'])
    
    # PASO 2: Scraping de detalles de cada oferta
    #scrape_job_details()
    #scrape_job_details(test_mode=True)
    scrape_job_details(limit=10)
    
    # Mostrar estadísticas
    show_stats()
    print("\n✓ Proceso completado")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)