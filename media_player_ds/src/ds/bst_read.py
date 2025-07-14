from src.model.song import Song
from typing import Optional, List
import sqlite3

class BSTNode:
    def __init__(self, song: Song):
        self.song = song
        self.left = None
        self.right = None
        print(f"BST: Created new node for '{song.title}' by {song.artist}")

class SongBST:
    def __init__(self):
        self.root = None
        self.node_count = 0
        print("BST: Initialized empty Binary Search Tree")
    
    def insert(self, song: Song):
        """Insert a song into the BST with verbose logging"""
        print(f"\nBST INSERT: Starting insertion of '{song.title}'")
        
        def _insert(root, song, depth=0):
            indent = "  " * depth
            
            if root is None:
                print(f"{indent}BST: Creating new node at depth {depth}")
                self.node_count += 1
                return BSTNode(song)
            
            if root.song.title == song.title:
                print(f"{indent}BST: Song '{song.title}' already exists, skipping")
                return root
            elif song.title < root.song.title:
                print(f"{indent}BST: '{song.title}' < '{root.song.title}' -> Going LEFT")
                root.left = _insert(root.left, song, depth + 1)
            else:
                print(f"{indent}BST: '{song.title}' > '{root.song.title}' -> Going RIGHT")
                root.right = _insert(root.right, song, depth + 1)
            
            return root
        
        self.root = _insert(self.root, song)
        print(f"BST: Insertion complete. Tree now has {self.node_count} nodes")
        self._print_tree_structure()
    
    def search_by_title(self, title: str) -> Optional[Song]:
        """Search for song by title with verbose logging"""
        print(f"\nBST SEARCH: Looking for '{title}'")
        comparisons = 0
        
        def _search(root, title, depth=0):
            nonlocal comparisons
            indent = "  " * depth
            comparisons += 1
            
            if root is None:
                print(f"{indent}BST: Reached leaf node - NOT FOUND")
                return None
            
            print(f"{indent}BST: Comparing '{title}' with '{root.song.title}'")
            
            if root.song.title == title:
                print(f"{indent}BST: FOUND! '{title}' at depth {depth}")
                return root.song
            elif title < root.song.title:
                print(f"{indent}BST: '{title}' < '{root.song.title}' -> Searching LEFT")
                return _search(root.left, title, depth + 1)
            else:
                print(f"{indent}BST: '{title}' > '{root.song.title}' -> Searching RIGHT")
                return _search(root.right, title, depth + 1)
        
        result = _search(self.root, title)
        print(f"BST: Search completed in {comparisons} comparisons")
        print(f"BST: Result: {'FOUND' if result else 'NOT FOUND'}")
        return result
    
    def inorder_traversal(self) -> List[Song]:
        """Return all songs in sorted order with verbose logging"""
        print(f"\nBST TRAVERSAL: Starting in-order traversal of {self.node_count} nodes")
        songs = []
        visit_count = 0
        
        def _inorder(root, depth=0):
            nonlocal visit_count
            indent = "  " * depth
            
            if root:
                visit_count += 1
                print(f"{indent}BST: Visiting node '{root.song.title}' at depth {depth}")
                
                # Left subtree
                if root.left:
                    print(f"{indent}BST: Traversing LEFT subtree")
                    _inorder(root.left, depth + 1)
                else:
                    print(f"{indent}BST: No left child")
                
                # Process current node
                print(f"{indent}BST: Processing '{root.song.title}' (#{len(songs) + 1} in sorted order)")
                songs.append(root.song)
                
                # Right subtree
                if root.right:
                    print(f"{indent}BST: Traversing RIGHT subtree")
                    _inorder(root.right, depth + 1)
                else:
                    print(f"{indent}BST: No right child")
        
        _inorder(self.root)
        print(f"BST: Traversal complete. Visited {visit_count} nodes, collected {len(songs)} songs")
        print(f"BST: Songs in alphabetical order:")
        for i, song in enumerate(songs, 1):
            print(f"   {i}. {song.title} - {song.artist}")
        
        return songs
    
    def _print_tree_structure(self):
        """Print visual representation of tree structure"""
        if not self.root:
            print("BST: Tree is empty")
            return
        
        print("BST: Current tree structure:")
        
        def _print_structure(root, level=0, prefix="Root: "):
            if root:
                print("  " * level + prefix + f"'{root.song.title}'")
                if root.left or root.right:
                    if root.left:
                        _print_structure(root.left, level + 1, "L--- ")
                    else:
                        print("  " * (level + 1) + "L--- (empty)")
                    if root.right:
                        _print_structure(root.right, level + 1, "R--- ")
                    else:
                        print("  " * (level + 1) + "R--- (empty)")
        
        _print_structure(self.root)

# Legacy functions with verbose output
def get_all_songs():
    """Get songs from database as Song objects with verbose logging"""
    print("\nBST: Loading songs from database (legacy function)")
    try:
        conn = sqlite3.connect("songs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, artist, album, year FROM songs")
        rows = cursor.fetchall()
        conn.close()
        
        print(f"BST: Retrieved {len(rows)} songs from database")
        
        songs = []
        for i, row in enumerate(rows, 1):
            song = Song(
                song_id=row[0],
                title=row[1],
                artist=row[2],
                album=row[3],
                year=row[4]
            )
            songs.append(song)
            print(f"BST: Loaded song #{i}: {song.title} - {song.artist}")
        
        return songs
    except Exception as e:
        print(f"BST: Error loading songs: {e}")
        return []

def read_song_data():
    """Legacy function - returns dict format for GUI with verbose logging"""
    print("\nBST: Converting songs to dictionary format for GUI compatibility")
    songs = get_all_songs()
    song_dicts = [song.to_dict() for song in songs]
    print(f"BST: Converted {len(song_dicts)} songs to dictionary format")
    return song_dicts

def insert(root, song_data):
    """Legacy insert function with verbose logging"""
    if isinstance(song_data, dict):
        print(f"BST: Converting dictionary to Song object: {song_data.get('title')}")
        song = Song(
            song_id=song_data.get("id"),
            title=song_data.get("title", ""),
            artist=song_data.get("artist", ""),
            album=song_data.get("album", ""),
            year=song_data.get("year")
        )
    else:
        song = song_data
        print(f"BST: Using Song object directly: {song.title}")
    
    if root is None:
        print(f"BST: Creating root node for '{song.title}'")
        return BSTNode(song)
    elif song.title < root.song.title:
        print(f"BST: '{song.title}' goes to LEFT of '{root.song.title}'")
        root.left = insert(root.left, song)
    else:
        print(f"BST: '{song.title}' goes to RIGHT of '{root.song.title}'")
        root.right = insert(root.right, song)
    
    return root

def search_by_title(root, title):
    """Legacy search function with verbose logging"""
    if root is None:
        print(f"BST: Search reached null node - '{title}' not found")
        return None
    
    print(f"BST: Comparing '{title}' with '{root.song.title}'")
    
    if root.song.title == title:
        print(f"BST: Found '{title}' - returning song data")
        return root.song.to_dict()
    elif title < root.song.title:
        print(f"BST: '{title}' < '{root.song.title}' - searching left")
        return search_by_title(root.left, title)
    else:
        print(f"BST: '{title}' > '{root.song.title}' - searching right")
        return search_by_title(root.right, title)

def inorder(root):
    """Legacy inorder function with verbose logging"""
    if root:
        inorder(root.left)
        print(f"BST DISPLAY: {root.song.title} - {root.song.artist}")
        inorder(root.right)
