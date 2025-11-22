"""Abstract repository interface for file operations."""

from abc import ABC, abstractmethod
from pathlib import Path


class FileRepository(ABC):
    """Interface for file system operations."""
    
    @abstractmethod
    def save_file(self, content: bytes, file_path: Path) -> bool:
        """Save binary content to a file."""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: Path) -> bool:
        """Check if a file exists."""
        pass
    
    @abstractmethod
    def create_directory(self, dir_path: Path) -> bool:
        """Create a directory if it doesn't exist."""
        pass
    
    @abstractmethod
    def get_file_size(self, file_path: Path) -> int:
        """Get file size in bytes."""
        pass
