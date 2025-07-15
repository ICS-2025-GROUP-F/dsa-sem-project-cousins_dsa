from src.model.song import Song
from typing import List, Optional

class SongTable:
    def __init__(self):
        # Hash table: key = song ID, value = Song object
        self.table = {}
        self.total_operations = 0
        self.total_updates = 0
        self.collision_count = 0
        print("HASH TABLE: Initialized empty hash table for song updates")
        print("HASH TABLE: Using song ID as hash key for O(1) access time")
        self._print_table_stats()

    def load_from_list(self, song_list: List[Song]):
        """Load songs from list into the hash table with verbose logging"""
        print(f"\nHASH TABLE LOAD: Loading {len(song_list)} songs into hash table")
        print("HASH TABLE LOAD: Demonstrating hash function: song.id -> table[song.id]")
        
        for i, song in enumerate(song_list, 1):
            print(f"\nHASH TABLE LOAD: Processing song #{i}: '{song.title}'")
            
            # Show hash function operation
            hash_key = song.id
            print(f"HASH FUNCTION: hash(song.id={song.id}) = {hash_key}")
            print(f"HASH TABLE: Storing at table[{hash_key}]")
            
            # Check for collision (ID already exists)
            if song.id in self.table:
                print(f"COLLISION DETECTED: Key {song.id} already exists!")
                existing_song = self.table[song.id]
                print(f"   Existing: {existing_song.title} - {existing_song.artist}")
                print(f"   New: {song.title} - {song.artist}")
                self.collision_count += 1
                print(f"COLLISION HANDLING: Overwriting existing entry (collision #{self.collision_count})")
            else:
                print(f"HASH TABLE: No collision - key {song.id} is available")
            
            # Store in hash table
            self.table[song.id] = song
            print(f"HASH TABLE: Successfully stored '{song.title}' at key {song.id}")
            print(f"HASH TABLE: Table size now: {len(self.table)} entries")
            print(f"HASH TABLE: Load factor: {len(self.table)/1000:.3f} (assuming max 1000 songs)")
        
        print(f"\nHASH TABLE LOAD COMPLETE:")
        print(f"   Total songs processed: {len(song_list)}")
        print(f"   Final table size: {len(self.table)}")
        print(f"   Collisions encountered: {self.collision_count}")
        print(f"   Average access time: O(1) - constant time")
        self._print_table_stats()

    def load_from_database(self):
        """Load all songs from database into hash table with verbose logging"""
        print("\nHASH TABLE: Loading songs from database...")
        
        try:
            from src.db.database import get_all_songs
            songs = get_all_songs()
            print(f"DATABASE: Retrieved {len(songs)} songs from database")
            
            if songs:
                self.load_from_list(songs)
                print(f"HASH TABLE: Successfully loaded {len(songs)} songs into hash table")
            else:
                print("DATABASE: No songs found in database")
                
        except ImportError:
            print("HASH TABLE: Database module not available")

    def display_all(self):
        """Print all songs in the table with verbose logging"""
        print(f"\nHASH TABLE DISPLAY: Showing all {len(self.table)} entries")
        print("HASH TABLE DISPLAY: Format: Key[hash_value] -> Song_Object")
        
        if not self.table:
            print("HASH TABLE DISPLAY: Library is empty - no songs to display")
            return
        
        print("HASH TABLE CONTENTS:")
        sorted_items = sorted(self.table.items())  # Sort by ID for readability
        
        for key, song in sorted_items:
            print(f"   Key[{key}] -> '{song.title}' - {song.artist}")
            if song.album:
                print(f"              Album: {song.album}")
            if song.year:
                print(f"              Year: {song.year}")
            if song.genre:
                print(f"              Genre: {song.genre}")
        
        print(f"HASH TABLE DISPLAY: Complete - {len(self.table)} total entries")
        print(f"HASH TABLE DISPLAY: Each lookup takes O(1) constant time")

    def get_song(self, song_id: int) -> Optional[Song]:
        """Get a song by ID with verbose logging"""
        print(f"\nHASH TABLE GET: Looking up song with ID {song_id}")
        self.total_operations += 1
        
        # Demonstrate hash function lookup
        print(f"HASH FUNCTION: Calculating hash(song_id={song_id}) = {song_id}")
        print(f"HASH TABLE: Accessing table[{song_id}] directly")
        print(f"TIME COMPLEXITY: O(1) - constant time lookup")
        
        # Check if key exists
        if song_id in self.table:
            song = self.table[song_id]
            print(f"HASH TABLE GET: FOUND! '{song.title}' - {song.artist}")
            print(f"HASH TABLE GET: Retrieved in 1 operation (O(1) access)")
            return song
        else:
            print(f"HASH TABLE GET: NOT FOUND - No song with ID {song_id}")
            print(f"HASH TABLE GET: Available keys: {sorted(self.table.keys())}")
            return None

    def update_song(self, song_id: int, title=None, artist=None, album=None,
                    genre=None, year=None, duration=None, file_path=None) -> bool:
        """Update a song by ID with enhanced fields and verbose logging"""
        print(f"\nHASH TABLE UPDATE: Attempting to update song ID {song_id}")
        self.total_operations += 1
        
        # First, demonstrate hash lookup
        print(f"HASH FUNCTION: hash(song_id={song_id}) = {song_id}")
        print(f"HASH TABLE: Checking table[{song_id}] for existing entry")
        
        if song_id not in self.table:
            print(f"HASH TABLE UPDATE: Song ID '{song_id}' not found in hash table")
            print(f"HASH TABLE UPDATE: Hash lookup failed - key does not exist")
            print(f"HASH TABLE UPDATE: Available IDs: {sorted(self.table.keys())}")
            return False

        song = self.table[song_id]
        print(f"HASH TABLE UPDATE: Found song: '{song.title}' - {song.artist}")
        print(f"HASH TABLE UPDATE: Hash lookup successful in O(1) time")
        
        # Show original values
        print(f"ORIGINAL VALUES:")
        print(f"   Title: '{song.title}'")
        print(f"   Artist: '{song.artist}'")
        print(f"   Album: '{song.album}'")
        print(f"   Genre: '{song.genre}'")
        print(f"   Year: {song.year}")
        print(f"   Duration: {song.duration} seconds")
        
        # Track what's being updated
        updates_made = []
        
        print(f"\nUPDATE OPERATIONS:")
        
        # Update provided fields
        if title:
            print(f"UPDATING TITLE: '{song.title}' -> '{title}'")
            song.title = title
            updates_made.append("title")
            
        if artist:
            print(f"UPDATING ARTIST: '{song.artist}' -> '{artist}'")
            song.artist = artist
            updates_made.append("artist")
            
        if album:
            print(f"UPDATING ALBUM: '{song.album}' -> '{album}'")
            song.album = album
            updates_made.append("album")
            
        if genre:
            print(f"UPDATING GENRE: '{song.genre}' -> '{genre}'")
            song.genre = genre
            updates_made.append("genre")
            
        if year:
            print(f"UPDATING YEAR: {song.year} -> {year}")
            song.year = year
            updates_made.append("year")
            
        if duration:
            print(f"UPDATING DURATION: {song.duration} -> {duration} seconds")
            song.duration = duration
            updates_made.append("duration")
            
        if file_path:
            print(f"UPDATING FILE_PATH: '{song.file_path}' -> '{file_path}'")
            song.file_path = file_path
            updates_made.append("file_path")

        if not updates_made:
            print("HASH TABLE UPDATE: No updates provided - no changes made")
            return True

        print(f"HASH TABLE UPDATE: Updated fields: {', '.join(updates_made)}")
        print(f"HASH TABLE UPDATE: In-memory update completed in O(1) time")
        self.total_updates += 1

        # Persist to database if available
        print(f"DATABASE PERSISTENCE: Attempting to save changes to database...")
        try:
            from src.db.database import update_song_in_db
            
            if update_song_in_db(song):
                print(f"HASH TABLE UPDATE: Successfully updated song '{song_id}' in both hash table and database")
                print(f"UPDATE STATISTICS: Update operation #{self.total_updates} completed")
                self._print_updated_song(song)
                return True
            else:
                print(f"HASH TABLE UPDATE: Failed to update song '{song_id}' in database")
                print(f"HASH TABLE UPDATE: Hash table updated but database update failed")
                return True
                
        except ImportError:
            print(f"HASH TABLE UPDATE: Song '{song_id}' updated in memory (database not available)")
            print(f"UPDATE STATISTICS: Update operation #{self.total_updates} completed")
            self._print_updated_song(song)
            return True

    def refresh_song(self, song_id: int) -> bool:
        """Refresh a song from database with verbose logging"""
        print(f"\nHASH TABLE REFRESH: Refreshing song ID {song_id} from database")
        print(f"HASH FUNCTION: hash(song_id={song_id}) = {song_id}")
        
        try:
            from src.db.database import get_song_by_id
            updated_song = get_song_by_id(song_id)
            
            if updated_song:
                old_song = self.table.get(song_id)
                
                print(f"HASH TABLE REFRESH: Retrieved updated song from database")
                print(f"HASH TABLE: Updating table[{song_id}] with new data")
                
                self.table[song_id] = updated_song
                
                print(f"HASH TABLE REFRESH: Successfully refreshed song ID {song_id}")
                if old_song:
                    print(f"HASH TABLE REFRESH: Updated from '{old_song.title}' to '{updated_song.title}'")
                
                return True
            else:
                print(f"HASH TABLE REFRESH: Song ID {song_id} not found in database")
                return False
                
        except ImportError:
            print("HASH TABLE REFRESH: Database module not available for refresh")
            return False

    def _print_table_stats(self):
        """Internal method to print hash table statistics"""
        max_capacity = 1000  # Assuming reasonable max capacity
        load_factor = len(self.table) / max_capacity if len(self.table) > 0 else 0
        
        print(f"HASH TABLE STATISTICS:")
        print(f"   Current size: {len(self.table)} entries")
        print(f"   Total operations: {self.total_operations}")
        print(f"   Total updates: {self.total_updates}")
        print(f"   Collisions encountered: {self.collision_count}")
        print(f"   Load factor: {load_factor:.3f}")
        print(f"   Average access time: O(1) - constant")
        
        if len(self.table) > 0:
            collision_rate = (self.collision_count / len(self.table)) * 100
            print(f"   Collision rate: {collision_rate:.1f}%")

    def _print_updated_song(self, song):
        """Internal method to print updated song details"""
        print(f"UPDATED SONG DETAILS:")
        print(f"   ID: {song.id}")
        print(f"   Title: '{song.title}'")
        print(f"   Artist: '{song.artist}'")
        print(f"   Album: '{song.album}'")
        print(f"   Genre: '{song.genre}'")
        print(f"   Year: {song.year}")
        print(f"   Duration: {song.duration} seconds")

    def demonstrate_hash_function(self, song_ids):
        """Demonstrate hash function operation with multiple IDs"""
        print(f"\nHASH FUNCTION DEMONSTRATION:")
        print(f"Showing how hash function maps song IDs to table indices")
        
        for song_id in song_ids:
            hash_value = song_id  # Simple hash function for integer IDs
            print(f"hash({song_id}) = {hash_value} -> table[{hash_value}]")
            
            if song_id in self.table:
                song = self.table[song_id]
                print(f"   -> Contains: '{song.title}' - {song.artist}")
            else:
                print(f"   -> Empty slot")

# Test functionality with verbose output
if __name__ == "__main__":
    print("=" * 60)
    print("HASH TABLE DEMONSTRATION: Testing with verbose output")
    print("=" * 60)
    
    song_table = SongTable()

    # Create test songs
    songs = [
        Song(song_id=1, title="Hotel California", artist="Eagles", album="Hotel California", genre="Rock", year=1976),
        Song(song_id=5, title="Bohemian Rhapsody", artist="Queen", album="A Night at the Opera", genre="Rock", year=1975),
        Song(song_id=3, title="Imagine", artist="John Lennon", album="Imagine", genre="Pop", year=1971),
        Song(song_id=7, title="Yesterday", artist="The Beatles", album="Help!", genre="Pop", year=1965)
    ]

    print("\nTesting HASH TABLE LOAD operations:")
    song_table.load_from_list(songs)

    print("\nTesting HASH FUNCTION demonstration:")
    song_table.demonstrate_hash_function([1, 3, 5, 7, 9])

    print("\nTesting HASH TABLE GET operations:")
    song_table.get_song(5)  # Should find Bohemian Rhapsody
    song_table.get_song(99)  # Should not find

    print("\nTesting HASH TABLE UPDATE operations:")
    song_table.update_song(1, artist="The Eagles", year=1977, genre="Classic Rock")

    print("\nTesting HASH TABLE DISPLAY:")
    song_table.display_all()

    print("\nTesting collision scenario:")
    # Try to add song with existing ID
    duplicate_song = Song(song_id=1, title="Duplicate Song", artist="Test Artist")
    song_table.load_from_list([duplicate_song])

    print("\n" + "=" * 60)
    print("HASH TABLE DEMONSTRATION COMPLETE")
    print("O(1) constant time access demonstrated for all operations")
    print("=" * 60)
