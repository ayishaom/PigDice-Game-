"""Single die.
- Keep number of sides (default 6).
- roll() returns a random int in [1..sides].
- No printing/input; logic only."""

import random

class Dice:
    """A simple six-sided die."""

    def __init__(self):
        self.sides = 6

    def roll(self) -> int:
        """Return a random number between 1 and 6 inclusive."""
        return random.randint(1, self.sides)
