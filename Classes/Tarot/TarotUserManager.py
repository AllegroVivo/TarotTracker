from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes import TarotManager
################################################################################

__all__ = ("TarotUserManager", )

################################################################################
class TarotUserManager:

    __slots__ = (
        "_mgr",
        "_users",
    )

################################################################################
    def __init__(self, mgr: TarotManager) -> None:

        self._mgr: TarotManager = mgr
        self._users: dict[int, TarotUser] = {}

################################################################################
