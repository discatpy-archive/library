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

from datetime import datetime
from typing import Any, Dict, Optional

from .abs import APIType
from .user import User

__all__ = (
    "Member",
)

class Member(APIType):
    def __init__(
        self,
        d: Dict[str, Any],
        client,
        user: User,
        nick: Optional[str],
        joined_at: datetime,
        premium_since: Optional[datetime],
        deaf: bool,
        mute: bool,
        pending: Optional[bool],
        timeout_until: Optional[datetime]
    ) -> None:
        super().__init__(d, client)

        self.user = user
        self.nick = nick
        self.joined_at = joined_at
        self.premium_since = premium_since
        self.deaf = deaf
        self.mute = mute
        self.pending = pending
        self.timeout_until = timeout_until

    @classmethod
    def from_dict(cls, client, d: Dict[str, Any]):
        user: Optional[User] = User.from_dict(client, d.get("user")) if d.get("user") is not None else None
        nick: Optional[str] = d.get("nick")
        # TODO: Use unified Asset type for guild avatar, roles
        joined_at: datetime = datetime.fromisoformat(d.get("joined_at"))
        premium_since: Optional[datetime] = datetime.fromisoformat(d.get("premium_since")) if d.get("premium_since") is not None else None
        deaf: bool = d.get("deaf")
        mute: bool = d.get("mute")
        pending: Optional[bool] = d.get("pending")
        # TODO: permissions
        timeout_until: Optional[datetime] = datetime.fromisoformat(d.get("communication_disabled_until")) if d.get("communication_disabled_until") is not None else None

        return cls(d, client, user, nick, joined_at, premium_since, deaf, mute, pending, timeout_until)