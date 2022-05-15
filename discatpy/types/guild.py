"""
The MIT License (MIT)

Copyright (c) 2022-present EmreTech
Copyright (c) 2022-present AarushOS

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
from ..user import User

__all__ = (
    "GuildBan",
    "VerificationLevel",
    "MessageNotificationLevel",
    "ExplicitContentFilterLevel",
    "MFALevel",
    "NSFWLevel",
    "PremiumTier",
    "SystemChannelFlags",
    "to_guild_ban",
)

class GuildBan:
    reason: Optional[str]
    user: User

class VerificationLevel:
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

class MessageNotificationLevel:
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1

class ExplicitContentFilterLevel:
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2

class MFALevel:
    NONE = 0
    ELEVATED = 1

class NSFWLevel:
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

class PremiumTier:
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3

class SystemChannelFlags:
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3

def to_guild_ban(d: Dict[str, Any]):
    reason: Optional[str] = d.get("reason")
    user: User = User.from_dict(d.get("user"))

    guild_ban = GuildBan()
    guild_ban.reason = reason
    guild_ban.user = user

    return guild_ban