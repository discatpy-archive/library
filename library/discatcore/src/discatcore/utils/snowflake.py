# SPDX-License-Identifier: MIT

import typing as t
from datetime import datetime

__all__ = ("DISCORD_EPOCH", "Snowflake")


DISCORD_EPOCH: t.Final[int] = 1420070400000


class Snowflake(int):
    @property
    def raw_timestamp(self) -> float:
        return ((self >> 22) + DISCORD_EPOCH) / 1000

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.raw_timestamp)

    @property
    def internal_worker_id(self) -> int:
        return (self & 0x3E0000) >> 17

    @property
    def internal_process_id(self) -> int:
        return (self & 0x1F000) >> 12

    iwid = internal_worker_id
    ipid = internal_process_id

    @property
    def increment(self) -> int:
        return self & 0xFFF
