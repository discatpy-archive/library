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

from typing import Any, Dict, List, Optional

from .types.message import MessageReference
from .embed import Embed

__all__ = (
    "APIType",
    "Messageable",
)

class APIType:
    """
    A raw API type. 
    All types here from the Discord API use this as a base.
    """

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        """
        Returns this API type from a provided Dict.

        Usually used to convert types directly from the API.
        """
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns this type converted into a Dict.

        Usually used to convert types for the API.
        """
        raise NotImplementedError

def _message_reference_to_dict(mr: MessageReference) -> Dict[str, Any]:
    ret_dict: Dict[str, Any] = {
        "message_id": mr.message_id,
        "fail_if_not_exists": mr.fail_if_not_exists,
    }

    if mr.channel_id:
        ret_dict["channel_id"] = mr.channel_id

    if mr.guild_id:
        ret_dict["guild_id"] = mr.guild_id

    return ret_dict

class Messageable:
    """
    An abstract type for API types that can send messages.
    """
    __slots__ = ()
    
    # Has to be implemented by the child class
    async def __send(self, json_data: Dict[str, Any]):
        raise NotImplementedError

    async def _send(
        self,
        content: str,
        /,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        message_reference: Optional[MessageReference] = None,
        tts: bool = False,
        # TODO: components, stickers, files/attachments
    ):
        json_data: Dict[str, Any] = {
            "content": content,
            "tts": tts,
        }

        if embed and embeds:
            raise RuntimeError("Both embed and embeds are specified!")

        if embed:
            json_data["embeds"] = [embed.to_dict()]

        if embeds:
            json_data["embeds"] = [e.to_dict() for e in embeds]

        if message_reference:
            json_data["message_reference"] = _message_reference_to_dict(message_reference)

        await self.__send(json_data)

    async def send(
        self,
        content: str,
        /,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: bool = False,
        # TODO: components, stickers, files/attachments
    ):
        await self._send(content, embed=embed, embeds=embeds, tts=tts)