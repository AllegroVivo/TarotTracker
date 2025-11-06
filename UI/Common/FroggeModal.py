from __future__ import annotations

from typing import Any, Optional

from discord.ui import DesignerModal
################################################################################

__all__ = ("FroggeModal",)

################################################################################
class FroggeModal(DesignerModal):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.complete: bool = False
        self.value: Optional[Any] = None

################################################################################
        