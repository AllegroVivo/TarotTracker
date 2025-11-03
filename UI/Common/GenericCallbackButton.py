from __future__ import annotations

from typing import Callable, Awaitable, Optional

from discord import ButtonStyle, Interaction

from .FroggeButton import FroggeButton
################################################################################
class GenericCallbackButton(FroggeButton):

    def __init__(
        self,
        callback: Callable[[Interaction], Awaitable[None]],
        *,
        label: str,
        emoji: Optional[str] = None,
        style: ButtonStyle = ButtonStyle.secondary,
        disabled: bool = False,
        custom_id: Optional[str] = None
    ):

        super().__init__(style=style, label=label, emoji=emoji, disabled=disabled, custom_id=custom_id)
        self.callback = callback

################################################################################
