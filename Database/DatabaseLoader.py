from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any, Optional, List, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def load_all(self) -> Dict[str, Any]:

        with self._parent.get_db() as db:
            decks = db.scalars(select(TarotDeckModel)).all()

            return {
                "decks": [TarotDeckSchema.model_validate(deck).model_dump() for deck in decks]
            }

################################################################################
