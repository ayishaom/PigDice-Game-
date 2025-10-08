# for dice roll visualization

"""Roll frequency stats.
- Count how many times each face appears.
- Provide counts() and total_rolls().
- No printing; data only."""

from collections import defaultdict

class Histogram:
    """Counts integer outcomes and renders a basic text bar chart."""
    def __init__(self):
        self.counts = defaultdict(int)

    def add(self, value: int) -> None:
        self.counts[value] += 1

    def render(self) -> str:
        if not self.counts:
            return "(empty)"
        lines = []
        for k in sorted(self.counts):
            lines.append(f"{k}: " + "█" * self.counts[k] + f" ({self.counts[k]})")
        return "\n".join(lines)
