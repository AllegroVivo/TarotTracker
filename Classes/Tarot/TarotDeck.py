from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Dict, Any

from discord import Interaction

from Classes.Common import DatabaseIdentifiable
from UI.Common import BasicTextModal
from .TarotCard import TarotCard

if TYPE_CHECKING:
    from Classes import TarotDeckManager, TarotTracker
################################################################################

__all__ = ("TarotDeck", )

################################################################################
class TarotDeck(DatabaseIdentifiable):

    __slots__ = (
        "_mgr",
        "name",
        "description",
        "cards",
    )

################################################################################
    def __init__(self, mgr: TarotDeckManager, id: int, **kwargs) -> None:

        super().__init__(id)

        self._mgr: TarotDeckManager = mgr

        self.name: Optional[str] = kwargs.get("name")
        self.description: Optional[str] = kwargs.get("description")
        self.cards: List[TarotCard] = kwargs.get("cards", [])

################################################################################
    @classmethod
    def new(cls, mgr: TarotDeckManager, name: str) -> TarotDeck:

        new_data = mgr.bot.db.insert.tarot_deck(name)
        return cls(mgr, **new_data)

################################################################################
    def __len__(self) -> int:

        return len(self.cards)

################################################################################
    def __getitem__(self, card_id: int) -> Optional[TarotCard]:

        return next((card for card in self.cards if card.id == int(card_id)), None)

################################################################################
    @property
    def bot(self) -> TarotTracker:

        return self._mgr.bot

################################################################################
    def update(self) -> None:

        self.bot.db.update.tarot_deck(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "description": self.description,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.tarot_deck(self.id)

################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Deck Name",
            attribute="Name",
            cur_val=self.name,
            max_length=200,
            example="My Tarot Deck",
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value
        self.update()

################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Deck Description",
            attribute="Description",
            cur_val=self.description,
            max_length=1000,
            example="A description of my tarot deck.",
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value
        self.update()

################################################################################
