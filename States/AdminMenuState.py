from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, ButtonStyle

from Assets import BotEmojis
from UI.Common import *
from .BaseState import BaseState
from .DeckMenuState import DeckMenuState

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager
################################################################################

__all__ = ("AdminMenuState",)

################################################################################
class AdminMenuState(BaseState):

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        from Classes.Common import GenericSelectState

        self.ctx: TarotManager = controller.ctx.tarot_manager

        container.add_text(f"## Tarot System Dashboard")
        container.add_separator()

        container.add_text(
            "### Deck Management\n"
            f"**Total Decks:** `{len(self.ctx.decks)}`\n"
        )

        async def add_deck_callback(i: Interaction):
            new_deck = await self.ctx.decks.add_deck(i)
            await controller.transition_to(DeckMenuState(new_deck), i)

        container.add_item(
            GenericCallbackButton(
                add_deck_callback,
                label="Add",
                style=ButtonStyle.success,
                emoji=BotEmojis.Plus
            )
        )

        async def modify_deck_callback(i: Interaction, values: List[str], _):
            deck = self.ctx.decks[values[0]]
            if deck is not None:
                await controller.transition_to(DeckMenuState(deck), i, replace=True)

        container.add_item(
            GenericTransitionButton(
                GenericSelectState(
                    description="Select an event to modify.",
                    placeholder="Select an Event...",
                    options_provider=self.ctx.decks.select_options,
                    on_select=modify_deck_callback,
                ),
                label="Modify",
                style=ButtonStyle.primary,
                emoji=BotEmojis.Cycle,
                disabled=len(self.ctx.decks) == 0
            )
        )

        async def remove_event_callback(i: Interaction, values: List[str], _):
            from Classes.Common import GenericRemovalState
            event = self.ctx.decks[values[0]]
            await controller.transition_to(GenericRemovalState(event), i, replace=True)

        container.add_item(
            GenericTransitionButton(
                GenericSelectState(
                    description="Select an event to remove.",
                    placeholder="Select an Event...",
                    options_provider=self.ctx.decks.select_options,
                    on_select=remove_event_callback,
                ),
                label="Remove",
                style=ButtonStyle.danger,
                emoji=BotEmojis.Trash,
                disabled=len(self.ctx.decks) == 0
            )
        )

        return container

################################################################################
