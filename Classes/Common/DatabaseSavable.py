from __future__ import annotations

from typing import Any, Dict

from .Identifiable import Identifiable
################################################################################

__all__ = ("DatabaseSavable", "DatabaseIdentifiable")

################################################################################
class DatabaseSavable:

    def update(self) -> None:

        raise NotImplementedError("This method should be implemented by subclasses.")

################################################################################
    def to_dict(self) -> Dict[str, Any]:

        raise NotImplementedError("This method should be implemented by subclasses.")

################################################################################
    def delete(self) -> None:

        raise NotImplementedError("This method should be implemented by subclasses.")

################################################################################
class DatabaseIdentifiable(Identifiable, DatabaseSavable):

    def __init__(self, id: int) -> None:
        super().__init__(id)
        DatabaseSavable.__init__(self)

################################################################################
