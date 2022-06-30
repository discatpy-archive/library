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

import builtins
import importlib
from dataclasses import dataclass, KW_ONLY
from typing import Any, Optional

from ...types import Snowflake, MISSING, MissingOr, MissingType

__all__ = (
    "APIEndpointData",
    "generate_api_wrapper_functions",
)

def _indent_text(txt: str) -> str:
    return f"    {txt}"

def _indent_all_text(strs: list[str]) -> list[str]:
    output: list[str] = []

    for txt in strs:
        output.append(_indent_text(txt))

    return output

# Code taken from the dataclasses module in the Python stdlib
def _create_fn(name, args, body, *, globals=None, locals=None,
               return_type=MISSING, asynchronous=False):
    if locals is None:
        locals = {}
    if "BUILTINS" not in locals:
        locals["BUILTINS"] = builtins
    return_annotation = ""
    if return_type is not MISSING:
        locals["_return_type"] = return_type
        return_annotation = "->_return_type"
    args = ", ".join(args)
    body = "\n".join(_indent_all_text(body))

    # Compute the text of the entire function.
    txt = ""
    if asynchronous:
        txt += "async "
    txt += f"def {name}({args}){return_annotation}:\n{body}"

    local_vars = ", ".join(locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{_indent_text(txt)}\n return {name}"
    ns = {}
    exec(txt, globals, ns)
    return ns["__create_fn__"](**locals)

@dataclass
class APIEndpointData:
    method: str
    path: str
    _: KW_ONLY
    format_args: Optional[dict[str, MissingOr[type]]] = None
    param_args: Optional[list[tuple[Any, ...]]] = None
    supports_reason: bool = False

def _generate_args(data: APIEndpointData):
    func_args = ["self"]

    if data.format_args is not None:
        for name, annotation in data.format_args.items():
            arg = f"{name}"
            if annotation is not MISSING:
                arg += f": {annotation.__name__}"

            func_args.append(arg)

    if data.param_args is not None:
        func_args.append("*")

        for arg in data.param_args:
            str_arg = ""
            if len(arg) >= 1:
                arg_name = str(arg[0])
                str_arg += arg_name
            if len(arg) >= 2:
                arg_annotation = arg[1]
                str_arg += f": {arg_annotation.__name__}"  # type: ignore
            if len(arg) == 3:
                arg_default = arg[2]
                str_arg += f"= {arg_default}"  # type: ignore

            func_args.append(str_arg)

    return func_args

def _generate_body(data: APIEndpointData):
    body: list[str] = []
    params_dict_name = "{0}_params"

    if data.param_args is not None:
        params_dict_name = params_dict_name.format("query" if data.method is "GET" else "json")
        body.append(_indent_text(f"{params_dict_name}: dict[str, Any] = {{}}"))

        template_if_statment = "if {0} is not MISSING:\n" + _indent_text("{1}[\"{0}\"] = {0}")

        for arg in data.param_args:
            arg_name = str(arg[0])

            if data.supports_reason and arg_name != "reason":
                body.append(_indent_text(template_if_statment.format(arg_name, params_dict_name)))

    request_line = f"return await self.request({data.method}, {data.path},"

    if data.format_args is not None:
        url_format_params = "{"
        for arg_name in data.format_args.keys():
            url_format_params += f"\"{arg_name}\": {arg_name}, "
        url_format_params += "}"

        request_line += f"{url_format_params}, "

    if data.param_args is not None:
        request_line += f"{params_dict_name}={params_dict_name}, "

    if data.supports_reason:
        request_line += f"reason=reason, "

    request_line += ")"

    body.append(request_line)
    return body

def _from_import(module: str, custom_builtins: builtins, objs_to_grab: Optional[tuple[str]] = None):
    actual_module = importlib.import_module(module)

    if not objs_to_grab:
        objs_to_grab = (k for k in dir(actual_module) if not (k.startswith("_") and k.endswith("_")))

    for obj in objs_to_grab:
        setattr(custom_builtins, obj, getattr(actual_module, obj))

# I would use a metaclass for this, but I don't want to pollute the HTTPClient with an unnecesary metaclass via inheritence
def generate_api_wrapper_functions(cls):
    for k in dir(cls):
        v = getattr(cls, k)

        if isinstance(v, APIEndpointData):
            if v.supports_reason:
                v.param_args.append(("reason", Optional[str], None))

            func_args = _generate_args(v)
            func_body = _generate_body(v)

            custom_builtins = builtins
            _from_import("typing", custom_builtins, ("Any", "Optional", "Union"))
            _from_import("discord_typings", custom_builtins)

            func = _create_fn(k, func_args, func_body, locals={
                "BUILTINS": custom_builtins,
                "Snowflake": Snowflake,
                "MISSING": MISSING,
                "MissingType": MissingType,
                "MissingOr": MissingOr,
            }, asynchronous=True)

            setattr(cls, k, func)

    return cls