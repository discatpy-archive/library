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

import io
from os import path
from typing import Optional, Union

__all__ = ("BasicFile",)


class BasicFile:
    __slots__ = (
        "fp",
        "filename",
        "_owner",
        "_orig_close",
        "content_type",
    )

    def __init__(
        self,
        fp: Union[io.IOBase, str, bytes],
        content_type: str,
        *,
        filename: Optional[str] = None,
        spoiler: bool = False,
    ):
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError(f"IOBase object {fp!r} must be seekable & readable.")

            self.fp = fp
            self._owner = False
        else:
            self.fp = open(fp, "rb")
            self._owner = True

        if filename is None:
            if isinstance(fp, str):
                self.filename = path.split(fp)[1]
            else:
                raise ValueError("Filename must be provided if fp is of type IOBase.")
        else:
            self.filename = filename

        if spoiler and not self.filename.startswith("SPOILER_"):
            self.filename = f"SPOILER_{self.filename}"

        self._orig_close = self.fp.close
        self.fp.close = lambda: None
        self.content_type = content_type

    @property
    def spoiler(self):
        return self.filename.startswith("SPOILER_")

    def close(self):
        self.fp.close = self._orig_close
        if not self._owner:
            self.fp.close()

    def reset(self, hard: bool = True):
        if hard:
            self.fp.seek(0)
