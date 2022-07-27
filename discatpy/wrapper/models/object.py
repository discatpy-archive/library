"""
The MIT License (MIT)

Copyright (c) 2022-present EmreTech

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

if TYPE_CHECKING:
    from ..bot import Bot

__all__ = ("DiscordObject",)


class DiscordObject:
    """A raw Discord Object.
    All models here from the Discord API use this as a base.

    This base class uses the :class:`DiscordObjectMeta` metaclass for its subclasses.

    Attributes
    ----------
    bot: :Class:`Bot`
        The bot tied to this Discord Object.
    as_dict: Mapping[:class:`str`, Any]
        The dict version of this object.
    """

    __slots__ = (
        "_bot",
        "as_dict",
    )

    def __init__(self, *, data: Mapping[str, Any], bot: Bot) -> None:
        self._bot = bot
        self.as_dict = data
