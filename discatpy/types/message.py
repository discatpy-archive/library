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

from typing import Any, Dict, Optional

from .snowflake import *

__all__ = (
    "MessageActivityType",
    "MessageActivity",
    "MessageType",
    "MessageFlags",
    "PartialEmoji",
    "Reaction",
    "MessageReference",
    "to_message_activity",
    "to_partial_emoji",
    "to_reaction",
    "to_message_reference",
)

class MessageActivityType:
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5

class MessageActivity:
    type: int
    party_id: Optional[str]

class MessageType:
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    GUILD_MEMBER_JOIN = 7
    USER_PREMIUM_GUILD_SUBSCRIPTION = 8
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_1 = 9
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_2 = 10
    USER_PREMIUM_GUILD_SUBSCRIPTION_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23

class MessageFlags:
    CROSSPOSTED = 1 << 0
    IS_CROSSPOST = 1 << 1
    SUPPRESS_EMBEDS = 1 << 2
    SOURCE_MESSAGE_DELETED = 1 << 3
    URGENT = 1 << 4
    HAS_THREAD = 1 << 5
    EPHEMERAL = 1 << 6
    LOADING = 1 << 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 1 << 8

# TODO: Move this somewhere else
class PartialEmoji:
    id: Optional[Snowflake]
    name: Optional[str]

class Reaction:
    count: int
    me: bool
    emoji: PartialEmoji

class MessageReference:
    message_id: Snowflake
    channel_id: Optional[Snowflake]
    guild_id: Snowflake
    fail_if_not_exists: bool = True

def to_message_activity(d: Dict[str, Any]):
    type: int = d.get("type")
    party_id: Optional[str] = d.get("party_id")

    msg_activ = MessageActivity()
    msg_activ.type = type
    msg_activ.party_id = party_id

    return msg_activ

# TODO: Move this somewhere else
def to_partial_emoji(d: Dict[str, Any]):
    id: Optional[Snowflake] = d.get("id")
    name: Optional[str] = d.get("name")

    partial_emoji = PartialEmoji()
    partial_emoji.id = id
    partial_emoji.name = name

    return partial_emoji

def to_reaction(d: Dict[str, Any]):
    count: int = d.get("count")
    me: bool = d.get("me")
    emoji: PartialEmoji = to_partial_emoji(d.get("emoji"))

    reaction = Reaction()
    reaction.count = count
    reaction.me = me
    reaction.emoji = emoji

    return reaction

def to_message_reference(d: Dict[str, Any]):
    message_id: Snowflake = d.get("message_id")
    channel_id: Optional[Snowflake] = d.get("channel_id")
    guild_id: Snowflake = d.get("guild_id")
    fail_if_not_exists: bool = d.get("fail_if_not_exists")

    msg_ref = MessageReference()
    msg_ref.message_id = message_id
    msg_ref.channel_id = channel_id
    msg_ref.guild_id = guild_id
    msg_ref.fail_if_not_exists = fail_if_not_exists

    return msg_ref