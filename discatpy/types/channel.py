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

from .snowflake import *

__all__ = (
    "ChannelType",
    "ChannelOverwrite",
    "VoiceRegion",
    "VideoQualityModes",
    "ThreadMetadata",
    "ThreadMember",
    "to_channel_overwrite",
    "to_voice_region",
    "to_thread_metadata",
    "to_thread_member",
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
    archive_timestamp: datetime
    locked: bool
    invitable: Optional[bool]
    create_timestamp: Optional[datetime]

class ThreadMember:
    id: Optional[Snowflake]
    user_id: Optional[Snowflake]
    join_timestamp: datetime
    flags: int

def to_channel_overwrite(d: Dict[str, Any]):
    id: Snowflake = d.get("id")
    type: int = d.get("type")
    allow: str = d.get("allow")
    deny: str = d.get("deny")

    chan_over = ChannelOverwrite()
    chan_over.id = id
    chan_over.type = type
    chan_over.allow = allow
    chan_over.deny = deny

    return chan_over

def to_voice_region(d: Dict[str, Any]):
    id: str = d.get("id")
    name: str = d.get("name")
    optimal: bool = d.get("optimal")
    deprecated: bool = d.get("deprecated")
    custom: bool = d.get("custom")

    voice_reg = VoiceRegion()
    voice_reg.id = id
    voice_reg.name = name
    voice_reg.optimal = optimal
    voice_reg.deprecated = deprecated
    voice_reg.custom = custom

    return voice_reg

def to_thread_metadata(d: Dict[str, Any]):
    archived: bool = d.get("archived")
    auto_archive_duration: int = d.get("auto_archive_duration")
    archive_timestamp: datetime = datetime.fromisoformat(d.get("archive_timestamp"))
    locked: bool = d.get("locked")
    invitable: Optional[bool] = d.get("invitable")
    create_timestamp: Optional[datetime] = datetime.fromisoformat(d.get("create_timestamp"))

    thread_md = ThreadMetadata()
    thread_md.archived = archived
    thread_md.auto_archive_duration = auto_archive_duration
    thread_md.archive_timestamp = archive_timestamp
    thread_md.locked = locked
    thread_md.invitable = invitable
    thread_md.create_timestamp = create_timestamp

    return thread_md

def to_thread_member(d: Dict[str, Any]):
    id: Optional[Snowflake] = d.get("id")
    user_id: Optional[Snowflake] = d.get("user_id")
    join_timestamp: datetime = d.get("join_timestamp")
    flags: int = d.get("flags")

    thread_mem = ThreadMember()
    thread_mem.id = id
    thread_mem.user_id = user_id
    thread_mem.join_timestamp = join_timestamp
    thread_mem.flags = flags

    return thread_mem