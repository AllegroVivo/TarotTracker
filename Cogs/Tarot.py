from discord import (
    ApplicationContext,
    AutocompleteContext,
    Cog,
    Member,
    Option,
    SlashCommandGroup,
    SlashCommandOptionType,
    User
)
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from Classes import TarotTracker
################################################################################
def _autocomplete_card_names(ctx: AutocompleteContext) -> List[str]:

    bot: "TarotTracker" = ctx.bot  # type: ignore
    return bot.tarot_manager.autocomplete_card_names(ctx)

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

    tarot = SlashCommandGroup(
        name="tarot",
        description="Tarot reading commands."
    )

################################################################################
    @tarot.command(
        name="lookup",
        description="Lookup a given tarot card's information."
    )
    async def tarot_lookup(
        self,
        ctx: ApplicationContext,
        card_name: Option(
            SlashCommandOptionType.string,
            name="card",
            description="The tarot card to look up.",
            required=True,
            autocomplete=_autocomplete_card_names,
        )
    ) -> None:

        if not await self.bot.is_loaded(ctx.interaction):
            return

        await self.bot.tarot_manager.lookup_card(ctx.interaction, card_name)

################################################################################
def setup(bot: "TarotTracker") -> None:

    bot.add_cog(Tarot(bot))

################################################################################
