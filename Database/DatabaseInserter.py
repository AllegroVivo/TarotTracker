from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Any, Dict

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseInserter", )

################################################################################
class DatabaseInserter:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def tarot_deck(self, name: str) -> Dict[str, Any]:

        with self._parent.get_db() as db:
            deck = TarotDeckModel(name=name)
            db.add(deck)
            db.flush()
            db.refresh(deck)

            return TarotDeckSchema.model_validate(deck).model_dump()

################################################################################
