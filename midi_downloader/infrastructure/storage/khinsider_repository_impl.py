"""Khinsider repository implementation."""

from typing import List
from midi_downloader.domain.entities import Game, GameSystem, MidiFile
from midi_downloader.domain.repositories import KhinsiderRepository
from midi_downloader.infrastructure.http.khinsider_client import KhinsiderClient
from midi_downloader.infrastructure.scraping.khinsider_scraper import KhinsiderScraper


class KhinsiderRepositoryImpl(KhinsiderRepository):
    """Concrete implementation of KhinsiderRepository."""
    
    def __init__(self, client: KhinsiderClient, scraper: KhinsiderScraper):
        """
        Initialize repository with dependencies.
        
        Args:
            client: HTTP client for making requests
            scraper: Scraper for parsing HTML
        """
        self.client = client
        self.scraper = scraper
    
    def get_systems(self) -> List[GameSystem]:
        """Retrieve all available gaming systems."""
        # This would require scraping the main MIDI page
        # For simplicity, returning empty list (can be enhanced)
        return []
    
    def get_games_for_system(self, system_name: str) -> List[Game]:
        """Retrieve all games for a specific system."""
        url = f"{self.scraper.BASE_URL}/{system_name}"
        html = self.client.get_text(url)
        
        if html:
            return self.scraper.parse_game_list(html, system_name)
        return []
    
    def get_midi_files_for_game(self, game_url: str) -> List[MidiFile]:
        """Retrieve all MIDI files for a specific game."""
        html = self.client.get_text(game_url)
        
        if not html:
            return []
        
        # Extract game name and system from URL
        # URL format: https://www.khinsider.com/midi/{system}/{game}
        parts = game_url.rstrip('/').split('/')
        game_name = parts[-1] if len(parts) > 0 else "unknown"
        system_name = parts[-2] if len(parts) > 1 else "unknown"
        
        midi_list = self.scraper.parse_midi_list(html, game_name, system_name)
        
        # Resolve actual download URLs
        for midi in midi_list:
            detail_html = self.client.get_text(midi.url)
            if detail_html:
                download_url = self.scraper.parse_midi_download_url(detail_html)
                if download_url:
                    midi.url = download_url
        
        return midi_list
