# SPDX-License-Identifier: MIT

import typing as t

import discord_typings as dt
from aiohttp import ClientResponse

__all__ = (
    "DisCatCoreException",
    "HTTPException",
    "UnsupportedAPIVersionWarning",
    "GatewayReconnect",
)


class DisCatCoreException(Exception):
    """Basis for all exceptions in DisCatPy. If you wanted to catch any exception
    thrown by DisCatPy, you would catch this exception.
    """

    pass


def _shorten_error_dict(d: dt.NestedHTTPErrorsData, parent_key: str = "") -> dict[str, str]:
    ret_items: dict[str, str] = {}

    _errors = d.get("_errors")
    if _errors is not None and isinstance(_errors, list):
        ret_items[parent_key] = ", ".join([msg["message"] for msg in _errors])
    else:
        for key, value in d.items():
            key_path = f"{parent_key}.{key}" if parent_key else key
            # pyright thinks the type of value could be object which violates the first parameter
            # of this function
            ret_items.update([(k, v) for k, v in _shorten_error_dict(value, key_path).items()])  # type: ignore

    return ret_items


class HTTPException(DisCatCoreException):
    """Represents an error while attempting to connect to the Discord REST API.

    Args:
        response (aiohttp.ClientResponse): The response from the attempted REST API request.
        data (Union[discord_typings.HTTPErrorResponseData, str, None]): The raw data retrieved from the response.

    Attributes:
        text (str): The error text. Might be empty.
        code (int): The Discord specfic error code of the request.
    """

    __slots__ = ("text", "code")

    def __init__(
        self, response: ClientResponse, data: t.Optional[t.Union[dt.HTTPErrorResponseData, str]]
    ) -> None:
        self.code: int
        self.text: str
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

        # more shitty aiohttp typing
        super().__init__(format.format(response.status, response.reason, self.code, self.text))  # type: ignore


class UnsupportedAPIVersionWarning(Warning):
    """Represents a warning for unsupported API versions."""

    pass


class GatewayReconnect(DisCatCoreException):
    """Represents an exception signaling that the Gateway needs to be reconnected.

    Args:
        url (str): The url to reconnect with. This will be set to the normal gateway url if we cannot resume.
        resume (bool): Whether we can resume or not.

    Attributes:
        url (str): The url to reconnect with. This will be set to the normal gateway url if we cannot resume.
        resume (bool): Whether we can resume or not.
    """

    __slots__ = ("url", "resume")

    def __init__(self, url: str, resume: bool) -> None:
        self.url: str = url
        self.resume: bool = resume

        super().__init__(f"The Gateway should be reconnected to with url {self.url}.")
