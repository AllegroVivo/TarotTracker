from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis
from UI.Common import *

from .BaseState import BaseState

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotDeck
################################################################################

__all__ = ("DeckMenuState",)

################################################################################
class DeckMenuState(BaseState):

    ctx: TarotDeck

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        from Classes.Common import GenericSelectState

        container.add_text(f"## Deck Management")

        async def set_name_callback(i: Interaction):
            await self.ctx.set_name(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(f"__**Deck Name**__: `{self.ctx.name}`"),
                accessory=GenericCallbackButton(
                    set_name_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )

        async def set_description_callback(i: Interaction):
            await self.ctx.set_description(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(f"__**Description**__:\n`{self.ctx.description or 'Not Set'}`"),
                accessory=GenericCallbackButton(
                    set_description_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )
        container.add_separator()

        container.add_text(f"Cards in Deck: `{len(self.ctx.cards)}`")

        async def add_card_callback(i: Interaction):
            from .CardMenuState import CardMenuState
            new_card = await self.ctx.add_card(i)
            await controller.transition_to(CardMenuState(new_card), i, replace=True)

        container.add_item(
            GenericCallbackButton(
                add_card_callback,
                label="Add",
                style=ButtonStyle.success,
                emoji=BotEmojis.Plus,
            )
        )

        async def modify_card_callback(i: Interaction, values: List[str], _):
            from .CardMenuState import CardMenuState
            card = self.ctx[values[0]]
            if card is not None:
                await controller.transition_to(CardMenuState(card), i, replace=True)

        container.add_item(
            GenericTransitionButton(
                GenericSelectState(
                    header="Select a Card to Modify",
                    placeholder="Select a Card...",
                    on_select=modify_card_callback,
                    options_provider=self.ctx.select_options
                ),
                label="Modify",
                style=ButtonStyle.primary,
                emoji=BotEmojis.Cycle,
                disabled=len(self.ctx) == 0
            )
        )

        return container

################################################################################
