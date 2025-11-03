from __future__ import annotations

from typing import TYPE_CHECKING, Type

from . import Models

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseDeleter",)

################################################################################
class DatabaseDeleter:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def _delete_record(self, model_class: Type, _id: int) -> None:

        with self._parent.get_db() as db:
            record = db.get(model_class, _id)
            db.delete(record)
            db.flush()

################################################################################
    def tarot_deck(self, deck_id: int) -> None:

        self._delete_record(Models.TarotDeckModel, deck_id)

################################################################################
