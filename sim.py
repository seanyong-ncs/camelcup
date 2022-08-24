from board import Board
from models.properties import Color
import logging
import itertools


# simulateRound(dict, dict) -> list of results
# Takes in a dictionary of camel positions and a dictionary of tile modifiers
# Returns a list of probabilities for each camel

def simulateRound(pos_dict, mod_dict):
    
    colors = [c for c in Color]
    color_permutations = itertools.permutations(colors)
    results = []

    # Create a board for validation
    b = Board(pos_dict)
    b.validateDict(pos_dict)

    # Run all dice combinations permuted with color order
    for order in color_permutations:
        for i in range(1, 3):
            for j in range(1, 3):
                for k in range(1, 3):
                    for l in range(1, 3):
                        for m in range(1, 3):
                            b = Board(pos_dict) # Create new sim board
                            b.moveCamel(order[0], i)
                            b.moveCamel(order[1], j)
                            b.moveCamel(order[2], k)
                            b.moveCamel(order[3], l)
                            b.moveCamel(order[4], m)
                            results.append(b.getCurrentRankings())

    camel_results = []
    for c in colors:
        outcomes = [0 for _ in Color]
        for r in results:
            outcomes[r.index(c.value)] += 1

        first_place = round(outcomes[0]/3840*100, 1)
        second_place = round(outcomes[1]/3840*100, 1)
        other_places = round((outcomes[2] + outcomes[3] + outcomes[4])/3840*100, 1)

        # Results are formated as ["Camel_color", "1st_probability", "2nd_probability", "3rd-5th_probability"]
        camel_results.append([c.name, first_place, second_place, other_places])

    return camel_results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pos_dict = {3: [Color.GREEN, Color.YELLOW], 5: [Color.BLUE], 6:[Color.WHITE, Color.ORANGE]}
    print(simulateRound(pos_dict))
