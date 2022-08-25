import sim
import logging
from models.properties import *
import re

def printHeader():
    header = [
    "   _____                     _  _____              ________      __   _____       _                ",
    "  / ____|                   | |/ ____|            |  ____\ \    / /  / ____|     | |               ",
    " | |     __ _ _ __ ___   ___| | |    _   _ _ __   | |__   \ \  / /  | (___   ___ | |_   _____ _ __ ",
    " | |    / _` | '_ ` _ \ / _ \ | |   | | | | '_ \  |  __|   \ \/ /    \___ \ / _ \| \ \ / / _ \ '__|",
    " | |___| (_| | | | | | |  __/ | |___| |_| | |_) | | |____   \  /     ____) | (_) | |\ V /  __/ |   ",
    "  \_____\__,_|_| |_| |_|\___|_|\_____\__,_| .__/  |______|   \/     |_____/ \___/|_| \_/ \___|_|   ",
    "                                          | |                                                      ",
    "                                          |_|                                                      "
    ]
    print(*header, sep = "\n")

def getUserInput():
    user_input = input("Enter camel positions:")
    tokens = user_input.split(" ")
    tokens.reverse()

    if len(tokens) != 5:
        print("invalid input")
        return False

    char_mapping = {"B": Color.BLUE, "G": Color.GREEN, "O": Color.ORANGE, "Y": Color.YELLOW, "W": Color.WHITE}
    pos_dict = {}
    color_list = []
    for t in tokens:
        try:
            camel = char_mapping[t[0]]
            pos = int(re.findall(r'\d+', t)[0])
            if t[-1] != 'x':
                color_list.append(camel)

            if pos in pos_dict:
                pos_dict[pos].append(camel)
            else:
                pos_dict[pos] = [camel]
            
        except Exception as e:
            print("You mostly likely entered something wrong... please try again")
            return False

    return color_list, pos_dict

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # # List of camels that can still move this round
    color_list = [Color.GREEN, Color.BLUE, Color.ORANGE, Color.WHITE, Color.YELLOW] 
    # # Dict of camel positions
    pos_dict = {10: [Color.GREEN, Color.ORANGE], 11: [Color.BLUE], 13:[Color.YELLOW], 15:[Color.WHITE]}
    # # Dict of modifier locations
    mod_dict = {14: {TileMod.BOOST}, 12: {TileMod.BOOST}}


    printHeader()

    print("Input format: \"[Color][Pos][Cannot Move] [Color][Pos][Cannot Move] .... \"")
    # color_list, pos_dict = getUserInput()
    # mod_dict = {}

    rs = sim.RoundSimulator(color_list, pos_dict, mod_dict)
    rs.printBoard()
    probabilities = rs.simulateRound()
    evs = rs.calculateEV()

    print(probabilities)
    print(evs)