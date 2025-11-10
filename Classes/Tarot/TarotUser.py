from __future__ import annotations

from typing import TYPE_CHECKING

from Classes.Common import DatabaseIdentifiable, LazyUser

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("TarotUser", )

################################################################################
class TarotUser(DatabaseIdentifiable):

    __slots__ = (
        "_mgr",
        "_user",
        "_readings",
    )

################################################################################
    def __init__(self) -> None:

        pass

################################################################################
