from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Awaitable, Sequence, Optional, Any, List

from discord import SelectOption, Interaction, ComponentType, ChannelType

from States import BaseState
from UI.Common import *
from Classes.Core import MenuController

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("GenericSelectState", )

OnSelect = Callable[[Interaction, Any, MenuController], Awaitable[None]]
OptionsProvider = Callable[[], Sequence[SelectOption]]

################################################################################
def _slice_page(items: Sequence[SelectOption], page: int, size: int) -> list[SelectOption]:

    start = page * size
    end = start + size
    return list(items[start:end])

################################################################################
def _page_count(total: int, size: int) -> int:

    if total <= 0:
        return 1
    return (total + size - 1) // size

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
        page_size: int = 25,
        enable_search: bool = False,
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
        self._page_size = page_size
        self._enable_search = enable_search

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

        if self._select_type != ComponentType.string_select or len(opts) <= min(self._page_size, 25):
            select = ActionSelect(
                on_select=self._on_select,
                placeholder=self._placeholder,
                options=opts,
                select_type=self._select_type,
                channel_types=self._channel_types,
                max_values=(1 if not self._multi_select else min(len(opts), 25)),
                disabled=opts[0].value == "-1"
            )
            container.add_item(select)
            return container

        paged = PaginatedActionSelect(
            self._on_select,
            controller,
            placeholder=self._placeholder,
            all_options=opts,
            multi_select=self._multi_select,
            page_size=min(self._page_size, 25),
        )
        prev_btn = _PrevPage(paged)
        next_btn = _NextPage(paged)

        container.add_item(paged)
        container.add_item(prev_btn)
        container.add_item(next_btn)

        return container

################################################################################
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
class PaginatedActionSelect(Select):
    def __init__(
        self,
        on_select: OnSelect,
        controller: MenuController,
        *,
        placeholder: str,
        all_options: Sequence[SelectOption],
        multi_select: bool = False,
        page_size: int = 25,
        page: int = 0,
    ):

        self._on_select: OnSelect = on_select
        self._controller: MenuController = controller

        self.all_options: List[SelectOption] = list(all_options)
        self.page_size = max(1, min(page_size, 25))  # Discord hard limit
        self.page = max(0, page)
        self.page_total = _page_count(len(self.all_options), self.page_size)

        current = _slice_page(self.all_options, self.page, self.page_size)
        max_values = 1 if not multi_select else max(1, min(len(current), 25))

        super().__init__(
            select_type=ComponentType.string_select,
            placeholder=f"{placeholder} — Page {self.page + 1}/{self.page_total}",
            options=current or [SelectOption(label="No Items Available", value="-1")],
            min_values=1,
            max_values=max_values,
            disabled=(len(current) == 0),
        )

    def go_page(self, page: int):
        self.page = max(0, min(page, self.page_total - 1))
        current = _slice_page(self.all_options, self.page, self.page_size)
        self.options = current or [SelectOption(label="No Items Available", value="-1")]
        self.max_values = 1 if self.max_values == 1 else max(1, min(len(current), 25))
        self.placeholder = self.placeholder.split(" — Page")[0] + f" — Page {self.page+1}/{self.page_total}"

    async def callback(self, interaction: Interaction):
        await interaction.edit()
        await self._on_select(interaction, self.values, self.view.controller)

################################################################################
class _PrevPage(Button):
    def __init__(self, select: PaginatedActionSelect):
        super().__init__(label="Previous", style=discord.ButtonStyle.secondary)
        self._select = select

    async def callback(self, interaction: Interaction):
        self._select.go_page(self._select.page - 1)
        # Re-render the message with updated select state
        await interaction.response.edit_message(view=self.view)

class _NextPage(Button):
    def __init__(self, select: PaginatedActionSelect):
        super().__init__(label="Next", style=discord.ButtonStyle.primary)
        self._select = select

    async def callback(self, interaction: Interaction):
        self._select.go_page(self._select.page + 1)
        await interaction.response.edit_message(view=self.view)

################################################################################
