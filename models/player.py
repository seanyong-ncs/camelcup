from .properties import Color
from .modifierCard import ModifierCard
import logging

class Player:

    def __init__(self, id):
        self.id = id
        self.cash = 10

        self.finalbet_cards = [c for c in Color]
        self.modifier_card = ModifierCard()
        self.held_cards = []
