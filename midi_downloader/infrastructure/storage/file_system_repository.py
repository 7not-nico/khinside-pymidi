"""File system repository implementation."""

from pathlib import Path
from typing import Optional
from midi_downloader.domain.repositories import FileRepository


class FileSystemRepository(FileRepository):
    """Concrete implementation of FileRepository using pathlib."""
    
    def save_file(self, content: bytes, file_path: Path) -> bool:
        """Save binary content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(content)
            return True
        except Exception as e:
            print(f"Failed to save file {file_path}: {e}")
            return False
    
    def file_exists(self, file_path: Path) -> bool:
        """Check if a file exists."""
        return file_path.exists() and file_path.is_file()
    
    def create_directory(self, dir_path: Path) -> bool:
        """Create a directory if it doesn't exist."""
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create directory {dir_path}: {e}")
            return False
    
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        try:
            return file_path.stat().st_size if self.file_exists(file_path) else 0
        except Exception:
            return 0
