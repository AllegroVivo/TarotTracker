from __future__ import annotations
from discord.ui import Button
################################################################################

__all__ = ("FroggeButton", )

################################################################################
class FroggeButton(Button):

    @property
    def custom_id(self) -> str | None:

        return getattr(self._underlying, "custom_id", None)

################################################################################
