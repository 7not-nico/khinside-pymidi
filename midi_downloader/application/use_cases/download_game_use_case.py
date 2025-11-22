"""Download use case for downloading MIDIs from a game."""

from pathlib import Path
from typing import List
from tqdm import tqdm
from midi_downloader.domain.entities import MidiFile
from midi_downloader.domain.repositories import KhinsiderRepository, FileRepository
from midi_downloader.infrastructure.http.khinsider_client import KhinsiderClient


class DownloadGameUseCase:
    """Use case for downloading all MIDIs from a game."""
    
    def __init__(
        self,
        khinsider_repo: KhinsiderRepository,
        file_repo: FileRepository,
        client: KhinsiderClient
    ):
        """
        Initialize use case with dependencies.
        
        Args:
            khinsider_repo: Repository for khinsider data
            file_repo: Repository for file operations
            client: HTTP client for downloads
        """
        self.khinsider_repo = khinsider_repo
        self.file_repo = file_repo
        self.client = client
    
    def execute(
        self,
        game_url: str,
        output_dir: Path,
        resume: bool = False
    ) -> List[MidiFile]:
        """
        Download all MIDI files from a game.
        
        Args:
            game_url: URL of the game page
            output_dir: Directory to save files
            resume: Skip already downloaded files
            
        Returns:
            List of successfully downloaded MidiFile objects
        """
        # Get MIDI file list
        midi_files = self.khinsider_repo.get_midi_files_for_game(game_url)
        
        if not midi_files:
            print("No MIDI files found for this game.")
            return []
        
        # Create output directory
        self.file_repo.create_directory(output_dir)
        
        downloaded = []
        
        # Download with tqdm progress bar (Context7 pattern)
        with tqdm(midi_files, desc="Downloading MIDIs", unit="file") as pbar:
            for midi in pbar:
                pbar.set_postfix_str(f"{midi.name[:30]}...")
                
                file_path = output_dir / midi.filename
                
                # Skip if resuming and file exists
                if resume and self.file_repo.file_exists(file_path):
                    midi.mark_downloaded()
                    downloaded.append(midi)
                    continue
                
                # Download file
                content = self.client.get(midi.url)
                if content:
                    if self.file_repo.save_file(content, file_path):
                        midi.size_bytes = len(content)
                        midi.mark_downloaded()
                        downloaded.append(midi)
        
        return downloaded
