import sqlite3
from datetime import datetime
from typing import List, Optional

DB_PATH = "songs.db"

class Song:
    """Song data model"""

    def __init__(self, song_id=None, title="", artist="", album="", duration=0,
                 file_path="", genre="", year=None, created_at=None):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration  # in seconds
        self.file_path = file_path
        self.genre = genre
        self.year = year
        self.created_at = created_at or datetime.now()

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def __repr__(self):
        return f"Song(id={self.id}, title='{self.title}', artist='{self.artist}')"


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
                album=row[3],
                duration=row[4],
                file_path=row[5],
                genre=row[6],
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
                album=row[3],
                duration=row[4],
                file_path=row[5],
                genre=row[6],
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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT id, title, artist, album, year FROM songs")
    rows = cursor.fetchall()

    connection.close()

    songs = []
    for row in rows:
        song = {
            "id": row[0],
            "title": row[1],
            "artist": row[2],
            "album": row[3],
            "year": row[4]
        }
        songs.append(song)

    return songs
def insert_song_to_db(song):
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

        cursor.execute('SELECT title, artist FROM songs WHERE id = ?', (song_id,))
        song_info = cursor.fetchone()

        if not song_info:
            print(f"No song found with ID: {song_id}")
            return False

        cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
        conn.commit()

        print(f"Successfully deleted song: {song_info[0]} - {song_info[1]}")
        return True

    except sqlite3.Error as e:
        print(f"Error deleting song: {e}")
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
                album=row[3],
                duration=row[4],
                file_path=row[5],
                genre=row[6],
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

if __name__ == "__main__":
    # Initialize database
    init_db()

    song1 = Song(
        title="Bohemian Rhapsody",
        artist="Queen",
        album="A Night at the Opera",
        duration=355,
        file_path="/music/queen/bohemian_rhapsody.mp3",
        genre="Rock",
        year=1975
    )

    song2 = Song(
        title="Hotel California",
        artist="Eagles",
        album="Hotel California",
        duration=391,
        file_path="/music/eagles/hotel_california.mp3",
        genre="Rock",
        year=1976
    )

    insert_song_to_db(song1)
    insert_song_to_db(song2)

    all_songs = get_all_songs()
    print(f"\nAll songs in database ({len(all_songs)}):")
    for song in all_songs:
        print(f"  {song}")

    if all_songs:
        song_to_update = all_songs[0]
        song_to_update.year = 1974  # Update year
        update_song_in_db(song_to_update)

    search_results = search_songs("Queen")
    print(f"\nSearch results for 'Queen':")
    for song in search_results:
        print(f"  {song}")
