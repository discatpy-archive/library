"""
discatpy.core
~~~~~~~~~~~~~

The core API of DisCatPy. This is low level and not to indented to be used. 
But, it can be used if you'd like to.

The main design was inspired by orx, a low level Discord API wrapper.
"""

from .errors import *
from .gateway import *
from .http import *
from . import types