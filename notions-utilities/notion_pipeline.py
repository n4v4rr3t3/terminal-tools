#!/usr/bin/env python3
"""
CLI simple para agregar oportunidades al Pipeline de Oportunidades de Notion.

Ejemplos:
    python notion_pipeline.py "https://instagram.com/cliente"
    python notion_pipeline.py "https://instagram.com/cliente" --canal PyME --nota "Vende por WhatsApp"
    python notion_pipeline.py "https://www.workana.com/job/..." --estado "Analizando" --prioridad Alta
"""

import argparse
import sys

from config import (
    DEFAULTS,
    CLI_TO_NOTION,
    DETECCION_AUTOMATICA,
    SELECT_OPTIONS,
)
from notion_client import NotionPipelineClient
from utils import (
    detectar_origen,
    nombre_desde_url,
    normalizar_url,
    parse_bool,
)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Agregar oportunidades al Pipeline de Oportunidades de Notion."
    )

    parser.add_argument(
        "url",
        help="URL del prospecto/oportunidad. Ej: https://instagram.com/posiblecliente",
    )

    parser.add_argument(
        "--nombre",
        help="Nombre de la oportunidad. Si se omite se intenta inferir desde la URL.",
    )
    parser.add_argument("--canal", help="Columna Canal de Notion.")
    parser.add_argument("--estado", help="Estado de la oportunidad.")
    parser.add_argument("--nota", "--notas", dest="notas", help="Notas sobre el prospecto.")
    parser.add_argument("--prioridad", help="Prioridad: Alta, Media o Baja.")
    parser.add_argument("--dificultad", help="Dificultad: Baja, Media o Alta.")
    parser.add_argument("--competencia", help="Competencia: Baja, Media, Alta o Desconocida.")
    parser.add_argument("--dinero", type=float, help="Dinero potencial.")
    parser.add_argument("--moneda", help="Moneda: USD, ARS, Premio o Desconocido.")
    parser.add_argument("--tecnologia", help="Tecnología principal.")
    parser.add_argument("--proxima-accion", dest="proxima_accion", help="Próxima acción.")
    parser.add_argument("--deadline", help="Fecha YYYY-MM-DD.")
    parser.add_argument("--demo-rapida", type=parse_bool, help="true/false.")
    parser.add_argument("--recurrente", type=parse_bool, help="true/false.")

    parser.add_argument(
        "--sin-deteccion",
        action="store_true",
        help="Desactiva la detección automática basada en la URL.",
    )
    parser.add_argument(
        "--permitir-duplicado",
        action="store_true",
        help="Permite crear otra fila aunque la misma URL ya exista.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra qué se enviaría a Notion sin crear la fila.",
    )
    parser.add_argument(
        "--mostrar-config",
        action="store_true",
        help="Muestra defaults y reglas de detección cargadas.",
    )

    return parser


def validar_select(nombre_cli: str, valor: str | None) -> None:
    if valor is None:
        return

    opciones = SELECT_OPTIONS.get(nombre_cli)
    if opciones and valor not in opciones:
        opciones_texto = ", ".join(opciones)
        raise ValueError(
            f"Valor inválido para --{nombre_cli.replace('_', '-')}: {valor!r}. "
            f"Opciones: {opciones_texto}"
        )


def resolver_campos(args: argparse.Namespace) -> dict:
    url = normalizar_url(args.url)

    campos = dict(DEFAULTS)

    if not args.sin_deteccion:
        detectado = detectar_origen(url, DETECCION_AUTOMATICA)
        campos.update({k: v for k, v in detectado.items() if v is not None})

    argumentos = {
        "nombre": args.nombre,
        "canal": args.canal,
        "estado": args.estado,
        "notas": args.notas,
        "prioridad": args.prioridad,
        "dificultad": args.dificultad,
        "competencia": args.competencia,
        "dinero": args.dinero,
        "moneda": args.moneda,
        "tecnologia": args.tecnologia,
        "proxima_accion": args.proxima_accion,
        "deadline": args.deadline,
        "demo_rapida": args.demo_rapida,
        "recurrente": args.recurrente,
    }

    # Los argumentos explícitos siempre ganan sobre detección y defaults.
    for clave, valor in argumentos.items():
        if valor is not None:
            campos[clave] = valor

    if not campos.get("nombre"):
        campos["nombre"] = nombre_desde_url(url)

    campos["fuente"] = url

    for clave in SELECT_OPTIONS:
        validar_select(clave, campos.get(clave))

    return campos


def main() -> int:
    parser = construir_parser()
    args = parser.parse_args()

    if args.mostrar_config:
        print("DEFAULTS:")
        for k, v in DEFAULTS.items():
            print(f"  {k}: {v}")
        print("\nDETECCION_AUTOMATICA:")
        for regla in DETECCION_AUTOMATICA:
            print(f"  {regla}")
        return 0

    try:
        campos = resolver_campos(args)
        cliente = NotionPipelineClient()

        if not args.permitir_duplicado and cliente.existe_fuente(campos["fuente"]):
            print("⚠️  Ya existe una oportunidad con esta URL:")
            print(f"   {campos['fuente']}")
            print("   Usa --permitir-duplicado si realmente quieres crear otra.")
            return 2

        propiedades = cliente.construir_propiedades(campos, CLI_TO_NOTION)

        if args.dry_run:
            print("DRY RUN — no se enviará nada a Notion.\n")
            print(json_pretty({
                "campos_resueltos": campos,
                "properties": propiedades,
            }))
            return 0

        resultado = cliente.crear_oportunidad(propiedades)

        print("✅ Oportunidad agregada a Notion")
        print(f"   Nombre: {campos['nombre']}")
        print(f"   Fuente: {campos['fuente']}")
        if campos.get("canal"):
            print(f"   Canal: {campos['canal']}")
        if campos.get("estado"):
            print(f"   Estado: {campos['estado']}")
        if resultado.get("url"):
            print(f"   Notion: {resultado['url']}")

        return 0

    except KeyboardInterrupt:
        print("\nCancelado.")
        return 130
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        return 1


def json_pretty(data: dict) -> str:
    import json
    return json.dumps(data, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    raise SystemExit(main())
