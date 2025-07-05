# backend/utils/section_classifier.py

from rapidfuzz import fuzz
from .section_patterns import SECTION_PATTERNS
from typing import Optional
import unicodedata
import re

def normalize_text(text: str) -> str:
    """Normaliza el texto removiendo emojis, acentos y caracteres especiales."""
    # AGREGAR ESTA LÍNEA: Remover emojis y caracteres especiales
    text = re.sub(r'[^\w\s\-\']', ' ', text, flags=re.UNICODE)
    
    # Tu código existente
    text = ''.join(c for c in unicodedata.normalize('NFD', text) 
                   if unicodedata.category(c) != 'Mn')
    return text.lower().strip()

def section_classifier(texto: str, min_score: int = 70) -> Optional[str]:
    """
    Clasifica un texto en una categoría de sección.
    
    Parámetros:
        texto (str): Texto a clasificar (idealmente título o título + contenido)
        min_score (int): Puntaje mínimo para considerar una coincidencia válida
        
    Retorna:
        str | None: Nombre de la categoría o None si no hay match
    """
    if not texto:
        return None
        
    texto_norm = normalize_text(texto)
    
    # Si el texto es muy largo, probablemente es solo contenido
    # Enfocarse en las primeras palabras que podrían ser el título
    if len(texto_norm) > 100:
        # Tomar las primeras 50 palabras para la comparación
        texto_norm = ' '.join(texto_norm.split()[:50])
    
    best_match = None
    best_score = 0
    
    for categoria, patrones in SECTION_PATTERNS.items():
        for patron in patrones:
            patron_norm = normalize_text(patron)
            
            # Usar partial_ratio para encontrar el patrón dentro del texto
            score = fuzz.partial_ratio(patron_norm, texto_norm)
            
            if score > best_score:
                best_score = score
                best_match = categoria
    
    return best_match if best_score >= min_score else None