"""Dice module for the Pig game.

This module defines the Dice class, which represents a single die used
in the Pig game. The class includes logic for rolling the die, storing
its current value, and changing the number of sides.
"""

import random


class Dice:
    """A single die used in the Pig game.

    Attributes:
        sides (int): Number of sides on the die.
        current_value (int | None): Last rolled value or None if not rolled
        yet.
    """

    def __init__(self, sides=6):
        """Initialize a die with a given number of sides.

        Args:
            sides (int, optional): Number of sides for the die. Defaults to 6.

        Raises:
            ValueError: If sides is not an integer >= 2.
        """
        if not isinstance(sides, int) or sides < 2:
            raise ValueError("Number of sides must be an integer >= 2.")

        self.sides = sides
        self.current_value = None

    def roll(self):
        """Roll the die and return a random number between 1 and sides."""
        self.current_value = random.randint(1, self.sides)
        return self.current_value

    def get_current_value(self):
        """Return the last rolled value."""
        return self.current_value

    def set_sides(self, num_sides):
        """Change the number of sides for the die."""
        if not isinstance(num_sides, int) or num_sides < 2:
            raise ValueError("Number of sides must be an integer >= 2.")
        self.sides = num_sides

    def get_sides(self):
        """Return the number of sides."""
        return self.sides
