#!/usr/bin/env python3
"""Main entry point for MIDI Downloader CLI."""

import argparse
from pathlib import Path
from midi_downloader.infrastructure.http.khinsider_client import KhinsiderClient
from midi_downloader.infrastructure.scraping.khinsider_scraper import KhinsiderScraper
from midi_downloader.infrastructure.storage.file_system_repository import FileSystemRepository
from midi_downloader.infrastructure.storage.khinsider_repository_impl import KhinsiderRepositoryImpl
from midi_downloader.application.use_cases.download_game_use_case import DownloadGameUseCase
from midi_downloader.application.use_cases.download_system_use_case import DownloadSystemUseCase


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Download MIDI files from khinsider.com"
    )
    
    parser.add_argument(
        '--system',
        type=str,
        help='Gaming system to download (e.g., gameboy, nes)'
    )
    
    parser.add_argument(
        '--game',
        type=str,
        help='Specific game URL to download'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./midi_downloads',
        help='Output directory for downloads'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds'
    )
    
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Skip already downloaded files'
    )
    
    parser.add_argument(
        '--user-agent',
        type=str,
        help='Custom user agent string'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.system and not args.game:
        parser.error("Must specify either --system or --game")
    
    output_dir = Path(args.output)
    
    # Initialize dependencies (Dependency Injection)
    client = KhinsiderClient(
        rate_limit_delay=args.delay,
        user_agent=args.user_agent
    )
    scraper = KhinsiderScraper()
    file_repo = FileSystemRepository()
    khinsider_repo = KhinsiderRepositoryImpl(client, scraper)
    
    try:
        if args.game:
            # Download specific game
            download_game_uc = DownloadGameUseCase(khinsider_repo, file_repo, client)
            downloaded = download_game_uc.execute(args.game, output_dir, args.resume)
            print(f"\nDownloaded {len(downloaded)} MIDI files")
        
        elif args.system:
            # Download entire system
            download_game_uc = DownloadGameUseCase(khinsider_repo, file_repo, client)
            download_system_uc = DownloadSystemUseCase(khinsider_repo, download_game_uc)
            games = download_system_uc.execute(args.system, output_dir, args.resume)
            
            total_midis = sum(len(game.midi_files) for game in games)
            print(f"\nDownloaded {total_midis} MIDI files from {len(games)} games")
    
    finally:
        client.close()


if __name__ == '__main__':
    main()
