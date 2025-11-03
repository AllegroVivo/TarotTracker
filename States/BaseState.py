from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from Classes import MenuController
    from UI.Common import FroggeContainer
################################################################################

__all__ = ("BaseState", )

################################################################################
class BaseState(ABC):

    id: str

    __slots__ = (
        "ctx",
    )

################################################################################
    def __init__(self, ctx: Any) -> None:

        self.ctx = ctx

################################################################################
    @abstractmethod
    async def render(self, controller: MenuController, container: FroggeContainer) -> FroggeContainer: ...

################################################################################
