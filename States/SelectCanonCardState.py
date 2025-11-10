from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis, BotImages
from Classes.Common import GenericSelectState
from Enums import TarotSuit, MajorArcana, TarotRank
from UI.Common import *

from .BaseState import BaseState
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotCard
################################################################################

__all__ = ("SelectCanonCardState",)

################################################################################
class SelectCanonCardState(BaseState):

    ctx: TarotCard

    def __init__(self, ctx: TarotCard) -> None:
        super().__init__(ctx)

        self._suit: Optional[TarotSuit] = None
        self._rank: Optional[TarotRank] = None
        self._major: Optional[MajorArcana] = None

################################################################################
    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        container.add_text("## Canonical Card Selection")

        async def suit_select_callback(i: Interaction, selected: List[str]):
            self._suit = TarotSuit(int(selected[0]))
            # Reset sub-selections when suit changes
            self._rank = None
            self._major = None
            await controller.redraw(i)

        suit_select = FroggeSelect(
            suit_select_callback,
            placeholder=(
                "Select a suit..."
                if self._suit is None
                else self._suit.proper_name
            ),
            options=TarotSuit.select_options()
        )
        container.add_item(ActionRow(suit_select))

        if self._suit is not None:
            if self._suit is TarotSuit.Major_Arcana:
                options = MajorArcana.select_options()
            else:
                options = TarotRank.select_options_with_suit(self._suit)

            async def rank_select_callback(i: Interaction, selected: List[str]):
                if self._suit is TarotSuit.Major_Arcana:
                    self._major = MajorArcana(int(selected[0]))
                    self.ctx.set_canon_card(self._suit, self._major)
                else:
                    self._rank = TarotRank(int(selected[0]))
                    self.ctx.set_canon_card(self._suit, self._rank)
                await controller.redraw(i)

            rank_select = FroggeSelect(
                rank_select_callback,
                placeholder=(
                    "Select a rank..." if (
                        (self._suit is not TarotSuit.Major_Arcana and self._rank is None) or
                        (self._suit is TarotSuit.Major_Arcana and self._major is None)
                    ) else (
                        self._major.proper_name if self._suit is TarotSuit.Major_Arcana and self._major is not None
                        else self._rank.proper_name
                    )
                ),
                options=options
            )
            container.add_item(ActionRow(rank_select))

        return container

################################################################################
