"""
Config flow for domain_mapper
"""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import entity_registry as er

from .const import (
    _LOGGER,
    DOMAIN,
    CONF_TARGET_DOMAIN,
    CONF_SOURCE_ENTITY,
    SUPPORTED_MAPPINGS
)

class DomainMapperConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Config flow for domain_mapper
    """
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """
        First step: select target domain
        """
        if user_input is not None:
            self.target_domain = user_input[CONF_TARGET_DOMAIN]
            return await self.async_step_select_source()

        schema = vol.Schema({
            vol.Required(CONF_TARGET_DOMAIN): vol.In(set(SUPPORTED_MAPPINGS.values()))
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_select_source(self, user_input=None):
        """
        Second step: select source entity filtered by target
        """
        reverse_map = {v: k for k, v in SUPPORTED_MAPPINGS.items()}
        expected_source_domain = reverse_map.get(self.target_domain)

        entity_registry = er.async_get(self.hass)
        filtered_entities = [
            e.entity_id for e in entity_registry.entities.values()
            if e.domain == expected_source_domain
        ]
        _LOGGER.debug("Filtered entities: %s", filtered_entities)

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_SOURCE_ENTITY],
                data={
                    CONF_TARGET_DOMAIN: self.target_domain,
                    CONF_SOURCE_ENTITY: user_input[CONF_SOURCE_ENTITY],
                },
            )

        schema = vol.Schema({
            vol.Required(CONF_SOURCE_ENTITY): vol.In(filtered_entities)
        })
        return self.async_show_form(step_id="select_source", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return DomainMapperOptionsFlowHandler(config_entry)


class DomainMapperOptionsFlowHandler(config_entries.OptionsFlow):
    """
    Options flow for domain_mapper
    """

    def __init__(self, config_entry):
        self.config_entry = config_entry
        self.target_domain = None

    async def async_step_init(self, user_input=None):
        """
        Step 1: choose target domain in options
        """
        if user_input is not None:
            self.target_domain = user_input[CONF_TARGET_DOMAIN]
            return await self.async_step_select_source()

        current = self.config_entry.options or self.config_entry.data
        schema = vol.Schema({
            vol.Required(CONF_TARGET_DOMAIN, default=current.get(CONF_TARGET_DOMAIN)): vol.In(set(SUPPORTED_MAPPINGS.values()))
        })
        return self.async_show_form(step_id="init", data_schema=schema)

    async def async_step_select_source(self, user_input=None):
        """
        Step 2: select source entity filtered by chosen target domain
        """
        reverse_map = {v: k for k, v in SUPPORTED_MAPPINGS.items()}
        expected_source_domain = reverse_map.get(self.target_domain)

        entity_registry = er.async_get(self.hass)
        filtered_entities = [
            e.entity_id for e in entity_registry.entities.values()
            if e.domain == expected_source_domain
        ]
        _LOGGER.debug("Filtered entities: %s", filtered_entities)

        current = self.config_entry.options or self.config_entry.data
        _LOGGER.debug("Current options: %s", current)

        if user_input is not None:
            return self.async_create_entry(
                title="Options",
                data={
                    CONF_TARGET_DOMAIN: self.target_domain,
                    CONF_SOURCE_ENTITY: user_input[CONF_SOURCE_ENTITY]
                },
            )

        schema = vol.Schema({
            vol.Required(CONF_SOURCE_ENTITY, default=current.get(CONF_SOURCE_ENTITY)): vol.In(filtered_entities)
        })
        return self.async_show_form(step_id="select_source", data_schema=schema)
