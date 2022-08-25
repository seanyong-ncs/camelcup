from .properties import Color

class Camel:
    def __init__(self, color=Color.WHITE):
        self.color = color # Set default color to white
        self.position = 0
        self.stacked_camel_color = None
