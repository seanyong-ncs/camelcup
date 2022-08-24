from enum import Enum
import logging

class Color(Enum):
    BLUE = 0
    GREEN = 1
    ORANGE = 2
    YELLOW = 3
    WHITE = 4

class TileMod(Enum):
    BOOST = 1
    NEUTRAL = 0
    TRAP = -1