import json
from datetime import date

class Score:
    """Manages player scores."""

    def __init__(self, file_path="scores.json"):
        self.file_path = file_path
        self.scores = self.load_scores()

    def load_scores(self):
        """Load scores from file if it exists, else return an empty dict"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_scores(self):
        """Save all scores to JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.scores, f, indent=4)

    def record_game(self, player_name: str, points: int):
        """Record a single game for a player."""
        today = str(date.today())

        if player_name not in self.scores:
            self.scores[player_name] = {
                "games": [],
                "total_points": 0
            }

        self.scores[player_name]["games"].append({
            "date": today,
            "points": points
        })

        # Update total points
        self.scores[player_name]["total_points"] += points

        self.save_scores()

    def get_high_scores(self):
        """
        Return all players ranked by total points (descending).
        Returns: list of tuples: [(player_name, {stats}), ...]
        """
        return sorted(
            self.scores.items(),
            key=lambda x: x[1].get("total_points", 0),
            reverse=True
        )

    def get_player_history(self, name: str):
        """Get all recorded games for a player."""
        return self.scores.get(name, {}).get("games", [])

    def rename_player(self, old_name: str, new_name: str):
        """
        Rename a player while keeping all their existing stats.
        Returns: bool: True if rename succeeded, False if old_name not found
        """
        if old_name not in self.scores:
            return False

        if old_name == new_name:
            return True

        if new_name in self.scores:
            # merge stats
            self.scores[new_name]["games"].extend(self.scores[old_name].get("games", []))
            self.scores[new_name]["total_points"] = (
                self.scores[new_name].get("total_points", 0) + self.scores[old_name].get("total_points", 0)
            )
        else:
            # Move the entry to the new name
            self.scores[new_name] = self.scores.pop(old_name)
            # we already removed old_name by pop

        # If old_name still exists for some reason, remove it
        if old_name in self.scores:
            del self.scores[old_name]

        self.save_scores()
        return True

    def clear_scores(self):
        """Clear all player scores."""
        self.scores = {}
        self.save_scores()