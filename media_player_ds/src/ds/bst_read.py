import sqlite3

class Node:
    def __init__(self, key):
        self.right = None
        self.left = None
        self.value = key

def insert(root, key):
    if root is None:
        return Node(key)
    elif root.value["title"] == key["title"]:
        return root  # No duplicates
    elif root.value["title"] < key["title"]:
        root.right = insert(root.right, key)
    else:
        root.left = insert(root.left, key)
    return root 

def inorder(root):
    if root:
        inorder(root.left)
        print(f"Title: {root.value['title']}, Artist: {root.value['artist']}")
        inorder(root.right)
        
def search_by_title(root, title):
    if root is None:
        return None
    if root.value["title"] == title:
        return root.value
    elif title < root.value["title"]:
        return search_by_title(root.left, title)
    else:
        return search_by_title(root.right, title)

def read_song_data():
    conn = sqlite3.connect("songs.db")
    cursor = conn.cursor()
    
   
    cursor.execute("SELECT title, artist, location FROM songs")
    rows = cursor.fetchall()

    conn.close()

    return [{"title": row[0], "artist": row[1],"location":row[2]} for row in rows]

# Example usage:
if __name__ == "__main__":
    songs = read_song_data()

    root = None
    for song in songs:
        root = insert(root, song)

    print("All songs in order:")
    inorder(root)
