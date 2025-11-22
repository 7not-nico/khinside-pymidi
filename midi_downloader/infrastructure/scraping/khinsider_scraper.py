"""Web scraper for khinsider.com using BeautifulSoup."""

from typing import List, Optional
from bs4 import BeautifulSoup
from midi_downloader.domain.entities import Game, MidiFile, GameSystem


class KhinsiderScraper:
    """Scrapes khinsider.com for MIDI information."""
    
    BASE_URL = "https://www.khinsider.com/midi"
    
    def parse_game_list(self, html_content: str, system_name: str) -> List[Game]:
        """
        Parse game list page for a system.
        
        Args:
            html_content: HTML content of the system page
            system_name: Name of the gaming system
            
        Returns:
            List of Game objects
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        games = []
        
        # Find the table containing games
        table = soup.find('table')
        if not table:
            return games
        
        # Find all rows (Context7 pattern for table parsing)
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                link = cells[0].find('a')
                if link:
                    game_name = link.text.strip()
                    game_url = link.get('href', '')
                    if game_url.startswith('/'):
                        game_url = f"https://www.khinsider.com{game_url}"
                    
                    games.append(Game(
                        name=game_name,
                        url=game_url,
                        system=system_name
                    ))
        
        return games
    
    def parse_midi_list(self, html_content: str, game_name: str, system_name: str) -> List[MidiFile]:
        """
        Parse MIDI file list for a game.
        
        Args:
            html_content: HTML content of the game page
            game_name: Name of the game
            system_name: Name of the system
            
        Returns:
            List of MidiFile objects
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        midi_files = []
        
        # Find table with MIDI downloads - it has no ID, just find the first table
        table = soup.find('table')
        if not table:
            return midi_files
        
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                # First cell has the MIDI file link
                link = cells[0].find('a')
                if link:
                    midi_name = link.text.strip()
                    midi_url = link.get('href', '')
                    
                    # The link goes directly to .mid file, not a detail page
                    if midi_url.startswith('//'):
                        midi_url = f"https:{midi_url}"
                    elif midi_url.startswith('/'):
                        midi_url = f"https://www.khinsider.com{midi_url}"
                    
                    # Only add if it's a .mid file
                    if '.mid' in midi_url:
                        midi_files.append(MidiFile(
                            name=midi_name,
                            url=midi_url,  # Direct download URL
                            game_name=game_name,
                            system=system_name
                        ))
        
        return midi_files
    
    def parse_midi_download_url(self, html_content: str) -> Optional[str]:
        """
        Parse the actual MIDI download URL from a MIDI detail page.
        
        Args:
            html_content: HTML content of the MIDI detail page
            
        Returns:
            Direct download URL or None
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find download link (usually marked with a distinct class or id)
        download_link = soup.find('a', string=lambda text: text and 'Click here to download' in text)
        if download_link:
            url = download_link.get('href', '')
            if url.startswith('//'):
                url = f"https:{url}"
            return url
        
        return None
