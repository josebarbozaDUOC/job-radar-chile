# job-radar-chile

Sistema de análisis del mercado laboral tech chileno mediante web scraping y procesamiento de datos.

Herramienta que automatiza la recolección de ofertas de trabajo desde portales chilenos para generar insights sobre el mercado tecnológico local.

## Estado Actual
### Implementado
- Scraping de ofertas desde GetOnBoard
- Filtrado por fecha (últimos 30 días)
- Almacenamiento en SQLite
- Arquitectura modular
- Extracción de datos detallados de ofertas (GetOnBoard)
- Doble validación de fecha de publicación
- Refinar scraping detallado (formatos)

### En Desarrollo
- Rediseñar esquema [job_offers](docs/job_offer_schema.md)
- Separar las secciones del cuerpo de publicación (sections_raw)
- Reporte simple en excel
- Migrar a postgres e implementar ORM
- Implementar Docker compose
- Procesamiento con LLM local
- Dashboard de visualización


## Tecnologías
- Python 3.x
- BeautifulSoup4
- SQLite
- Requests


## Docs
- Ver [Esquema de datos para ofertas](docs/job_offer_schema.md)
- Ver [Portales de ofertas de empleos](docs/employment_portals.md)
- Ver [Estructura de archivos propuesta](docs/structure.md)

## License
This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for more information.

For commercial use or alternative licensing, please contact the author.