from uuid import uuid4

__all__ = ("get_uuid")


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())