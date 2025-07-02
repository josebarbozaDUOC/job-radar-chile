# job-radar-chile
Herramienta de análisis del mercado laboral tech chileno. Web scraping en tiempo real + insights con IA para rastrear demanda de skills, tendencias salariales y patrones de contratación.

## Funcionalidades
**Completado:**
- Web scrap a portal de empleos (getonbrd.com)
- Filtra todas las ofertas de empleos del último mes
- Guarda el listado (de urls) en SQLite

**Pendiente:**
- Refactor a main (separar database, config, scrap_getonbrd)
- Extraer y guardar data de cada oferta de empleo
- Probar con modelo LLM en ollama para transformar data
- Crear frontend tipo dashboard
- Expandir scrap a más portales de empleos
- UI para información del usuario, así hacer match con ofertas de empleos, crear roadmap para usuario, etc


**Console:**

    Scrapeando categoría: programming
    URL: https://www.getonbrd.com/jobs/programming
    Status: 200
    Trabajos encontrados totales: 461
    Trabajos encontrados filtrados: 200
    Guardado: data/raw/job_urls.txt
    Insertados 200 registros en DB

## License
This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for more information.

For commercial use or alternative licensing, please contact the author.