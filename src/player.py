"""Player class for the Pig game.

Stores player name, total score and whether it is an AI.
No printing or input; logic only.
"""


class Player:
    """Represents a player in the Pig game."""

    def __init__(self, name, is_ai=False):
        """Initialize a player with a name and AI status.

        Args:
            name (str): Player's name.
            is_ai (bool, optional): Whether the player is AI. Defaults to
            False.

        Raises:
            ValueError: If `name` is empty or not a string.
        """
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string.")

        self.name = name
        self.is_ai = is_ai
        self.total_score = 0

    def get_name(self):
        """Return the player's name.

        Returns:
            str: Player's name.
        """
        return self.name

    def set_name(self, name):
        """Change the player's name.

        Args:
            name (str): New player name.

        Raises:
            ValueError: If `name` is empty or not a string.
        """
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string.")

        self.name = name

    def get_score(self):
        """Return the player's total score.

        Returns:
            int: Total score.
        """
        return self.total_score

    def set_score(self, score):
        """Set the player's total score.

        Args:
            score (int): New total score.

        Raises:
            ValueError: If `score` is negative or not an integer.
        """
        if not isinstance(score, int) or score < 0:
            raise ValueError("Score must be a non-negative integer.")
        self.total_score = score

    def add_score(self, points):
        """Add points to the player's total score.

        Args:
            points (int): Points to add.

        Raises:
            ValueError: If `points` is negative or not an integer.
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Points must be a non-negative integer.")
        self.total_score += points

    def reset_score(self):
        """Reset the player's total score to zero."""
        self.total_score = 0
