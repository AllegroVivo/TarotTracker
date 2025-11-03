from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from discord import Interaction

from .TarotDeckManager import TarotDeckManager
from States import AdminMenuState

if TYPE_CHECKING:
    from Classes import TarotTracker
################################################################################

__all__ = ("TarotManager", )

################################################################################
class TarotManager:

    __slots__ = (
        "_state",
        "decks",
    )

################################################################################
    def __init__(self, state: TarotTracker) -> None:

        self._state: TarotTracker = state

        self.decks: TarotDeckManager = TarotDeckManager(self)

################################################################################
    async def load_all(self, payload: Dict[str, any]) -> None:

        self.decks.load_all(payload["decks"])

################################################################################
    @property
    def bot(self) -> TarotTracker:

        return self._state

################################################################################
    async def admin_menu(self, interaction: Interaction) -> None:

        from ..Core import MenuController

        controller = MenuController(interaction.user, self._state)
        await controller.begin(interaction, AdminMenuState(self), ephemeral=False)

################################################################################
