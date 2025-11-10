from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict, List, Optional

from discord import Interaction, AutocompleteContext

from .TarotDeckManager import TarotDeckManager
from States import AdminMenuState
from Utilities import Utilities as U
from .CanonicalCard import CanonicalCard

if TYPE_CHECKING:
    from Classes import TarotTracker
################################################################################

__all__ = ("TarotManager", )

################################################################################
class TarotManager:

    __slots__ = (
        "_state",
        "decks",
        "canonical_cards",
    )

    STD_DECK_NAME = "Standard"

################################################################################
    def __init__(self, state: TarotTracker) -> None:

        self._state: TarotTracker = state

        self.decks: TarotDeckManager = TarotDeckManager(self)
        self.canonical_cards: List[CanonicalCard] = []

################################################################################
    async def load_all(self, payload: Dict[str, any]) -> None:

        self.decks.load_all(payload["decks"])

        # Load canonical card data
        with open("Data/CanonicalCards.json", "r", encoding="utf-8") as f:
            self.canonical_cards = [CanonicalCard(**data) for data in json.load(f)]

################################################################################
    @property
    def bot(self) -> TarotTracker:

        return self._state

################################################################################
    async def admin_menu(self, interaction: Interaction) -> None:

        from ..Core import MenuController

        controller = MenuController(interaction.user, self._state)
        await controller.begin(interaction, AdminMenuState(self), ephemeral=False)

################################################################################
    def autocomplete_card_names(self, ctx: AutocompleteContext) -> List[str]:

        query = ctx.value or ""
        # user_id = ctx.interaction.user.id

        # Fetch the user's deck preference eventually
        deck_name = None

        # If no deck set yet, fall back to the standard deck
        try:
            deck = self.decks.get(deck_name or self.STD_DECK_NAME)
            names = [card.name for card in deck.cards]
        except KeyError:
            names = []

        return U.ac_ranked_match(names, query)

################################################################################
    async def lookup_card(self, interaction: Interaction, card: str) -> None:

        from ..Core import MenuController
        from States import ViewCardState

        card = self.decks.get("Standard").get_card_by_name(card)
        if card is None:
            error = U.make_error(
                title="Invalid Card Name",
                message=f"A card with the name '`{card}`' does not exist in the selected deck.",
                solution="Please check the card name and try again."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        controller = MenuController(interaction.user, self._state)
        await controller.begin(interaction, ViewCardState(card), ephemeral=False)

################################################################################
    def get_canonical_card(self, *, id: int = None, name: str = None) -> Optional[CanonicalCard]:

        if id is not None:
            return next((c for c in self.canonical_cards if c.id == id), None)

        query = name.lower()
        return next((c for c in self.canonical_cards if c.name.lower() == query), None)

################################################################################
    def name_matches_canonical(self, name: str) -> bool:

        return bool(self.get_canonical_card(name=name))

################################################################################
