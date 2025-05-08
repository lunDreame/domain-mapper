"""
Proxy entity for domain_mapper
"""

from homeassistant.core import HomeAssistant, Event
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.components.water_heater.const import STATE_GAS
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import Platform, STATE_ON, STATE_OFF, UnitOfTemperature

from .const import _LOGGER, DOMAIN
from .helper import get_domain

def create_proxy_entity(
    hass: HomeAssistant, source_entity_id: str, target_domain: str
):
    if target_domain == Platform.CLIMATE:
        return ProxyClimateEntity(hass, source_entity_id)
    elif target_domain == Platform.BINARY_SENSOR:
        return ProxyOccupancySensor(hass, source_entity_id)
    return None


class ProxyBaseEntity:
    """
    Base class for proxy entities
    """

    def __init__(self, hass: HomeAssistant, source_entity_id: str) -> None:
        self.hass = hass
        self._source_entity_id = source_entity_id
        self._unsub = None

    async def async_setup(self) -> None:
        """
        Register for state changes
        """
        _LOGGER.debug("Setting up proxy for: %s", self._source_entity_id)
        self._unsub = async_track_state_change_event(
            self.hass, [self._source_entity_id], self._handle_event
        )

    async def async_unload(self) -> None:
        """
        Unregister state listener
        """
        if self._unsub:
            _LOGGER.debug("Unloading proxy for: %s", self._source_entity_id)
            self._unsub()
            self._unsub = None

    async def _handle_event(self, event: Event) -> None:
        self.async_write_ha_state()

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def snake_to_title_case(self) -> str:
        # water_heater -> Water Heater
        words = get_domain(self._source_entity_id).split('_')
        return ' '.join(word.capitalize() for word in words)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, get_domain(self._source_entity_id))},
            name=f"Map {self.snake_to_title_case}",
            manufacturer="DomainMapper",
            model="Virtual Proxy Entity"
        )


class ProxyClimateEntity(ProxyBaseEntity, ClimateEntity):
    HVAC_MODE_MAP = {
        STATE_GAS: HVACMode.HEAT,
        STATE_OFF: HVACMode.OFF
    }

    def __init__(self, hass: HomeAssistant, source_entity_id: str) -> None:
        super().__init__(hass, source_entity_id)
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE |
            ClimateEntityFeature.TURN_OFF |
            ClimateEntityFeature.TURN_ON
        )

    @property
    def name(self) -> str:
        return f"{get_domain(self._source_entity_id, 1)}"

    @property
    def unique_id(self) -> str:
        return f"{get_domain(self._source_entity_id, 1)}_cli"

    @property
    def hvac_mode(self) -> HVACMode:
        state = self.hass.states.get(self._source_entity_id).state
        _LOGGER.debug("Source entity state: %s", state)
        return self.HVAC_MODE_MAP.get(state)

    @property
    def target_temperature(self) -> float | None:
        state = self.hass.states.get(self._source_entity_id)
        return state.attributes.get("temperature")

    @property
    def current_temperature(self) -> float | None:
        state = self.hass.states.get(self._source_entity_id)
        return state.attributes.get("current_temperature")

    @property
    def extra_state_attributes(self) -> dict:
        return {"source_entity": self._source_entity_id}

    @property
    def icon(self) -> str:
        return "mdi:thermostat"


class ProxyOccupancySensor(ProxyBaseEntity, BinarySensorEntity):

    def __init__(self, hass: HomeAssistant, source_entity_id: str) -> None:
        super().__init__(hass, source_entity_id)

    @property
    def name(self) -> str:
        return f"{get_domain(self._source_entity_id, 1)}"

    @property
    def unique_id(self) -> str:
        return f"{get_domain(self._source_entity_id, 1)}_occu"

    @property
    def is_on(self) -> bool:
        state = self.hass.states.get(self._source_entity_id).state
        return state == STATE_ON

    @property
    def device_class(self) -> str:
        return "occupancy"

    @property
    def extra_state_attributes(self) -> dict:
        return {"source_entity": self._source_entity_id}

    @property
    def icon(self) -> str:
        return "mdi:motion-sensor"
