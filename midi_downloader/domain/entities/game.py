"""Domain entity representing a game on khinsider.com."""

from dataclasses import dataclass
from typing import List


@dataclass
class Game:
    """Represents a game with MIDI files available for download."""
    
    name: str
    url: str
    system: str
    midi_files: List['MidiFile'] = None
    
    def __post_init__(self):
        if self.midi_files is None:
            self.midi_files = []
    
    def add_midi_file(self, midi_file: 'MidiFile') -> None:
        """Add a MIDI file to this game."""
        self.midi_files.append(midi_file)
    
    @property
    def total_midi_count(self) -> int:
        """Return the total number of MIDI files."""
        return len(self.midi_files)
