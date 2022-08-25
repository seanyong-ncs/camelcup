import sim
import logging
from models.properties import *

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # List of camels that can still move this round
    color_list = [Color.GREEN, Color.BLUE, Color.ORANGE, Color.WHITE, Color.YELLOW] 
    # Dict of camel positions
    # pos_dict = {10: [Color.GREEN, Color.ORANGE], 11: [Color.BLUE], 13:[Color.YELLOW], 15:[Color.WHITE]}
    pos_dict = {0: [Color.GREEN, Color.BLUE, Color.ORANGE, Color.WHITE, Color.YELLOW]}
    # Dict of modifier locations
    mod_dict = {2: {TileMod.TRAP}}

    rs = sim.RoundSimulator(color_list, pos_dict, mod_dict)
    # rs.printBoard()
    probabilities = rs.simulateRound()
    evs = rs.calculateEV()

    print(probabilities)
    print(evs)