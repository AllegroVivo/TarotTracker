from __future__ import annotations

from typing import List

from discord import SelectOption, PartialEmoji

from .TarotSuit import TarotSuit
from ._Enum import FroggeEnum
################################################################################
class TarotRank(FroggeEnum):

    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Page = 11
    Knight = 12
    Queen = 13
    King = 14

################################################################################
    @classmethod
    def select_options_with_suit(cls, suit: TarotSuit) -> List[SelectOption]:

        return [
            SelectOption(
                label=f"{rank.proper_name} of {suit.proper_name}",
                value=str(rank.value),
                emoji=rank.emoji
            )
            for rank in cls
        ]

################################################################################
    @property
    def emoji(self) -> PartialEmoji:

        match self.value:
            case 1:
                return PartialEmoji(name="♠️")  # Ace
            case 2:
                return PartialEmoji(name="2️⃣")  # Two
            case 3:
                return PartialEmoji(name="3️⃣")  # Three
            case 4:
                return PartialEmoji(name="4️⃣")  # Four
            case 5:
                return PartialEmoji(name="5️⃣")  # Five
            case 6:
                return PartialEmoji(name="6️⃣")  # Six
            case 7:
                return PartialEmoji(name="7️⃣")  # Seven
            case 8:
                return PartialEmoji(name="8️⃣")  # Eight
            case 9:
                return PartialEmoji(name="9️⃣")  # Nine
            case 10:
                return PartialEmoji(name="🔟")  # Ten
            case 11:
                return PartialEmoji(name="📯")  # Page
            case 12:
                return PartialEmoji(name="🐎")  # Knight
            case 13:
                return PartialEmoji(name="👸")  # Queen
            case 14:
                return PartialEmoji(name="👑")  # King
            case _:
                raise NotImplemented(f"No emoji defined for TarotRank value {self.value}")

################################################################################
