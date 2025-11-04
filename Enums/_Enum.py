from __future__ import annotations

from enum import IntEnum
from typing import List

from discord import SelectOption
################################################################################

__all__ = ("FroggeEnum",)

################################################################################
class FroggeEnum(IntEnum):

    @property
    def proper_name(self) -> str:

        return self.name.replace("_", " ")

################################################################################
    @classmethod
    def select_options(cls) -> List[SelectOption]:

        return [x.select_option for x in cls]

################################################################################
    @property
    def select_option(self) -> SelectOption:

        return SelectOption(label=self.proper_name, value=str(self.value))

################################################################################
