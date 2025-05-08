"""
Constant definitions
"""

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "domain_mapper"

CONF_TARGET_DOMAIN = "target_domain"
CONF_SOURCE_ENTITY = "source_entity"

SUPPORTED_MAPPINGS = {
    "water_heater": "climate",
    "switch": "binary_sensor"
}
