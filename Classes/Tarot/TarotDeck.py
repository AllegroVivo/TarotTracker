from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List, Dict, Any, Union

from discord import Interaction, SelectOption

from Classes.Common import DatabaseIdentifiable
from UI.Common import BasicTextModal
from .TarotCard import TarotCard
from Utilities import Utilities as U

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
        self.cards: List[TarotCard] = [
            TarotCard(self, **data)
            for data in kwargs.get("cards", [])
        ]

################################################################################
    @classmethod
    def new(cls, mgr: TarotDeckManager, name: str) -> TarotDeck:

        new_data = mgr.bot.db.insert.tarot_deck(name)
        return cls(mgr, **new_data)

################################################################################
    def __len__(self) -> int:

        return len(self.cards)

################################################################################
    def __getitem__(self, card_id: Union[str, int]) -> Optional[TarotCard]:

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
    def select_options(self) -> List[SelectOption]:

        return [
            SelectOption(
                label=card.name,
                # description=???,
                value=str(card.id)
            )
            for card in self.cards
        ]

################################################################################
    def get_card_by_name(self, name: str) -> Optional[TarotCard]:

        return next((card for card in self.cards if card.name.lower() == name.lower()), None)

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
    async def add_card(self, interaction: Interaction) -> Optional[TarotCard]:

        modal = BasicTextModal(
            title="Enter Card Name",
            attribute="Name",
            example="Five of Pentacles",
            max_length=200,
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        existing = self.get_card_by_name(modal.value)
        if existing:
            error = U.make_error(
                title="Card Already Exists",
                message=f"Card {modal.value} already exists in this deck.",
                solution="Please select another name",
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        new_card = TarotCard.new(self, modal.value)
        self.cards.append(new_card)
        new_card.guess_attributes()
        return new_card

################################################################################
