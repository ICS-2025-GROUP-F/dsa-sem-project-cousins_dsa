
from src.model.song import Song
from typing import Optional, List
import sqlite3

class BSTNode:
    def __init__(self, song: Song):
        self.song = song
        self.left = None
        self.right = None

class SongBST:
    def __init__(self):
        self.root = None
    
    def insert(self, song: Song):
        """Insert a song into the BST"""
        def _insert(root, song):
            if root is None:
                return BSTNode(song)
            elif root.song.title == song.title:
                return root
            elif song.title < root.song.title:
                root.left = _insert(root.left, song)
            else:
                root.right = _insert(root.right, song)
            return root
        
        self.root = _insert(self.root, song)
    
    def search_by_title(self, title: str) -> Optional[Song]:
        """Search for song by title"""
        def _search(root, title):
            if root is None:
                return None
            if root.song.title == title:
                return root.song
            elif title < root.song.title:
                return _search(root.left, title)
            else:
                return _search(root.right, title)
        
        return _search(self.root, title)
    
    def inorder_traversal(self):
        """Print all songs in sorted title order"""
        def _inorder(root):
            if root:
                _inorder(root.left)
                print(f"Title: {root.song.title}, Artist: {root.song.artist}")
                _inorder(root.right)
        
        _inorder(self.root)

# Legacy functions for GUI compatibility
def get_all_songs():
    """Get songs from database as Song objects"""
    try:
        conn = sqlite3.connect("songs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, artist, album, year FROM songs")
        rows = cursor.fetchall()
        conn.close()
        
        songs = []
        for row in rows:
            song = Song(
                song_id=row[0],
                title=row[1],
                artist=row[2],
                album=row[3],
                year=row[4]
            )
            songs.append(song)
        return songs
    except:
        return []

def read_song_data():
    """Legacy function - returns dict format for GUI"""
    songs = get_all_songs()
    return [song.to_dict() for song in songs]

def insert(root, song_data):
    """Legacy insert function"""
    if isinstance(song_data, dict):
        song = Song(
            song_id=song_data.get("id"),
            title=song_data.get("title", ""),
            artist=song_data.get("artist", ""),
            album=song_data.get("album", ""),
            year=song_data.get("year")
        )
    else:
        song = song_data
    
    if root is None:
        return BSTNode(song)
    elif song.title < root.song.title:
        root.left = insert(root.left, song)
    else:
        root.right = insert(root.right, song)
    return root

def search_by_title(root, title):
    """Legacy search function"""
    if root is None:
        return None
    if root.song.title == title:
        return root.song.to_dict()
    elif title < root.song.title:
        return search_by_title(root.left, title)
    else:
        return search_by_title(root.right, title)

def inorder(root):
    """Legacy inorder function"""
    if root:
        inorder(root.left)
        print(f"Title: {root.song.title}, Artist: {root.song.artist}")
        inorder(root.right)
