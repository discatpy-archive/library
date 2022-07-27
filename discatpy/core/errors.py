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

from typing import Any, Dict, List, Optional, Tuple, Union

from aiohttp import ClientResponse

__all__ = (
    "DisCatPyException",
    "HTTPException",
    "UnsupportedAPIVersionWarning",
)


class DisCatPyException(Exception):
    """Basis for all exceptions in DisCatPy. If you wanted to catch any exception
    thrown by DisCatPy, you would catch this exception.
    """

    pass


def _shorten_error_dict(d: Dict[str, Any], key: str = "") -> Dict[str, str]:
    ret_items: List[Tuple[str, str]] = []

    for k, val in d.items():
        new_k = key + "." + k if key else k

        if isinstance(val, dict):
            try:
                _errors: List[Dict[str, Any]] = val["_errors"]
            except KeyError:
                # recursively go through the dict to find the _errors list
                ret_items.extend(_shorten_error_dict(val, new_k).items())
            else:
                ret_items.append((new_k, " ".join(x.get("message", "") for x in _errors)))
        else:
            ret_items.append((new_k, val))

    return dict(ret_items)


class HTTPException(DisCatPyException):
    """Represents an error while attempting to connect to the Discord REST API.

    Attributes
    ----------
    response: :type:`aiohttp.ClientResponse`
        The response from the attempted REST API request.
    text :type:`str`
        The error text. Might be empty.
    status :type:`int`
        The status of the request.
    code :type:`int`
        The Discord specfic error code of the request.
    """

    __all__ = ()

    def __init__(self, response: ClientResponse, data: Optional[Union[Dict[str, Any], str]]):
        self.response = response
        self.status = response.status

        if isinstance(data, dict):
            self.code = data.get("code", 0)
            base = data.get("message", "")
            errors = data.get("errors")
            if errors:
                errors = _shorten_error_dict(errors)
                helpful_msg = "In {0}: {0}".format(t for t in errors.items())
                self.text = f"{base}\n{helpful_msg}"
            else:
                self.text = base
        else:
            self.text = data or ""
            self.code = 0

        format = "{0} {1} (error code: {2}"
        if self.text:
            format += ": {3}"

        format += ")"

        super().__init__(format.format(response.status, response.reason, self.code, self.text))


class UnsupportedAPIVersionWarning(Warning):
    """Represents a warning for unsupported API versions."""
    pass
