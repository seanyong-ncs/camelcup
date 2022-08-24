from models.camel import Camel
from models.properties import Color, TileMod
import logging
import copy

num_players = 2
num_tiles = 32

class BoardTile:
    def __init__(self, pos):
        self.pos = pos 
        self.camel_stack = []
        self.modifier = None # Either a +1 or -1

class Board:
    
    def __init__(self, pos_dict=None, mod_dict=None):
        logging.debug("Creating Board")
        # Add camels to the board
        self.camels = [Camel(c) for c in Color]
        # Add tiles to the board
        self.tiles = [BoardTile(n) for n in range(num_tiles + 1)]

        self.tiles[0].camel_stack = copy.copy(self.camels)

        if pos_dict is not None:
            self.setupFromDict(pos_dict, mod_dict)

    def setupFromDict(self, pos_dict, mod_dict):
        # Set up camels from pos_dict
        for key in pos_dict:
            for camel in pos_dict[key]:
                self.moveCamel(camel, key)
        
        # Set up traps/boost tiles from mod_dict
        for key in mod_dict:
            for mod in mod_dict[key]:
                self.tiles[key].modifier = mod.value

    def validateDict(self, pos_dict, mod_dict=None):
        # Check if exactly 1 of each camel
        check_list = [c for c in Color]
        for key in pos_dict:
            for c in pos_dict[key]:
                    check_list.pop(check_list.index(c))

        if mod_dict:
            # Todo: enforce mod tile placement validation
            # 1. Check if mod tile is on camel occupied tiles
            # 2. Check if mod tile is directly adjacent to an another mod tile
            pass

        if len(check_list) == 0:
            return True
        else:
            raise RuntimeError("configuration is not valid")
    
        


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
            dest_tile_idx = camel.position + steps

            # if modifier is a trap
            if self.tiles[dest_tile_idx].modifier == -1:
                dest_tile_idx -= 1
                self.tiles[dest_tile_idx].camel_stack[:0] = move_stack # Prepend stack 
            # if modifier is a bost
            else: # if modifier is None or 1
                if self.tiles[dest_tile_idx].modifier == 1:
                    dest_tile_idx += 1
                self.tiles[dest_tile_idx].camel_stack.extend(move_stack)

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



