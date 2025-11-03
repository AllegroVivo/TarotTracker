from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from discord import Cog

if TYPE_CHECKING:
    from Classes import TarotTracker
################################################################################
class Internal(Cog):

    def __init__(self, bot: TarotTracker):

        self.bot: TarotTracker = bot

################################################################################
    @Cog.listener("on_ready", once=True)
    async def load_internals(self) -> None:

        logging.info("Loading internals...")
        await self.bot.load_all()

        # logging.info("Starting tasks...")

        logging.info("TarotTracker Online!")

################################################################################
def setup(bot: TarotTracker) -> None:

    bot.add_cog(Internal(bot))

################################################################################
