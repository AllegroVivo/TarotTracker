from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, Dict

from discord import Interaction, SelectOption

from UI.Common import BasicTextModal
from .TarotDeck import TarotDeck
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import TarotManager, TarotTracker
################################################################################

__all__ = ("TarotDeckManager", )

################################################################################
class TarotDeckManager:

    __slots__ = (
        "_mgr",
        "_decks"
    )

    MAX_DECKS = 100

################################################################################
    def __init__(self, mgr: TarotManager) -> None:

        self._mgr: TarotManager = mgr
        self._decks: List[TarotDeck] = []

################################################################################
    def load_all(self, payload: List[Dict[str, any]]) -> None:

        self._decks = [TarotDeck(self, **data) for data in payload]
        print(self._decks)

################################################################################
    def __len__(self) -> int:

        return len(self._decks)

################################################################################
    def __getitem__(self, deck_id: Union[str, int]) -> Optional[TarotDeck]:

        return next((deck for deck in self._decks if deck.id == int(deck_id)), None)

################################################################################
    @property
    def bot(self) -> TarotTracker:

        return self._mgr.bot

################################################################################
    def select_options(self) -> List[SelectOption]:

        return [
            SelectOption(
                label=deck.name,
                description=f"{len(deck)} cards",
                value=str(deck.id)
            )
            for deck in self._decks
        ]

################################################################################
    def get_deck_by_name(self, name: str) -> Optional[TarotDeck]:

        return next((deck for deck in self._decks if deck.name.lower() == name.lower()), None)

################################################################################
    async def add_deck(self, interaction: Interaction) -> Optional[TarotDeck]:

        if len(self._decks) >= self.MAX_DECKS:
            error = U.make_error(
                title="Maximum Decks Reached",
                message="You have reached the maximum number of decks allowed ({self.MAX_DECKS}).",
                solution="Please delete an existing deck before creating a new one."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        modal = BasicTextModal(
            title="Enter New Deck Name",
            attribute="Name",
            example="New Deck Name",
            max_length=200
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        existing = self.get_deck_by_name(modal.value)
        if existing:
            error = U.make_error(
                title="Deck Already Exists",
                message=f"A deck with the name '{modal.value}' already exists.",
                solution="Please choose a different name for your deck."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        deck = TarotDeck.new(self, modal.value)
        self._decks.append(deck)
        return deck

################################################################################
