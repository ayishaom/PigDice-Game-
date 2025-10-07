import uuid
from dataclasses import dataclass, field

@dataclass
class Player:
    """Represents a player with immutable id and mutable name/score."""
    name: str
    pid: str = field(default_factory=lambda: str(uuid.uuid4()))
    score: int = 0

    def rename(self, new_name: str) -> None:
        self.name = new_name
