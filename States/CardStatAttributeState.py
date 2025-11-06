from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis
from Classes.Common import GenericSelectState
from Enums import PipValue, ArcanaType, TarotSuit
from UI.Common import *

from .BaseState import BaseState

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotCard
################################################################################

__all__ = ("CardStatAttributeState",)

################################################################################
class CardStatAttributeState(BaseState):

    ctx: TarotCard

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        container.add_text(
            f"## Statistic Attribute Setter\n"
            f"`{self.ctx.name}` from deck `{self.ctx.deck.name}`"
        )
        container.add_separator()

        async def set_suit_callback(i: Interaction, values: List[str], _):
            await self.ctx.set_suit_value(i, TarotSuit(int(values[0])))

        container.add_item(
            FroggeSection(
                TextDisplay(f"Current Suit: `{self.ctx.suit.proper_name if self.ctx.suit is not None else 'N/A'}`"),
                accessory=GenericTransitionButton(
                    GenericSelectState(
                        header="Select the Card's Suit",
                        placeholder="Select Suit...",
                        on_select=set_suit_callback,
                        options_provider=TarotSuit.select_options,
                    ),
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil
                )
            )
        )

        async def set_pip_callback(i: Interaction, values: List[str], _):
            await self.ctx.set_pip_value(i, PipValue(int(values[0])))

        container.add_item(
            FroggeSection(
                TextDisplay(f"Current Pip Value: `{self.ctx.pip_value.proper_name if self.ctx.pip_value is not None else 'N/A'}`"),
                accessory=GenericTransitionButton(
                    GenericSelectState(
                        header="Select the Card's Pip Value",
                        placeholder="Select Pip Value...",
                        on_select=set_pip_callback,
                        options_provider=PipValue.select_options,
                    ),
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil
                )
            )
        )

        async def set_arcana_callback(i: Interaction):
            await self.ctx.toggle_arcana(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(f"Current Arcana Type: `{self.ctx.arcana.proper_name}`"),
                accessory=GenericCallbackButton(
                    set_arcana_callback,
                    label="Toggle",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.ArrowLeftRight
                )
            )
        )

        return container

################################################################################
