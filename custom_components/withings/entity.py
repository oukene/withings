"""Base entity for Withings."""
from __future__ import annotations

from dataclasses import dataclass

from withings_api.common import GetSleepSummaryField, MeasureType, NotifyAppli

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, Measurement
from .coordinator import WithingsDataUpdateCoordinator

# modify (add)
from .const import VERSION

@dataclass
class WithingsEntityDescriptionMixin:
    """Mixin for describing withings data."""

    measurement: Measurement
    measure_type: NotifyAppli | GetSleepSummaryField | MeasureType


@dataclass
class WithingsEntityDescription(EntityDescription, WithingsEntityDescriptionMixin):
    """Immutable class for describing withings data."""


class WithingsEntity(CoordinatorEntity[WithingsDataUpdateCoordinator]):
    """Base class for withings entities."""
    # base
    # entity_description: WithingsEntityDescription
    # _attr_has_entity_name = True
    
    #modify
    entity_description: WithingsEntityDescription
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_entity_registry_enabled_default = True
    _attr_entity_registry_visible_default = True
    _attr_force_update = True

    def __init__(
        self,
        coordinator: WithingsDataUpdateCoordinator,
        description: WithingsEntityDescription,
    ) -> None:
        """Initialize the Withings entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"withings_{coordinator.config_entry.unique_id}_{description.measurement.value}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(coordinator.config_entry.unique_id))},
            manufacturer="Withings",
            # modify (add)
            sw_version=VERSION,
        )


    # modify (add)
    @property
    def translation_key(self) -> str | None:
        return self.entity_description.key
