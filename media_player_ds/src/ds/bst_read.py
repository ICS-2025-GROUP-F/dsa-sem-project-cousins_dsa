import sqlite3

class BSTNode:
    def __init__(self, song):
        self.song = song
        self.left = None
        self.right = None

class SongBST:
    def __init__(self):
        self.root = None

    def insert(self, song):
        def _insert(root, song):
            if root is None:
                return BSTNode(song)
            elif root.song["title"] == song["title"]:
                return root
            elif root.song["title"] < song["title"]:
                root.right = _insert(root.right, song)
            else:
                root.left = _insert(root.left, song)
            return root

        self.root = _insert(self.root, song)

    def search_by_title(self, title):
        def _search(root, title):
            if root is None:
                return None
            if root.song["title"] == title:
                return root.song
            elif title < root.song["title"]:
                return _search(root.left, title)
            else:
                return _search(root.right, title)

        return _search(self.root, title)

    def inorder_traversal(self):
        def _inorder(root):
            if root:
                _inorder(root.left)
                print(f"Title: {root.song['title']}, Artist: {root.song['artist']}")
                _inorder(root.right)

        _inorder(self.root)
