from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Awaitable, Sequence, Optional, Any

from discord import SelectOption, Interaction, ComponentType, ChannelType

from States import BaseState
from Classes.Core import MenuController
from UI.Common import *

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("GenericSelectState", )

OnSelect = Callable[[Interaction, Any, MenuController], Awaitable[None]]
OptionsProvider = Callable[[], Sequence[SelectOption]]

################################################################################
class GenericSelectState(BaseState):

    def __init__(
        self,
        *,
        header: Optional[str] = None,
        description: Optional[str] = None,
        placeholder: str,
        on_select: OnSelect,
        select_type: ComponentType = ComponentType.string_select,
        options: Optional[Sequence[SelectOption]] = None,
        options_provider: Optional[OptionsProvider] = None,
        channel_types: Optional[Sequence[ChannelType]] = None,
        multi_select: bool = False,
    ):

        super().__init__(None)
        self._header = header
        self._description = description
        self._placeholder = placeholder
        self._on_select = on_select
        self._options = options
        self._options_provider = options_provider
        self._select_type = select_type
        self._channel_types = channel_types
        self._multi_select = multi_select

    async def render(self, controller: MenuController, container: FroggeContainer):
        if self._header:
            container.add_text(f"## {self._header}")
        if self._description:
            container.add_text(self._description)

        opts = self._options if self._options is not None else (
            self._options_provider() if self._options_provider else None
        )
        if not opts:
            opts = [SelectOption(label="No Items Available", value="-1")]

        select = ActionSelect(
            on_select=self._on_select,
            placeholder=self._placeholder,
            options=opts,
            select_type=self._select_type,
            channel_types=self._channel_types,
            max_values=(
                1
                if not self._multi_select
                else (
                    len(opts)
                    if self._select_type == ComponentType.string_select
                    else 25
                )
            ),
            disabled=opts[0].value == "-1"
        )
        container.add_item(select)

        return container

class ActionSelect(Select):

    def __init__(
        self,
        on_select: OnSelect,
        *,
        placeholder: str,
        options: Optional[Sequence[SelectOption]] = None,
        select_type: Optional[ComponentType] = ComponentType.string_select,
        channel_types: Optional[Sequence[ChannelType]] = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
    ):

        if select_type == ComponentType.string_select:
            assert options is not None
        else:
            assert options is None

        super().__init__(
            select_type=select_type,
            channel_types=channel_types,
            placeholder=placeholder,
            options=options,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
        )
        self._on_select: OnSelect = on_select

    async def callback(self, interaction: Interaction):
        await interaction.edit()
        await self._on_select(interaction, self.values, self.view.controller)

################################################################################
