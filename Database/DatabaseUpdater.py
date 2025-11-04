from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Type, List, Union, TypeVar, Optional

from sqlalchemy import select

from . import Models

if TYPE_CHECKING:
    from Classes import *
    from Database import Database
################################################################################

__all__ = ("DatabaseUpdater",)

T = TypeVar("T")

################################################################################
class DatabaseUpdater:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def _update_record(
        self,
        model_class: Type[T],
        _id: int,
        data: Dict[str, Any],
    ) -> None:

        with self._parent.get_db() as db:
            record: T = db.get(model_class, _id)
            if record is None:
                raise ValueError(f"{model_class.__name__} not found with id {_id}")

            for key, value in data.items():
                setattr(record, key, value)
            db.flush()

################################################################################
    def tarot_deck(self, deck: TarotDeck) -> None:

        self._update_record(Models.TarotDeckModel, deck.id, deck.to_dict())

################################################################################
    def tarot_card(self, card: TarotCard) -> None:

        self._update_record(Models.TarotCardModel, card.id, card.to_dict())

################################################################################
