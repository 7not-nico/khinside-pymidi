# MIDI Downloader

Download MIDI files from khinsider.com with a clean architecture.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Download all MIDIs from a gaming system:
```bash
python main.py --system gameboy --output ./midis
```

### Download MIDIs from a specific game:
```bash
python main.py --game https://www.khinsider.com/midi/gameboy/pokemon-red --output ./pokemon
```

### Resume interrupted downloads:
```bash
python main.py --system gameboy --output ./midis --resume
```

### Custom options:
```bash
python main.py --system nes --output ./nes_midis --delay 2.0 --user-agent "MyBot/1.0"
```

## Options

- `--system`: Gaming system to download (e.g., `gameboy`, `nes`, `snes`)
- `--game`: Specific game URL to download
- `--output`: Output directory (default: `./midi_downloads`)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--resume`: Skip already downloaded files
- `--user-agent`: Custom user agent string

## Architecture

This project follows Clean Architecture principles:

- **Domain Layer**: Pure business logic with no external dependencies
- **Application Layer**: Use cases and business services
- **Infrastructure Layer**: HTTP, scraping, file I/O implementations
- **Presentation Layer**: CLI interface

## Dependencies

- `requests`: HTTP requests with retry logic
- `beautifulsoup4`: HTML parsing
- `tqdm`: Progress bars
