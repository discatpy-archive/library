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

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..core.types import Snowflake
from .message import Message

if TYPE_CHECKING:
    #from .client import Client
    from .embed import Embed

__all__ = ("Messageable",)


class Messageable:
    """
    An abstract type for API types that can send messages.
    """

    client: Any
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
            tts=tts,
        )

    async def bulk_delete(self, messages: List[Message]):
        """
        Bulk deletes a list of messages.

        Parameters
        ----------
        messages: :type:`List[Message]`
            The list of messages to bulk delete.
        """
        ids: List[Snowflake] = [m.id for m in messages]
        return await self.client.http.bulk_delete_messages(ids, self.raw_id)

    async def history(
        self,
        limit: int = 50,
        /,
        around: Optional[Snowflake] = None,
        before: Optional[Snowflake] = None,
        after: Optional[Snowflake] = None,
    ):
        # TODO: Move iterator implementation to a separate class
        msgs: List[Dict[str, Any]]
        if limit <= 100:
            msgs = await self.client.http.get_messages(
                self.raw_id, limit=limit, around=around, before=before, after=after
            )
        else:
            # paginator mode activated
            amount_of_loops = limit // 100
            msgs = []
            for _ in range(amount_of_loops):
                msgs.extend(
                    await self.client.http.get_messages(
                        self.raw_id, limit=limit, around=around, before=before, after=after
                    )
                )
                if len(msgs) != 100:
                    # we either hit the limit of the channel or the limit according to the parameters
                    break
                else:
                    if limit > 100:
                        limit -= 100
                    before = msgs[0].get("id")

        for m in msgs:
            yield Message(m, self.client)

    async def pins(self):
        msgs: List[Dict[str, Any]] = await self.client.http.get_pinned_messages(self.raw_id)

        for m in msgs:
            yield Message(m, self.client)
