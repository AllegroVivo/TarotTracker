from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord.components import Section as SectionComponent
from discord.ui import Section, Item

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("FroggeSection",)

################################################################################
class FroggeSection(Section):

    def __init__(self, *items: Item, accessory: Item = None):
        super().__init__(*items, accessory=accessory)

################################################################################
    def refresh_component(self, component: SectionComponent) -> None:

        # This is highly duct taped, check future updates of PyCord for fixes.
        self._underlying = component
        if hasattr(component, "components"):
            for x, y in zip(self.items, component.components):
                x.refresh_component(y)
        if self.accessory and hasattr(component, "accessory") and component.accessory:
            self.accessory.refresh_component(component.accessory)

################################################################################
