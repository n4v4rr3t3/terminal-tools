# Notion Pipeline CLI

Utilidad de terminal en Python para agregar oportunidades al **Pipeline de Oportunidades** de Notion sin cargar filas manualmente.

La idea central es simple:

> Los argumentos de terminal representan campos del CRM.

```bash
python notion_pipeline.py "https://instagram.com/posiblecliente" \
  --canal PyME \
  --nota "Vende por WhatsApp" \
  --prioridad Alta
```

Eso crea una oportunidad en Notion usando la URL como `Fuente` y completando las columnas correspondientes.

## Instalación

Recomendado: Python 3.11+.

```bash
git clone https://github.com/n4v4rr3t3/terminal-tools.git
cd terminal-tools/notions-utilities
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Instalá dependencias:

```bash
pip install -r requirements.txt
```

## Configurar Notion

1. Creá una integración interna en Notion.
2. Dale acceso al espacio donde vive `Pipeline de Oportunidades`.
3. Copiá `.env.example` a `.env`.
4. Pegá el token en `NOTION_TOKEN`.

```env
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATA_SOURCE_ID=e9e9a200-f68f-4bba-bb94-84526fcbdf55
NOTION_VERSION=2026-03-11
```

Nunca subas `.env` a Git.

## Uso básico

### Instagram

```bash
python notion_pipeline.py "https://instagram.com/posiblecliente"
```

### Sobrescribir campos

```bash
python notion_pipeline.py "https://instagram.com/posiblecliente" \
  --prioridad Alta \
  --nota "12k seguidores. Catálogo por historias. Cierra todo por WhatsApp."
```

### Workana

```bash
python notion_pipeline.py "https://www.workana.com/job/ejemplo" \
  --dinero 500 \
  --moneda USD \
  --dificultad Media
```

### Freelancer

```bash
python notion_pipeline.py "https://www.freelancer.com/projects/ejemplo" \
  --estado Analizando
```

### Nombre manual

```bash
python notion_pipeline.py "https://instagram.com/meteor_seeds" \
  --nombre "Meteor Seeds"
```

### Próxima acción

```bash
python notion_pipeline.py "https://instagram.com/cliente" \
  --proxima-accion "Preparar demo catálogo → WhatsApp"
```

### Marcar demo rápida

```bash
python notion_pipeline.py "https://instagram.com/cliente" --demo-rapida true
```

## Parámetros disponibles

| CLI | Columna Notion |
|---|---|
| `--nombre` | Oportunidad |
| URL posicional | Fuente |
| `--canal` | Canal |
| `--estado` | Estado |
| `--nota` / `--notas` | Notas |
| `--prioridad` | Prioridad |
| `--dificultad` | Dificultad |
| `--competencia` | Competencia |
| `--dinero` | Dinero potencial |
| `--moneda` | Moneda |
| `--tecnologia` | Tecnología |
| `--proxima-accion` | Próxima acción |
| `--deadline` | Deadline |
| `--demo-rapida` | Demo rápida |
| `--recurrente` | Recurrente |

Ver ayuda:

```bash
python notion_pipeline.py --help
```

## Detección automática

La configuración editable vive en `config.py`.

```python
DETECCION_AUTOMATICA = [
    {
        "nombre": "Instagram",
        "contiene": ["instagram.com"],
        "valores": {
            "canal": "PyME",
            "prioridad": "Media",
            "competencia": "Baja",
        },
    },
]
```

Las reglas actuales detectan:

- Instagram
- Google Maps
- Workana
- Freelancer
- Facebook

Para agregar otra fuente, agregás otra regla. No hace falta tocar el resto de la lógica.

Ejemplo para TikTok:

```python
{
    "nombre": "TikTok",
    "contiene": ["tiktok.com"],
    "valores": {
        "canal": "PyME",
        "prioridad": "Media",
        "competencia": "Media",
        "proxima_accion": "Revisar perfil y detectar proceso de venta.",
    },
},
```

## Precedencia

Los valores se resuelven así:

```text
DEFAULTS
   ↓
DETECCION_AUTOMATICA
   ↓
ARGUMENTOS ESCRITOS POR VOS
```

Los argumentos explícitos siempre ganan.

```bash
python notion_pipeline.py "https://instagram.com/x" --prioridad Alta
```

Aunque Instagram tenga `Media` por defecto, el resultado será `Alta`.

## Evitar duplicados

La herramienta consulta Notion antes de crear la fila y busca una `Fuente` con la misma URL.

Para forzar un duplicado:

```bash
python notion_pipeline.py "https://instagram.com/x" --permitir-duplicado
```

## Dry run

Para ver qué se enviaría a Notion sin modificar nada:

```bash
python notion_pipeline.py "https://instagram.com/x" --nota "prueba" --dry-run
```

## Arquitectura

```text
notions-utilities/
├── notion_pipeline.py   # CLI / argparse
├── config.py            # configuración y detección automática
├── notion_client.py     # comunicación con Notion
├── utils.py             # funciones auxiliares
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

La separación es intencional:

- `notion_pipeline.py`: argumentos, precedencia y salida de terminal.
- `config.py`: lugar principal para modificar comportamiento.
- `notion_client.py`: llamadas HTTP a la API de Notion.
- `utils.py`: funciones pequeñas y reutilizables.

## Agregar una columna nueva

Si agregás una columna de texto `Nicho` en Notion:

En `config.py`:

```python
"nicho": {
    "notion_name": "Nicho",
    "type": "rich_text",
},
```

En `notion_pipeline.py`:

```python
parser.add_argument("--nicho")
```

y en el diccionario `argumentos`:

```python
"nicho": args.nicho,
```

Tipos soportados actualmente:

- `title`
- `rich_text`
- `url`
- `select`
- `number`
- `checkbox`
- `date`

## Próximas mejoras posibles

La estructura permite evolucionar hacia comandos como:

```bash
python notion_pipeline.py list
python notion_pipeline.py followup
python notion_pipeline.py stats
python notion_pipeline.py update <id>
```

La primera versión tiene una misión concreta: **copiar una URL mientras prospectás, ejecutar un comando y tener la oportunidad cargada en Notion en segundos.**
