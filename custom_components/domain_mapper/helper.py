"""
Helper functions
"""

from .const import _LOGGER

def get_domain(entity_id: str, index: int = 0) -> str | None:
    """
    Get domain from entity id
    """
    try:
        return entity_id.split(".")[index]
    except IndexError:
        _LOGGER.error("Invalid entity id: %s", entity_id)
        return None
