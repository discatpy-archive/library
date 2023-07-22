# SPDX-License-Identifier: MIT

import typing as t

has_orjson: bool = False
try:
    import orjson

    has_orjson = True
except ImportError:
    import json

__all__ = ("JSONObject", "dumps", "loads")


JSONObject = t.Union[
    str, int, float, bool, None, t.Sequence["JSONObject"], t.Mapping[str, "JSONObject"]
]


def dumps(obj: t.Any) -> str:
    if has_orjson:
        return orjson.dumps(obj).decode("utf-8")
    return json.dumps(obj)


def loads(obj: str) -> t.Any:
    if has_orjson:
        return orjson.loads(obj)
    return json.loads(obj)
