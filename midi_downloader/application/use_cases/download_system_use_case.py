"""Download use case for downloading MIDIs from an entire system."""

from pathlib import Path
from typing import List
from tqdm import tqdm
from midi_downloader.domain.entities import Game
from midi_downloader.domain.repositories import KhinsiderRepository
from midi_downloader.application.use_cases.download_game_use_case import DownloadGameUseCase


class DownloadSystemUseCase:
    """Use case for downloading all MIDIs from a gaming system."""
    
    def __init__(
        self,
        khinsider_repo: KhinsiderRepository,
        download_game_use_case: DownloadGameUseCase
    ):
        """
        Initialize use case with dependencies.
        
        Args:
            khinsider_repo: Repository for khinsider data
            download_game_use_case: Use case for downloading individual games
        """
        self.khinsider_repo = khinsider_repo
        self.download_game_use_case = download_game_use_case
    
    def execute(
        self,
        system_name: str,
        output_dir: Path,
        resume: bool = False
    ) -> List[Game]:
        """
        Download all MIDI files from a gaming system.
        
        Args:
            system_name: Name of the gaming system (e.g., 'gameboy')
            output_dir: Base directory to save files
            resume: Skip already downloaded files
            
        Returns:
            List of Game objects with downloaded files
        """
        # Get game list for system
        games = self.khinsider_repo.get_games_for_system(system_name)
        
        if not games:
            print(f"No games found for system: {system_name}")
            return []
        
        print(f"Found {len(games)} games for {system_name}")
        
        # Create system directory
        system_dir = output_dir / system_name
        system_dir.mkdir(parents=True, exist_ok=True)
        
        # Download each game with progress tracking
        with tqdm(games, desc=f"Processing {system_name}", unit="game") as pbar:
            for game in pbar:
                pbar.set_postfix_str(f"{game.name[:30]}...")
                
                game_dir = system_dir / game.name
                game.midi_files = self.download_game_use_case.execute(
                    game.url,
                    game_dir,
                    resume=resume
                )
        
        return games
