"""
discatpy.core
~~~~~~~~~~~~~

The core API of DisCatPy. This is low level and not to indented to be used. 
But, it can be used if you'd like to.

The main design was inspired by orx, a low level Discord API wrapper.
"""

from .client import *
from .dispatcher import *
from .enums import *
from .errors import *
from .file import *
from .flags import *
from .gateway import *
from .http import *
from . import types, utils