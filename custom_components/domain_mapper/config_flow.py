"""
Config flow for domain_mapper
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import entity_registry as er

from .const import (
    _LOGGER,
    DOMAIN,
    CONF_SOURCE_DOMAIN,
    CONF_TARGET_DOMAIN,
    CONF_SOURCE_ENTITY,
    SUPPORTED_MAPPINGS,
    MAPPINGS_TO_PROPERTIES,
)

class DomainMapperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Config flow for domain_mapper
    """
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """
        First step: select source domain
        """
        if user_input is not None:
            self.source_domain = user_input[CONF_SOURCE_DOMAIN]
            return await self.async_step_mappable_domain()

        schema = vol.Schema({
            vol.Required(CONF_SOURCE_DOMAIN): vol.In(list(SUPPORTED_MAPPINGS.keys()))
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_mappable_domain(self, user_input=None):
        """
        Second step: select mappable domain from selected source entity
        """
        if user_input is not None:
            self.target_domain = user_input[CONF_TARGET_DOMAIN]
            return await self.async_step_select_source()

        schema = vol.Schema({
            vol.Required(CONF_TARGET_DOMAIN): vol.In(list(SUPPORTED_MAPPINGS[self.source_domain]))
        })
        return self.async_show_form(step_id="mappable_domain", data_schema=schema)

    async def async_step_select_source(self, user_input=None):
        """
        Third step: select source entity filtered by target domain
        """
        entity_registry = er.async_get(self.hass)
        filtered_entities = [
            e.entity_id for e in entity_registry.entities.values()
            if e.domain == self.source_domain
        ]
        _LOGGER.debug("Filtered entities: %s", filtered_entities)

        if user_input is not None:
            user_input[CONF_SOURCE_DOMAIN] = self.source_domain
            user_input[CONF_TARGET_DOMAIN] = self.target_domain
            _LOGGER.debug("User input: %s", user_input)

            await self.async_set_unique_id(user_input[CONF_SOURCE_ENTITY])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=self.target_domain, data=user_input)

        schema_dict = {
            vol.Required(CONF_SOURCE_ENTITY): vol.In(filtered_entities)
        }
        for prop in MAPPINGS_TO_PROPERTIES[self.target_domain]:
            schema_dict[prop] = MAPPINGS_TO_PROPERTIES[self.target_domain][prop]

        schema = vol.Schema(schema_dict)
        return self.async_show_form(step_id="select_source", data_schema=schema)
