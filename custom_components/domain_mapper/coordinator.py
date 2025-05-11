""""
State tracking coordinator
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State, Event, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    _LOGGER,
    CONF_SOURCE_DOMAIN,
    CONF_TARGET_DOMAIN,
    CONF_SOURCE_ENTITY,
    PROPERTY_NAME,
)

class StateTrackingCoordinator(DataUpdateCoordinator):
    """
    Coordinates state tracking and updates.
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__(hass, _LOGGER, name="StateTracker")
        self.hass = hass
        self.entry = entry
        self.source_domain = entry.data.get(CONF_SOURCE_DOMAIN)
        self.target_domain = entry.data.get(CONF_TARGET_DOMAIN)
        self.entity_id = entry.data.get(CONF_SOURCE_ENTITY)
        self.entity_name = entry.data.get(PROPERTY_NAME)

        # Register an event for status tracking
        async_track_state_change_event(hass, [self.entity_id], self._handle_state_change)

    async def _async_update_data(self) -> State | None:
        return self.hass.states.get(self.entity_id)

    @callback
    def _handle_state_change(self, event: Event) -> None:
        new_state = event.data.get("new_state")
        self.async_set_updated_data(new_state)
