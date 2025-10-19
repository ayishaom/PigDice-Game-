"""Histogram module.

Provides the Histogram class for generating text-based histograms
for player scores in the Pig game.
"""

class Histogram:
    """Generate text-based histograms for player scores."""

    def __init__(self, scale=1):
        """
        Initialize histogram.

        Args:
            scale (int): scale factor for bar length (1 unit = scale points)
        """
        self.scale = scale

    def generate_total(self, players_scores):
        """Generate histogram for total points per player.

        Args:
            players_scores (list of tuples): [(player_name, stats_dict), ...]
        
        Returns:
            list of str: Lines representing the histogram.
        """
        lines = []
        for name, stats in players_scores:
            total_points = stats.get("total_points", 0)
            bar_length = int(total_points / self.scale)
            bar = "*" * bar_length
            lines.append(f"{name:^12} | {total_points:^6} | {bar}")
        return lines

    def generate_per_game(self, players_scores):
        """Generate histogram showing each game for each player.

        Args:
            players_scores (list of tuples): [(player_name, stats_dict), ...]
        
        Returns:
            list of str: Lines representing the histogram per game.
        """
        lines = []
        for name, stats in players_scores:
            for game in stats.get("games", []):
                points = game.get('points', 0)
                bar_length = int(points / self.scale)
                bar = "*" * bar_length
                lines.append(f"{name:^12} | {points:^6} | {bar} ({game.get('date')})")
        return lines

    def key(self):
        """Return a simple key/legend for the histogram."""
        lines = [
            "------------ KEY ------------",
            "*  | Bar represents points scored",
            f"Note: bar length scaled by {self.scale} points per *"
        ]
        return lines