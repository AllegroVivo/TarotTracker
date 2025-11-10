from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Dict, Any, Union, List

from discord import Interaction

from Classes.Common import DatabaseIdentifiable
from Enums import ArcanaType, TarotSuit, TarotRank, MajorArcana
from UI.Common import BasicTextModal, FileUploadModal
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import TarotDeck, TarotTracker, CanonicalCard
################################################################################

__all__ = ("TarotCard", )

TC = TypeVar("TC", bound="TarotCard")

_PIP_PATTERNS: Dict[TarotRank, re.Pattern] = {
    TarotRank.Ace:    re.compile(r"\bace\b", re.I),
    TarotRank.Two:    re.compile(r"\b(?:two|2)\b", re.I),
    TarotRank.Three:  re.compile(r"\b(?:three|3)\b", re.I),
    TarotRank.Four:   re.compile(r"\b(?:four|4)\b", re.I),
    TarotRank.Five:   re.compile(r"\b(?:five|5)\b", re.I),
    TarotRank.Six:    re.compile(r"\b(?:six|6)\b", re.I),
    TarotRank.Seven:  re.compile(r"\b(?:seven|7)\b", re.I),
    TarotRank.Eight:  re.compile(r"\b(?:eight|8)\b", re.I),
    TarotRank.Nine:   re.compile(r"\b(?:nine|9)\b", re.I),
    TarotRank.Ten:    re.compile(r"\b(?:ten|10)\b", re.I),

    # Court cards: include common synonyms
    TarotRank.Page:   re.compile(r"\b(?:page|knave)\b", re.I),
    TarotRank.Knight: re.compile(r"\bknight\b", re.I),
    TarotRank.Queen:  re.compile(r"\bqueen\b", re.I),
    TarotRank.King:   re.compile(r"\bking\b", re.I),
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
        "meaning_upright",
        "meaning_reversed",
        "upright_keywords",
        "reversed_keywords",
        "description",
        "image_url",
        "canonical_id",
    )

################################################################################
    def __init__(self, parent: TarotDeck, id: int, **kwargs) -> None:

        super().__init__(id)

        self._deck: TarotDeck = parent

        self.name: str = kwargs.pop("name")
        self.canonical_id: Optional[int] = kwargs.get("canonical_id")

        self.meaning_upright: Optional[str] = kwargs.get("meaning_upright")
        self.meaning_reversed: Optional[str] = kwargs.get("meaning_reversed")
        self.upright_keywords: List[str] = kwargs.get("upright_keywords")
        self.reversed_keywords: List[str] = kwargs.get("reversed_keywords")

        self.description: Optional[str] = kwargs.get("description")
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
    @property
    def canonical_card(self) -> Optional[CanonicalCard]:

        if self.canonical_id is None:
            return
        return self.bot.tarot_manager.get_canonical_card(id=self.canonical_id)

################################################################################
    @property
    def proper_name(self) -> str:

        match = self.bot.tarot_manager.get_canonical_card(id=self.canonical_id)
        if match:
            return match.name
        return "Unspecified"

################################################################################
    def update(self) -> None:

        self.bot.db.update.tarot_card(self)

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        return {
            "name": self.name,
            "canonical_id": self.canonical_id,
            "meaning_upright": self.meaning_upright,
            "meaning_reversed": self.meaning_reversed,
            "upright_keywords": self.upright_keywords,
            "reversed_keywords": self.reversed_keywords,
            "description": self.description,
            "image_url": self.image_url,
        }

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.tarot_card(self.id)

################################################################################
    def guess_canon_card(self) -> None:

        match = self.bot.tarot_manager.get_canonical_card(name=self.name)
        if match:
            self.canonical_id = match.id
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
            multiline=True,
            required=False
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.meaning_reversed = modal.value
        self.update()

################################################################################
    async def set_description(self, interaction: Interaction) -> None:

        modal = BasicTextModal(
            title="Set Card Notes",
            attribute="Notes Text",
            cur_val=self.description,
            example="eg. 'This card is associated with the element of Water...'",
            max_length=1000,
            multiline=True,
            required=False
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.description = modal.value
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
    def set_canon_card(self, suit: TarotSuit, value: Union[MajorArcana, TarotRank]) -> None:

        if suit is TarotSuit.Major_Arcana:
            match = next((
                cc for cc in self.bot.tarot_manager.canonical_cards
                if cc.arcana is ArcanaType.Major and cc.major_arcana == value
            ), None)
        else:
            match = next((
                cc for cc in self.bot.tarot_manager.canonical_cards
                if cc.arcana is ArcanaType.Minor and cc.suit == suit and cc.rank == value
            ), None)
        if match:
            self.canonical_id = match.id
            self.update()

################################################################################
