"""
Constant definitions
"""

import logging
import voluptuous as vol

from homeassistant.const import Platform
from homeassistant.components.binary_sensor import DEVICE_CLASSES
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "domain_mapper"

CONF_SOURCE_DOMAIN = "source_domain" # original domain
CONF_TARGET_DOMAIN = "target_domain"
CONF_SOURCE_ENTITY = "source_entity"

PROPERTY_NAME = "property_name"
PROPERTY_DEVICE_CLASS = "property_device_class"

SUPPORTED_MAPPINGS = {
    Platform.WATER_HEATER.value: {Platform.CLIMATE},
    Platform.SWITCH.value: {Platform.BINARY_SENSOR}
}

MAPPINGS_TO_PROPERTIES = {
    Platform.BINARY_SENSOR.value: {
        vol.Optional(PROPERTY_NAME): cv.string,
        vol.Required(PROPERTY_DEVICE_CLASS): vol.In(DEVICE_CLASSES)
    },
    Platform.CLIMATE.value: {
        vol.Optional(PROPERTY_NAME): cv.string
    }
}