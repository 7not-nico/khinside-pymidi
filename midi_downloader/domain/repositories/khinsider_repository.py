"""Abstract repository interface for khinsider.com data access."""

from abc import ABC, abstractmethod
from typing import List
from midi_downloader.domain.entities import Game, GameSystem, MidiFile


class KhinsiderRepository(ABC):
    """Interface for accessing khinsider.com data."""
    
    @abstractmethod
    def get_systems(self) -> List[GameSystem]:
        """Retrieve all available gaming systems."""
        pass
    
    @abstractmethod
    def get_games_for_system(self, system_name: str) -> List[Game]:
        """Retrieve all games for a specific system."""
        pass
    
    @abstractmethod
    def get_midi_files_for_game(self, game_url: str) -> List[MidiFile]:
        """Retrieve all MIDI files for a specific game."""
        pass
