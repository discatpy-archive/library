# SPDX-License-Identifier: MIT

import typing as t

has_orjson: bool = False
try:
    import orjson

    has_orjson = True
except ImportError:
    import json

__all__ = ("dumps", "loads")


def dumps(obj: t.Any) -> str:
    if has_orjson:
        return orjson.dumps(obj).decode("utf-8")
    return json.dumps(obj)


def loads(obj: str) -> t.Any:
    if has_orjson:
        return orjson.loads(obj)
    return json.loads(obj)
