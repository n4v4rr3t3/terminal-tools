"""
Toda la configuración editable de la herramienta está acá.

Idea:
- Si mañana aparece otro canal, agregás una regla a DETECCION_AUTOMATICA.
- Si querés cambiar los valores por defecto, editás DEFAULTS.
- Si agregás una columna compatible en Notion, la mapeás en CLI_TO_NOTION.
"""

DEFAULT_DATA_SOURCE_ID = "e9e9a200-f68f-4bba-bb94-84526fcbdf55"

DEFAULTS = {
    "estado": "Detectada",
    "prioridad": "Media",
    "competencia": "Desconocida",
    "moneda": "Desconocido",
    "demo_rapida": False,
    "recurrente": False,
}

CLI_TO_NOTION = {
    "nombre": {"notion_name": "Oportunidad", "type": "title"},
    "fuente": {"notion_name": "Fuente", "type": "url"},
    "canal": {"notion_name": "Canal", "type": "select"},
    "estado": {"notion_name": "Estado", "type": "select"},
    "notas": {"notion_name": "Notas", "type": "rich_text"},
    "prioridad": {"notion_name": "Prioridad", "type": "select"},
    "dificultad": {"notion_name": "Dificultad", "type": "select"},
    "competencia": {"notion_name": "Competencia", "type": "select"},
    "dinero": {"notion_name": "Dinero potencial", "type": "number"},
    "moneda": {"notion_name": "Moneda", "type": "select"},
    "tecnologia": {"notion_name": "Tecnología", "type": "select"},
    "proxima_accion": {"notion_name": "Próxima acción", "type": "rich_text"},
    "deadline": {"notion_name": "Deadline", "type": "date"},
    "demo_rapida": {"notion_name": "Demo rápida", "type": "checkbox"},
    "recurrente": {"notion_name": "Recurrente", "type": "checkbox"},
}

SELECT_OPTIONS = {
    "canal": ["Cliente publicado", "PyME", "White-label", "KIT 4.0", "Estado", "Hackathon/Bounty"],
    "estado": ["Detectada", "Analizando", "Demo", "Propuesta enviada", "Negociando", "Ganada", "Perdida", "lo vio pero no respondio"],
    "prioridad": ["Alta", "Media", "Baja"],
    "dificultad": ["Baja", "Media", "Alta"],
    "competencia": ["Baja", "Media", "Alta", "Desconocida"],
    "moneda": ["USD", "ARS", "Premio", "Desconocido"],
    "tecnologia": ["Python", "React", "Next.js", "JavaScript", "TypeScript", "WhatsApp", "IA", "Web3", "Firebase", "Supabase"],
}

DETECCION_AUTOMATICA = [
    {
        "nombre": "Instagram",
        "contiene": ["instagram.com"],
        "valores": {
            "canal": "PyME",
            "prioridad": "Media",
            "competencia": "Baja",
            "proxima_accion": "Revisar perfil, detectar problema comercial y contactar.",
        },
    },
    {
        "nombre": "Google Maps",
        "contiene": ["google.com/maps", "maps.google.com", "maps.app.goo.gl"],
        "valores": {
            "canal": "PyME",
            "prioridad": "Media",
            "competencia": "Baja",
            "proxima_accion": "Revisar negocio, encontrar Instagram/web/WhatsApp y evaluar contacto.",
        },
    },
    {
        "nombre": "Workana",
        "contiene": ["workana.com"],
        "valores": {
            "canal": "Cliente publicado",
            "prioridad": "Alta",
            "competencia": "Media",
            "proxima_accion": "Evaluar publicación y decidir propuesta/demo.",
        },
    },
    {
        "nombre": "Freelancer",
        "contiene": ["freelancer.com"],
        "valores": {
            "canal": "Cliente publicado",
            "prioridad": "Alta",
            "competencia": "Alta",
            "proxima_accion": "Evaluar publicación y decidir si gastar bid.",
        },
    },
    {
        "nombre": "Facebook",
        "contiene": ["facebook.com", "fb.com"],
        "valores": {
            "canal": "PyME",
            "prioridad": "Media",
            "competencia": "Media",
            "proxima_accion": "Revisar perfil/grupo y evaluar contacto.",
        },
    },
]
