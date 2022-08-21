import random
import logging

class Dice:

    def __init__(self, color, num_sides = 3):
        self.color = color
        self.num_sides = num_sides
        self.last_rolled = None
        logging.debug(f"Created a {self.num_sides} side Dice with color {self.color}")

    def roll(self):
        self.last_rolled = random.randint(1, 3)
        logging.debug(f"{self.color} color dice rolled a {self.last_rolled}")
        return self.last_rolled    

        
