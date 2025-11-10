from __future__ import annotations

from discord import PartialEmoji, SelectOption

from ._Enum import FroggeEnum
################################################################################
class TarotSuit(FroggeEnum):

    Major_Arcana = 0
    Swords = 1
    Cups = 2
    Wands = 3
    Pentacles = 4

################################################################################
    @property
    def emoji(self) -> PartialEmoji:

        match self.value:
            case 0:
                return PartialEmoji(name="🎴")  # Major Arcana
            case 1:
                return PartialEmoji(name="⚔️")  # Swords
            case 2:
                return PartialEmoji(name="🏆")  # Cups
            case 3:
                return PartialEmoji(name="🪄")  # Wands
            case 4:
                return PartialEmoji(name="⭐")  # Pentacles
            case _:
                raise NotImplementedError("Emoji not defined for this Tarot Suit.")

################################################################################
    @property
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.proper_name, value=str(self.value), emoji=self.emoji)

################################################################################
