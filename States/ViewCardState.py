from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis, BotImages
from Classes.Common import GenericSelectState
from UI.Common import *

from .BaseState import BaseState
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotCard
################################################################################

__all__ = ("ViewCardState",)

################################################################################
class ViewCardState(BaseState):

    ctx: TarotCard

    def __init__(self, ctx: TarotCard):
        super().__init__(ctx)
        self._display_reversed: bool = False

################################################################################
    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        title_text = f"## {self.ctx.name}"
        if not self.ctx.bot.tarot_manager.name_matches_canonical(self.ctx.name):
            title_text += f"\n_(aka {self.ctx.proper_name})_"

        container.add_text(title_text)
        container.add_item(
            MediaGallery(
                MediaGalleryItem(
                    url=(
                        self.ctx.image_url
                        if self.ctx.image_url is not None
                        else BotImages.ThumbnailMissing
                    )
                )
            )
        )
        container.add_separator()

        async def toggle_meaning_callback(i: Interaction):
            self._display_reversed = not self._display_reversed
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(
                    (
                        self.ctx.meaning_upright
                        if not self._display_reversed
                        else self.ctx.meaning_reversed
                    )
                    or "*No meaning available.*"
                ),
                accessory=GenericCallbackButton(
                    toggle_meaning_callback,
                    label=f"{'Upright' if self._display_reversed else 'Reversed'}",
                    style=ButtonStyle.secondary,
                    emoji=BotEmojis.ArrowLeftRight,
                    disabled=self.ctx.meaning_reversed is None,
                )
            )
        )
        container.add_separator()

        if self.ctx.notes is not None:
            container.add_text(f"### __Notes__\n{self.ctx.notes}")
            container.add_separator()

        async def deck_select_callback(i: Interaction, selected_values: List[str]):
            new_deck = self.ctx.bot.tarot_manager.decks[selected_values[0]]
            card_in_new_deck = new_deck.get_card_by_name(self.ctx.name)
            if card_in_new_deck is not None:
                self.ctx = card_in_new_deck
                await controller.redraw(i)

        deck_select = FroggeSelect(
            deck_select_callback,
            placeholder=f"Current Deck: {self.ctx.deck.name}",
            options=self.ctx.bot.tarot_manager.decks.select_options(),
            disabled=len(self.ctx.bot.tarot_manager.decks) <= 1,
        )
        container.add_item(ActionRow(deck_select))

        return container

################################################################################
