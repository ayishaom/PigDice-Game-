#Basic computer intelligence for deciding when to hold or roll.

"""Intelligence module.

Basic AI decision logic for the Pig dice game.
Given the computer's total score, the opponent's score,
and the current turn total, it returns a decision: 'roll' or 'hold'.

Deterministic, no randomness, no I/O.
"""

class Intelligence:
    """Represents a simple AI for the Pig dice game."""

    def __init__(self, hold_threshold: int = 20) -> None:
        """
        Initialize the AI with a hold threshold.

        Parameters
        ----------
        hold_threshold : int
            The turn total at which the AI decides to hold (default = 20).
        """
        self.hold_threshold = hold_threshold

    def decide(self, turn_total: int, my_score: int, opponent_score: int) -> str:
        """
        Decide whether to 'roll' or 'hold' based on scores.

        Parameters
        ----------
        turn_total : int
            Points accumulated in the current turn.
        my_score : int
            AI's total score so far.
        opponent_score : int
            Opponent's total score.

        Returns
        -------
        str
            'roll' or 'hold'.
        """
        # If holding would win the game, hold immediately
        if my_score + turn_total >= 100:
            return "hold"

        # Basic strategy: hold if turn_total reaches threshold
        if turn_total >= self.hold_threshold:
            return "hold"

        # Otherwise, roll
        return "roll"

    def set_difficulty(self, level: str) -> None:
        """
        Adjust the hold threshold based on difficulty level.

        Parameters
        ----------
        level : str
            Difficulty level: 'easy', 'medium', or 'hard'.
        """
        if level == "easy":
            self.hold_threshold = 15
        elif level == "medium":
            self.hold_threshold = 20
        elif level == "hard":
            self.hold_threshold = 25
        else:
            raise ValueError("Invalid difficulty level. Choose 'easy', 'medium', or 'hard'.")

