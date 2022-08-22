from models.camel import Camel
from models.properties import Color
# from models.player import Player
# from models.dice import Dice
import logging
import copy

num_players = 2
num_tiles = 32

class BoardTile:
    def __init__(self, pos):
        self.pos = pos 
        self.camel_stack = []
        self.modifier_card = None

class Board:
    
    def __init__(self, pos_dict=None):
        logging.debug("Creating Board")
        # Add camels to the board
        self.camels = [Camel(c) for c in Color]
        # # Add players to the board
        # self.players = [Player(p) for p in range(num_players)]
        # # Add dice to the board
        # self.dices = [Dice(c) for c in Color]
        # Add tiles to the board
        self.tiles = [BoardTile(n) for n in range(num_tiles + 1)]

        self.tiles[0].camel_stack = copy.copy(self.camels)

        if pos_dict is not None:
            self.setupFromDict(pos_dict)

    def setupFromDict(self, pos_dict):
        for key in pos_dict:
            for camel in pos_dict[key]:
                self.moveCamel(camel, key)

    
    def moveCamel(self, color, steps):
        camel = self.camels[color.value]
        initial_move = True if camel.position == 0 else False

        cur_tile_stack = self.tiles[camel.position].camel_stack
        # Get camel's position in starting stack
        stack_pos = cur_tile_stack.index(camel)
        if not initial_move:

            # Slice stack at camel position
            move_stack = cur_tile_stack[stack_pos:]
            # Extend destination tile's stack with moving stack
            dest_tile = camel.position + steps
            self.tiles[dest_tile].camel_stack.extend(move_stack)

            # Reduce origin tile's stack 
            self.tiles[camel.position].camel_stack = cur_tile_stack[:stack_pos]
            # Update camel positions in the moving stack
            for c in move_stack:
                c.position += steps
        else:

            # Just pop camel from original stack and push to dest stack if initial_move
            self.tiles[camel.position].camel_stack.pop(stack_pos)
            self.tiles[steps].camel_stack.append(camel)
            camel.position += steps

    def getCurrentRankings(self):
        occupied_tiles = [t for t in self.tiles if len(t.camel_stack) > 0]
        rankings = []
        for tile in occupied_tiles:
            for camel in tile.camel_stack:
                rankings.append(camel.color.value)
        rankings.reverse()
        return rankings

    def printBoard(self):

        for i,t in enumerate(self.tiles):
            line = ""
            if i == 0:
                line += "S: "
            elif i == num_tiles:
                line += "E: "
            else:
                line += f"{i}: "
            
            for c in t.camel_stack:
                line += f"{c.color.name} "
            print(line)



        
def main():
    b = Board()
    b.moveCamel(Color.ORANGE, 1)
    b.moveCamel(Color.YELLOW, 2)
    b.moveCamel(Color.BLUE, 3)
    b.moveCamel(Color.WHITE, 2)
    b.moveCamel(Color.GREEN, 3)
    rankings = b.getCurrentRankings()
    print(rankings)
    b.printBoard()
    print("Generated Board")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()


