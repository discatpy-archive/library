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

from enum import Enum

__all__ = (
    "VerificationLevel",
    "MessageNotificationLevel",
    "ExplicitContentFilterLevel",
    "MFALevel",
    "NSFWLevel",
    "PremiumTier",
)

class VerificationLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4

class MessageNotificationLevel(Enum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1

class ExplicitContentFilterLevel(Enum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2

class MFALevel(Enum):
    NONE = 0
    ELEVATED = 1

class NSFWLevel(Enum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3

class PremiumTier(Enum):
    NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3