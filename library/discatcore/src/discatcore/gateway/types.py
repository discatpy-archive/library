# SPDX-License-Identifier: MIT

import builtins
import typing as t
from dataclasses import dataclass

import aiohttp
from typing_extensions import Self, TypeGuard

DT = t.TypeVar("DT")

__all__ = (
    "BaseTypedWSMessage",
    "TextTypedWSMessage",
    "BinaryTypedWSMessage",
    "is_text",
    "is_binary",
)


@dataclass
class BaseTypedWSMessage(t.Generic[DT]):
    type: aiohttp.WSMsgType
    data: DT
    extra: str

    @classmethod
    def convert_from_untyped(cls: builtins.type[Self], msg: aiohttp.WSMessage) -> Self:
        return cls(
            t.cast(aiohttp.WSMsgType, msg[0]),
            t.cast(DT, msg[1]),
            t.cast(str, msg[2]),
        )


TextTypedWSMessage = BaseTypedWSMessage[str]
BinaryTypedWSMessage = BaseTypedWSMessage[bytes]


def is_text(base: BaseTypedWSMessage[t.Any]) -> TypeGuard[TextTypedWSMessage]:
    return base.type is aiohttp.WSMsgType.TEXT


def is_binary(base: BaseTypedWSMessage[t.Any]) -> TypeGuard[BinaryTypedWSMessage]:
    return base.type is aiohttp.WSMsgType.BINARY
