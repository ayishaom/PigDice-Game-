import random

class Dice:
    """A simple six-sided die."""

    def __init__(self):
        self.sides = 6

    def roll(self) -> int:
        """Return a random number between 1 and 6 inclusive."""
        return random.randint(1, self.sides)
