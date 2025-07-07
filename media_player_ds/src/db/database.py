import sqlite3

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
    """Update an existing song in the DB"""
    pass  # TODO: Match by ID and update metadata


def delete_song_from_db(song_id):
    """Delete a song from the DB by ID"""
    try:
        conn = sqlite3.connect("songs.db")  
        cursor = conn.cursor()

        # DELETE command
        cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))

        # Check if a song was deleted
        if cursor.rowcount == 0:
            print(f"No song found with ID {song_id}.")
        else:
            print(f"Song with ID {song_id} deleted from database.")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

   
