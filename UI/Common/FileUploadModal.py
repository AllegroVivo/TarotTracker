from __future__ import annotations

from typing import Optional

from discord import Interaction, NotFound
from discord.ui import FileUpload, TextDisplay, Label

from .FroggeModal import FroggeModal
################################################################################

__all__ = ("FileUploadModal",)

################################################################################
class FileUploadModal(FroggeModal):

    def __init__(
        self,
        title: str,
        attribute: str,
        description: Optional[str] = None,
        required: bool = True,
        max_files: int = 1,
        instructions: Optional[str] = None
    ):

        super().__init__(title=title)

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
                item=FileUpload(
                    min_values=1 if required else 0,
                    max_values=max_files,
                    required=required,
                ),
                description=description,
            )
        )
        
    async def callback(self, interaction: Interaction):
        values = (
            (self.children[1].item.values or None)
            if len(self.children) == 2
            else (self.children[0].item.values or None)
        )
        self.value = values[0] if len(values) == 1 else values
        self.complete = True

        try:
            # First try to silently consume the interaction
            await interaction.edit()
        except NotFound:
            # Otherwise do a quick & dirty follow-up
            await interaction.respond("** **", delete_after=0.1)

        self.stop()
        
################################################################################
