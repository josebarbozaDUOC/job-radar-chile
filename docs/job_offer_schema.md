## Campos contemplados para Entidad JobOffer

**Identificación Básica:**

    id: identificador único interno (autoincremental)
    job_id: ID de la oferta según el portal
    source_url: URL original de la oferta
    portal_name: portal donde se encontró (GetOnBrd, LinkedIn, etc.)
    scraped_at: timestamp del scraping
    posted_date: fecha de publicación original
    job_title_raw: título exacto como aparece en el portal
    job_title_normalized: título normalizado por LLM
    job_category_raw: categoría general (programming, machine-learning-ai, etc)
    job_role: rol o puesto de trabajo (Backend, Frontend, DevOps, etc.)

**Empresa:**

    company_name_raw: nombre de la empresa
    company_url_raw: URL pública de la empresa
    company_type: startup/scaleup/enterprise/consultora/agencia
    company_description_raw: descripción de la empresa

**Ubicación:**

    location_work_mode_raw: ubicación y modo de trabajo
    location_raw: ubicación como aparece en el portal
    country: país
    city: ciudad
    work_mode_raw: presencial/remoto/híbrido
    remote_location_allowed: si permite trabajo desde otras ciudades/países

**Experiencia:**

    seniority_raw: seniority como aparece en el portal
    seniority_normalized: junior/semi-senior/senior/lead
    years_experience_min: años mínimos requeridos
    years_experience_max: años máximos si especificado

**Modalidad Laboral:**

    employment_type_raw: full-time/part-time/freelance/indefinido
    contract_duration_months: duración en meses si es contrato temporal

**Remuneración:**

    salary_disclosed: si informa sueldo o no (booleano)
    salary_raw: salario como aparece en el portal
    salary_min_raw: sueldo mínimo en moneda original
    salary_max_raw: sueldo máximo en moneda original
    salary_currency_raw: moneda original si no es CLP (ej. USD)
    salary_unit_raw: unidad de sueldo (MONTH/HOUR/PROJECT)
    salary_type_raw: tipo de sueldo (neto (gross), líquido (net))
    salary_frequency: frecuencia de pago si aplica
    salary_min_clp: sueldo mínimo en pesos chilenos
    salary_max_clp: sueldo máximo en pesos chilenos
    salary_min_usd: sueldo mínimo en dólares
    salary_max_usd: sueldo máximo en dólares
    salary_min_market: sueldo mínimo promedio aprox en el mercado
    salary_max_market: sueldo máximo promedio aprox en el mercado
    salary_estimated_by_llm: booleano si fue estimado por LLM

**Requisitos Técnicos:**

    requirements_raw: requisitos completos como aparecen en el portal
    tech_stack_raw: tecnologías mencionadas (texto libre)
    main_techs: lista de principales tecnologías
    skills_required: habilidades obligatorias extraídas por LLM (JSON array)
    skills_preferred: habilidades deseables extraídas por LLM (JSON array)
    english_required: booleano si requiere inglés
    english_level: basic/conversational/fluent/native

**Descripción:**

    job_description_raw: descripción completa original
    sections_raw: lista de secciones con título y contenido (JSON array en texto)
    job_summary_llm: resumen generado por LLM
    responsibilities_llm: responsabilidades principales (JSON array)
    benefits_raw: beneficios como aparecen en el portal
    benefits_parsed_llm: beneficios parseados (JSON array)
    perks: lista de perks (JSON array en texto)

**Procesamiento:**

    llm_processed: booleano si ya fue procesado por LLM
    llm_processed_at: timestamp del procesamiento por LLM
    llm_confidence_score: confianza del LLM en la extracción (de 0.0 a 1.0)
    processing_notes: notas o errores generados durante el procesamiento

**Estado:**

    is_active: si la oferta sigue vigente
    last_checked_at: última vez que verificamos si aún está publicada
    applications_raw: número de solicitantes al empleo
    application_deadline: fecha límite para postular si está especificada
    reply_time_raw: tiempo estimado de respuesta
    remote_policy_raw: detalle de política de trabajo remoto
    apply_url: URL directa para postular a la oferta