from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle, NotFound
from discord.ui import InputText, TextDisplay, Label

from .FroggeModal import FroggeModal
################################################################################

__all__ = ("BasicTextModal",)

################################################################################
class BasicTextModal(FroggeModal):

    def __init__(
        self,
        title: str,
        attribute: str,
        description: Optional[str] = None,
        cur_val: Optional[str] = None,
        example: Optional[str] = None,
        min_length: int = 1,
        max_length: int = 100,
        required: bool = True,
        instructions: Optional[str] = None,
        multiline: bool = False,
        return_interaction: bool = False,
    ):

        super().__init__(title=title)

        self.return_interaction: bool = return_interaction

        if instructions is not None:
            self.add_item(
                TextDisplay(
                    "## Instructions\n"
                    f"{instructions}"
                )
            )
        
        self.add_item(
            Label(
                label=attribute,
                item=InputText(
                    style=(
                        InputTextStyle.multiline if multiline
                        else InputTextStyle.singleline
                    ),
                    placeholder=example,
                    value=cur_val,
                    min_length=min_length if required else 0,
                    max_length=max_length,
                    required=required
                ),
                description=description,
            )
        )
        
    async def callback(self, interaction: Interaction):
        value = (
            (self.children[1].item.value or None)
            if len(self.children) == 2
            else (self.children[0].item.value or None)
        )
        self.value = (
            value if not self.return_interaction
            else (interaction, value)
        )
        self.complete = True

        if not self.return_interaction:
            try:
                # First try to silently consume the interaction
                await interaction.edit()
            except NotFound:
                # Otherwise do a quick & dirty follow-up
                await interaction.respond("** **", delete_after=0.1)
        self.stop()
        
################################################################################
