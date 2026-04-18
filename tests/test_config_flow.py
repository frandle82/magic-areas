"""Tests for config flow behavior."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import ATTR_NAME
from homeassistant.helpers.area_registry import async_get as areareg_async_get

from custom_components.magic_areas.config_flow import OptionsFlowHandler
from custom_components.magic_areas.const import (
    AREA_STATE_BRIGHT,
    CONF_ENABLED_FEATURES,
    CONF_FEATURE_LIGHT_GROUPS,
    CONF_ID,
    CONF_OVERHEAD_LIGHTS_BLOCKING_STATES,
    CONF_OVERHEAD_LIGHTS_TURN_OFF_WHEN_BRIGHT,
    DOMAIN,
)
from tests.const import DEFAULT_MOCK_AREA
from tests.helpers import get_basic_config_entry_data


async def test_options_flow_keeps_extended_light_group_options(hass) -> None:
    """Test that extended light-group options survive reopening options flow."""

    area_registry = areareg_async_get(hass)
    area_registry.async_create(
        name=DEFAULT_MOCK_AREA.value,
    )

    config_entry_options = get_basic_config_entry_data(DEFAULT_MOCK_AREA)
    config_entry_options[CONF_ENABLED_FEATURES] = {
        CONF_FEATURE_LIGHT_GROUPS: {
            CONF_OVERHEAD_LIGHTS_BLOCKING_STATES: [AREA_STATE_BRIGHT],
            CONF_OVERHEAD_LIGHTS_TURN_OFF_WHEN_BRIGHT: True,
        }
    }

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        title=str(config_entry_options[ATTR_NAME]),
        data={CONF_ID: DEFAULT_MOCK_AREA.value},
        options=config_entry_options,
    )
    config_entry.add_to_hass(hass)

    flow = OptionsFlowHandler(config_entry)
    flow.hass = hass

    result = await flow.async_step_init()

    assert result["type"] == "menu"
    assert (
        flow.area_options[CONF_ENABLED_FEATURES][CONF_FEATURE_LIGHT_GROUPS][
            CONF_OVERHEAD_LIGHTS_BLOCKING_STATES
        ]
        == [AREA_STATE_BRIGHT]
    )
    assert (
        flow.area_options[CONF_ENABLED_FEATURES][CONF_FEATURE_LIGHT_GROUPS][
            CONF_OVERHEAD_LIGHTS_TURN_OFF_WHEN_BRIGHT
        ]
        is True
    )
