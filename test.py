from models.dice import Dice
from models.properties import Color
import unittest


class TestDice(unittest.TestCase):

    def testDiceCreation(self):
        dice_sides = 3
        dice_color = Color.RED
        d = Dice(color = dice_color, num_sides=dice_sides)
        self.assertEqual(d.color, dice_color)
        self.assertEqual(d.num_sides, dice_sides)
        self.assertEqual(d.last_rolled, None)

    def testDiceRoll(self):
        dice_color = Color.WHITE
        d = Dice(color = dice_color)
        self.assertIsNotNone(d.roll())
        self.assertIsNotNone(d.last_rolled)


if __name__ == '__main__':
    unittest.main()