from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union, List, Tuple, Any, Type

from discord import Colour, EmbedField, Embed

from Assets import BotEmojis
from .Colors import CustomColor
from .ErrorMessage import ErrorMessage

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("Utilities", )

_IRREGULAR_PLURALS = {
    "person": "people",
    # Add here as needed eg: "child": "children", etc.
}

################################################################################
class Utilities:

    @staticmethod
    def camel_to_snake(name: str) -> str:
        # Handles acronyms like URLThing -> url_thing
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

################################################################################
    @staticmethod
    def pluralize(s: str) -> str:

        if s in _IRREGULAR_PLURALS:
            return _IRREGULAR_PLURALS[s]
        if s.endswith(("s", "x", "z", "ch", "sh")):
            return s + "es"
        if len(s) >= 2 and s.endswith("y") and s[-2] not in "aeiou":
            return s[:-1] + "ies"
        return s + "s"

################################################################################
    @staticmethod
    def split_class_name(_type: Type[Any]) -> str:
        """
        Split a CamelCase or PascalCase class name into words,
        keeping acronyms together.

        Examples:
            "DatabaseLoadingManagerObject" -> "Database Loading Manager Object"
            "HTTPRequestHandler" -> "HTTP Request Handler"
            "FFXIVRPVenueBot" -> "FFXIV RP Venue Bot"
        """
        # Regex explanation:
        # - [A-Z]+(?=[A-Z][a-z])   : consecutive capitals before a lowercase (acronym like 'HTTP')
        # - [A-Z][a-z]+            : normal CapitalizedWord
        # - [A-Z]+                 : trailing capitals (like 'RP', 'ID')
        # - \d+                    : numbers, if present
        parts = re.findall(r"[A-Z]+(?=[A-Z][a-z])|[A-Z][a-z]+|[A-Z]+|\d+", _type.__name__)
        return " ".join(parts)

################################################################################
    @staticmethod
    def make_embed(
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        color: Optional[Union[Colour, int]] = None,
        thumbnail_url: Optional[str] = None,
        image_url: Optional[str] = None,
        author_text: Optional[str] = None,
        author_url: Optional[str] = None,
        author_icon: Optional[str] = None,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        timestamp: Union[datetime, bool] = False,
        fields: Optional[List[Union[Tuple[str, Any, bool], EmbedField]]] = None,
        _color_override: bool = False
    ) -> Embed:
        """Creates and returns a Discord embed with the provided parameters.

        All parameters are optional.

        Parameters:
        -----------
        title: :class:`str`
            The embed's title.

        description: :class:`str`
            The main text body of the embed.

        url: :class:`str`
            The URL for the embed title to link to.

        color: Optional[Union[:class:`Colour`, :class:`int`]]
            The desired accent color. Defaults to :func:`colors.random_all()`

        thumbnail_url: :class:`str`
            The URL for the embed's desired thumbnail image.

        image_url: :class:`str`
            The URL for the embed's desired main image.

        footer_text: :class:`str`
            The text to display at the bottom of the embed.

        footer_icon: :class:`str`
            The icon to display to the left of the footer text.

        author_name: :class:`str`
            The text to display at the top of the embed.

        author_url: :class:`str`
            The URL for the author text to link to.

        author_icon: :class:`str`
            The icon that appears to the left of the author text.

        timestamp: Union[:class:`datetime`, `bool`]
            Whether to add the current time to the bottom of the embed.
            Defaults to ``False``.

        fields: Optional[List[Union[Tuple[:class:`str`, Any, :class:`bool`], :class:`EmbedField`]]]
            List of tuples or EmbedFields, each denoting a field to be added
            to the embed. If entry is a tuple, values are as follows:
                0 -> Name | 1 -> Value | 2 -> Inline (bool)
            Note that in the event of a tuple, the value at index one is automatically cast to a string for you.

        Returns:
        --------
        :class:`Embed`
            The finished embed object.
        """

        if title:
            if not title.startswith("__") and not title.endswith("__"):
                title = f"__{title}__"

        embed = Embed(
            colour=(
                color
                if color is not None
                else CustomColor.random_all()
            ) if not _color_override else color,
            title=title,
            description=description,
            url=url
        )

        embed.set_thumbnail(url=thumbnail_url)
        embed.set_image(url=image_url)

        if author_text is not None:
            embed.set_author(
                name=author_text,
                url=author_url,
                icon_url=author_icon
            )

        if footer_text is not None:
            embed.set_footer(
                text=footer_text,
                icon_url=footer_icon
            )

        if isinstance(timestamp, datetime):
            embed.timestamp = timestamp
        elif timestamp is True:
            embed.timestamp = datetime.now()

        if fields is not None:
            if all(isinstance(f, EmbedField) for f in fields):
                embed.fields = fields
            else:
                for f in fields:
                    if isinstance(f, EmbedField):
                        embed.fields.append(f)
                    elif isinstance(f, tuple):
                        embed.add_field(name=f[0], value=f[1], inline=f[2])
                    else:
                        continue

        return embed

################################################################################
    @staticmethod
    def make_error(
        *,
        title: str,
        message: str,
        solution: str,
        description: Optional[str] = None
    ) -> Embed:

        # We only need this function as a basic wrapper, so we don't need to
        # subclass ErrorMessage every single time. v5 edit. ~SP 8/19/24
        return ErrorMessage(
            title=title,
            message=message,
            solution=solution,
            description=description
        )

################################################################################
    @staticmethod
    def yes_no_emoji(value: Any, _old: bool = False) -> str:

        return str(
            (BotEmojis.CheckGreen if not _old else BotEmojis.Check)
            if bool(value)
            else (BotEmojis.Cross if not _old else BotEmojis.CrossOld)
        )

################################################################################
    @staticmethod
    def string_clamp(text: Optional[str], length: int) -> str:

        if text is None:
            return "N/A"

        return text[:length - 3] + "..." if len(text) > length else text

################################################################################
