from models.camel import Camel
from models.properties import Color
from models.player import Player
from models.dice import Dice
import logging

num_players = 2

class BoardTile:
    def __init__(self):
        camelStack = None
        modifierCard = None

class Board:
    
    def __init__(self):
        logging.info("Creating Board")
        # Add camels to the board
        self.camels = [Camel(c) for c in Color]
        # Add players to the board
        self.players = [Player(p) for p in range(num_players)]
        # Add dice to the board
        self.dices = [Dice(c) for c in Color]


def main():
    b = Board()

    print("Generated Board")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()


