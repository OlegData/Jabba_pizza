import os
import time
import structlog
import jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-super-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_SECONDS = 3600 * 48
BASE_DIR = os.getenv("CERTS_DIR", "/home/oleg/projects/python/jabbas_pizza/certs")

logger = structlog.get_logger()


def _read_binary_file(path: str) -> bytes:
    with open(path, "rb") as file:
        return file.read()


def generate_token(email, first_name, last_name) -> str:
    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "exp": int(time.time()) + JWT_EXPIRES_SECONDS,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def load_credentials():
    cert_file = os.path.join(BASE_DIR, "accounts.crt")
    key_file = os.path.join(BASE_DIR, "accounts.key")
    try:
        server_key, server_cert = tuple(_read_binary_file(path) for path in (key_file, cert_file))
    except FileNotFoundError as err:
        logger.error(
            "Certificate files not found",
            error=str(err),
            cert_file=cert_file,
            key_file=key_file,
        )
        raise
    return [(server_key, server_cert)]
