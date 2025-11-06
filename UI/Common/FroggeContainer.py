from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Awaitable

from discord import ButtonStyle, Interaction, ActionRow as AR
from discord.ui import Container, Item, Button, ActionRow
from discord.components import Container as ContainerComponent
from .FroggeButton import FroggeButton

from Assets import BotEmojis
from Utilities import CustomColor

if TYPE_CHECKING:
    from Classes import MenuController
################################################################################

__all__ = ("FroggeContainer", )

################################################################################
class FroggeContainer(Container):

    def __init__(self, *items: Item, **kwargs):

        super().__init__(
            *items,
            color=CustomColor.random_all(),
            **kwargs
        )

################################################################################
    def refresh_component(self, component: ContainerComponent) -> None:

        # This is highly duct taped, check future updates of PyCord for fixes.
        self._underlying = component
        i = 0
        flattened = []
        for c in component.components:
            if isinstance(c, AR):
                flattened += c.children
            else:
                flattened.append(c)
        for j, y in enumerate(flattened):
            if j < len(self.items):
                x = self.items[i]
                try:
                    x.refresh_component(y)
                except Exception:
                    pass
                i += 1

################################################################################
    def add_navigation_buttons(self, controller: MenuController):

        self.add_separator()
        self.add_item(
            ActionRow(
                BackButton(controller),
                HomeButton(controller),
                CloseButton(controller)
            )
        )

################################################################################
    def add_confirm_cancel_buttons(
        self,
        controller: MenuController,
        confirm_callback: Callable[[Interaction], Awaitable[None]],
        cancel_callback: Callable[[Interaction], Awaitable[None]] = None,
        confirm_label: Optional[str] = "Confirm",
        cancel_label: Optional[str] = "Cancel",
        confirm_style: ButtonStyle = ButtonStyle.success,
        cancel_style: ButtonStyle = ButtonStyle.danger
    ):

        if cancel_callback is None:
            async def cancel_callback(i: Interaction):
                await controller.back(i)

        self.add_item(
            ActionRow(
                ConfirmCancelButton(confirm_style, confirm_label, confirm_callback),
                ConfirmCancelButton(cancel_style, cancel_label, cancel_callback)
            )
        )

################################################################################
class BackButton(Button):

    def __init__(self, controller: MenuController):

        super().__init__(
            label="Back",
            style=ButtonStyle.secondary,
            emoji=BotEmojis.ArrowLeft
        )

        self.menu_controller: MenuController = controller

    async def callback(self, interaction: Interaction):
        await interaction.edit()
        await self.menu_controller.back()

################################################################################
class HomeButton(Button):

    def __init__(self, controller: MenuController):

        super().__init__(
            label="Home",
            style=ButtonStyle.secondary,
            emoji=BotEmojis.House
        )

        self.menu_controller: MenuController = controller

    async def callback(self, interaction: Interaction):
        await interaction.edit()
        await self.menu_controller.home()

################################################################################
class CloseButton(Button):

    def __init__(self, controller: MenuController):

        super().__init__(
            label="Close Message",
            style=ButtonStyle.secondary,
            emoji=BotEmojis.CrossOld
        )

        self.menu_controller: MenuController = controller

    async def callback(self, interaction: Interaction):
        await interaction.edit()
        self.view.complete = True
        await self.menu_controller.end()

################################################################################
class ConfirmCancelButton(FroggeButton):

    def __init__(
        self,
        style: ButtonStyle,
        label: str,
        callback: Callable[[Interaction], Awaitable[None]]
    ):
        super().__init__(label=label, style=style)
        self.cb = callback

    async def callback(self, interaction: Interaction):
        await interaction.edit()
        await self.cb(interaction)

################################################################################
