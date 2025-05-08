"""
Platform for proxy climate entity
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, CONF_TARGET_DOMAIN, CONF_SOURCE_ENTITY
from .entity import ProxyClimateEntity

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """
    Add proxy climate entity
    """
    if entry.data.get(CONF_TARGET_DOMAIN) != Platform.CLIMATE:
        _LOGGER.debug("Not a climate entity, skipping")
        return
    entity = ProxyClimateEntity(hass, entry.data[CONF_SOURCE_ENTITY])
    await entity.async_setup()
    async_add_entities([entity], True)
