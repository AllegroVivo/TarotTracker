from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel
################################################################################

__all__ = (
    "TarotDeckSchema",
    "TarotCardSchema",
)

################################################################################
class SchemaBase(BaseModel):

    id: int

    class Config:
        from_attributes = True

################################################################################
class TarotDeckSchema(SchemaBase):

    name: Optional[str]
    description: Optional[str]
    cards: List[TarotCardSchema] = []

################################################################################
class TarotCardSchema(SchemaBase):

    name: Optional[str]
    arcana: Optional[int]
    suit: Optional[int]
    pip_value: Optional[int]
    meaning_upright: Optional[str]
    meaning_reversed: Optional[str]
    notes: Optional[str]

################################################################################
