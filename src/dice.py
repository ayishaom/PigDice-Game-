"""Single die for the Pig game.
- Keep number of sides (default 6).
- roll() returns a random number between 1 and sides.
- No printing or input; logic only."""

import random

class Dice:
    """A single die used in the Pig game."""

    def __init__(self, sides = 6):
        """Create a die with a given number of sides."""
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
