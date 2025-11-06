from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction
from discord.ui import DesignerView

if TYPE_CHECKING:
    from Classes import MenuController
    from .FroggeContainer import FroggeContainer
################################################################################

__all__ = ("FroggeMenuView", )

################################################################################
class FroggeMenuView(DesignerView):

    __slots__ = (
        "controller",
    )

################################################################################
    def __init__(
        self,
        controller: MenuController,
        container: FroggeContainer,
        *,
        timeout: int = 1200,
        show_nav_buttons: bool = True
    ) -> None:

        if show_nav_buttons:
            container.add_navigation_buttons(controller)

        super().__init__(container, timeout=timeout)

        self.controller: MenuController = controller

################################################################################
    async def interaction_check(self, interaction: Interaction) -> bool:

        return interaction.user == self.controller.owner

################################################################################
