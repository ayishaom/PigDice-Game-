"""Player class for the Pig game.
- Stores player name, total score and whether it is an AI.
- No printing or input; logic only."""

class Player:
    """Represents a player in the Pig game."""

    def __init__(self, name, is_ai = False):
        """Create a player with a name and AI tag."""
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string.")
        
        self.name = name
        self.is_ai = is_ai
        self.total_score = 0

    def get_name(self):
        """Returns the player's name"""
        return self.name
    
    def set_name(self, name):
        """Chanege the player's name."""
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string.")
        
        self.name = name

    def get_score(self):
        """Return the player's total score."""
        return self.total_score
    
    def set_score(self, score):
        """Set player's total score."""
        if not isinstance(score, int) or score < 0:
            raise ValueError("Score must be a non-negative integer.")
        self.total_score = score

    def add_score(self, points):
        """Add points to the player's total score."""
        if not isinstance(points, int) or points < 0:
            raise ValueError("Points must be a non-negative integer.")
        self.total_score += points
        
    def reset_score(self):
        """Reset the player's total score to zero."""
        self.total_score = 0
