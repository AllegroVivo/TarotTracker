from discord import (
    ApplicationContext,
    Cog,
    Member,
    Option,
    SlashCommandGroup,
    SlashCommandOptionType,
    User
)
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Classes import TarotTracker
################################################################################
class Tarot(Cog):

    def __init__(self, bot: "TarotTracker"):

        self.bot: "TarotTracker" = bot

################################################################################

    admin = SlashCommandGroup(
        name="admin",
        description="Tarot administration commands."
    )

################################################################################
    @admin.command(
        name="menu",
        description="View the tarot admin menu."
    )
    async def admin_menu(self, ctx: ApplicationContext) -> None:

        if not await self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.tarot_manager.admin_menu(ctx.interaction)

################################################################################
def setup(bot: "TarotTracker") -> None:

    bot.add_cog(Tarot(bot))

################################################################################
