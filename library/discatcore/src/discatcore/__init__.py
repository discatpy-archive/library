# SPDX-License-Identifier: MIT

__title__ = "DisCatCore"
__author__ = "EmreTech"
__version__ = "0.2.0"
__license__ = "MIT"

import typing as t

from . import gateway, http, types, utils
from .errors import *
from .file import *


class VersionInfo(t.NamedTuple):
    major: int
    minor: int
    patch: int
    release_level: t.Literal["alpha", "beta", "final"]


def parse_version_string(string: str) -> VersionInfo:
    major, minor, patch = string.split(".")

    if "-" in string:
        release_level = string.partition("-")[2]
    else:
        release_level = "final"

    return VersionInfo(
        major=int(major),
        minor=int(minor),
        patch=int(patch),
        release_level=release_level,  # pyright: ignore
    )


version_info: VersionInfo = parse_version_string(__version__)
del parse_version_string, t


__all__ = (
    "gateway",
    "http",
    "types",
    "utils",
    "VersionInfo",
    "version_info",
)
__all__ += errors.__all__
__all__ += file.__all__
