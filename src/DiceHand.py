"""Group of dice.
- Hold N Dice and roll them together.
- Helpers: values list, sum, flags like 'any 1', 'double 1' (for variants).
- No I/O; just return data."""


"""DiceHand module.

Group of dice that can be rolled together.
Handles multiple dice, stores their values, and provides 
helper methods such as total sum, checking if any die shows 1,
and dectecting doubles 
"""

from __future__ import annotations
import random
from typing import List 
from .dice import Dice


class DiceHand:
    """Represents a group of dice that can be rolled together."""

    def __init__(self, num_dice: int = 1, sides: int = 6) -> None:
        """Initialize a hand with N dice.
        Parameters 
        ----------
        num_dice : int 
            Number of dice in the hand (default = 1 ).
        sides : int 
            Number of sides on each die (default = 6).
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
        """Return True if any die rolled a 1."""
        return sum(self.values)
    
    