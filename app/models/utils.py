from datetime import datetime
from uuid import uuid4
from urllib.parse import urlparse


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())


def is_domain(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.path == '' or parsed_url.path == '/'


def clean_url(url: str) -> str:
    return url.encode().decode().replace(" ", "").rstrip("/")
