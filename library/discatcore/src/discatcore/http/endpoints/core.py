# SPDX-License-Identifier: MIT

import typing as t

from ...file import BasicFile
from ...types import Unset, UnsetOr
from ..route import Route

__all__ = ("EndpointMixin",)


class EndpointMixin:
    async def request(
        self,
        route: Route,
        *,
        query_params: t.Optional[dict[str, t.Any]] = None,
        json_params: UnsetOr[t.Union[dict[str, t.Any], list[t.Any]]] = Unset,
        reason: t.Optional[str] = None,
        files: UnsetOr[list[BasicFile]] = Unset,
        **extras: t.Any,
    ) -> t.Union[t.Any, str]:
        pass
