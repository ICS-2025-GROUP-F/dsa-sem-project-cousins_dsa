from src.model.song import Song
from typing import List, Optional


class SongTable:
    def __init__(self):
        # Hash table: key = song ID, value = Song object
        self.table = {}

    def load_from_list(self, song_list: List[Song]):
        """Load songs from list into the hash table"""
        for song in song_list:
            self.table[song.id] = song

    def load_from_database(self):
        """Load all songs from database into hash table"""
        try:
            from src.db.database import get_all_songs
            songs = get_all_songs()
            self.load_from_list(songs)
            print(f"Loaded {len(songs)} songs into hash table")
        except ImportError:
            print("Database module not available")

    def display_all(self):
        """Print all songs in the table"""
        if not self.table:
            print("Library is empty.")
            return
        print(f"Songs in library ({len(self.table)}):")
        for song in self.table.values():
            print(f"  {song}")

    def get_song(self, song_id: int) -> Optional[Song]:
        """Get a song by ID"""
        return self.table.get(song_id)

    def update_song(self, song_id: int, title=None, artist=None, album=None,
                    genre=None, year=None, duration=None, file_path=None) -> bool:
        """Update a song by ID with enhanced fields"""
        if song_id not in self.table:
            print(f"❌ Song ID '{song_id}' not found.")
            return False

        song = self.table[song_id]

        # Update provided fields
        if title:
            song.title = title
        if artist:
            song.artist = artist
        if album:
            song.album = album
        if genre:
            song.genre = genre
        if year:
            song.year = year
        if duration:
            song.duration = duration
        if file_path:
            song.file_path = file_path

        # Persist to database if available
        try:
            from src.db.database import update_song_in_db
            if update_song_in_db(song):
                print(f"✅ Song '{song_id}' updated successfully.")
                return True
            else:
                print(f"❌ Failed to update song '{song_id}' in database.")
                return False
        except ImportError:
            print(f"✅ Song '{song_id}' updated in memory (database not available).")
            return True

    def refresh_song(self, song_id: int) -> bool:
        """Refresh a song from database"""
        try:
            from src.db.database import get_song_by_id
            updated_song = get_song_by_id(song_id)
            if updated_song:
                self.table[song_id] = updated_song
                return True
            return False
        except ImportError:
            return False


# Test functionality if run directly
if __name__ == "__main__":
    song_table = SongTable()

    # Create test songs
    songs = [
        Song(song_id=1, title="Imagine", artist="John Lennon", album="Imagine"),
        Song(song_id=2, title="Bohemian Rhapsody", artist="Queen", album="A Night at the Opera")
    ]

    song_table.load_from_list(songs)
    song_table.display_all()

    # Test update
    result = song_table.update_song(2, artist="Freddie Mercury", year=1975)
    print(f"Update result: {result}")

    song_table.display_all()