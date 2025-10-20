"""DiceHand module.

Group of dice that can be rolled together.
Handles multiple dice, stores their values, and provides
helper methods such as total sum, checking if any die shows 1,
and detecting doubles (for variants of the Pig game).
"""

from __future__ import annotations  # MUST be at the top, after the docstring
from typing import List
from dice import Dice  # assuming Dice class exists in dice.py


class DiceHand:
    """Represents a group of dice that can be rolled together.

    Attributes:
        dice (List[Dice]): List of Dice objects in the hand.
        values (List[int]): Last rolled values of all dice.
    """

    def __init__(self, num_dice: int = 1, sides: int = 6) -> None:
        """Initialize a hand with N dice.

        Args:
            num_dice (int, optional): Number of dice in the hand. Defaults to
            1.
            sides (int, optional): Number of sides on each die. Defaults to 6.

        Raises:
            ValueError: If num_dice is less than 1.
        """
        if num_dice < 1:
            raise ValueError("A DiceHand must contain at least one die.")
        self.dice: List[Dice] = [Dice(sides) for _ in range(num_dice)]
        self.values: List[int] = []

    def roll(self) -> List[int]:
        """Roll all dice in the hand and return their values."""
        self.values = [die.roll() for die in self.dice]
        return self.values

    def total(self) -> int:
        """Return the sum of the most recent roll."""
        return sum(self.values)

    def any_one(self) -> bool:
        """Return True if any die rolled a 1."""
        return 1 in self.values

    def double_ones(self) -> bool:
        """Return True if two or more dice rolled a 1."""
        return self.values.count(1) >= 2

    def __len__(self) -> int:
        """Return number of dice in hand."""
        return len(self.dice)

    def __repr__(self) -> str:
        """Return string representation for debugging."""
        return f"DiceHand({self.values})"
