from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis
from Classes.Common import GenericSelectState
from UI.Common import *

from .BaseState import BaseState
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotCard
################################################################################

__all__ = ("CardMeaningState",)

################################################################################
class CardMeaningState(BaseState):

    ctx: TarotCard

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        container.add_text(
            f"## {self.ctx.name} from '{self.ctx.deck.name}'"
        )
        container.add_separator()

        async def set_upright_meaning_callback(i: Interaction):
            await self.ctx.set_meaning_upright(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(
                    f"__**Upright Meaning**__\n"
                    f"{U.string_clamp(self.ctx.meaning_upright, 250) or '`Not Set`'}"
                ),
                accessory=GenericCallbackButton(
                    set_upright_meaning_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )

        async def set_reversed_meaning_callback(i: Interaction):
            await self.ctx.set_meaning_reversed(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(
                    f"__**Reversed Meaning**__\n"
                    f"{U.string_clamp(self.ctx.meaning_reversed, 250) or '`Not Set`'}"
                ),
                accessory=GenericCallbackButton(
                    set_reversed_meaning_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )

        return container

################################################################################
