"""Domain entity representing a gaming system."""

from dataclasses import dataclass
from typing import List


@dataclass
class GameSystem:
    """Represents a gaming system (e.g., gameboy, nes)."""
    
    name: str
    url: str
    games: List['Game'] = None
    
    def __post_init__(self):
        if self.games is None:
            self.games = []
    
    def add_game(self, game: 'Game') -> None:
        """Add a game to this system."""
        self.games.append(game)
    
    @property
    def total_games(self) -> int:
        """Return the total number of games."""
        return len(self.games)
