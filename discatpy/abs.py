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

from typing import Any, Dict, List, Optional, overload, TYPE_CHECKING

from .types.snowflake import *
from .embed import Embed

if TYPE_CHECKING:
    from .client import Client

__all__ = (
    "APIType",
    "Messageable",
)

class APIType:
    """
    A raw API type. 
    All types here from the Discord API use this as a base.

    Attributes
    ----------
    client: :type:`Client`
        The parent client of this type.
    d: :type:`Dict[str, Any]`
        The raw data from the API.
    """
    if TYPE_CHECKING:
        client: Client

    client = None
    d: Dict[str, Any] 

    def __init__(self, d: Dict[str, Any], client):
        self.client = client
        self.d = d

    if TYPE_CHECKING:
        @overload
        @classmethod
        def from_dict(cls, client: Client, d: Dict[str, Any]):
            ...

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        """
        Returns this API type from a provided Dict.

        Usually used to convert types directly from the API.

        Parameters
        ----------
        client: :type:`Client`
            The parent client of this type.
        d: :type:`Dict[str, Any]`
            The raw data from the API.
        """
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns this type converted into a Dict.

        Usually used to convert types for the API.
        """
        raise NotImplementedError

class Messageable:
    """
    An abstract type for API types that can send messages.
    """
    client = None
    raw_id: Snowflake

    async def send(
        self,
        content: str,
        /,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: bool = False,
        # TODO: components, stickers, files/attachments
    ):
        """
        Sends a message.

        Parameters
        ----------
        content: str
            The content of the message.
        embed: Optional[Embed]
            The embed to send.
        embeds: Optional[List[Embed]]
            A list of embeds to send.
        tts: bool
            Whether the message should be sent using text-to-speech.
        """
        await self.client.http.send_message(
            self.raw_id,
            content,
            embed=embed,
            embeds=embeds,
            msg_reference=None,
            tts=tts
        )