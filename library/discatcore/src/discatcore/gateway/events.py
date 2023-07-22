# SPDX-License-Identifier: MIT
from __future__ import annotations

import dataclasses
import typing as t

import discord_typings as dt

from ..utils.dispatcher import Event

__all__ = (
    "GatewayEvent",
    "DispatchEvent",
    "InvalidSessionEvent",
    "ReadyEvent",
    "ReconnectEvent",
    "ResumedEvent",
)


@dataclasses.dataclass
class GatewayEvent(Event):
    pass


@dataclasses.dataclass
class DispatchEvent(GatewayEvent):
    data: t.Mapping[str, t.Any]


@dataclasses.dataclass
class ReadyEvent(GatewayEvent):
    data: dt.ReadyData


@dataclasses.dataclass
class ResumedEvent(GatewayEvent):
    pass


@dataclasses.dataclass
class ReconnectEvent(GatewayEvent):
    pass


@dataclasses.dataclass
class InvalidSessionEvent(GatewayEvent):
    resumable: bool
