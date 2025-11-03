from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from discord import Interaction

from Classes.Common import DatabaseIdentifiable
from States import BaseState
from UI.Common import *
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import MenuController
################################################################################

__all__ = ("GenericRemovalState",)

################################################################################
class GenericRemovalState(BaseState):

    def __init__(self, ctx: DatabaseIdentifiable):
        super().__init__(ctx)

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        async def confirm_callback(i: Interaction):
            self.ctx.delete(i.user.id)
            await controller.back(i)

        container.add_text(f"Are you sure you want to remove the `{U.split_class_name(self.ctx.__class__)}`?")
        container.add_confirm_cancel_buttons(
            controller,
            confirm_callback=confirm_callback,
        )

        return container

################################################################################
