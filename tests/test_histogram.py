"""Unit tests for Histogram: total, per-game, scaling, and key generation."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from histogram import Histogram


class TestHistogram(unittest.TestCase):
    """Covers initialization, total/per-game histograms, scaling, empty input, and key."""

    def setUp(self):
        self.hist_default = Histogram(scale=1)
        self.hist_scaled = Histogram(scale=5)

        self.players = [
            ("Ayisha", {"total_points": 10, "games": [{"date": "2025-01-01", "points": 5}, {"date": "2025-01-02", "points": 5}]}),
            ("Lulu", {"total_points": 15, "games": [{"date": "2025-01-01", "points": 7}, {"date": "2025-01-02", "points": 8}]}),
            ("Charlie", {"games": [{"date": "2025-01-01", "points": 0}]})  # no total_points
        ]


    def test_default_scale_init(self):
        self.assertEqual(self.hist_default.scale, 1)

    def test_custom_scale_init(self):
        h = Histogram(scale=3)
        self.assertEqual(h.scale, 3)

    # generate_total 

    def test_generate_total_default(self):
        lines = self.hist_default.generate_total(self.players)
        # Check name, points, and bar length
        name, points, bar = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(name, "Ayisha")
        self.assertEqual(points, "10")
        self.assertEqual(len(bar), 10)

        name, points, bar = [s.strip() for s in lines[1].split("|")]
        self.assertEqual(name, "Lulu")
        self.assertEqual(points, "15")
        self.assertEqual(len(bar), 15)

        name, points, bar = [s.strip() for s in lines[2].split("|")]
        self.assertEqual(name, "Charlie")
        self.assertEqual(points, "0")
        self.assertEqual(bar, "")

    def test_generate_total_scaled(self):
        lines = self.hist_scaled.generate_total(self.players)
        # Bar length scaled by 5
        name, points, bar = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(name, "Ayisha")
        self.assertEqual(points, "10")
        self.assertEqual(len(bar), 2)  # 10 / 5

        name, points, bar = [s.strip() for s in lines[1].split("|")]
        self.assertEqual(name, "Lulu")
        self.assertEqual(points, "15")
        self.assertEqual(len(bar), 3)  # 15 / 5

    def test_generate_total_empty_list(self):
        lines = self.hist_default.generate_total([])
        self.assertEqual(lines, [])

    # generate_per_game 

    def test_generate_per_game_default(self):
        lines = self.hist_default.generate_per_game(self.players)
        # Check first line
        name, points, rest = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(name, "Ayisha")
        self.assertEqual(points, "5")
        self.assertIn("*****", rest)
        self.assertIn("2025-01-01", rest)

        # Check second line
        name, points, rest = [s.strip() for s in lines[1].split("|")]
        self.assertEqual(name, "Ayisha")
        self.assertEqual(points, "5")
        self.assertIn("*****", rest)
        self.assertIn("2025-01-02", rest)

    def test_generate_per_game_scaled(self):
        lines = self.hist_scaled.generate_per_game(self.players)
        # Check bar length scaling
        name, points, rest = [s.strip() for s in lines[0].split("|")]
        self.assertEqual(len(rest.split(" ")[0]), 1)  # 5 / 5 = 1 star

    def test_generate_per_game_empty_list(self):
        lines = self.hist_default.generate_per_game([])
        self.assertEqual(lines, [])

    # key 

    def test_key_contents(self):
        key_lines = self.hist_default.key()
        self.assertIn("------------ KEY ------------", key_lines[0])
        self.assertIn("*  | Bar represents points scored", key_lines)
        self.assertIn(f"Note: bar length scaled by {self.hist_default.scale} points per *", key_lines)

    # Edge cases 

    def test_zero_and_negative_points(self):
        players = [
            ("Zero", {"total_points": 0, "games": [{"date": "2025-01-01", "points": 0}]}),
            ("Negative", {"total_points": -5, "games": [{"date": "2025-01-01", "points": -3}]})
        ]
        lines_total = self.hist_default.generate_total(players)
        name, points, bar = [s.strip() for s in lines_total[0].split("|")]
        self.assertEqual(name, "Zero")
        self.assertEqual(points, "0")
        self.assertEqual(bar, "")

        name, points, bar = [s.strip() for s in lines_total[1].split("|")]
        self.assertEqual(name, "Negative")
        self.assertEqual(points, "-5")
        self.assertEqual(bar, "")

        lines_per_game = self.hist_default.generate_per_game(players)
        name, points, rest = [s.strip() for s in lines_per_game[0].split("|")]
        self.assertEqual(name, "Zero")
        self.assertEqual(points, "0")
        self.assertIn("2025-01-01", rest)

        name, points, rest = [s.strip() for s in lines_per_game[1].split("|")]
        self.assertEqual(name, "Negative")
        self.assertEqual(points, "-3")
        self.assertIn("2025-01-01", rest)


if __name__ == "__main__":
    unittest.main()
