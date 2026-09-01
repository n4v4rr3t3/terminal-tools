from urllib.parse import urlparse, unquote


def normalizar_url(url: str) -> str:
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url.rstrip("/")


def detectar_origen(url: str, reglas: list[dict]) -> dict:
    url_lower = url.lower()

    for regla in reglas:
        if any(fragmento.lower() in url_lower for fragmento in regla["contiene"]):
            return dict(regla.get("valores", {}))

    return {}


def nombre_desde_url(url: str) -> str:
    """Intenta generar un título humano y predecible sin hacer scraping."""
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    path = unquote(parsed.path).strip("/")

    if "instagram.com" in host and path:
        usuario = path.split("/")[0]
        return f"Instagram — @{usuario}"

    if "workana.com" in host:
        slug = path.split("/")[-1] if path else "oportunidad"
        return f"Workana — {slug.replace('-', ' ').strip().title()}"

    if "freelancer.com" in host:
        slug = path.split("/")[-1] if path else "oportunidad"
        return f"Freelancer — {slug.replace('-', ' ').strip().title()}"

    if path:
        primer_segmento = path.split("/")[0]
        return f"{host} — {primer_segmento}"

    return host or "Nueva oportunidad"


def parse_bool(value: str) -> bool:
    valor = value.strip().lower()

    verdaderos = {"1", "true", "si", "sí", "yes", "y"}
    falsos = {"0", "false", "no", "n"}

    if valor in verdaderos:
        return True
    if valor in falsos:
        return False

    raise ValueError(
        f"No pude interpretar {value!r} como booleano. Usa true/false o si/no."
    )
