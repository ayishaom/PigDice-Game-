"""Test the Histogram class: total, per-game, scaling, and key generation."""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from histogram import Histogram


class TestHistogram(unittest.TestCase):
    """Test initialization, total/per-game histograms, scaling, empty input,
    and key generation."""

    def setUp(self):
        """Create default and scaled Histogram instances and sample
        player data."""
        self.hist_default = Histogram(scale=1)
        self.hist_scaled = Histogram(scale=5)

        self.players = [
            (
                "Ayisha",
                {
                    "total_points": 10,
                    "games": [
                        {"date": "2025-01-01", "points": 5},
                        {"date": "2025-01-02", "points": 5},
                    ],
                },
            ),
            (
                "Lulu",
                {
                    "total_points": 15,
                    "games": [
                        {"date": "2025-01-01", "points": 7},
                        {"date": "2025-01-02", "points": 8},
                    ],
                },
            ),
            (
                "Charlie",
                {
                    "games": [
                        {"date": "2025-01-01", "points": 0},
                    ],
                },
            ),  # no total_points
        ]

    def test_default_scale_init(self):
        """Verify that Histogram initializes with default scale correctly."""
        self.assertEqual(self.hist_default.scale, 1)

    def test_custom_scale_init(self):
        """Verify that Histogram initializes with a custom scale."""
        h = Histogram(scale=3)
        self.assertEqual(h.scale, 3)

    def test_generate_total_default(self):
        """Generate total points histogram and verify names, points,
        and bar lengths."""
        lines = self.hist_default.generate_total(self.players)
        name, points, bar = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(name, "Ayisha")
        self.assertEqual(points, "10")
        self.assertEqual(len(bar), 10)

    def test_generate_total_scaled(self):
        """Generate scaled total points histogram and verify bar
        lengths are scaled."""
        lines = self.hist_scaled.generate_total(self.players)
        name, points, bar = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(len(bar), 2)  # 10 / 5

    def test_generate_total_empty_list(self):
        """Return empty list when generating total histogram for no players."""
        lines = self.hist_default.generate_total([])
        self.assertEqual(lines, [])

    def test_generate_per_game_default(self):
        """Generate per-game histograms and verify stars and dates
        for each game."""
        lines = self.hist_default.generate_per_game(self.players)
        name, points, rest = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(name, "Ayisha")
        self.assertEqual(points, "5")
        self.assertIn("*****", rest)
        self.assertIn("2025-01-01", rest)

    def test_generate_per_game_scaled(self):
        """Generate scaled per-game histogram and verify bar lengths
        are scaled."""
        lines = self.hist_scaled.generate_per_game(self.players)
        name, points, rest = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(len(rest.split(" ")[0]), 1)  # 5 / 5 = 1 star

    def test_generate_per_game_empty_list(self):
        """Return empty list when generating per-game histogram
        for no players."""
        lines = self.hist_default.generate_per_game([])
        self.assertEqual(lines, [])

    def test_key_contents(self):
        """Generate histogram key and verify content lines."""
        key_lines = self.hist_default.key()
        self.assertIn("------------ KEY ------------", key_lines[0])
        self.assertIn("*  | Bar represents points scored", key_lines)
        self.assertIn(
            f"Note: bar length scaled by {self.hist_default.scale} " f"points per *",
            key_lines,
        )

    def test_zero_and_negative_points(self):
        """Verify histogram behavior for zero and negative points."""
        players = [
            (
                "Zero",
                {
                    "total_points": 0,
                    "games": [
                        {"date": "2025-01-01", "points": 0},
                    ],
                },
            ),
            (
                "Negative",
                {
                    "total_points": -5,
                    "games": [
                        {"date": "2025-01-01", "points": -3},
                    ],
                },
            ),
        ]
        lines_total = self.hist_default.generate_total(players)
        name, points, bar = [s.strip() for s in lines_total[0].split("|")]
        self.assertEqual(points, "0")
        self.assertEqual(bar, "")
