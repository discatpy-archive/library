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

from functools import reduce
from typing import Any, ClassVar, Dict, Tuple, Type, Union

from typing_extensions import Self

__all__ = (
    "BaseFlags",
    "Intents",
    "MessageFlags",
)


class flag_value:
    __slots__ = (
        "value",
        "name",
    )

    def __init__(self, value: int):
        self.value = value

    def __get__(self, instance: BaseFlags, owner: Type[BaseFlags]):
        if not isinstance(instance, BaseFlags):
            raise TypeError("Owner instance has to be of type BaseFlags!")

        return instance._has_flag(self.value)

    def __set__(self, instance: BaseFlags, value: bool):
        if not isinstance(instance, BaseFlags):
            raise TypeError("Owner instance has to be of type BaseFlags!")

        instance._set_flag(self.value, value)


class FlagMeta(type):
    """The metaclass for all flag classes.

    This metaclass takes all of the attributes from the given flag class and processes
    them so the ones that have an int value become a :class:`flag_value`. These flag values
    along with their names are stored into a separate valid_flags dict. This also calculates
    the default value.

    Parameters
    ----------
    inverted: :type:`bool`
        Whether or not this flag class is inverted.
    """

    def __new__(
        cls,
        name: str,
        bases: Tuple[type],
        attrs: Dict[str, Any],
        *,
        inverted: bool = False,
    ):
        valid_flags: Dict[str, int] = {}
        default_value = 0

        for k, v in attrs.items():
            if isinstance(v, flag_value):
                valid_flags[k] = v.value
                v.name = k

        if inverted:
            max_bits = max(valid_flags.values()).bit_length()
            default_value = -1 + (2**max_bits)

        attrs["VALID_FLAGS"] = valid_flags
        attrs["DEFAULT_VALUE"] = default_value

        return super(FlagMeta, cls).__new__(cls, name, bases, attrs)


class BaseFlags(metaclass=FlagMeta):
    """The base class for all flag classes.
    This class uses FlagMeta as its metaclass, so subclasses of this class also use that metaclass.

    Parameters
    ----------
    VALID_FLAGS: :type:`ClassVar[Dict[str, int]]`
        The valid flags for this flag class. Automatically generated via the metaclass.
    DEFAULT_VALUE: :type:`ClassVar[int]`
        The default value for this flag class. Automatically generated via the metaclass.
    value: :type:`int`
        The current value of this flag class instance. Automatically set to the default value.
    """

    VALID_FLAGS: ClassVar[Dict[str, int]]
    DEFAULT_VALUE: ClassVar[int]

    __slots__ = ("value",)

    def __init__(self, **kwargs):
        self.value: int = self.DEFAULT_VALUE

        for k, v in kwargs.items():
            if k not in self.VALID_FLAGS:
                raise TypeError(f"Invalid flag name {k} passed in")
            self._set_flag(self.VALID_FLAGS[k], v)

    def _get_error_msg(self, other: Union[BaseFlags, flag_value, int], op: str):
        form = '{0} and {1} are incompatible with operator "{2}"'
        if isinstance(other, flag_value):
            return form.format(type(self), f"flag_value {other.name}", op)
        elif isinstance(other, int):
            return form.format(type(self), f"int value {other}", op)
        else:  # BaseFlags and other types
            return form.format(type(self), type(other), op)

    def __or__(self, other: Union[BaseFlags, flag_value, int]):
        if isinstance(other, BaseFlags) and isinstance(other, self.__class__):
            return self.__class__._from_value(self.value | other.value)
        elif isinstance(other, flag_value) and other in self.__dict__:
            return self.__class__._from_value(self.value | other.value)
        elif isinstance(other, int) and other in self.VALID_FLAGS.values():
            return self.__class__._from_value(self.value | other)
        else:
            raise TypeError(self._get_error_msg(other, "|"))

    def __and__(self, other: Union[BaseFlags, flag_value, int]):
        if isinstance(other, BaseFlags) and isinstance(other, self.__class__):
            return self.__class__._from_value(self.value & other.value)
        elif isinstance(other, flag_value) and other in self.__dict__:
            return self.__class__._from_value(self.value & other.value)
        elif isinstance(other, int) and other in self.VALID_FLAGS.values():
            return self.__class__._from_value(self.value & other)
        else:
            raise TypeError(self._get_error_msg(other, "&"))

    def __add__(self, other: Union[BaseFlags, flag_value, int]):
        try:
            return self | other
        except TypeError:
            raise TypeError(self._get_error_msg(other, "+")) from None

    def __sub__(self, other: Union[BaseFlags, flag_value, int]):
        if isinstance(other, BaseFlags) and isinstance(other, self.__class__):
            return self.__class__._from_value(self.value & ~other.value)
        elif isinstance(other, flag_value) and other in self.__dict__:
            return self.__class__._from_value(self.value & ~other.value)
        elif isinstance(other, int) and other in self.VALID_FLAGS.values():
            return self.__class__._from_value(self.value & ~other)
        else:
            raise TypeError(self._get_error_msg(other, "-"))

    def __invert__(self):
        return self.__class__._from_value(~self.value)

    @classmethod
    def _from_value(cls: Type[Self], value: int) -> Self:
        self = cls.__new__(cls)
        self.value = value
        return self

    def _has_flag(self, v: int):
        return (self.value & v) == v

    def _set_flag(self, v: int, toggle: bool):
        if toggle:
            self.value |= v
        else:
            self.value &= ~v


class Intents(BaseFlags):
    GUILDS = flag_value(1 << 0)
    GUILD_MEMBERS = flag_value(1 << 1)
    GUILD_BANS = flag_value(1 << 2)
    GUILD_EMOJIS_AND_STICKERS = flag_value(1 << 3)
    GUILD_INTEGRATIONS = flag_value(1 << 4)
    GUILD_WEBHOOKS = flag_value(1 << 5)
    GUILD_INVITES = flag_value(1 << 6)
    GUILD_VOICE_STATES = flag_value(1 << 7)
    GUILD_PRESENCES = flag_value(1 << 8)
    GUILD_MESSAGES = flag_value(1 << 9)
    GUILD_MESSAGE_REACTIONS = flag_value(1 << 10)
    GUILD_MESSAGE_TYPING = flag_value(1 << 11)
    DIRECT_MESSAGES = flag_value(1 << 12)
    DIRECT_MESSAGE_REACTIONS = flag_value(1 << 13)
    DIRECT_MESSSAGE_TYPING = flag_value(1 << 14)
    MESSAGE_CONTENT = flag_value(1 << 15)
    GUILD_SCHEDULED_EVENTS = flag_value(1 << 16)
    # TODO: Automod

    @classmethod
    def ALL(cls: Type[Intents]) -> Intents:
        """A classmethod that returns a :class:`Intents` instance with everything set."""
        value = reduce(lambda a, b: a | b, cls.VALID_FLAGS.values())
        return cls._from_value(value)

    @classmethod
    def NONE(cls: Type[Intents]) -> Intents:
        """A classmethod that returns a :class:`Intents` instance with nothing set."""
        return cls._from_value(cls.DEFAULT_VALUE)

    @classmethod
    def DEFAULT(cls: Type[Intents]) -> Intents:
        """A classmethod that returns a :class:`Intents` instance with everything except privileged intents set."""
        self = cls.ALL()
        self.GUILD_PRESENCES = False
        self.GUILD_MEMBERS = False
        self.MESSAGE_CONTENT = False
        return self


class MessageFlags(BaseFlags):
    CROSSPOSTED = flag_value(1 << 0)
    IS_CROSSPOST = flag_value(1 << 1)
    SUPPRESS_EMBEDS = flag_value(1 << 2)
    SOURCE_MESSAGE_DELETED = flag_value(1 << 3)
    URGENT = flag_value(1 << 4)
    HAS_THREAD = flag_value(1 << 5)
    EPHEMERAL = flag_value(1 << 6)
    LOADING = flag_value(1 << 7)
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = flag_value(1 << 8)
