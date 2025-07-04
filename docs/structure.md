## Estructura de archivos del proyecto

```
job-radar-chile/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                 # Orquestador principal
│   ├── config.py               # Todas las constantes y configuración
│   ├── database.py             # Funciones de DB (SQLite)
│   ├── requirements.txt        # Dependencias backend
│   │
│   ├── scrapers/               # Carpeta para todos los scrapers
│   │   ├── __init__.py
│   │   └── getonbrd.py         # Scraper específico de GetOnBoard
│   │
│   └── utils/
│       ├── __init__.py
│       └── date_utils.py       # Funciones de fecha compartidas
│
├── data/                       # Git ignorado
│   ├── jobs.db                 # Base de datos SQLite
│   └── raw/                    # HTMLs y json crudos para debug
│       ├── soup.txt
│       ├── job_items.txt
│       └── job_urls.txt
│
├── docs/
│   ├── employment_portals.md   # Lista de portales de ofertas de empleos
│   ├── job_offer_schema.md     # Esquema de datos de ofertas de empleos
│   ├── structure.md            # Estructura de archivos del proyecto
│   ├── architecture.md         # Explicación de la arquitectura
│   └── api_notes.md            # Notas sobre las APIs/sitios scrapeados
│
├── frontend/                   # Vacío por ahora
│   └── 
│
├── tests/                      # Vacío por ahora (pytest)
│   ├── __init__.py
│   └── 
│
├── .gitignore
├── LICENSE
└── README.md
```