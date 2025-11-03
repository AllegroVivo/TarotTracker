from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from Classes.Common import DatabaseIdentifiable

if TYPE_CHECKING:
    from Classes import TarotDeck
################################################################################

__all__ = ("TarotCard", )

################################################################################
class TarotCard(DatabaseIdentifiable):

    __slots__ = (
        "_deck",
        "name",
        "arcana",
        "suit",
        "number",
        "meaning_upright",
        "meaning_reversed",
        "description",
    )

################################################################################
    def __init__(self, parent: TarotDeck, id: int, **kwargs) -> None:

        super().__init__(id)

        self._deck: TarotDeck = parent

        self.name: str = kwargs.pop("name")
        self.arcana: ArcanaType = kwargs.get("arcana", False)
        self.suit: Optional[TarotSuit] = kwargs.get("suit", None)

################################################################################
