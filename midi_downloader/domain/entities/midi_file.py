"""Domain entity representing a MIDI file."""

from dataclasses import dataclass


@dataclass
class MidiFile:
    """Represents a downloadable MIDI file."""
    
    name: str
    url: str
    game_name: str
    system: str
    size_bytes: int = 0
    downloaded: bool = False
    
    @property
    def filename(self) -> str:
        """Extract filename from URL or use name."""
        if self.url:
            return self.url.split('/')[-1]
        return f"{self.name}.mid"
    
    def mark_downloaded(self) -> None:
        """Mark this file as downloaded."""
        self.downloaded = True
