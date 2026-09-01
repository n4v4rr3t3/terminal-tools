import os
from typing import Any

import requests
from dotenv import load_dotenv

from config import DEFAULT_DATA_SOURCE_ID

load_dotenv()


class NotionPipelineClient:
    API_BASE = "https://api.notion.com/v1"

    def __init__(self) -> None:
        self.token = os.getenv("NOTION_TOKEN")
        self.data_source_id = os.getenv(
            "NOTION_DATA_SOURCE_ID",
            DEFAULT_DATA_SOURCE_ID,
        )
        self.notion_version = os.getenv(
            "NOTION_VERSION",
            "2026-03-11",
        )

        if not self.token:
            raise RuntimeError(
                "Falta NOTION_TOKEN. Copiá .env.example a .env y agregá tu integration token."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        url = f"{self.API_BASE}{path}"
        response = self.session.request(method, url, timeout=30, **kwargs)

        if not response.ok:
            try:
                detalle = response.json()
            except Exception:
                detalle = response.text

            raise RuntimeError(
                f"Notion API respondió {response.status_code}: {detalle}"
            )

        return response.json()

    def existe_fuente(self, fuente: str) -> bool:
        """Evita duplicados exactos por URL usando la columna Fuente."""
        payload = {
            "filter": {
                "property": "Fuente",
                "url": {
                    "equals": fuente,
                },
            },
            "page_size": 1,
        }

        data = self._request(
            "POST",
            f"/data_sources/{self.data_source_id}/query",
            json=payload,
        )

        return bool(data.get("results"))

    def crear_oportunidad(self, properties: dict) -> dict:
        payload = {
            "parent": {
                "type": "data_source_id",
                "data_source_id": self.data_source_id,
            },
            "properties": properties,
        }

        return self._request("POST", "/pages", json=payload)

    def construir_propiedades(self, campos: dict, mapping: dict) -> dict:
        properties = {}

        for clave_cli, definicion in mapping.items():
            if clave_cli not in campos:
                continue

            valor = campos[clave_cli]
            if valor is None:
                continue

            nombre_notion = definicion["notion_name"]
            tipo = definicion["type"]

            properties[nombre_notion] = self._a_propiedad_notion(tipo, valor)

        return properties

    @staticmethod
    def _a_propiedad_notion(tipo: str, valor: Any) -> dict:
        if tipo == "title":
            return {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": str(valor)},
                    }
                ]
            }

        if tipo == "rich_text":
            return {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": str(valor)},
                    }
                ]
            }

        if tipo == "url":
            return {"url": str(valor)}

        if tipo == "select":
            return {"select": {"name": str(valor)}}

        if tipo == "number":
            return {"number": float(valor)}

        if tipo == "checkbox":
            return {"checkbox": bool(valor)}

        if tipo == "date":
            return {"date": {"start": str(valor)}}

        raise ValueError(f"Tipo de propiedad no soportado: {tipo}")
