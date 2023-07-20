"""
discatpy.models
~~~~~~~~~~~~~~~~~~

All of the Discord API models for `discatpy`.
"""

from .abc import *
from .asset import *
from .color import *
from .command import *
from .embed import *
from .emoji import *
from .iterators import *
from .message import *
from .permissions import *
from .user import *

__all__ = ()
__all__ += abc.__all__
__all__ += asset.__all__
__all__ += color.__all__
__all__ += command.__all__
__all__ += embed.__all__
__all__ += emoji.__all__
__all__ += iterators.__all__
__all__ += message.__all__
__all__ += permissions.__all__
__all__ += user.__all__
