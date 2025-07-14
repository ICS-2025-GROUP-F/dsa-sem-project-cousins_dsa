


from datetime import datetime

class Song:
    """Enhanced Song data model"""
    
    def __init__(self, song_id=None, title="", artist="", album="", duration=0,
                 file_path="", genre="", year=None, created_at=None):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.file_path = file_path
        self.genre = genre
        self.year = year
        self.created_at = created_at or datetime.now()
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    def __repr__(self):
        return f"Song(id={self.id}, title='{self.title}', artist='{self.artist}')"
    
    def to_dict(self):
        """Convert Song to dictionary for compatibility"""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "year": self.year,
            "duration": self.duration,
            "genre": self.genre,
            "file_path": self.file_path
        }

