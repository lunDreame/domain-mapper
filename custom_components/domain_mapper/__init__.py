"""
Domain mapper component setup
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN

PLATFORMS = [
    Platform.CLIMATE,
    Platform.BINARY_SENSOR
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Setup the domain mapper platforms
    """
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Unload the domain mapper platforms
    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
