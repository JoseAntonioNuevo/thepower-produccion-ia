"""Cliente SigV4: firma exactamente los bytes que enviará, con credenciales temporales."""

from urllib.parse import urlsplit

from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


def validar_url(url, region):
    """No enviar credenciales firmadas a dominios, puertos o rutas arbitrarios."""
    parsed = urlsplit(url)
    suffix = f".execute-api.{region}.amazonaws.com"
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or not parsed.hostname.endswith(suffix)
        or parsed.port not in (None, 443)
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path != "/clasificar"
    ):
        raise ValueError("La URL debe ser la ruta HTTPS /clasificar de la HTTP API de esta región")
    api_id = parsed.hostname[: -len(suffix)]
    if not api_id.isalnum() or not 5 <= len(api_id) <= 20:
        raise ValueError("Identificador de API inválido")


def signed_headers(url, body: bytes, region, credentials):
    """Los headers devueltos son secretos de transporte: no imprimirlos ni guardarlos."""
    validar_url(url, region)
    if credentials is None or not credentials.token:
        raise ValueError("La práctica requiere credenciales temporales con session token")
    req = AWSRequest(
        method="POST", url=url, data=body, headers={"Content-Type": "application/json"}
    )
    SigV4Auth(credentials, "execute-api", region).add_auth(req)
    return dict(req.headers.items())
