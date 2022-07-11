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

import platform
import sys

import aiohttp
import discord_typings

import discatpy


def neofetch():
    print(
        f"""
\033[31;40md8888b. d888888b .d8888.  .o88b.  .d8b.  d888888b d8888b. db    db\033[0m
\033[32;40m88  `8D   `88'   88'  YP d8P  Y8 d8' `8b    88    88  `8D `8b  d8'\033[0m
\033[33;40m88   88    88    `8bo.   8P      88ooo88    88    88oodD'  `8bd8' \033[0m
\033[34;40m88   88    88      `Y8b. 8b      88   88    88    88         88   \033[0m
\033[35;40m88  .8D   .88.   db   8D Y8b  d8 88   88    88    88         88   \033[0m
\033[36;40mY8888D' Y888888P `8888Y'  `Y88P' YP   YP    YP    88         YP   \033[0m

==================================================================

- Version: {discatpy.__version__}
- Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}-{sys.version_info.releaselevel}
- System Information: {platform.uname().system} {platform.uname().release}
- Dependencies:
  - aiohttp Version: {aiohttp.__version__}
  - discord_typings Version: {discord_typings.__version__}
    """
    )


if __name__ == "__main__":
    neofetch()
