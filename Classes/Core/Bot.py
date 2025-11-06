from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Optional

from discord import Bot, TextChannel, Interaction, Attachment

from Database import Database
from ..Tarot import TarotManager

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("TarotTracker", )

################################################################################
class TarotTracker(Bot):

    __slots__ = (
        "db",
        "tarot_manager",
        "_loaded",
        "_img_dump",
        "_error_dump",
    )

    IMAGE_DUMP = 991902526188302427
    ERROR_OUT = 974493350919045190

################################################################################
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._loaded: bool = False
        self._img_dump: TextChannel = None  # type: ignore
        self._error_dump: TextChannel = None  # type: ignore

        self.db: Database = Database(self.dev_mode)
        self.tarot_manager: TarotManager = TarotManager(self)

################################################################################
    async def load_all(self) -> None:

        self._loaded = False

        logging.info("Initializing... Fetching Dump Channels")
        self._img_dump = await self.fetch_channel(self.IMAGE_DUMP)
        self._error_dump = await self.fetch_channel(self.ERROR_OUT)

        logging.info("Retrieving full database payload...")
        payload = self.db.load_all()

        logging.info("Loading Tarot Manager...")
        await self.tarot_manager.load_all(payload)

        self._loaded = True

################################################################################
    @property
    def dev_mode(self) -> bool:

        return self.debug_guilds is not None

################################################################################
    async def is_loaded(self, interaction: Interaction) -> bool:

        if self._loaded:
            return True

        await interaction.respond(
            "The application is still starting up. Please wait a few minutes and try your command again...",
            ephemeral=True
        )
        return False

################################################################################
