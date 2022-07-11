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

from ...types import MISSING, MissingOr, Snowflake
from .core import APIEndpointData, CoreMixin

__all__ = ("StageInstanceEndpointMixin",)


class StageInstanceEndpointMixin(CoreMixin):
    get_stage_instance = APIEndpointData(
        "GET", "/stage-instances/{channel_id}", format_args={"channel_id": Snowflake}
    )
    create_stage_instance = APIEndpointData(
        "POST",
        "/stage-instances",
        supports_reason=True,
        param_args=[
            ("channel_id", Snowflake),
            ("topic", str),
            ("privacy_level", MissingOr[int], MISSING),
            ("send_start_notification", MissingOr[bool], MISSING),
        ],
    )
    modify_stage_instance = APIEndpointData(
        "PATCH",
        "/stage-instances/{channel_id}",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
        param_args=[
            ("topic", MissingOr[str], MISSING),
            ("privacy_level", MissingOr[int], MISSING),
        ],
    )
    delete_stage_instance = APIEndpointData(
        "DELETE",
        "/stage-instances/{channel_id}",
        format_args={"channel_id": Snowflake},
        supports_reason=True,
    )
