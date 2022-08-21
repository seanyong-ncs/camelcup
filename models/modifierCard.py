class ModifierCard:
    def __init__(self):
        self.boost_mode = True
        self.placed = False

    def setBoost(self):
        self.boost_mode = True

    def setTrap(self):
        self.boost_mode = False