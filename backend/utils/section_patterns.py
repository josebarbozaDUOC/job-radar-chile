# backend/utils/section_patterns.py

"""
Palabras claves para clasificar secciones de una publicación de empleo
Las secciones más comunes e importantes son: responsabilidades, requisitos, deseables, beneficios
Utilizada por backend/utils/section_classifier.py
"""

SECTION_PATTERNS = {
    # responsabilidades: SECCIÓN MUY IMPORTANTE
    "responsibilities": [
        # Español
        "funciones del cargo", "funciones", "tareas del cargo", "responsabilidades", 
        "responsabilidades principales", "funciones principales", "actividades principales",
        "qué harás", "que harás", "¿qué harás?", "tus responsabilidades", "tu misión",
        "rol del puesto", "día a día", "objetivos del cargo", "actividades", "tus funciones",
        "serás responsable de", "te encargarás de", "tus tareas", "alcance del rol",
        "descripción de funciones", "principales responsabilidades", "responsabilidades del rol",
        "desafío", "desafío profesional", "ser responsable", "responsable del desarrollo",
        # Inglés
        "key responsibilities", "main responsibilities", "what you'll do", "what you will do",
        "daily tasks", "responsibilities", "your responsibilities", "job responsibilities",
        "core responsibilities", "primary responsibilities", "key accountabilities",
        "what you'll be doing", "your mission", "duties", "role responsibilities",
        "key duties", "main duties", "job duties", "your role", "in this role",
        "what you'll actually do", "what you will actually do", "be responsible of"
        "day to day", "day-to-day", "your day to day", "responsible", "be responsible"
    ],
    # requisitos: SECCIÓN MUY IMPORTANTE
    "requirements": [
        # Español
        "requisitos", "requerimientos", "requisitos del cargo", "requerimientos del cargo",
        "requisitos y perfil", "perfil y requisitos", "requisitos mínimos", "requisitos excluyentes",
        "habilidades requeridas", "experiencia requerida", "conocimientos requeridos",
        "tecnologías requeridas", "conocimientos obligatorios", "perfil técnico",
        "qué esperamos de ti", "que esperamos de ti", "lo que buscamos", "qué necesitas",
        "que necesitas", "indispensable", "imprescindible", "necesario", "obligatorio",
        "competencias técnicas", "hard skills", "requisitos técnicos", "experiencia necesaria",
        # Inglés
        "required skills", "requirements", "technical requirements", "must have", "must-have",
        "mandatory skills", "required experience", "minimum requirements", "essential skills",
        "required qualifications", "what we're looking for", "what we are looking for",
        "what you need", "what you'll need", "what you will need", "qualifications",
        "mandatory requirements", "core requirements", "essential requirements",
        "technical skills required", "hard requirements", "non-negotiable requirements"
    ],
    # deseables: SECCIÓN MUY IMPORTANTE
    "nice_to_have": [
        # Español
        "deseables", "deseado", "plus", "un plus", "es un plus", "será un plus",
        "valorable", "se valorará", "valoramos", "habilidades opcionales", 
        "conocimientos deseables", "conocimientos valorables", "competencias deseables",
        "ventajas", "puntos extra", "sería genial si", "nos encantaría si",
        "ideal si tienes", "preferible", "preferentemente", "deseable pero no indispensable",
        "habilidades complementarias", "bonus", "extras", "adicionales",
        # Inglés
        "nice to have", "nice-to-have", "preferred qualifications", "bonus skills",
        "desirable skills", "preferred skills", "bonus points", "extra points",
        "would be great if", "we'd love if", "ideally", "preferably",
        "additional skills", "complementary skills", "a plus", "it's a plus",
        "bonus qualifications", "preferred experience", "great to have",
        "optional requirements", "soft requirements", "wish list"
    ],
    # perfil_candidato: SECCIÓN RELATIVA, NO SIEMPRE INCLUIDA EN CUERPO DE PUBLICACIÓN
    "candidate_profile": [
        # Español
        "perfil del candidato", "a quién buscamos", "a quien buscamos", "perfil buscado",
        "perfil ideal", "candidato ideal", "persona ideal", "buscamos a alguien",
        "cualidades personales", "soft skills", "habilidades blandas", "competencias blandas",
        "personalidad requerida", "características personales", "perfil personal",
        "cómo eres", "como eres", "tu perfil", "sobre ti", "acerca de ti",
        "valores del candidato", "fit cultural", "encaje cultural",
        # Inglés
        "candidate profile", "who we're looking for", "who we are looking for",
        "ideal candidate", "about you", "who you are", "personal qualities",
        "soft skills", "personal skills", "cultural fit", "personality traits",
        "who should apply", "is this you?", "are you the one?", "your profile",
        "personal characteristics", "behavioral competencies", "who will succeed",
        "you're a fit if you", "you are a fit if you"
    ],
    # beneficios: SECCIÓN IMPORTANTE
    "benefits": [
        # Español
        "beneficios", "lo que ofrecemos", "qué ofrecemos", "que ofrecemos",
        "por qué trabajar con nosotros", "por que trabajar con nosotros",
        "beneficios del cargo", "beneficios y cultura", "ventajas laborales",
        "compensaciones", "nuestra propuesta", "propuesta de valor", "qué incluye",
        "que incluye", "paquete de beneficios", "beneficios adicionales",
        "prestaciones", "compensación total", "retribución", "perks",
        "beneficios y cultura organizacional", "lo que recibirás",
        "vacaciones", "bono", "inclusión",
        # Inglés
        "benefits", "perks", "what we offer", "why join us", "employee benefits",
        "compensation package", "total rewards", "package", "what's in it for you",
        "perks and benefits", "benefits package", "our offer", "value proposition",
        "employee value proposition", "evp", "rewards", "company benefits",
        "why work with us", "why work here", "what you'll get", "what you will get",
        "vacations", "inclusion", "why join", "join us"
    ],
    # condiciones: SECCIÓN RELATIVA, NO SIEMPRE INCLUIDA EN CUERPO DE PUBLICACIÓN (PUEDE VENIR EN HEADER)
    "work_conditions": [
        # Español
        "condiciones", "condiciones laborales", "modalidad de trabajo", "modalidad",
        "jornada", "jornada laboral", "horario", "horario de trabajo",
        "salario", "remuneración", "rango salarial", "compensación económica",
        "ubicación", "lugar de trabajo", "tipo de contrato", "contrato",
        "esquema de trabajo", "formato de trabajo", "condiciones del cargo",
        "detalles del cargo", "información del cargo", "datos del cargo",
        # Inglés
        "work conditions", "workplace", "compensation", "schedule", "salary",
        "location", "contract type", "employment conditions", "working hours",
        "work arrangement", "work format", "job details", "position details",
        "employment type", "work schedule", "pay range", "salary range",
        "working conditions", "terms of employment", "job information"
    ],
    # como_aplicar: SECCIÓN RELATIVA, NO SIEMPRE INCLUIDA EN CUERPO DE PUBLICACIÓN (PUEDE VENIR COMO FOOTER)
    "how_to_apply": [
        # Español
        "cómo postular", "como postular", "cómo aplicar", "como aplicar",
        "postulación", "proceso de postulación", "envío de cv", "envio de cv",
        "link de postulación", "postula aquí", "postula aqui", "aplica aquí",
        "aplica aqui", "envía tu cv", "envia tu cv", "candidatura", "envia mail",
        "proceso de selección", "pasos para postular", "instrucciones",
        # Inglés
        "how to apply", "application process", "apply now", "submit your application",
        "application instructions", "apply here", "send your cv", "send your resume",
        "application procedure", "next steps", "selection process", "how to proceed",
        "submit application", "application method", "apply for this position", "send email"
    ],
    # proceso_seleccion: SECCIÓN POCO COMÚN
    "selection_process": [
        # Español
        "proceso de selección", "etapas del proceso", "pasos del proceso",
        "cómo es el proceso", "como es el proceso", "fases de selección",
        "timeline", "cronograma", "duración del proceso", "siguientes pasos",
        # Inglés
        "selection process", "interview process", "hiring process", "process steps",
        "recruitment process", "what to expect", "process timeline", "next steps",
        "stages", "interview stages", "selection stages", "hiring timeline"
    ],
    # otras_secciones: SECCIÓN SOLO EN CASO DE NECESIDAD
    "others": [
        # Español
        "otros detalles", "información adicional", "información complementaria",
        "notas adicionales", "observaciones", "consideraciones", "datos extra",
        "más información", "mas información", "detalles adicionales", "otros",
        # Inglés
        "additional info", "additional information", "miscellaneous", "extra information",
        "other details", "notes", "additional notes", "more info", "further information",
        "supplementary information", "other", "extras", "additional details"
    ],
}

"""
# OTRAS
# COMENTADO MIENTRAS, difícil de obtener del cuerpo de publicación
    "resumen_rol": [
        # Español
        "resumen del cargo", "resumen del rol", "overview del cargo", "descripción general",
        "acerca del cargo", "sobre el rol", "sobre la posición", "descripción del puesto",
        "objetivo del cargo", "propósito del rol", "misión del cargo", "sobre esta oportunidad",
        # Inglés
        "role summary", "position overview", "job summary", "about the role", 
        "mission of the role", "role purpose", "position summary", "opportunity overview",
        "about this opportunity", "job overview", "the opportunity", "role description"
    ],

    # COMENTADO MIENTRAS, YA QUE GETONBRD LO EXTRAE INDIVIDUALMENTE
    "sobre_empresa": [
        # Español
        "sobre nosotros", "acerca de nosotros", "sobre la empresa", "nuestra empresa",
        "quiénes somos", "quienes somos", "cultura organizacional", "cultura interna",
        "nuestros valores", "valores", "misión y visión", "historia", "nuestro equipo",
        "cultura de empresa", "ambiente laboral", "filosofía", "propósito",
        # Inglés
        "about us", "company culture", "our team", "our company", "who we are",
        "our values", "company values", "our mission", "our culture", "work culture",
        "company overview", "about the company", "our story", "company background",
        "work environment", "our philosophy", "company purpose"
    ],
"""