from board import Board
from models.properties import Color
import logging
import itertools


# simulateRound(dict, dict) -> list of results
# Takes in a dictionary of camel positions and a dictionary of tile modifiers
# Returns a list of probabilities for each camel

def simulateRound(color_move_list, pos_dict):

    # Generate color move order permutations
    color_permutations = itertools.permutations(color_move_list)
    # Construct a list of dice per color
    dice_list = [range(1, 4) for _ in color_list]
    # Generate list of possible dice permutations
    dice_permutations = list(itertools.product(*dice_list))
    
    results = []
    # Loop through color permutations
    for color_perm in color_permutations:
        # Then loop through dice permutations
        for perm in dice_permutations:
            # Generate new board simulation for each color/dice pairing
            b = Board(pos_dict) # Create new sim board
            # Roll n number of times depending on number of camels moving this simulated round
            for i, dice_roll in enumerate(perm):
                b.moveCamel(color_perm[i], dice_roll)
            results.append(b.getCurrentRankings()) # Save results to list and run analysis later


    camel_results = []
    for c in Color:
        outcomes = [0 for _ in Color] # Generate [0,0,0,0,0] array to accumulate positional results
        for r in results:
            outcomes[r.index(c.value)] += 1 # Accumulate at the position for that particular camel

        # Calculate wining probabilities
        denominator = sum(outcomes)
        first_place = round(outcomes[0]/denominator, 3)
        second_place = round(outcomes[1]/denominator, 3)
        other_places = round((outcomes[2] + outcomes[3] + outcomes[4])/denominator, 3)

        # Results are formated as ["Camel_color", "1st_probability", "2nd_probability", "3rd-5th_probability"]
        camel_results.append([c.name, first_place, second_place, other_places])

    return camel_results


def evCalculator(probabilities):
    winnings = [5, 3, 2] # The possible winning amounts based on the betting card


    ev_all = []
    for p in probabilities:
        ev_current = [p[0]] # Add back name of the current camel into list
        for w in winnings:
            ev = round(p[1] * w + p[2] * 1 + p[3] * -1, 2) # w for 1st place, 1 for 2nd place, -1 for 3rd place 
            ev_current.append(ev)
        ev_all.append(ev_current)

    ev_all = sorted(ev_all, key=lambda x: x[1], reverse=True)
    
    return ev_all

if __name__ == "__main__":

    color_list = [Color.WHITE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.ORANGE]

    logging.basicConfig(level=logging.INFO)
    pos_dict = {10: [Color.GREEN, Color.ORANGE], 11: [Color.BLUE], 13:[Color.YELLOW],14:[Color.WHITE]}
    b = Board(pos_dict)
    # b.printBoard()
    probabilities = simulateRound(color_list, pos_dict)
    # probabilities = simulateRound(pos_dict)
    evs = evCalculator(probabilities)

    print(probabilities)
    print(evs)