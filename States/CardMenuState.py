from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis
from Classes.Common import GenericSelectState
from UI.Common import *

from .BaseState import BaseState

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotCard
################################################################################

__all__ = ("CardMenuState",)

################################################################################
class CardMenuState(BaseState):

    ctx: TarotCard

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        container.add_text(f"## Card Management for {self.ctx.deck.name}")

        async def set_name_callback(i: Interaction):
            await self.ctx.set_name(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(f"Card Name: `{self.ctx.name}`"),
                accessory=GenericCallbackButton(
                    set_name_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )

        container.add_item(
            FroggeSection(
                TextDisplay(
                    "### Stat Tracker Attributes:\n"
                    f"Pip Value: `{self.ctx.pip_value.proper_name if self.ctx.pip_value is not None else 'Not Set'}`\n"
                    f"Suit: `{self.ctx.suit.proper_name if self.ctx.suit is not None else 'Not Set'}`\n"
                    f"Arcana: `{self.ctx.arcana.proper_name}`"
                ),
                accessory=GenericTransitionButton(
                    CardStatAttributeState(self.ctx),
                    label="Configure",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )

        return container

################################################################################
