# MIDI Downloader Project Documentation

## Overview

A Python script to download MIDI files from khinsider.com with maximum separation of concerns architecture.

## Website Structure

- **Base URL**: `https://www.khinsider.com/midi/{system}`
- **Example**: `https://www.khinsider.com/midi/gameboy`
- **Organization**: System → Game → Individual MIDI files

## Project Goals

1. Download MIDI files organized in folder structure
2. Respect website resources with rate limiting
3. Handle errors gracefully and resume interrupted downloads
4. Provide user-friendly CLI interface
5. Maintain clean, testable architecture

## Architecture Overview

### Core Architectural Principles

**Dependency Rule**: Dependencies can only point inward
```
Presentation → Application → Domain ← Infrastructure
```

### Layer 1: Domain Layer (Pure Business Logic)

**Purpose**: Core business entities with zero external dependencies

**Components**:
- `entities/`: Game, MidiFile, GameSystem, DownloadTask
- `value_objects/`: FilePath, Url, FileSize (immutable objects)
- `repositories/`: Abstract interfaces for data access

**Key Rules**:
- No imports from external libraries
- Pure Python objects and business rules
- Framework and database agnostic

### Layer 2: Application Layer (Use Cases)

**Purpose**: Orchestrates domain objects to fulfill business requirements

**Components**:
- `use_cases/`: DownloadSystemUseCase, DownloadGameUseCase, ListGamesUseCase
- `services/`: DownloadService, FileOrganizationService, ValidationService
- `dto/`: Data transfer objects for layer boundaries

**Key Rules**:
- Contains application business logic
- Depends only on domain layer
- No infrastructure concerns

### Layer 3: Infrastructure Layer (External Concerns)

**Purpose**: Implements interfaces defined in domain layer

**Components**:
- `http/`: KhinsiderHttpClient, RateLimiter
- `scraping/`: KhinsiderScraper, HtmlParser
- `storage/`: FileSystemRepository, ConfigurationRepository
- `logging/`: Logger implementation

**Key Rules**:
- Implements domain interfaces
- Contains all external dependencies
- Framework-specific code lives here

### Layer 4: Presentation Layer (User Interface)

**Purpose**: Handles user interaction and output formatting

**Components**:
- `cli/`: CLIController, commands, input validation
- `views/`: ProgressView, ErrorView, ResultView

**Key Rules**:
- Thin layer with minimal logic
- Routes to appropriate use cases
- Formats output for users

### Layer 5: Cross-Cutting Concerns

**Purpose**: Shared functionality across layers

**Components**:
- `config/`: Settings, constants
- `utils/`: FileUtils, StringUtils, RetryHandler
- `exceptions/`: Custom exceptions by layer

## Directory Structure

```
midi_downloader/
├── domain/                    # Core business entities
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── game.py
│   │   ├── midi_file.py
│   │   ├── game_system.py
│   │   └── download_task.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── file_path.py
│   │   ├── url.py
│   │   └── file_size.py
│   └── repositories/
│       ├── __init__.py
│       ├── khinsider_repository.py
│       ├── file_repository.py
│       └── download_repository.py
│
├── application/               # Use cases and business logic
│   ├── __init__.py
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── download_system_use_case.py
│   │   ├── download_game_use_case.py
│   │   ├── list_games_use_case.py
│   │   └── resume_download_use_case.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── download_service.py
│   │   ├── file_organization_service.py
│   │   └── validation_service.py
│   └── dto/
│       ├── __init__.py
│       ├── download_request.py
│       └── download_result.py
│
├── infrastructure/            # External implementations
│   ├── __init__.py
│   ├── http/
│   │   ├── __init__.py
│   │   ├── khinsider_client.py
│   │   └── rate_limiter.py
│   ├── scraping/
│   │   ├── __init__.py
│   │   ├── khinsider_scraper.py
│   │   └── html_parser.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── file_system_repository.py
│   │   └── configuration_repository.py
│   └── logging/
│       ├── __init__.py
│       └── logger.py
│
├── presentation/              # User interface
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── commands.py
│   │   └── validators.py
│   └── views/
│       ├── __init__.py
│       ├── progress_view.py
│       ├── error_view.py
│       └── result_view.py
│
├── shared/                     # Cross-cutting concerns
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── constants.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   ├── string_utils.py
│   │   └── retry_handler.py
│   └── exceptions/
│       ├── __init__.py
│       ├── domain_exceptions.py
│       ├── infrastructure_exceptions.py
│       └── application_exceptions.py
│
├── tests/                      # Test structure mirrors source
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   └── integration/
│
├── main.py                     # Application entry point
├── requirements.txt
├── setup.py
└── README.md
```

## Key Design Patterns Applied

1. **Repository Pattern**: Abstract data access
2. **Factory Pattern**: Entity creation
3. **Strategy Pattern**: Download strategies
4. **Observer Pattern**: Progress reporting
5. **Command Pattern**: CLI operations
6. **Dependency Injection**: Testable, loose coupling

## CLI Interface Design

```bash
# Download all Game Boy MIDI files
python midi_downloader.py --system gameboy --output ./midis

# Download all systems
python midi_downloader.py --all-systems --output ./all_midis

# Download specific game
python midi_downloader.py --system gameboy --game "pokemon-red" --output ./pokemon

# Preview without downloading
python midi_downloader.py --dry-run --system gameboy

# Resume interrupted downloads
python midi_downloader.py --resume --system gameboy --output ./midis
```

## Configuration Options

- `--system`: Specific gaming system to download
- `--game`: Specific game to download
- `--output`: Output directory for downloaded files
- `--delay`: Seconds between requests (default: 1)
- `--dry-run`: Preview without downloading
- `--resume`: Skip existing files
- `--user-agent`: Custom user agent string
- `--all-systems`: Download from all available systems

## File Organization

```
output_dir/
├── gameboy/
│   ├── pokemon-red/
│   │   ├── title-theme.mid
│   │   └── battle-theme.mid
│   └── zelda/
│       └── overworld.mid
└── nes/
    └── super-mario/
        └── main-theme.mid
```

## Dependencies

### Core Dependencies
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `tqdm` - Progress bars
- `pathlib` - Cross-platform file paths (built-in)

### Development Dependencies
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting

## Error Handling Strategy

### Network Errors
- Timeouts with exponential backoff
- HTTP error handling (404, 503, etc.)
- Rate limiting and retry logic

### File System Errors
- Permission checking
- Disk space validation
- Cross-platform filename sanitization

### Graceful Degradation
- Continue with next file on individual failures
- Log failed URLs for manual retry
- Progress persistence for resume capability

## Testing Strategy

### Unit Tests
- Domain entities: Pure business logic
- Use cases: Application logic
- Services: Business services

### Integration Tests
- HTTP client with real khinsider.com
- File system operations
- End-to-end download workflows

### Test Structure
- Mirrors source code structure
- Mock external dependencies
- Test coverage for all layers

## Benefits of This Architecture

- **Testability**: Each layer can be unit tested in isolation
- **Maintainability**: Changes in one layer don't affect others
- **Flexibility**: Easy to swap implementations (e.g., different scrapers)
- **Scalability**: Clear boundaries for adding new features
- **Readability**: Clear separation makes code self-documenting

## Implementation Phases

### Phase 1: Core Foundation
1. Domain entities and value objects
2. Basic repository interfaces
3. Configuration management

### Phase 2: Infrastructure
1. HTTP client and rate limiting
2. HTML scraper implementation
3. File system operations

### Phase 3: Application Logic
1. Use cases implementation
2. Business services
3. Error handling and retry logic

### Phase 4: User Interface
1. CLI controller and commands
2. Progress views and formatting
3. Input validation

### Phase 5: Testing & Polish
1. Comprehensive test suite
2. Documentation completion
3. Performance optimization

## Existing Tools Research

### Similar Projects Found
- `khinsider-dl` (PyPI package) - General audio downloads
- `AngeloM18/khinsider-scraper` - Python scraper
- `soxmonitor/khinsider_mass_downloader_script` - Mass downloader

### Key Insights
- Website structure is well-established
- Rate limiting is essential
- HTML parsing with BeautifulSoup is standard approach
- Progress tracking improves user experience

## Next Steps

1. Set up project structure
2. Implement domain entities
3. Create repository interfaces
4. Build HTTP client and scraper
5. Implement use cases
6. Create CLI interface
7. Add comprehensive testing
8. Documentation and deployment