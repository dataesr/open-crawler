from datetime import datetime, timezone, timedelta

CONTENT_TYPE_MAP: dict[str, str] = {
    "html": "text/html",
    "json": "application/json",
    # ... you can extend this mapping as needed
}


def assume_content_type(input_string: str) -> str:
    """
    Determines the content type based on the suffix of the given input string.

    Args:
    - input_string (str): The string to determine content type for.

    Returns:
    - str: The associated content type. If no match is found, it defaults to
           'application/octet-stream' as a generic binary format.
    """
    suffix = input_string.rsplit(".", 1)[-1].lower()
    return CONTENT_TYPE_MAP.get(suffix, "application/octet-stream")


def french_datetime() -> datetime:
    return datetime.now(timezone(timedelta(hours=2)))
