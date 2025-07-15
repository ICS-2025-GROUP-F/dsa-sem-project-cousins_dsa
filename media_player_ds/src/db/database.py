import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import sqlite3
from datetime import datetime
from typing import List, Optional
from src.model.song import Song




DB_PATH = "songs.db"

def init_db():
    """Initialize SQLite DB and create songs table if not exists"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                album TEXT,
                duration INTEGER DEFAULT 0,
                file_path TEXT,
                genre TEXT,
                year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        print("Database initialized successfully")

    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def get_all_songs() -> List[Song]:
    """Retrieve all songs from the database"""
    songs = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, artist, album, duration, file_path, genre, year, created_at
            FROM songs
            ORDER BY title, artist
        ''')

        rows = cursor.fetchall()

        for row in rows:
            song = Song(
                song_id=row[0],
                title=row[1],
                artist=row[2],
                album=row[3] or "",
                duration=row[4] or 0,
                file_path=row[5] or "",
                genre=row[6] or "",
                year=row[7],
                created_at=row[8]
            )
            songs.append(song)

    except sqlite3.Error as e:
        print(f"Error retrieving songs: {e}")
    finally:
        if conn:
            conn.close()

    return songs

def get_song_by_id(song_id: int) -> Optional[Song]:
    """Retrieve a specific song by ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, artist, album, duration, file_path, genre, year, created_at
            FROM songs WHERE id = ?
        ''', (song_id,))

        row = cursor.fetchone()

        if row:
            return Song(
                song_id=row[0],
                title=row[1],
                artist=row[2],
                album=row[3] or "",
                duration=row[4] or 0,
                file_path=row[5] or "",
                genre=row[6] or "",
                year=row[7],
                created_at=row[8]
            )

    except sqlite3.Error as e:
        print(f"Error retrieving song: {e}")
    finally:
        if conn:
            conn.close()

    return None

def insert_song_to_db(song: Song) -> bool:
    """Insert a new song into the DB"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO songs (title, artist, album, duration, file_path, genre, year)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (song.title, song.artist, song.album, song.duration,
              song.file_path, song.genre, song.year))

        song.id = cursor.lastrowid  # Set the ID from the inserted row
        conn.commit()

        print(f"Successfully inserted song: {song}")
        return True

    except sqlite3.Error as e:
        print(f"Error inserting song: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_song_in_db(song: Song) -> bool:
    """Update an existing song in the DB"""
    if not song.id:
        print("Error: Song ID is required for update")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE songs 
            SET title = ?, artist = ?, album = ?, duration = ?, 
                file_path = ?, genre = ?, year = ?
            WHERE id = ?
        ''', (song.title, song.artist, song.album, song.duration,
              song.file_path, song.genre, song.year, song.id))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Successfully updated song: {song}")
            return True
        else:
            print(f"No song found with ID: {song.id}")
            return False

    except sqlite3.Error as e:
        print(f"Error updating song: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_song_from_db(song_id: int) -> bool:
    """Delete a song from the DB by ID"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get song info before deleting for confirmation
        cursor.execute('SELECT title, artist FROM songs WHERE id = ?', (song_id,))
        song_info = cursor.fetchone()

        if not song_info:
            print(f"No song found with ID {song_id}.")
            return False

        # DELETE command
        cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
        
        # Verify deletion
        if cursor.rowcount > 0:
            conn.commit()
            print(f"Song with ID {song_id} deleted from database.")
            return True
        else:
            print(f"Failed to delete song with ID {song_id}.")
            return False
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def search_songs(query: str) -> List[Song]:
    """Search songs by title or artist"""
    songs = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, artist, album, duration, file_path, genre, year, created_at
            FROM songs 
            WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?
            ORDER BY title, artist
        ''', (f'%{query}%', f'%{query}%', f'%{query}%'))

        rows = cursor.fetchall()

        for row in rows:
            song = Song(
                song_id=row[0],
                title=row[1],
                artist=row[2],
                album=row[3] or "",
                duration=row[4] or 0,
                file_path=row[5] or "",
                genre=row[6] or "",
                year=row[7],
                created_at=row[8]
            )
            songs.append(song)

    except sqlite3.Error as e:
        print(f"Error searching songs: {e}")
    finally:
        if conn:
            conn.close()

    return songs

# Test functionality
if __name__ == "__main__":
    print("Testing database functionality...")
    
    # Initialize database
    init_db()
    
    # Create test songs
    song1 = Song(
        title="Bohemian Rhapsody",
        artist="Queen",
        album="A Night at the Opera",
        duration=355,
        genre="Rock",
        year=1975
    )
    
    song2 = Song(
        title="Hotel California",
        artist="Eagles",
        album="Hotel California",
        duration=391,
        genre="Rock",
        year=1976
    )
    
    # Test insert
    print("\n--- Testing Insert ---")
    insert_song_to_db(song1)
    insert_song_to_db(song2)
    
    # Test retrieve all
    print("\n--- Testing Retrieve All ---")
    all_songs = get_all_songs()
    print(f"Found {len(all_songs)} songs:")
    for song in all_songs:
        print(f"  {song}")
    
    # Test delete
    if all_songs:
        print("\n--- Testing Delete ---")
        first_song_id = all_songs[0].id
        success = delete_song_from_db(first_song_id)
        print(f"Delete success: {success}")
    
    print("\n✅ Database test completed!")
