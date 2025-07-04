# backend/scrapers/getonbrd.py

"""
Scraper específico para GetOnBoard Chile
Extrae ofertas de trabajo por categorías
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List, Tuple, Optional
import json

from config import (
    GETONBOARD_JOBS_URL,
    DEFAULT_HEADERS,
    DEFAULT_TIMEOUT,
    RAW_DATA_PATH,
    MAX_JOB_AGE_DAYS
)


class GetOnBoardScraper:
    """Scraper para el portal GetOnBoard"""
    
    def __init__(self):
        self.base_url = GETONBOARD_JOBS_URL
        self.headers = DEFAULT_HEADERS
        self.timeout = DEFAULT_TIMEOUT
        self.portal_name = "getonbrd.com" # harcodeado
    
    def scrape_job_listings(self, category: str = "programming") -> List[Tuple[str, str]]:
        """
        Obtener listado de trabajos de una categoría
        Args: category: Categoría a scrapear (ej: 'programming')
        Returns: Lista de tuplas (url, posted_date)
        """
        url = f"{self.base_url}/{category}"
        print(f"Scrapeando categoría: {category}")
        print(f"URL: {url}")
        print("... 👀 ...")
        
        try:
            # Request
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            print(f"Status: {response.status_code}")
            
            # Parsear HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Guardar HTML para debugging
            self._save_raw_html(soup, f"soup_{category}.txt")
            
            # Buscar trabajos
            job_items = soup.find_all('a', class_='gb-results-list__item')
            print(f"Trabajos encontrados totales: {len(job_items)}")
            
            # Procesar cada trabajo
            jobs_data = []
            for job_item in job_items:
                job_url = job_item.get('href', '')
                
                # Extraer fecha
                date_element = job_item.select_one('.opacity-half.size0')
                date_text = date_element.get_text(strip=True) if date_element else ""
                
                # Solo agregar si es reciente
                if self._is_recent_job(date_text):
                    jobs_data.append((job_url, date_text))
            
            print(f"Trabajos filtrados (últimos {MAX_JOB_AGE_DAYS} días): {len(jobs_data)}")
            
            # Guardar URLs filtradas para debugging
            self._save_job_urls(jobs_data, f"job_urls_{category}.txt")
            
            return jobs_data
            
        except requests.RequestException as e:
            print(f"Error en request: {e}")
            return []
        except Exception as e:
            print(f"Error scrapeando {category}: {e}")
            return []


    def _is_recent_job(self, date_text: str) -> bool:
        """
        Validar si la fecha está dentro del rango aceptable
        Args: date_text: Texto de fecha (ej: 'jul 02')
        Returns: True si el trabajo es reciente
        """
        if not date_text:
            return True
        
        try:
            # Parsear fecha
            month_str, day_str = date_text.lower().split()
            months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
            
            job_month = months.index(month_str) + 1
            job_day = int(day_str)
            
            # Inferir año (si el mes es futuro, es del año anterior)
            current_date = datetime.now()
            job_year = current_date.year
            
            job_date = datetime(job_year, job_month, job_day)
            
            # Si la fecha es futura, es del año anterior
            if job_date > current_date:
                job_date = job_date.replace(year=job_year - 1)
            
            # Verificar si está en el rango
            max_age = current_date - relativedelta(days=MAX_JOB_AGE_DAYS)
            
            return max_age <= job_date <= current_date
            
        except Exception as e:
            #print(f"Error parseando fecha '{date_text}': {e}")
            return False
    
    def _save_raw_html(self, soup: BeautifulSoup, filename: str):
        """Guardar HTML crudo para debugging"""
        os.makedirs(RAW_DATA_PATH, exist_ok=True)
        filepath = os.path.join(RAW_DATA_PATH, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"HTML guardado: {filepath}")
    
    def _save_job_urls(self, jobs_data: List[Tuple[str, str]], filename: str):
        """Guardar URLs de trabajos para debugging"""
        os.makedirs(RAW_DATA_PATH, exist_ok=True)
        filepath = os.path.join(RAW_DATA_PATH, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for url, date in jobs_data:
                f.write(f"{url} | {date}\n")
        print(f"URLs guardadas: {filepath}")
    

    def scrape_job_detail(self, job_url: str) -> Optional[dict]:
        """
        Obtener detalle de una oferta de trabajo
        Args: job_url: URL del trabajo
        Returns: Diccionario con los detalles del trabajo o None si falla
        """
        try:
            time.sleep(2)  # Rate limiting
            
            # Validar y construir URL completa
            if not job_url.startswith('http'):
                job_url = f"https://www.getonbrd.com{job_url}"
            
            print(f"Scrapeando detalle: {job_url}")
            
            # Request con headers y timeout
            response = requests.get(job_url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer job_id primero para usar en filename
            job_id_match = re.search(r'GETONBRD Job ID: (\d+)', soup.get_text())
            job_id = job_id_match.group(1) if job_id_match else "unknown"
            
            # Guardar HTML para debugging
            # self._save_raw_html(soup, f"job_detail_{job_id}.txt")
            
            # Básicos
            job_portal = self.portal_name

            title = soup.find('span', itemprop='title')
            job_title = title.get_text(strip=True) if title else None
            
            company_tag = soup.find('strong', itemprop='name')
            company_name = company_tag.get_text(strip=True) if company_tag else None
            
            company_url_tag = soup.find('span', itemprop='url')
            company_url = company_url_tag.get_text(strip=True) if company_url_tag else None
            
            """
            AHORA QUE SE PUEDE ACCEDER A LA FECHA COMPLETA DE PUBLICACIÓN
            ACÁ FALTA VALIDAR E IGNORAR ESTA PUBLICACIÓN SI NO ES DE LOS ÚLTIMOS 30 DÍAS
            REUTILIZAR _is_recent_job() ?
            """
            date_posted_tag = soup.find('time', itemprop='datePosted')
            date_posted = date_posted_tag['datetime'] if date_posted_tag and date_posted_tag.has_attr('datetime') else None
            posted_date_clean = datetime.fromisoformat(date_posted).date().isoformat() if date_posted else None
            
            # Location y Modalidad combinados
            location_modality = None
            location_element = soup.select_one('.location')

            if location_element:
                # Primero eliminar elementos ocultos
                for hidden in location_element.select('.hide, .location-tooltip-content'):
                    hidden.decompose()
                
                # Buscar diferentes estructuras
                # Caso 1: Con link (Santiago)
                location_link = location_element.select_one('a')
                if location_link:
                    # Obtener el texto del link
                    location_text = location_link.get_text(strip=True)
                    # Buscar el texto después del link (debería ser "(In-office)" o similar)
                    next_text = location_link.next_sibling
                    if next_text and isinstance(next_text, str):
                        location_modality = location_text + ' ' + next_text.strip()
                    else:
                        # Buscar en todo el elemento padre
                        parent_text = location_element.get_text(separator=' ', strip=True)
                        location_modality = ' '.join(parent_text.split())
                else:
                    # Caso 2: Sin link (Remote)
                    location_modality = location_element.get_text(separator=' ', strip=True)
                    location_modality = ' '.join(location_modality.split())
                
                # Limpiar caracteres especiales
                location_modality = location_modality.replace('\xa0', ' ').strip()

            # Separar location y modality
            location = None
            modality = None

            if location_modality:
                # Buscar paréntesis
                match = re.search(r'^(.*?)\s*\((.*?)\)$', location_modality)
                if match:
                    first_part = match.group(1).strip()
                    second_part = match.group(2).strip()
                    
                    # Determinar qué es qué
                    if first_part.lower() == 'remote' or first_part.lower() == 'remoto':
                        # Remote (Chile) -> location=Chile, modality=Remote
                        location = second_part
                        modality = first_part
                    else:
                        # Santiago (In-office) -> location=Santiago, modality=In-office
                        location = first_part
                        modality = second_part
                else:
                    # Sin paréntesis, asumir que todo es location
                    location = location_modality
                    modality = None


            experience_tag = soup.find('span', itemprop='qualifications')
            experience = experience_tag.get_text(strip=True) if experience_tag else None
            
            employment_type_tag = soup.find('span', itemprop='employmentType')
            employment_type = employment_type_tag.get_text(strip=True) if employment_type_tag else None
            
            # Extraer categoría de la URL
            category = None
            try:
                # Buscar el patrón después de /jobs/ o /empleos/ o cualquier idioma
                match = re.search(r'/(?:jobs|empleos|empregos|emplois)/([^/]+)/', job_url)
                if match:
                    category = match.group(1)
                    # Normalizar: programming -> Programming, design-ux -> Design Ux
                    category = category.replace('-', ' ').title()
            except:
                category = None

            # Sueldo
            salary_scope = soup.find('span', itemprop='baseSalary')
            if salary_scope:
                min_salary = salary_scope.find('span', itemprop='minValue')
                max_salary = salary_scope.find('span', itemprop='maxValue')
                currency = salary_scope.find('span', itemprop='currency')
                unit = salary_scope.find('span', itemprop='unitText')
                salary_min = min_salary['content'] if min_salary and min_salary.has_attr('content') else None
                salary_max = max_salary['content'] if max_salary and max_salary.has_attr('content') else None
                salary_currency = currency['content'] if currency and currency.has_attr('content') else None
                salary_unit = unit['content'] if unit and unit.has_attr('content') else None
                salary_disclosed = True
                salary_raw = f"{salary_min} - {salary_max} {salary_currency}/{salary_unit}"

                # Detectar si es sueldo bruto o líquido
                salary_type_span = salary_scope.find('span', class_='hide-on-small-mobile')
                salary_type = salary_type_span.get_text(strip=True).lower() if salary_type_span else None

            else:
                salary_min = salary_max = salary_currency = salary_unit = salary_raw = salary_type = None
                salary_disclosed = False
            
            # Descripción HTML cruda
            description_div = soup.find('div', itemprop='description')
            
            # Extraer descripción de la empresa
            company_description = ""
            if description_div:
                first_rich_txt = description_div.find('div', class_='gb-rich-txt')
                if first_rich_txt:
                    # Buscar el primer elemento hijo que sea p o div
                    first_content = first_rich_txt.find(['p', 'div'])
                    if first_content:
                        company_description = first_content.get_text(strip=True)

            # Secciones textuales (functions, requirements, nice_to_have, benefits)
            sections = []
            for div in soup.find_all('div', class_='mb4'):
                h3 = div.find('h3')
                content_div = div.find('div', class_='gb-rich-txt')
                
                if h3 and content_div:  # Solo agregar si ambos existen
                    sections.append({
                        'title': h3.get_text(strip=True),
                        'content': content_div.get_text(separator='\n', strip=True)
                    })
            
            # Postulaciones y revisión
            meta_info = soup.select_one('.size0.mt1')
            meta_text = meta_info.get_text() if meta_info else ""
            
            # Buscar applications en inglés o español
            # Prefiero confiar en el html que en palabras en algún idioma
            applications_match = re.search(r'(\d+)\s+(applications?|postulaciones?)', meta_text, re.IGNORECASE) 
            applications = int(applications_match.group(1)) if applications_match else None

            # Para reply_time y last_checked - buscar el div específico
            # Igual puede dar lo mismo en el idioma que venga, y que extraigamos las palabras originales
            reply_time = None
            last_checked = None
            meta_div = soup.find('div', class_='size0 mt1')
            if meta_div:
                # Buscar dos números para reply time
                numbers = re.findall(r'\d+', meta_div.get_text())
                if len(numbers) >= 3:  # 46, 15, 27
                    reply_time = f"{numbers[1]}-{numbers[2]} days"
                
                # Para last checked, buscar la última línea del div
                lines = [line.strip() for line in meta_div.get_text().split('\n') if line.strip()]
                if lines:
                    last_checked = 'today' if any(word in lines[-1].lower() for word in ['hoy', 'today']) else None

            
            # Perks (íconos con texto)
            perks = []
            perk_tags = soup.select('.gb-fluid-boxes__item strong')
            for tag in perk_tags:
                perks.append(tag.get_text(strip=True))
            
            # Remote work policy
            remote_policy = None
            # Buscar en inglés y español
            for h2 in soup.find_all('h2'):
                h2_text = h2.get_text(strip=True)
                if 'Remote work policy' in h2_text or 'Política de trabajo remoto' in h2_text:
                    # El siguiente elemento después del h2
                    next_elem = h2.find_next_sibling()
                    if next_elem and next_elem.name == 'p':
                        # El párrafo con la descripción está después del primero
                        desc_elem = next_elem.find_next_sibling('p')
                        if desc_elem:
                            remote_policy = desc_elem.get_text(strip=True)
                            break


            # Tags tecnológicos (dentro del contenedor de skills)
            technologies = []
            skills_container = soup.find('div', class_='gb-tags', itemprop='skills')
            if skills_container:
                tech_tags = skills_container.find_all('a', class_='gb-tags__item')
                technologies = [tag.get_text(strip=True) for tag in tech_tags]

            
            # URL de postulación
            apply_btn = soup.find('a', id='apply_bottom')
            apply_url = apply_btn['href'] if apply_btn and apply_btn.has_attr('href') else None

            scraped_at_clean = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Construir diccionario de resultado
            job_detail = {
                'job_id': job_id,
                'source_url': job_url,
                'portal_name': job_portal,
                'posted_date': posted_date_clean,
                'job_title_raw': job_title,
                'job_category_raw': category,
                'company_name_raw': company_name,
                'company_url_raw': company_url,
                'company_description_raw': company_description,
                'location_work_mode_raw': location_modality,
                'location_raw': location,
                'work_mode_raw': modality,
                'seniority_raw': experience,
                'employment_type_raw': employment_type,
                'salary_disclosed': salary_disclosed,
                'salary_raw': salary_raw,
                'salary_min_raw': salary_min,
                'salary_max_raw': salary_max,
                'salary_currency_raw': salary_currency,
                'salary_unit_raw': salary_unit,
                'salary_type_raw': salary_type,
                'tech_stack_raw': technologies,
                'sections_raw': sections,
                'perks_raw': perks,
                'last_checked': last_checked,
                'applications_raw': applications,
                'reply_time_raw': reply_time,
                'remote_policy_raw': remote_policy,
                'apply_url': apply_url,
                'scraped_at': scraped_at_clean,
            }
            
            '''# SOLO PARA TEST DEBUG COMENTAR PARA DESARROLLO
            # Guardar publicación en json
            os.makedirs(RAW_DATA_PATH, exist_ok=True)
            # Extraer el slug de la URL
            url_parts = job_url.rstrip('/').split('/')
            slug = url_parts[-1] if url_parts else 'unknown'
            # Limitar longitud del slug y combinarlo con job_id
            slug_truncated = slug[:50]  # Limitar a 50 caracteres
            filename = f"job_{job_id}_{slug_truncated}.json"

            filepath = os.path.join(RAW_DATA_PATH, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(job_detail, f, ensure_ascii=False, indent=4)'''

            
            return job_detail
            
        except requests.RequestException as e:
            print(f"Error de conexión con {job_url}: {e}")
            return None
        except Exception as e:
            print(f"Error parseando {job_url}: {e}")
            return None