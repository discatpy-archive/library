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

from typing import Optional

from .snowflake import *

__all__ = (
    "ChannelType",
    "ChannelOverwrite",
    "VoiceRegion",
    "VideoQualityModes",
    "ThreadMetadata",
    "ThreadMember",
)

class ChannelType:
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13

class ChannelOverwrite:
    id: Snowflake
    type: int
    allow: str
    deny: str

class VoiceRegion:
    id: str
    name: str
    optimal: bool
    deprecated: bool
    custom: bool

class VideoQualityModes:
    AUTO = 1
    FULL = 2

class ThreadMetadata:
    archived: bool
    auto_archive_duration: int
    archive_timestamp: int # TODO: Maybe convert this to a more appropriate type for "ISO8601 timestamp"
    locked: bool
    invitable: Optional[bool]
    create_timestamp: Optional[int] # TODO: Maybe convert this to a more appropriate type for "ISO8601 timestamp"

class ThreadMember:
    id: Optional[Snowflake]
    user_id: Optional[Snowflake]
    join_timestamp: int # TODO: Maybe convert this to a more appropriate type for "ISO8601 timestamp"
    flags: int
