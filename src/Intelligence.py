#Basic computer intelligence for deciding when to hold or roll.

"""Intelligence module.

Advanced AI decision logic for the Pig dice game.
Given the computer's total score, the opponent's score,
and the current turn total, it returns a decision: 'roll' or 'hold'.

Implements different difficulty levels:
- Easy: Conservative, holds early.
- Medium: Balanced.
- Hard: Strategic and adaptive — considers probability, score difference,
  opponent proximity to winning, and expected gain from rolling again.

Deterministic and testable; no randomness or I/O.
"""

class Intelligence:
    """Represents AI decision-making for the Pig dice game."""

    def __init__(self, hold_threshold: int = 20, difficulty: str = "medium") -> None:
        """
        Initialize the AI with a hold threshold and difficulty level.

        Parameters
        ----------
        hold_threshold : int
            The base turn total at which the AI decides to hold (default = 20).
        difficulty : str
            Difficulty level: 'easy', 'medium', or 'hard' (default = 'medium').
        """
        self.hold_threshold = hold_threshold
        self.difficulty = difficulty

    def set_difficulty(self, level: str) -> None:
        """
        Adjust AI behavior based on the selected difficulty level.

        Parameters
        ----------
        level : str
            Difficulty level: 'easy', 'medium', or 'hard'.

        Raises
        ------
        ValueError
            If an invalid difficulty level is provided.
        """
        valid_levels = {"easy", "medium", "hard"}
        if level not in valid_levels:
            raise ValueError("Invalid difficulty level. Choose 'easy', 'medium', or 'hard'.")
        self.difficulty = level
        if level == "easy":
            self.hold_threshold = 15
        elif level == "medium":
            self.hold_threshold = 20
        else:
            self.hold_threshold = 25

    def decide(self, turn_total: int, my_score: int, opponent_score: int) -> str:
        """
        Decide whether to 'roll' or 'hold' based on game state.

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
        if my_score + turn_total >= 100:
            return "hold"

        if self.difficulty == "easy":
            return "hold" if turn_total >= self.hold_threshold else "roll"

        if self.difficulty == "medium":
            if turn_total >= self.hold_threshold:
                return "hold"
            if opponent_score > 85:
                return "hold" if turn_total >= 18 else "roll"
            return "roll"

        # --- Hard difficulty: strategic AI ---
        return self._decide_hard(turn_total, my_score, opponent_score)

    def _decide_hard(self, turn_total: int, my_score: int, opponent_score: int) -> str:
        """
        Advanced decision-making for hard difficulty.

        Considers probability, opponent proximity, score gap,
        and expected value of rolling again.

        Returns
        -------
        str
            'roll' or 'hold'.
        """
        score_gap = my_score - opponent_score
        base_threshold = self.hold_threshold

        if score_gap < 0:
            base_threshold += 3
        elif score_gap > 15:
            base_threshold -= 3

        if opponent_score >= 90:
            base_threshold -= 2

        p_lose = 1 / 6
        p_continue = 5 / 6
        expected_gain = p_continue * 3.5

        expected_next_score = my_score + turn_total + expected_gain
        if expected_next_score >= 100:
            return "roll" if p_continue * expected_gain > p_lose * turn_total else "hold"

        if turn_total >= base_threshold:
            return "hold"

        risk_factor = p_lose * turn_total
        return "roll" if risk_factor < 5 else "hold"
