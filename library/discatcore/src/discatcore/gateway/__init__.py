"""
discatcore.gateway
~~~~~~~~~~~~~~~~~~~~~

The Gateway modules for `discatcore`.
"""

from .client import *
from .events import *
from .ratelimiter import *

__all__ = ()
__all__ += client.__all__
__all__ += events.__all__
__all__ += ratelimiter.__all__
