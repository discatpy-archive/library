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

class SnowflakeMixin:
    __slots__ = ()

    raw_id: int

    @property
    def id(self):
        """
        Alias for the raw Snowflake ID of this object.
        """
        return self.raw_id

    @id.setter
    def id(self, new_id: int):
        """
        Alias for the raw Snowflake ID of this object.
        """
        self.raw_id = new_id

    @property
    def snowflake_timestamp(self):
        """
        The timestamp stored in this object's Snowflake ID.
        """
        return (self.raw_id >> 22) + 1420070400000

    @property
    def snowflake_iwid(self):
        """
        The internal worker ID stored in this object's
        Snowflake ID.
        """
        return (self.raw_id & 0x3E0000) >> 17

    @property
    def snowflake_ipid(self):
        """
        The internal process ID stored in this object's
        Snowflake ID.
        """
        return (self.raw_id & 0x1F000) >> 12

    @property
    def snowflake_increment(self):
        """
        The increment of the object's Snowflake ID.
        """
        return self.raw_id & 0xFFF