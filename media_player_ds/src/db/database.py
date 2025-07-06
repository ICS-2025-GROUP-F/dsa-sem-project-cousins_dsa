import sqlite3
from src.model.song import Song

DB_PATH = "songs.db"

def init_db():
    """Initialize SQLite DB and create songs table if not exists"""
    pass  # TODO: Implement DB creation and schema

def get_all_songs():
    """Retrieve all songs from the database"""
    pass  # TODO: Return list of Song objects

def insert_song_to_db(song):
    """Insert a new song into the DB"""
    pass  # TODO: Accept a Song object and insert into table

def update_song_in_db(song):
    """Update a song row in the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE songs
        SET title = ?, artist = ?, album = ?
        WHERE id = ?
    """, (song.title, song.artist, song.album, song.id))
    conn.commit()
    conn.close()

def delete_song_from_db(song_id):
    """Delete a song from the DB by ID"""
    pass  # TODO: Delete entry using song ID
