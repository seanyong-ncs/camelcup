from board import Board
from models.properties import Color
import logging
import itertools
itertools.permutations([1, 2, 3])

def main():
    pos_dict = {3: [Color.GREEN, Color.YELLOW], 5: [Color.BLUE], 6:[Color.WHITE, Color.ORANGE]}
    b = Board(pos_dict)
    b.printBoard()
    colors = [c for c in Color]
    color_permutations = itertools.permutations(colors)
    results = []
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

    print(pos_dict)
    for c in colors:
        outcomes = [0 for c in Color]
        for r in results:
            outcomes[r.index(c.value)] += 1

        first_place = round(outcomes[0]/3840*100, 1)
        second_place = round(outcomes[1]/3840*100, 1)
        other_places = round((outcomes[2] + outcomes[3] + outcomes[4])/3840*100, 1)

        print(c.name, first_place, second_place, other_places)
    # print(results)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()