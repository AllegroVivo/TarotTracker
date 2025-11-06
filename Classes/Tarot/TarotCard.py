from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Dict, Any

from discord import Interaction

from Classes.Common import DatabaseIdentifiable
from Enums import ArcanaType, TarotSuit, PipValue
from UI.Common import BasicTextModal, FileUploadModal
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import TarotDeck, TarotTracker
################################################################################

__all__ = ("TarotCard", )

TC = TypeVar("TC", bound="TarotCard")

_PIP_PATTERNS: Dict[PipValue, re.Pattern] = {
    PipValue.Ace:    re.compile(r"\bace\b", re.I),
    PipValue.Two:    re.compile(r"\b(?:two|2)\b", re.I),
    PipValue.Three:  re.compile(r"\b(?:three|3)\b", re.I),
    PipValue.Four:   re.compile(r"\b(?:four|4)\b", re.I),
    PipValue.Five:   re.compile(r"\b(?:five|5)\b", re.I),
    PipValue.Six:    re.compile(r"\b(?:six|6)\b", re.I),
    PipValue.Seven:  re.compile(r"\b(?:seven|7)\b", re.I),
    PipValue.Eight:  re.compile(r"\b(?:eight|8)\b", re.I),
    PipValue.Nine:   re.compile(r"\b(?:nine|9)\b", re.I),
    PipValue.Ten:    re.compile(r"\b(?:ten|10)\b", re.I),

    # Court cards: include common synonyms
    PipValue.Page:   re.compile(r"\b(?:page|knave)\b", re.I),
    PipValue.Knight: re.compile(r"\bknight\b", re.I),
    PipValue.Queen:  re.compile(r"\bqueen\b", re.I),
    PipValue.King:   re.compile(r"\bking\b", re.I),
}

SUIT_SYNONYMS: Dict[TarotSuit, tuple[str, ...]] = {
    TarotSuit.Cups:       ("cup", "cups", "chalice", "chalices"),
    TarotSuit.Pentacles:  ("pentacle", "pentacles", "coin", "coins", "disk", "disks", "disc", "discs", "denier", "deniers"),
    TarotSuit.Swords:     ("sword", "swords", "blade", "blades"),
    TarotSuit.Wands:      ("wand", "wands", "rod", "rods", "staff", "staffs", "stave", "staves", "baton", "batons"),
}

_SUIT_PATTERNS: Dict[TarotSuit, re.Pattern] = {
    suit: re.compile(r"\b(?:" + "|".join(map(re.escape, words)) + r")\b", re.I)
    for suit, words in SUIT_SYNONYMS.items()
}

################################################################################
class TarotCard(DatabaseIdentifiable):

    __slots__ = (
        "_deck",
        "name",
        "arcana",
        "suit",
        "pip_value",
        "meaning_upright",
        "meaning_reversed",
        "notes",
        "image_url",
    )

################################################################################
    def __init__(self, parent: TarotDeck, id: int, **kwargs) -> None:

        super().__init__(id)

        self._deck: TarotDeck = parent

        self.name: str = kwargs.pop("name")
        self.arcana: ArcanaType = ArcanaType(kwargs["arcana"])
        self.suit: Optional[TarotSuit] = (
            TarotSuit(kwargs["suit"])
            if kwargs.get("suit") is not None
            else None
        )
        self.pip_value = (
            PipValue(kwargs["pip_value"])
            if kwargs.get("pip_value") is not None
            else None
        )
        self.meaning_upright: Optional[str] = kwargs.get("meaning_upright")
        self.meaning_reversed: Optional[str] = kwargs.get("meaning_reversed")
        self.notes: Optional[str] = kwargs.get("notes")
        self.image_url: Optional[str] = kwargs.get("image_url")

################################################################################
    @classmethod
    def new(cls: Type[TC], parent: TarotDeck, name: str) -> TC:

        new_data = parent.bot.db.insert.tarot_card(parent.id, name)
        return cls(parent, **new_data)

################################################################################
    @property
    def bot(self) -> TarotTracker:

        return self._deck.bot

################################################################################
    @property
    def deck(self) -> TarotDeck:

        return self._deck

################################################################################
    def update(self) -> None:

        self.bot.db.update.tarot_card(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "arcana": self.arcana.value,
            "suit": self.suit.value if self.suit is not None else None,
            "pip_value": self.pip_value.value if self.pip_value is not None else None,
            "meaning_upright": self.meaning_upright,
            "meaning_reversed": self.meaning_reversed,
            "notes": self.notes,
            "image_url": self.image_url,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.tarot_card(self.id)

################################################################################
    def guess_attributes(self) -> None:

        if not self.name:
            return

        s = self.name.strip().lower()

        def guess_suit() -> Optional[TarotSuit]:
            for suit, pat in _SUIT_PATTERNS.items():
                if pat.search(s):
                    return suit

        def guess_pip_value() -> Optional[PipValue]:
            for pip, pat in _PIP_PATTERNS.items():
                if pat.search(s):
                    return pip

        self.pip_value = guess_pip_value()
        self.suit = guess_suit()
        self.arcana = ArcanaType.Minor if self.pip_value is not None else ArcanaType.Minor
        self.update()

################################################################################
    async def set_name(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Card Name",
            attribute="Unique Name",
            cur_val=self.name,
            example="eg. 'Five of Pentacles'",
            max_length=200
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value
        self.update()

################################################################################
    async def set_pip_value(self, interaction: Interaction, value: PipValue) -> None:

        existing = self._deck.get_card_by_attributes(
            suit=self.suit,
            pip=value,
            arcana=self.arcana,
        )
        if existing is not None:
            error = U.make_error(
                title="Invalid Pip Value",
                message=(
                    f"A card with the pip value '{value.name}' already exists "
                    f"for the '{self.suit.proper_name}' suit in this deck."
                ),
                solution="Please choose a different pip value or edit the existing card instead."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.pip_value = value
        self.update()

################################################################################
    async def set_suit_value(self, interaction: Interaction, value: TarotSuit) -> None:

        existing = self._deck.get_card_by_attributes(
            suit=value,
            pip=self.pip_value,
            arcana=self.arcana,
        )
        if existing is not None:
            error = U.make_error(
                title="Invalid Suit",
                message=(
                    f"A card with the suit '{value.proper_name}' already exists "
                    f"for the '{self.pip_value.name}' pip value in this deck."
                ),
                solution="Please choose a different suit or edit the existing card instead."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.suit = value
        self.update()

################################################################################
    async def toggle_arcana(self, interaction: Interaction) -> None:

        new_value = ArcanaType.Minor if self.arcana is ArcanaType.Major else ArcanaType.Major
        existing = self._deck.get_card_by_attributes(
            suit=self.suit,
            pip=self.pip_value,
            arcana=new_value,
        )
        if existing is not None:
            error = U.make_error(
                title="Invalid Arcana Type",
                message=(
                    f"A card with the arcana type '{new_value.name}' already exists "
                    f"for the '{self.suit.proper_name if self.suit else 'N/A'}' suit "
                    f"and '{self.pip_value.name if self.pip_value else 'N/A'}' pip value in this deck."
                ),
                solution="Please choose a different arcana type or edit the existing card instead."
            )
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.arcana = new_value
        self.update()

################################################################################
    async def set_meaning_upright(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Card Upright Meaning",
            attribute="Meaning Text",
            cur_val=self.meaning_upright,
            example="eg. 'New beginnings, potential, opportunity...'",
            max_length=1000,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.meaning_upright = modal.value
        self.update()

################################################################################
    async def set_meaning_reversed(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Card Reversed Meaning",
            attribute="Meaning Text",
            cur_val=self.meaning_reversed,
            example="eg. 'Delays, resistance, lack of progress...'",
            max_length=1000,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.meaning_reversed = modal.value
        self.update()

################################################################################
    async def set_notes(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Card Notes",
            attribute="Notes Text",
            cur_val=self.notes,
            example="eg. 'This card is associated with the element of Water...'",
            max_length=1000,
            multiline=True
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.notes = modal.value
        self.update()

################################################################################
    async def set_image(self, interaction: Interaction) -> None:

        modal = FileUploadModal(
            title="Upload Card Image",
            attribute="Image"
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.image_url = modal.value.url
        self.update()

################################################################################
    def clear_image(self) -> None:

        self.image_url = None
        self.update()

################################################################################
