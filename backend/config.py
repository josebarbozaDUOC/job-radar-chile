# backend/config.py

"""
Configuración global para JobRadar Chile
Contiene todas las constantes, paths y configuraciones compartidas
"""

import os
from datetime import datetime

# ==================== PATHS ====================
# Paths relativos desde backend/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_PATH, "jobs.db")
RAW_DATA_PATH = os.path.join(DATA_PATH, "raw")

# ==================== SCRAPERS ====================
# Configuración general de scraping
DEFAULT_TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 1
MAX_RETRIES = 3

# Headers HTTP compartidos
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
}

# ==================== GETONBOARD ====================
GETONBOARD_BASE_URL = "https://www.getonbrd.com"
GETONBOARD_JOBS_URL = f"{GETONBOARD_BASE_URL}/jobs"
GETONBOARD_CATEGORIES = [
    "design-ux",
    "programming",
    "data-science-analytics",
    "mobile-developer",
    "customer-support",
    "digital-marketing",
    "sysadmin-devops-qa",
    "operations-management",
    "sales",
    "advertising-media",
    "innovation-agile",
    "hr",
    "machine-learning-ai",
    "hardware-electronics",
    "cybersecurity",
    "education-coaching",
    "technical-support",
    "other"
]

# ==================== FILTROS ====================
# Filtros de tiempo (en días)
MAX_JOB_AGE_DAYS = 30  # Solo trabajos del último mes

# ==================== LOGGING ====================
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ==================== DATABASE ====================
"""
Las entidades no están normalizadas aún.
Usa SQL puro, y no un ORM de momento.
"""
# Esquema SQL LISTA DE URLS JOBS
SCHEMA_JOB_URLS = """
CREATE TABLE IF NOT EXISTS job_urls (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    posted_date TEXT,
    portal TEXT,
    category TEXT,
    scraped_at TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);
"""

# Query INSERT A LISTA DE URLS JOBS
INSERT_JOB_URL = """
INSERT OR IGNORE INTO job_urls 
    (url, posted_date, portal, category, scraped_at, processed) 
    VALUES (?, ?, ?, ?, ?, ?)
"""

# Esquema SQL DE JOB OFFERS. REVISAR: docs/job_offer_schema.md
SCHEMA_JOB_OFFERS = """
CREATE TABLE IF NOT EXISTS job_offers (
    id INTEGER PRIMARY KEY,
    job_id TEXT,
    source_url TEXT UNIQUE,
    portal_name TEXT,
    scraped_at TEXT,
    posted_date TEXT,
    job_title_raw TEXT,
    job_title_normalized TEXT,
    job_category_raw TEXT,
    job_role TEXT,
    company_name_raw TEXT,
    company_url_raw TEXT,
    company_type TEXT,
    company_description_raw TEXT,
    location_work_mode_raw TEXT,
    location_raw TEXT,
    country TEXT,
    city TEXT,
    work_mode_raw TEXT,
    remote_location_allowed INTEGER,
    seniority_raw TEXT,
    seniority_normalized TEXT,
    years_experience_min INTEGER,
    years_experience_max INTEGER,
    employment_type_raw TEXT,
    contract_duration_months INTEGER,
    salary_disclosed INTEGER,
    salary_raw TEXT,
    salary_min_raw TEXT,
    salary_max_raw TEXT,
    salary_currency_raw TEXT,
    salary_unit_raw TEXT,
    salary_type_raw TEXT,
    salary_frequency TEXT,
    salary_min_clp INTEGER,
    salary_max_clp INTEGER,
    salary_min_usd INTEGER,
    salary_max_usd INTEGER,
    salary_min_market_usd INTEGER,
    salary_max_market_usd INTEGER,
    salary_estimated_by_llm INTEGER,
    requirements_raw TEXT,
    tech_stack_raw TEXT,
    main_techs TEXT,
    skills_required TEXT,
    skills_preferred TEXT,
    english_required INTEGER,
    english_level TEXT,
    job_description_raw TEXT,
    sections_raw TEXT,
    job_summary_llm TEXT,
    responsibilities_llm TEXT,
    benefits_raw TEXT,
    benefits_parsed_llm TEXT,
    perks_raw TEXT,
    llm_processed INTEGER,
    llm_processed_at TEXT,
    llm_confidence_score REAL,
    processing_notes TEXT,
    is_active INTEGER,
    last_checked_at TEXT,
    applications_raw TEXT,
    application_deadline TEXT,
    reply_time_raw TEXT,
    remote_policy_raw TEXT,
    apply_url TEXT
);
"""

# Query INSERT A JOB OFFERS
INSERT_JOB_OFFER = """
INSERT OR IGNORE INTO job_offers (
    job_id, source_url, portal_name, scraped_at, posted_date,
    job_title_raw, job_title_normalized, job_category_raw, job_role,
    company_name_raw, company_url_raw, company_type, company_description_raw,
    location_work_mode_raw, location_raw, country, city, work_mode_raw,
    remote_location_allowed, seniority_raw, seniority_normalized,
    years_experience_min, years_experience_max, employment_type_raw,
    contract_duration_months, salary_disclosed, salary_raw, salary_min_raw,
    salary_max_raw, salary_currency_raw, salary_unit_raw, salary_type_raw,
    salary_frequency, salary_min_clp, salary_max_clp, salary_min_usd,
    salary_max_usd, salary_min_market_usd, salary_max_market_usd,
    salary_estimated_by_llm, requirements_raw, tech_stack_raw, main_techs,
    skills_required, skills_preferred, english_required, english_level,
    job_description_raw, sections_raw, job_summary_llm, responsibilities_llm,
    benefits_raw, benefits_parsed_llm, perks_raw, llm_processed,
    llm_processed_at, llm_confidence_score, processing_notes, is_active,
    last_checked_at, applications_raw, application_deadline, reply_time_raw,
    remote_policy_raw, apply_url
) VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
);
"""