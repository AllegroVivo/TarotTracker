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

    canonical_id: Optional[int]
    name: Optional[str]
    meaning_upright: Optional[str]
    meaning_reversed: Optional[str]
    upright_keywords: Optional[str]
    reversed_keywords: Optional[str]
    description: Optional[str]

################################################################################
