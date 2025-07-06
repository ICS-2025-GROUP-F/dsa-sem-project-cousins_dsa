from src.model.song import Song
from src.db.database import update_song_in_db

class SongTable:
    def __init__(self):
        # Hash table: key = song ID, value = Song object
        self.table = {}

    def load_from_list(self, song_list):
        """Load songs from list into the hash table"""
        for song in song_list:
            self.table[song.id] = song

    def display_all(self):
        """Print all songs in the table"""
        if not self.table:
            print("Library is empty.")
            return
        for song in self.table.values():
            print(song)

    def update_song(self, song_id, title=None, artist=None, album=None):
        """Update a song by ID"""
        if song_id not in self.table:
            print(f"❌ Song ID '{song_id}' not found.")
            return False

        song = self.table[song_id]

        if title:
            song.title = title
        if artist:
            song.artist = artist
        if album:
            song.album = album

        # Persist to SQLite
        update_song_in_db(song)

        print(f"✅ Song '{song_id}' updated successfully.")
        return True
