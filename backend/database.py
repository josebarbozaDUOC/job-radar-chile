# backend/database.py

"""
Manejo de base de datos para JobRadar Chile
Funciones para crear tablas, insertar y consultar datos
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Tuple, Optional
from contextlib import contextmanager

from config import (
    DB_PATH, 
    DATA_PATH,
    SCHEMA_JOB_URLS,
    INSERT_JOB_URL,
    SCHEMA_JOB_OFFERS,
    INSERT_JOB_OFFER
)


@contextmanager
def get_db_connection():
    """Context manager para manejar conexiones a la base de datos"""
    conn = None
    try:
        # Asegurar que existe el directorio
        os.makedirs(DATA_PATH, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        yield conn
    finally:
        if conn:
            conn.close()


def create_tables():
    """Crear todas las tablas necesarias en la base de datos"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(SCHEMA_JOB_URLS)     # Crea la de urls
        cursor.execute(SCHEMA_JOB_OFFERS)   # Crea la de publicaciones
        conn.commit()
        print(f"Tablas creadas/verificadas en: {DB_PATH}")


def insert_job_urls(jobs_data: List[Tuple[str, str]], portal: str, category: str) -> int:
    """
    Insertar múltiples URLs de trabajos en la base de datos
    Args:
        jobs_data: Lista de tuplas (url, posted_date)
        portal: Nombre del portal (ej: 'getonbrd.com')
        category: Categoría del trabajo (ej: 'programming')
    Returns: Número de registros insertados
    """
    if not jobs_data:
        return 0
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Preparar datos para executemany
        insert_data = [
            (url, posted_date, portal, category, datetime.now(), False)
            for url, posted_date in jobs_data
        ]
        
        cursor.executemany(INSERT_JOB_URL, insert_data)
        conn.commit()
        
        inserted_count = cursor.rowcount
        print(f"Insertados {inserted_count} registros en DB")
        return inserted_count


# UTILS: De tabla: job_urls
def get_job_urls_full(processed: Optional[bool] = None, limit: Optional[int] = None) -> List[sqlite3.Row]:
    """Obtener registros completos de job_urls"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        where = f" WHERE processed = {1 if processed else 0}" if processed is not None else ""
        limit_clause = f" LIMIT {limit}" if limit else ""
        cursor.execute(f"SELECT * FROM job_urls{where} ORDER BY scraped_at DESC{limit_clause}")
        return cursor.fetchall()
    
def get_all_urls() -> List[str]:
    """Obtener todas las URLs de trabajos"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT url FROM job_urls"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [row['url'] for row in rows]
        
def get_unprocessed_jobs(limit: Optional[int] = None) -> List[sqlite3.Row]:
    """
    Obtener trabajos que no han sido procesados aún
    Args: limit: Número máximo de registros a retornar
    Returns: Lista de trabajos no procesados
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM job_urls WHERE processed = FALSE"
        if limit:
            query += f" LIMIT {limit}"
            
        cursor.execute(query)
        return cursor.fetchall()

def mark_job_as_processed(job_id: int):
    """Marcar un trabajo como procesado"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE job_urls SET processed = TRUE WHERE id = ?",
            (job_id,)
        )
        conn.commit()

def get_job_count_by_portal() -> List[Tuple[str, int]]:
    """Obtener conteo de trabajos por portal"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT portal, COUNT(*) as count 
            FROM job_urls 
            GROUP BY portal
        """)
        return cursor.fetchall()

def get_recent_jobs(days: int = 7) -> List[sqlite3.Row]:
    """Obtener trabajos scrapeados en los últimos N días"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM job_urls 
            WHERE datetime(scraped_at) > datetime('now', '-' || ? || ' days')
            ORDER BY scraped_at DESC
        """, (days,))
        return cursor.fetchall()
    

def insert_job_offer(job_data: dict) -> bool:
    """
    Insertar una oferta de trabajo en la tabla job_offers
    Args: job_data: Diccionario con los datos del trabajo (del scraper)
    Returns: True si se insertó correctamente, False si ya existía o hubo error
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        try:            
            # Mapear datos del scraper a campos de la BD
            insert_values = (
                job_data.get('job_id'),
                job_data.get('source_url'),
                job_data.get('portal_name'),
                job_data.get('scraped_at'),
                job_data.get('posted_date'),
                job_data.get('job_title_raw'),
                None,  # job_title_normalized
                job_data.get('job_category_raw'),
                None,  # job_role
                job_data.get('company_name_raw'),
                job_data.get('company_url_raw'),
                None,  # company_type
                job_data.get('company_description_raw'),
                job_data.get('location_work_mode_raw'),
                job_data.get('location_raw'),
                None,  # country
                None,  # city
                job_data.get('work_mode_raw'),
                None,  # remote_location_allowed # puede ser bool, o str
                job_data.get('seniority_raw'),
                None,  # seniority_normalized
                None,  # years_experience_min
                None,  # years_experience_max
                job_data.get('employment_type_raw'),
                None,  # contract_duration_months
                job_data.get('salary_disclosed'),
                job_data.get('salary_raw'),
                job_data.get('salary_min_raw'),
                job_data.get('salary_max_raw'),
                job_data.get('salary_currency_raw'),
                job_data.get('salary_unit_raw'),
                job_data.get('salary_type_raw'),
                None,  # salary_frequency
                None,  # salary_min_clp
                None,  # salary_max_clp
                None,  # salary_min_usd
                None,  # salary_max_usd
                None,  # salary_min_market_usd
                None,  # salary_max_market_usd
                0,  # salary_estimated_by_llm
                None,  # requirements_raw
                json.dumps(job_data.get('tech_stack_raw', []), ensure_ascii=False) if job_data.get('tech_stack_raw') else None,
                None,  # main_techs
                None,  # skills_required
                None,  # skills_preferred
                None,  # english_required
                None,  # english_level
                None,  # job_description_raw
                json.dumps(job_data.get('sections_raw', []), ensure_ascii=False) if job_data.get('sections_raw') else None,
                None,  # job_summary_llm
                None,  # responsibilities_llm
                None,  # benefits_raw
                None,  # benefits_parsed_llm
                json.dumps(job_data.get('perks_raw', []), ensure_ascii=False) if job_data.get('perks_raw') else None,
                None, # responsibilities
                None, # requirements
                None, # nice_to_have
                None, # candidate_profile
                None, # benefits
                None, # work_conditions
                None, # selection_process
                None, # how_to_apply
                None, # others
                0,  # llm_processed
                None,  # llm_processed_at
                None,  # llm_confidence_score
                None,  # processing_notes
                1,  # is_active
                job_data.get('last_checked', datetime.now().isoformat()),
                job_data.get('applications_raw'),
                None,  # application_deadline
                job_data.get('reply_time_raw'),
                job_data.get('remote_policy_raw'),
                job_data.get('apply_url')
            )
            
            cursor.execute(INSERT_JOB_OFFER, insert_values)
            conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error insertando job offer: {e}")
            return False
        

def get_jobs_sections_raw() -> List[dict]:
    """
    Obtener job_id y sections_raw de todas las ofertas
    Returns: Lista de diccionarios con job_id y sections_raw parseado
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT job_id, sections_raw 
            FROM job_offers 
            WHERE sections_raw IS NOT NULL
        """)
        
        results = []
        for row in cursor.fetchall():
            try:
                sections = json.loads(row['sections_raw']) if row['sections_raw'] else []
                results.append({
                    'job_id': row['job_id'],
                    'sections': sections
                })
            except json.JSONDecodeError:
                print(f"Error parseando sections_raw para job_id: {row['job_id']}")
                continue
                
        return results


def update_job_sections(job_id: str, classified_sections: dict) -> bool:
    """
    Actualizar los campos de secciones clasificadas en job_offers
    Args:
        job_id: ID del trabajo
        classified_sections: Diccionario con las secciones clasificadas
    Returns: True si se actualizó correctamente
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE job_offers 
                SET 
                    responsibilities = ?,
                    requirements = ?,
                    nice_to_have = ?,
                    candidate_profile = ?,
                    benefits = ?,
                    work_conditions = ?,
                    selection_process = ?,
                    how_to_apply = ?,
                    others = ?
                WHERE job_id = ?
            """, (
                classified_sections.get('responsibilities'),
                classified_sections.get('requirements'),
                classified_sections.get('nice_to_have'),
                classified_sections.get('candidate_profile'),
                classified_sections.get('benefits'),
                classified_sections.get('work_conditions'),
                classified_sections.get('selection_process'),
                classified_sections.get('how_to_apply'),
                classified_sections.get('others'),
                job_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Error actualizando secciones para job_id {job_id}: {e}")
            return False