# src/model/song.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Song:
    """Model representing a song with metadata"""
    id: str
    title: str
    artist: str
    album: str
    duration: int  # Duration in seconds
    file_path: str
    genre: Optional[str] = None
    year: Optional[int] = None
    track_number: Optional[int] = None
    file_size: Optional[int] = None

    def __post_init__(self):
        """Validate song data after initialization"""
        if not self.id:
            raise ValueError("Song ID cannot be empty")
        if not self.title:
            raise ValueError("Song title cannot be empty")
        if not self.file_path:
            raise ValueError("File path cannot be empty")
        # Note: We allow duration = 0 for the test case, but validate negative values
        if self.duration < 0:
            raise ValueError("Duration cannot be negative")

    def __str__(self) -> str:
        return f"{self.artist} - {self.title} ({self.duration}s)"

    def __repr__(self) -> str:
        return f"Song(id='{self.id}', title='{self.title}', artist='{self.artist}')"

    def to_dict(self) -> dict:
        """Convert song to dictionary representation"""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration,
            'file_path': self.file_path,
            'genre': self.genre,
            'year': self.year,
            'track_number': self.track_number,
            'file_size': self.file_size
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Song':
        """Create Song instance from dictionary"""
        return cls(**data)

    def format_duration(self) -> str:
        """Format duration as MM:SS"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"


# Alternative simple implementation for comparison
class SimpleSong:
    def __init__(self, song_id, title, artist, album):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.album = album

    def __str__(self):
        return f"[{self.id}] {self.title} by {self.artist} ({self.album})"
