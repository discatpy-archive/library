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
import subprocess
import sys
import re

import aiohttp
import discord_typings

import discatpy

# get_installed_package_info taken from here:
# https://github.com/python/typeshed/blob/master/scripts/create_baseline_stubs.py#L25-L45

def search_pip_freeze_output(project: str, output: str):
    # Look for lines such as "typed-ast==1.4.2".  '-' matches '_' and
    # '_' matches '-' in project name, so that "typed_ast" matches
    # "typed-ast", and vice versa.
    regex = "^(" + re.sub(r"[-_]", "[-_]", project) + ")==(.*)"
    m = re.search(regex, output, flags=re.IGNORECASE | re.MULTILINE)
    if not m:
        return None
    return m.group(1), m.group(2)


def get_installed_package_info(project: str):
    """Find package information from pip freeze output.
    Match project name somewhat fuzzily (case sensitive; '-' matches '_', and
    vice versa).
    Return (normalized project name, installed version) if successful.
    """
    r = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=True)
    return search_pip_freeze_output(project, r.stdout)


def get_dependencies():
    r = subprocess.run([sys.executable, "-m", "pip", "show", "discatpy"], capture_output=True, text=True, check=True)
    m = re.search(r"Requires:\s+(.*)", r.stdout)
    if m:
        dependencies = "".join(m.group(1).split())
        return dependencies.split(",")


def dump_dependencies():
    dependencies = get_dependencies()
    if dependencies:
        pkgs_info = {}

        for dependency in dependencies:
            installed_pkg_info = get_installed_package_info(dependency)
            if installed_pkg_info:
                pkgs_info[dependency] = installed_pkg_info[1]
            else:
                raise RuntimeError(f"Installed package info for package {dependency} not found")

        str_template = "  - {0} Version: {1}"
        str_dependencies = [str_template.format(name, version) for name, version in pkgs_info.items()]
        return str_dependencies
    else:
        raise RuntimeError("Required dependencies for DisCatPy not found")


def neofetch():
    dependencies = dump_dependencies()
    dependencies_str = "\n".join(dependencies)

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
{dependencies_str}
    """
    )


if __name__ == "__main__":
    neofetch()
