## Campos para Entidad JobOffer

**Identificación Básica:**

    id: identificador único interno
    source_url: URL original de la oferta
    portal_name: portal donde se encontró (GetOnBoard, LinkedIn, etc.)
    scraped_at: timestamp del scraping
    posted_date: fecha publicación original
    job_title_raw: título exacto como aparece en el portal
    job_title_normalized: título normalizado por LLM
    job_category: categoría general (Backend, Frontend, DevOps, etc.)

**Empresa:**

    company_name: nombre de la empresa
    company_type: startup/scaleup/enterprise/consultora/agencia

**Ubicación:**

    location_raw: ubicación como aparece en el portal
    country: país
    city: ciudad
    work_mode: presencial/remoto/híbrido
    remote_location_allowed: si permite trabajo desde otras ciudades/países

**Experiencia:**

    seniority_raw: seniority como aparece en el portal
    seniority_normalized: junior/semi-senior/senior/lead
    years_experience_min: años mínimos requeridos
    years_experience_max: años máximos si especificado

**Modalidad Laboral:**

    employment_type: full-time/part-time/freelance/indefinido
    contract_duration_months: duración si es temporal

**Remuneración:**

    salary_disclosed: si informa sueldo o no
    salary_raw: salario como aparece en el portal
    salary_min_clp: sueldo mínimo en pesos chilenos
    salary_max_clp: sueldo máximo en pesos chilenos
    salary_currency_original: moneda original si no es CLP
    salary_frequency: mensual/hora/proyecto
    salary_estimated_by_llm: boolean si fue estimado por LLM

**Requisitos Técnicos:**

    requirements_raw: requisitos completos como aparecen
    tech_stack_raw: tecnologías mencionadas (texto)
    skills_required: skills obligatorios extraídos por LLM (JSON array)
    skills_preferred: skills deseables extraídos por LLM (JSON array)
    english_required: boolean
    english_level: basic/conversational/fluent/native

**Descripción:**

    job_description_raw: descripción completa original
    job_summary_llm: resumen de 2-3 líneas generado por LLM
    responsibilities_llm: responsabilidades principales (JSON array)
    benefits_raw: beneficios como aparecen en el portal
    benefits_parsed_llm: beneficios parseados (JSON array)

**Procesamiento:**

    llm_processed: boolean si ya fue procesado por LLM
    llm_processed_at: timestamp del procesamiento LLM
    llm_confidence_score: 0-1 confianza del LLM en la extracción
    processing_notes: notas/errores del procesamiento

**Estado:**

    is_active: si la oferta sigue vigente
    last_checked_at: última vez que verificamos si existe
    application_deadline: fecha límite si especificada