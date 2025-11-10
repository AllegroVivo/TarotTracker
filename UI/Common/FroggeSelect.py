from __future__ import annotations

from typing import List, Callable, Awaitable

from discord import Interaction, SelectOption
from discord.ui import Select
################################################################################

__all__ = ("FroggeSelect",)

################################################################################
class FroggeSelect(Select):

    def __init__(
        self,
        callback_func: Callable[[Interaction, List[str]], Awaitable[None]],
        placeholder: str,
        options: List[SelectOption],
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
    ) -> None:

        super().__init__(
            placeholder=placeholder, min_values=min_values,
            max_values=max_values, options=options, disabled=disabled
        )
        self._cb_func: Callable[[Interaction, List[str]], Awaitable[None]] = callback_func

    async def callback(self, interaction: Interaction) -> None:
        await self._cb_func(interaction, self.values)

################################################################################
