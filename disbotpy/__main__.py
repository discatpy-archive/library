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

import sys

import disbotpy
import platform

def neofetch():
    print(
    """
d8888b       **                d88888b.                       d888888b.  
88    `8D    **      .d8888.   88     8D                      88    `8D  
88     88            88'   YP  88     8D    .d88b.      00    88     8D  88     88
88     88    88      `8bo.     88oooooY'   88     88  888888  88oodD'    '88  88'
88     88    88        Y8b.    88     b.   88     88   '88'   88           '88'
88    .8D   .88.   db    8D    88     8D   88     88    88    88           88
Y88888D    888888   `8888Y'    Y8888P'      'Y88P'      'YP   88         YP

----------------------------------------------------------------------------------
----------------------------------------------------------------------------------
    """
    )

    entries = []
    entries.append("Python Version: {0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(sys.version_info))
    entries.append("DisBotPy Version: {}".format(disbotpy.__version__))
    entries.append("System Information: {0.system} {0.release} {0.version}".format(platform.uname()))
    print('\n'.join(entries))

if __name__ == '__main__':
    neofetch()