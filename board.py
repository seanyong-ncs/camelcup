from models.camel import Camel
from models.properties import Color, TileMod
import logging
import copy


class BoardTile:
    def __init__(self, pos):
        self.pos = pos 
        self.camel_stack = []
        self.modifier = TileMod.NEUTRAL # Either a +1 or -1

class Board:

    num_tiles = 32 # Number of tiles a race has
    
    def __init__(self, pos_dict=None, mod_dict=None):
        logging.debug("Creating Board")
        # Add camels to the board
        self.camels = [Camel(c) for c in Color]
        # Add tiles to the board
        self.tiles = [BoardTile(n) for n in range(Board.num_tiles + 1)] # Add one for the finish tile

        self.tiles[0].camel_stack = copy.copy(self.camels)

        if pos_dict is not None:
            self.setupFromDict(pos_dict, mod_dict)

    def setupFromDict(self, pos_dict, mod_dict):
        # Set up camels from pos_dict
        for key in pos_dict:
            for camel in pos_dict[key]:
                self.moveCamel(camel, key)
        
        # Check if mod_dict is not None since there can be no mod tiles
        if mod_dict:
            # Set up traps/boost tiles from mod_dict
            for key in mod_dict:
                self.tiles[key].modifier = mod_dict[key]

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
            
            # Calculate the destination tile position after making steps
            dest_tile_idx = camel.position + steps 
            # Don't allow the camel to move beyond last tile
            if dest_tile_idx > Board.num_tiles:
                dest_tile_idx = Board.num_tiles 

            mod_step = self.tiles[dest_tile_idx].modifier

            # Calculate stack landing position based on tile modifiers
            dest_tile_idx += mod_step.value

            # Reduce origin camel stack before modifying destination stack
            self.tiles[camel.position].camel_stack = cur_tile_stack[:stack_pos]

            # Augment destination tile's stack with moving stack
            # if last step modifier is a trap
            if mod_step == TileMod.TRAP:
                self.tiles[dest_tile_idx].camel_stack[:0] = move_stack # Prepend stack 
            # else boost
            else: 
                self.tiles[dest_tile_idx].camel_stack.extend(move_stack) # Extend stack

            # Update camel positions in the moving stack
            for c in move_stack:
                c.position += (steps + mod_step.value)
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
            mod = ""
            if t.modifier != TileMod.NEUTRAL:
                mod = f"[{t.modifier.name} {t.modifier.value}]"
            if i == 0:
                line += "S: "
            elif i == Board.num_tiles:
                line += "E: "
            else:
                line += f"{i}: "
            
            line += mod

            for c in t.camel_stack:
                line += f"{c.color.name} "
            print(line)



