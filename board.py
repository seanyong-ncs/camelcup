from models.camel import Camel
from models.properties import Color
from models.player import Player
from models.dice import Dice
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
    
    def __init__(self):
        logging.info("Creating Board")
        # Add camels to the board
        self.camels = [Camel(c) for c in Color]
        # Add players to the board
        self.players = [Player(p) for p in range(num_players)]
        # Add dice to the board
        self.dices = [Dice(c) for c in Color]
        # Add tiles to the board
        self.tiles = [BoardTile(n) for n in range(num_tiles + 1)]

        self.tiles[0].camel_stack = copy.copy(self.camels)

    
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

    def printBoard(self):
        board_string = ""
        positions_string = ""
        divider_string = "".join(["-" for _ in range(3*num_tiles)])
        for i,t in enumerate(self.tiles):
            if i == 0:
                board_string += "S "
            elif i == num_tiles:
                board_string += "E"
            else:
                board_string += f"{i} "
            
            for c in t.camel_stack:
                positions_string += f"{c.color.value}"
            positions_string += ","
    
        print(board_string)
        print(divider_string)
        lines = self.printVertically(positions_string)

        for line in self.printVertically(positions_string):
            print(line)

    def printVertically(self, s):
      s = s.split(",")
      x = []
      row = 0
      for i in s:
         row = max(row, len(i))
      col = len(s)
      ans = ["" for i in range(row)]
      j = 0
      for i in range(col):
         j = 0
         while j < len(s[i]):
            #print(j, i)
            while i - len(ans[j]) >= 1:
               ans[j] += "  "
            ans[j] += s[i][j] + " "
            j += 1
      return ans

        
def main():
    b = Board()
    b.moveCamel(Color.ORANGE, 1)
    b.moveCamel(Color.GREEN, 1)
    b.moveCamel(Color.YELLOW, 3)
    b.moveCamel(Color.BLUE, 2)
    b.moveCamel(Color.WHITE, 2)
    b.moveCamel(Color.ORANGE, 2)
    b.printBoard()
    print("Generated Board")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()


