import sqlite3

DB_PATH = "songs.db"

def init_db():
    """Initialize SQLite DB and create songs table if not exists"""
    pass  # TODO: Implement DB creation and schema

def get_all_songs():
    """Retrieve all songs from the database"""
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
    pass  # TODO: Accept a Song object and insert into table

def update_song_in_db(song):
    """Update an existing song in the DB"""
    pass  # TODO: Match by ID and update metadata

def delete_song_from_db(song_id):
    """Delete a song from the DB by ID"""
    pass  # TODO: Delete entry using song ID
