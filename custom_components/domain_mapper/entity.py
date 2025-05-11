"""
Proxy entity for domain_mapper
"""

from homeassistant.const import (
    STATE_ON,
    STATE_OFF,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF,
    CONF_FRIENDLY_NAME,
    CONF_ENTITY_ID,
    CONF_ATTRIBUTE,
    ATTR_TEMPERATURE,
    UnitOfTemperature,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.components.climate import ClimateEntity, PRESET_NONE, PRESET_AWAY
from homeassistant.components.climate.const import (
    HVACMode,
    ClimateEntityFeature,
    SERVICE_SET_TEMPERATURE,
    SERVICE_SET_PRESET_MODE,
    ATTR_PRESET_MODE,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_MIN_TEMP,
    ATTR_MAX_TEMP,
)
from homeassistant.components.water_heater import STATE_GAS, ATTR_AWAY_MODE
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import (
    _LOGGER,
    DOMAIN,
    CONF_SOURCE_ENTITY,
    PROPERTY_DEVICE_CLASS,
)
from .coordinator import StateTrackingCoordinator
from .helper import get_domain


class ProxyBaseEntity(Entity):
    """
    Base class for proxy entities
    """

    def __init__(self, coordinator: StateTrackingCoordinator) -> None:
        self._coordinator = coordinator

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self._coordinator.async_add_listener(self.async_write_ha_state)

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def title_case(self) -> str:
        """
        water_heater -> Water Heater
        """
        domain = self._coordinator.source_domain.split('_')
        return ' '.join(dom.capitalize() for dom in domain)

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._coordinator.source_domain)},
            name=self.title_case,
            manufacturer="DomainMapper",
            model="ProxyEntity",
        )


class ProxyClimateEntity(ProxyBaseEntity, ClimateEntity):
    HVAC_MODE_MAP = {
        STATE_GAS: HVACMode.HEAT,
        STATE_OFF: HVACMode.OFF
    }

    def __init__(self, coordinator: StateTrackingCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_hvac_modes = [HVACMode.HEAT, HVACMode.OFF]
        self._attr_preset_modes = [PRESET_NONE]
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
        self._attr_supported_features |= ClimateEntityFeature.TURN_ON
        self._attr_supported_features |= ClimateEntityFeature.TURN_OFF

    @property
    def name(self) -> str:
        return self._coordinator.entity_name or self._coordinator.data.attributes.get(CONF_FRIENDLY_NAME)

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{get_domain(self._coordinator.entity_id, 1)}"

    @property
    def supported_features(self) -> ClimateEntityFeature:
        if self._coordinator.data.attributes.get(ATTR_AWAY_MODE) and PRESET_AWAY not in self._attr_preset_modes:
            self._attr_preset_modes.append(PRESET_AWAY)
            self._attr_supported_features |= ClimateEntityFeature.PRESET_MODE
        return self._attr_supported_features

    @property
    def hvac_mode(self) -> HVACMode:
        return self.HVAC_MODE_MAP.get(self._coordinator.data.state, HVACMode.OFF)

    @property
    def preset_mode(self) -> str:
        if self._coordinator.data.attributes.get(ATTR_AWAY_MODE) == STATE_ON:
            return PRESET_AWAY
        return PRESET_NONE

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.HEAT:
            await self.hass.services.async_call(
                self._coordinator.target_domain,
                SERVICE_TURN_ON,
                {CONF_ENTITY_ID: self._coordinator.entity_id},
                blocking=True,
            )
        elif hvac_mode == HVACMode.OFF:
            await self.hass.services.async_call(
                self._coordinator.target_domain,
                SERVICE_TURN_OFF,
                {CONF_ENTITY_ID: self._coordinator.entity_id},
                blocking=True,
            )
        await self._coordinator.async_request_refresh()

    async def async_set_temperature(self, **kwargs) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            await self.hass.services.async_call(
                self._coordinator.target_domain,
                SERVICE_SET_TEMPERATURE,
                {
                    CONF_ENTITY_ID: self._coordinator.entity_id,
                    ATTR_TEMPERATURE: temperature
                },
                blocking=True
            )
            await self._coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        await self.hass.services.async_call(
            self._coordinator.target_domain,
            SERVICE_SET_PRESET_MODE,
            {
                CONF_ENTITY_ID: self._coordinator.entity_id,
                ATTR_PRESET_MODE: preset_mode
            },
            blocking=True
        )
        await self._coordinator.async_request_refresh()

    @property
    def target_temperature(self) -> float | None:
        return self._coordinator.data.attributes.get(ATTR_TEMPERATURE)

    @property
    def current_temperature(self) -> float | None:
        return self._coordinator.data.attributes.get(ATTR_CURRENT_TEMPERATURE)

    @property
    def min_temp(self) -> float | None:
        return self._coordinator.data.attributes.get(ATTR_MIN_TEMP)

    @property
    def max_temp(self) -> float | None:
        return self._coordinator.data.attributes.get(ATTR_MAX_TEMP)

    @property
    def extra_state_attributes(self) -> dict:
        return {
            CONF_SOURCE_ENTITY: self._coordinator.entity_id,
            CONF_ATTRIBUTE: self._coordinator.data.attributes
        }


class ProxyBinarySensor(ProxyBaseEntity, BinarySensorEntity):

    def __init__(self, coordinator: StateTrackingCoordinator) -> None:
        super().__init__(coordinator)

    @property
    def name(self) -> str:
        return self._coordinator.entity_name or self._coordinator.data.attributes.get(CONF_FRIENDLY_NAME)

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{get_domain(self._coordinator.entity_id, 1)}"

    @property
    def is_on(self) -> bool:
        return self._coordinator.data.state == STATE_ON

    @property
    def device_class(self) -> str | None:
        return self._coordinator.entry.data.get(PROPERTY_DEVICE_CLASS)

    @property
    def extra_state_attributes(self) -> dict:
        return {
            CONF_SOURCE_ENTITY: self._coordinator.entity_id,
            CONF_ATTRIBUTE: self._coordinator.data.attributes
        }
