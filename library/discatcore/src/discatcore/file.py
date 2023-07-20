# SPDX-License-Identifier: MIT

import io
import typing as t
from collections.abc import Callable
from os import path

__all__ = ("BasicFile",)


class BasicFile:
    """Represents a file being POSTed to the Discord API.

    Args:
        fp (Union[io.IOBase, str, bytes]): The raw file contents or the path to the target file.
        content_type (str): The content type of this file. This has to be in the HTTP format.
        filename (Optional[str]): The custom filename of this file. Defaults to None.
        spoiler (bool): Whether this file is a spoiler or not. Defaults to False.

    Attributes:
        fp (Union[io.IOBase, str, bytes]): The raw file contents.
        filename (str): The filename of this file. Defaults to the filename from the fp if the argument is None.
        content_type (str): The content type of this file. This has to be in the HTTP format.
    """

    __slots__ = (
        "fp",
        "filename",
        "_owner",
        "_orig_close",
        "content_type",
    )

    def __init__(
        self,
        fp: t.Union[io.IOBase, str, bytes],
        content_type: str,
        *,
        filename: t.Optional[str] = None,
        spoiler: bool = False,
    ) -> None:
        self.fp: io.IOBase
        self._owner: bool
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError(f"IOBase object {fp!r} must be seekable & readable.")

            self.fp = fp
            self._owner = False
        else:
            self.fp = open(fp, "rb")
            self._owner = True

        self.filename: str
        if filename is None:
            if isinstance(fp, str):
                self.filename = path.split(fp)[1]
            else:
                raise ValueError("Filename must be provided if fp is of type IOBase.")
        else:
            self.filename = filename

        if spoiler and not self.filename.startswith("SPOILER_"):
            self.filename = f"SPOILER_{self.filename}"

        self._orig_close: Callable[[], None] = self.fp.close
        self.fp.close = lambda: None
        self.content_type: str = content_type

    @property
    def spoiler(self) -> bool:
        """Whether the file is a spoiler or not."""
        return self.filename.startswith("SPOILER_")

    def close(self) -> None:
        """Closes the raw file."""
        self.fp.close = self._orig_close
        if not self._owner:
            self.fp.close()

    def reset(self, hard: bool = True) -> None:
        """Resets this file.

        Args:
            hard (bool): Whether the file should be hard reset or not. Defaults to True.
        """
        if hard:
            self.fp.seek(0)
