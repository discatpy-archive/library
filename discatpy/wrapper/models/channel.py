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

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union, cast

from discord_typings import (
    CategoryChannelData,
    DMChannelData,
    NewsChannelData,
    PartialChannelData,
    PermissionOverwriteData,
    TextChannelData,
    VoiceChannelData,
)

from ...core.enums import ChannelType
from ...core.types import EllipsisOr, GuildChannelData
from ..utils import parse_data
from .abc import Messageable
from .object import DiscordObject
from .user import User

if TYPE_CHECKING:
    from ..bot import Bot
    from .guild import Guild

__all__ = ("GuildChannel",)


class GuildChannel(DiscordObject):
    __slots__ = ("id", "type", "guild_id", "position", "permission_overwrites", "name", "parent_id",)

    def __init__(self, *, data: GuildChannelData, bot):
        DiscordObject.__init__(self, data=data, bot=bot)

        self.id: int = int(data["id"])
        self.type: ChannelType = ChannelType(data["type"])
        # this has None in its return type which is illegal for guild_id, but guild_id will never be None
        self.guild_id: EllipsisOr[int] = parse_data(  # type: ignore
            data, 
            "guild_id", 
            int, 
            (data.get("guild_id"),)
        )
        self.position: int = data["position"]
        self.permission_overwrites: List[PermissionOverwriteData] = data["permission_overwrites"]
        self.name: str = data["name"]
        self.parent_id: Optional[int] = parse_data(data, "parent_id", int, (data["parent_id"],))

    async def edit(
        self, 
        *, 
        reason: Optional[str] = None,
        name: EllipsisOr[str] = ..., 
        type: EllipsisOr[ChannelType] = ...,
        position: EllipsisOr[int] = ...,
        permission_overwrites: EllipsisOr[List[PermissionOverwriteData]] = ...,
        **kwargs,
    ) -> GuildChannel:
        if self.guild_id is ...:
            raise ValueError("Welp you chose the wrong Gateway Event dispatch to do this")

        if kwargs and self.__class__ is GuildChannel:
            raise ValueError("Users cannot set **kwargs, this is only for the internal API")

        if type is not ...:
            if self.type not in (ChannelType.GUILD_TEXT, ChannelType.GUILD_NEWS):
                raise TypeError(f"You cannot convert a channel of type {self.type.name}!")
            if type not in (ChannelType.GUILD_TEXT, ChannelType.GUILD_NEWS):
                # Pyright cannot infer that the parameter type at this point will have to be of type ChannelType
                raise TypeError(f"You cannot convert a channel to type {type.name}!")  # type: ignore

        new_channel_data = await self._bot.http.modify_channel(
            self.guild_id, # type: ignore  # PYRIGHT USE YOUR PROGRAM BRAIN TO INFER THAT THIS HAS TO BE INT
            reason=reason,
            name=name,
            type=type,
            position=position,
            permission_overwrites=permission_overwrites,
            **kwargs,
        )
        new_channel = self.__class__.__new__(self.__class__)
        new_channel.__init__(data=new_channel_data, bot=self._bot)
        return new_channel


class DMChannel(DiscordObject):
    __slots__ = (
        "id",
        "type",
        "last_message_id",
        "recipients",
        "last_pin_timestamp",
    )

    def __init__(self, *, data: DMChannelData, bot):
        DiscordObject.__init__(self, data=data, bot=bot)

        self.id: int = int(data["id"])
        self.type: ChannelType = ChannelType(data["type"])
        self.last_message_id: Optional[int] = parse_data(
            data, 
            "last_message_id", 
            int, 
            (data["last_message_id"],)
        )
        self.recipients: List[User] = [User(data=u, bot=self._bot) for u in data["recipients"]]
        # Pyright cannot infer that the default parameter for this is set to ...
        self.last_pin_timestamp: EllipsisOr[Optional[str]] = parse_data(  # type: ignore
            data,
            "last_pin_timestamp",
            datetime.fromisoformat,
            (data.get("last_pin_timestamp"),),
        )
