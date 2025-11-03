from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import ButtonStyle, Interaction, PartialEmoji
from .FroggeButton import FroggeButton

if TYPE_CHECKING:
    from Classes import BaseState
################################################################################
class GenericTransitionButton(FroggeButton):

    def __init__(
        self,
        transition_to: BaseState,
        *,
        label: str,
        style: ButtonStyle,
        emoji: Optional[PartialEmoji] = None,
        disabled: bool = False,
        replace: bool = False
    ):

        super().__init__(style=style, label=label, emoji=emoji, disabled=disabled)

        self.next_state = transition_to
        self.replace = replace

    async def callback(self, i: Interaction):
        await self.view.controller.transition_to(self.next_state, i, replace=self.replace)

################################################################################
