from enum import Enum

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

class BettingCards(Enum):
    PAYS_FIVE = [5, 1, -1]
    PAYS_THREE = [3, 1, -1]
    PAYS_TWO = [2, 1, -1]