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
from datetime import datetime

from .types.snowflake import Snowflake
from .types.message import *
from .abs import APIType
from .mixins import SnowflakeMixin
from .user import User

class Message(APIType, SnowflakeMixin):
    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        id: Snowflake = d.get("id")
        channel_id: Snowflake = d.get("channel_id")
        guild_id: Optional[Snowflake] = d.get("guild_id")
        # TODO: Check if the message author is instead a Webhook
        author: User = User.from_dict(d.get("author"))
        # TODO: member attribute
        content: str = d.get("content")
        timestamp: datetime = datetime.fromisoformat(d.get("timestamp"))
        edited_timestamp: Optional[datetime] = datetime.fromisoformat(d.get("edited_timestamp")) if d.get("edited_timestamp") is not None else None
        tts: bool = d.get("tts")
        mention_everyone: bool = d.get("mention_everyone")
        # TODO: mentions, attachments, embeds
        raw_reactions: Optional[List[Dict[str, Any]]] = d.get("reactions")
        reactions: Optional[List[Reaction]] = None

        if raw_reactions:
            reactions = []
            for i in raw_reactions:
                reaction = Reaction()
                reaction.count = i.get("count")
                reaction.me = i.get("me")
                reaction.emoji = PartialEmoji()
                reaction.emoji.id = i.get("emoji").get("id")
                reaction.emoji.name = i.get("emoji").get("name")

                reactions.append(reaction)

        pinned: bool = d.get("pinned")
        type: int = d.get("type")
        # TODO: application, application_id
        raw_activity: Dict[str, Any] = d.get("activity")
        activity: MessageActivity = MessageActivity()
        activity.type = raw_activity.get("type")
        activity.party_id = raw_activity.get("party_id")
        # TODO: message reference
        flags: Optional[int] = d.get("flags")
        referenced_message: Optional[Message] = cls.from_dict(d.get("referenced_message")) if d.get("referenced_message") is not None else None
        # TODO: interaction & components, thread, sticker_items
