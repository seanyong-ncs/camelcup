from .properties import Color

class Player:
    id = 0
    def __init__(self, alias = None):
        self.id = Player.assign_id() # assign id to player
        self.alias = f"Player {self.id}" if alias is None else alias
        self.cash = 10 # Players all start with 10 dollars
        self.color_cards = [c for c in Color] # The 5 color cards for betting in the end
        self.round_cards = []
        self.holding_mod_tile = True


    @staticmethod
    def assign_id():
        Player.id += 1
        return Player.id