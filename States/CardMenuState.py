from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Interaction, SelectOption, ButtonStyle

from Assets import BotEmojis, BotImages
from Classes.Common import GenericSelectState
from UI.Common import *

from .BaseState import BaseState
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import MenuController, TarotManager, TarotCard
################################################################################

__all__ = ("CardMenuState",)

################################################################################
class CardMenuState(BaseState):

    ctx: TarotCard

    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer:

        from .CardStatAttributeState import CardStatAttributeState
        from .CardMeaningState import CardMeaningState

        container.add_text(f"## Card Management for {self.ctx.deck.name}")

        async def set_name_callback(i: Interaction):
            await self.ctx.set_name(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(f"Card Name: `{self.ctx.name}`"),
                accessory=GenericCallbackButton(
                    set_name_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )
        container.add_separator()

        container.add_item(
            FroggeSection(
                TextDisplay(
                    "### Stat Tracker Attributes\n"
                    f"Pip Value: `{self.ctx.pip_value.proper_name if self.ctx.pip_value is not None else 'Not Set'}`\n"
                    f"Suit: `{self.ctx.suit.proper_name if self.ctx.suit is not None else 'Not Set'}`\n"
                    f"Arcana: `{self.ctx.arcana.proper_name}`"
                ),
                accessory=GenericTransitionButton(
                    CardStatAttributeState(self.ctx),
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil,
                )
            )
        )
        container.add_separator()

        container.add_item(
            FroggeSection(
                TextDisplay(
                    "### Card Meanings\n"
                    f"__**Upright Meaning Status:**__ {U.yes_no_emoji(self.ctx.meaning_upright)}\n"
                    f"__**Reversed Meaning Status:**__ {U.yes_no_emoji(self.ctx.meaning_reversed)}"
                ),
                accessory=GenericTransitionButton(
                    CardMeaningState(self.ctx),
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil
                )
            )
        )
        container.add_separator()

        container.add_item(
            FroggeSection(
                TextDisplay("### Card Image"),
                accessory=Thumbnail(self.ctx.image_url or BotImages.ThumbnailMissing)
            )
        )

        async def modify_image_callback(i: Interaction):
            await self.ctx.set_image(i)
            await controller.redraw(i)

        modify_image_btn = GenericCallbackButton(
            modify_image_callback,
            label="Modify",
            style=ButtonStyle.primary,
            emoji=BotEmojis.Image
        )

        async def clear_image_callback(i: Interaction):
            self.ctx.clear_image()
            await controller.redraw(i)

        clear_image_btn = GenericCallbackButton(
            clear_image_callback,
            label="Clear",
            style=ButtonStyle.danger,
            emoji=BotEmojis.Trash
        )

        row = ActionRow(modify_image_btn, clear_image_btn)
        container.add_item(row)
        container.add_separator()

        async def set_notes_callback(i: Interaction):
            await self.ctx.set_notes(i)
            await controller.redraw(i)

        container.add_item(
            FroggeSection(
                TextDisplay(f"### Notes:\n{self.ctx.notes or '`Not Set`'}"),
                accessory=GenericCallbackButton(
                    set_notes_callback,
                    label="Set",
                    style=ButtonStyle.primary,
                    emoji=BotEmojis.Pencil
                )
            )
        )

        return container

################################################################################
