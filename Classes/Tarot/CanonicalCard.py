from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from Enums import *

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("CanonicalCard", )

################################################################################
class CanonicalCard:

    __slots__ = (
        "id",
        "name",
        "arcana",
        "major_arcana",
        "suit",
        "rank",
    )

################################################################################
    def __init__(self, **kwargs):

        self.id: int = kwargs.pop("ID")
        self.name: str = kwargs.pop("Name")
        self.arcana: ArcanaType = ArcanaType(kwargs.pop("Arcana"))
        self.major_arcana: Optional[MajorArcana] = (
            MajorArcana(kwargs.pop("MajorIndex"))
            if self.arcana is ArcanaType.Major
            else None
        )
        self.suit: Optional[TarotSuit] = (
            TarotSuit(kwargs.pop("Suit"))
            if self.arcana is ArcanaType.Minor
            else None
        )
        self.rank: Optional[TarotRank] = (
            TarotRank(kwargs.pop("Rank"))
            if self.arcana is ArcanaType.Minor
            else None
        )

################################################################################
