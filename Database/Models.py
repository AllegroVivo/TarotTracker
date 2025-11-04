from __future__ import annotations

import json
import re
from enum import IntEnum
from typing import Optional, List, Type, Any

from sqlalchemy import (
    TypeDecorator, TEXT, Integer, Boolean, MetaData, String,
    ForeignKey, UniqueConstraint, Text, Dialect
)
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
)

from Enums import *
from Utilities import Utilities as U
################################################################################

__all__ = (
    "TarotCardModel",
    "TarotDeckModel",
    "BaseModel",
)

################################################################################
class BaseModel(DeclarativeBase):
    """Base class for all ORM models."""
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    DC_TYPE: Type[T] = None  # type: ignore

    # noinspection PyMethodParameters
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # If a subclass explicitly sets __tablename__, honor it
        if "__tablename__" in cls.__dict__:
            return cls.__dict__["__tablename__"]

        base = re.sub(r"Model$", "", cls.__name__)  # EditionContributionModel -> EditionContribution
        return U.pluralize(U.camel_to_snake(base))  # -> edition_contribution -> edition_contributions

################################################################################
class ArrayOrJSON(TypeDecorator):
    """Uses Postgres ARRAY for native arrays, JSON (or TEXT) fallback elsewhere."""
    impl = TEXT
    cache_ok = True

    def __init__(self, inner_type=Integer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inner_type = inner_type  # E.g., Integer or String

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_ARRAY(self.inner_type))
        else:
            return dialect.type_descriptor(TEXT())  # Stored as JSON string in SQLite

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return value  # Pass native list directly to Postgres
        return json.dumps(value)  # Store as JSON text elsewhere

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        if dialect.name == "postgresql":
            return value  # Already a native Python list
        return json.loads(value)  # Convert JSON string back to list

################################################################################
class NormalizedBoolean(TypeDecorator):
    """
    A cross-dialect BOOLEAN type.
    - Stores as INTEGER(0/1) in SQLite.
    - Uses native BOOLEAN in Postgres (or other dialects).
    """
    impl = Boolean
    cache_ok = True

    def load_dialect_impl(self, dialect):
        # SQLite has no BOOLEAN → fallback to Integer
        if dialect.name == "sqlite":
            return dialect.type_descriptor(Integer())
        return dialect.type_descriptor(Boolean())

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return 1 if bool(value) else 0 if dialect.name == "sqlite" else bool(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return bool(value)

################################################################################
class DBEnum(TypeDecorator):
    """
    A cross-dialect ENUM type.
    - Stores IntEnum as INTEGER in the DB and returns IntEnum in Python.
    """
    impl = Integer
    cache_ok = True

    def __init__(self, enum_cls: Type[IntEnum], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_cls = enum_cls

    def process_bind_param(self, value: Optional[Any], dialect: Dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_cls):
            return int(value.value)
        return int(value)

    def process_result_value(self, value: Optional[Any], dialect: Dialect):
        if value is None:
            return None
        return self.enum_cls(int(value))

    @property
    def python_type(self):
        return self.enum_cls

################################################################################
class IDMixin:
    """Base class for models with an integer primary key ID."""
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

################################################################################
class TarotDeckModel(BaseModel, IDMixin):

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    cards: Mapped[List[TarotCardModel]] = relationship(
        "TarotCardModel",
        back_populates="deck",
        cascade="all, delete-orphan",
    )

################################################################################
class TarotCardModel(BaseModel, IDMixin):

    deck_id: Mapped[int] = mapped_column(ForeignKey("tarot_decks.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    arcana: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    suit: Mapped[Optional[int]] = mapped_column(Integer)
    pip_value: Mapped[Optional[int]] = mapped_column(Integer)
    meaning_upright: Mapped[Optional[str]] = mapped_column(Text)
    meaning_reversed: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))

    __table_args__ = (
        UniqueConstraint("deck_id", "arcana", "suit", "pip_value", name="uq_tarot_deck_identifiers"),
    )

    # Relationships
    deck: Mapped[TarotDeckModel] = relationship("TarotDeckModel", back_populates="cards")

################################################################################
