# AGENTS.md

## Development Commands

### Environment Setup
```bash
# Install dependencies with uv
uv sync

# Run with uv
uv run pytest tests/ -v --cov=midi_downloader
uv run black midi_downloader/ tests/
uv run flake8 midi_downloader/ tests/
uv run mypy midi_downloader/
```

### Testing
```bash
# Run all tests
uv run pytest tests/ -v --cov=midi_downloader

# Run single test file
uv run pytest tests/unit/domain/test_game.py -v

# Run single test function
uv run pytest tests/unit/domain/test_game.py::TestGame::test_game_creation -v

# Run with coverage report
uv run pytest tests/ --cov=midi_downloader --cov-report=html
```

### Code Quality
```bash
# Format code
uv run black midi_downloader/ tests/

# Lint code
uv run flake8 midi_downloader/ tests/

# Type checking
uv run mypy midi_downloader/
```

## Code Style Guidelines

### Architecture
- Follow 5-layer clean architecture: Presentation → Application → Domain ← Infrastructure
- Dependencies must only point inward
- Domain layer has zero external dependencies

### Imports
- Group imports: standard library, third-party, local application
- Use explicit relative imports within layers
- No circular dependencies between layers

### Formatting & Types
- Use Black for formatting (line length 88)
- Type hints required for all function signatures and class attributes
- Use dataclasses for domain entities
- Use protocols for interfaces

### Naming Conventions
- Classes: PascalCase (Game, MidiFile, DownloadService)
- Functions/variables: snake_case (download_file, game_url)
- Constants: UPPER_SNAKE_CASE (DEFAULT_DELAY, MAX_RETRIES)
- Private members: leading underscore (_internal_method)

### Error Handling
- Use custom exceptions for each layer (DomainException, InfrastructureException)
- Handle errors at appropriate layer boundaries
- Log errors with context and stack traces
- Never let exceptions cross layer boundaries without wrapping

### Testing
- Follow TDD: Red-Green-Refactor cycle
- Test coverage must exceed 90%
- Use descriptive test names that explain behavior
- Mock external dependencies in unit tests

### Documentation
- Docstrings for all public classes and functions
- Use Google-style docstring format
- Include type hints in docstring examples
- Update documentation with each increment