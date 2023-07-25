def clean_url(url: str) -> str:
    return url.encode().decode().replace(" ", "").rstrip("/")
