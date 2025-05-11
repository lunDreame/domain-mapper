"""
Platform for proxy climate entity
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER, DOMAIN
from .coordinator import StateTrackingCoordinator
from .entity import ProxyClimateEntity

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """
    Add proxy climate entity
    """
    coordinator: StateTrackingCoordinator = hass.data[DOMAIN][entry.entry_id]

    if coordinator.target_domain == Platform.CLIMATE.value:
        entity = ProxyClimateEntity(coordinator)
        async_add_entities([entity])
