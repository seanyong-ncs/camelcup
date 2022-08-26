from board import Board
from models.properties import Color, BettingCards
import itertools
import numpy as np



class RoundSimulator():

    def __init__(self, color_move_list=None, pos_dict=None, mod_dict=None):
        self.updateBoard(color_move_list, pos_dict, mod_dict)
        self.pos_probabilities = None

    def updateBoard(self, color_move_list=None, pos_dict=None, mod_dict=None):
        self.color_move_list = color_move_list
        self.pos_dict = pos_dict
        self.mod_dict = mod_dict

    def printBoard(self):
        b = Board(self.pos_dict, self.mod_dict)
        b.printBoard()

    # simulateRound(list, dict, dict) -> list of results
    # Takes in a list of camels to move, a dictionary of camel positions, and a dictionary of tile modifiers
    # Returns a list of probabilities for each camel

    def simulateRound(self):

        # Generate color move order permutations
        color_permutations = itertools.permutations(self.color_move_list)
        # Construct a list of dice per color
        dice_list = [range(1, 4) for _ in self.color_move_list]
        # Generate list of possible dice permutations
        dice_permutations = list(itertools.product(*dice_list))
        
        results = []
        # Loop through color permutations
        for color_perm in color_permutations:
            # Then loop through dice permutations
            for perm in dice_permutations:
                # Generate new board simulation for each color/dice pairing
                b = Board(self.pos_dict, self.mod_dict) # Create new sim board
                # Roll n number of times depending on number of camels moving this simulated round
                for i, dice_roll in enumerate(perm):
                    b.moveCamel(color_perm[i], dice_roll)
                results.append(b.getCurrentRankings()) # Save results to list and run analysis later


        pos_probabilities = []
        for c in Color:
            outcomes = [0 for _ in Color] # Generate [0,0,0,0,0] array to accumulate positional results
            for r in results:
                outcomes[r.index(c.value)] += 1 # Accumulate at the position for that particular camel

            # Calculate wining probabilities
            denominator = sum(outcomes)
            first_place = round(outcomes[0]/denominator, 4)
            second_place = round(outcomes[1]/denominator, 4)
            other_places = round((outcomes[2] + outcomes[3] + outcomes[4])/denominator, 4)

            # Results are formated as ["Camel_color", "1st_probability", "2nd_probability", "3rd-5th_probability"]
            pos_probabilities.append([c.name, first_place, second_place, other_places])

            pos_probabilities = sorted(pos_probabilities, key=lambda x: x[1], reverse=True)

            self.pos_probabilities = pos_probabilities

        return pos_probabilities


    def calculateEV(self):

        ev_all = []
        for p in self.pos_probabilities:
            ev_current = [p[0]] # Add back name of the current camel into list
            
            p = p[1:] # Truncate name of camel at start of list
            for w in BettingCards:
                ev = round(sum(np.multiply(w.value, p)), 2) # w for 1st place, 1 for 2nd place, -1 for 3rd place 
                ev_current.append(ev)
            ev_all.append(ev_current)
        
        return ev_all

