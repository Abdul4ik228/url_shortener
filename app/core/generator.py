import base64
from hashlib import blake2b

from ..config import settings


def generate_short_code(original_url: str, length: int = 8) -> str:
    hasher = blake2b(digest_size=6, key=settings.SECRET_SALT.encode())
    hasher.update(original_url.encode("utf-8"))
    encoded = base64.urlsafe_b64encode(hasher.digest()).decode('ascii').rstrip('=')
    return encoded[:length]
