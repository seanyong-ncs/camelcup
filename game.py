import random
from board import Board
from models.player import Player
from models.properties import *

class Game:
    def __init__(self):
        self.round_counter = 0
        self.unmoved_list = [c for c in Color] # List of camels that can still move this round
        self.reset_move_state() # Set unmoved_list and moved_dict
        self.board = Board()

    def add_player(self, player_alias):
        self.player_list.append(Player(player_alias))

    def roll_dice(self):
        # Roll dice to move random Camel
        random.shuffle(self.unmoved_list)
        picked_color = self.unmoved_list.pop()
        rolled_number = random.randint(1, 3) # Dice rolls between 1 and 3
        self.moved_dict[picked_color] = rolled_number

        self.board.move_camel(picked_color, rolled_number)                

        if len(self.unmoved_list) < 1:
            self.end_round()

    def reset_move_state(self):
        self.unmoved_list = [c for c in Color]
        self.moved_dict = {}

    def end_round(self):
        # Perform end of round operations
        self.round_counter += 1
        self.reset_move_state()
        
        

    def set_modifier(mod, pos):
        # Set a modifier on the board
        pass

    def bet_finals(bet_type, color, player):
        # Set a bet for the final win/lose camel
        pass

    def take_bet(color, player):
        # Take a betting card for the specific color
        pass