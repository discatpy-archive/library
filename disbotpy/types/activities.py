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

from typing import List, Optional

__all__ = (
    "ActivityTimestamps",
    "ActivityEmoji",
    "ActivityParty",
    "ActivityAssets",
    "ActivitySecrets",
    "ActivityButton",
    "Activity",
)

class ActivityTimestamps:
    start: Optional[int]
    end: Optional[int]

class ActivityEmoji:
    name: str
    id: Optional[int]
    animated: bool = False

class ActivityParty:
    id: str
    size: List[int]

class ActivityAssets:
    large_image: Optional[str]
    large_text: Optional[str]
    small_image: Optional[str]
    small_text: Optional[str]

class ActivitySecrets:
    join: Optional[str]
    spectate: Optional[str]
    match: Optional[str]

class ActivityButton:
    label: str
    url: str

class Activity:
    name: str
    type: int
    url: Optional[str]
    created_at: int
    timestamps: ActivityTimestamps
    application_id: int
    details: Optional[str]
    state: Optional[str]
    emoji: ActivityEmoji
    party: ActivityParty
    assets: ActivityAssets
    secrets: ActivitySecrets
    instance: bool
    flags: int
    buttons: List[ActivityButton]
