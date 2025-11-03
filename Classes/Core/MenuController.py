from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import User, Message, Interaction, NotFound

from UI.Common import FroggeContainer, FroggeMenuView

if TYPE_CHECKING:
    from Classes import BaseState, TarotTracker
################################################################################

__all__ = ("MenuController",)

################################################################################
class MenuController:

    __slots__ = (
        "owner",
        "ctx",
        "_close_on_complete",
        "_message",
        "_stack",
        "_current",
    )

################################################################################
    def __init__(self, owner: User, ctx: TarotTracker, *, close_on_complete: bool = True) -> None:

        self.owner: User = owner
        self.ctx: TarotTracker = ctx

        self._close_on_complete: bool = close_on_complete
        self._message: Optional[Message] = None
        self._stack: List[BaseState] = []
        self._current: Optional[BaseState] = None

################################################################################
    async def begin(self, interaction: Interaction, initial: BaseState, *, ephemeral: bool = True):

        self._stack.append(initial)
        self._current = initial

        container = await initial.render(self, FroggeContainer())
        view = FroggeMenuView(self, container, show_nav_buttons=False)
        await interaction.response.send_message(view=view, ephemeral=ephemeral)

        self._message = await interaction.original_response()

        await view.wait()

################################################################################
    async def redraw(self, interaction: Interaction = None):

        if interaction and not interaction.response.is_done():
            await interaction.edit()

        if not self._current:
            return

        container = await self._current.render(self, FroggeContainer())
        view = FroggeMenuView(self, container, show_nav_buttons=len(self._stack) != 1)

        if self._message:
            try:
                await self._message.edit(view=view)
            except NotFound:
                # If the message was deleted, we can ignore this error
                pass

################################################################################
    async def transition_to(self, new_state: BaseState, interaction: Interaction = None, *, replace: bool = False):

        if interaction and not interaction.response.is_done():
            await interaction.edit()

        if replace:
            if self._stack:
                self._stack[-1] = new_state
        else:
            self._stack.append(new_state)

        self._current = new_state
        container = await new_state.render(self, FroggeContainer())
        view = FroggeMenuView(self, container, show_nav_buttons=len(self._stack) != 1)

        if self._message:
            await self._message.edit(view=view)

################################################################################
    async def back(self, interaction: Interaction = None):

        if interaction and not interaction.response.is_done():
            await interaction.edit()

        if len(self._stack) <= 1:
            return

        self._stack.pop()
        self._current = self._stack[-1]

        container = await self._current.render(self, FroggeContainer())
        view = FroggeMenuView(self, container, show_nav_buttons=len(self._stack) != 1)

        if self._message:
            await self._message.edit(view=view)

################################################################################
    async def end(self):

        if self._message and self._close_on_complete:
            try:
                await self._message.delete()
            except NotFound:
                pass

        self._stack.clear()
        self._current = None

################################################################################
    async def home(self, interaction: Interaction = None) -> None:

        if interaction and not interaction.response.is_done():
            await interaction.edit()

        if not self._stack:
            return

        home = self._stack[0]
        self._stack = [home]
        self._current = self._stack[0]

        container = await self._current.render(self, FroggeContainer())
        view = FroggeMenuView(self, container, show_nav_buttons=False)

        if self._message:
            await self._message.edit(view=view)

################################################################################
