## Campos para Entidad JobOffer

**Identificación Básica:**

    id: identificador único interno
    source_url: URL original de la oferta
    portal_name: portal donde se encontró (GetOnBoard, LinkedIn, etc.)
    scraped_at: timestamp del scraping
    job_title_raw: título exacto como aparece en el portal
    job_title_normalized: título normalizado por LLM
    job_category: categoría general (Backend, Frontend, DevOps, etc.)

**Empresa:**

    company_name: nombre de la empresa
    company_size: tamaño empresa (startup, pyme, enterprise, etc.)
    company_industry: rubro/industria de la empresa

**Ubicación:**

    country: país
    region: región/estado
    city: ciudad
    address: dirección específica si disponible
    work_mode: presencial/remoto/híbrido
    hybrid_days: días presenciales si es híbrido
    timezone_requirement: restricción horaria si aplica

**Experiencia:**

    experience_level: junior/semi-senior/senior/lead
    years_experience_min: años mínimos requeridos
    years_experience_max: años máximos si especificado
    education_required: educación requerida
    is_entry_level: si acepta sin experiencia

**Modalidad Laboral:**

    employment_type: full-time/part-time/freelance/contrato
    schedule_flexibility: horario fijo/flexible
    contract_duration: duración si es temporal

**Remuneración:**

    salary_disclosed: si informa sueldo o no
    salary_min_clp: sueldo mínimo en pesos chilenos
    salary_max_clp: sueldo máximo en pesos chilenos
    salary_currency_original: moneda original si no es CLP
    salary_includes_benefits: si incluye beneficios en el monto
    salary_estimated_clp: sueldo estimado por LLM si no informado

**Requisitos Técnicos:**

    required_skills: array de skills obligatorios
    preferred_skills: array de skills deseables
    programming_languages: lenguajes específicos requeridos
    frameworks_libraries: frameworks/librerías específicas
    databases: bases de datos requeridas
    cloud_platforms: plataformas cloud requeridas
    certifications: certificaciones requeridas

**Descripción:**

    job_description_raw: descripción completa original
    job_summary: resumen generado por LLM
    responsibilities: responsabilidades principales
    benefits: beneficios ofrecidos
    application_instructions: instrucciones para postular

**Metadata:**

    is_active: si la oferta sigue vigente
    application_deadline: fecha límite si especificada
    posted_date: fecha publicación original
    updated_at: última actualización nuestra