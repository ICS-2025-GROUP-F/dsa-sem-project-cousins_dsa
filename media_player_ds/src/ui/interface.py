import tkinter as tk
from tkinter import messagebox, simpledialog

from src.model.song import Song
from src.ds.queue_create import SongQueue
from src.ds.bst_read import insert, inorder, search_by_title, read_song_data
from src.ds.hashtable_update import SongTable
from src.ds.stack_delete import DeleteStack

class MediaPlayerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Media Player DS")

        # DATA STRUCTURE INITIALIZATION
        self.song_queue = SongQueue()
        self.song_table = SongTable()
        self.delete_stack = DeleteStack()

        # For viewing songs
        self.bst_root = None
        self.reload_bst()

        # Load update table
        all_songs = read_song_data()
        self.song_table.load_from_list([
            Song(idx+1, song['title'], song['artist'], song['location']) for idx, song in enumerate(all_songs)
        ])

        self.setup_widgets()

    def reload_bst(self):
        """Rebuild BST from DB"""
        self.bst_root = None
        songs = read_song_data()
        for song in songs:
            self.bst_root = insert(self.bst_root, song)

    def setup_widgets(self):
        """Initialize UI widgets and layout"""
        tk.Label(self.root, text="🎶 Media Player", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.root, text="Title").pack()
        self.entry_title = tk.Entry(self.root, width=40)
        self.entry_title.pack()

        tk.Label(self.root, text="Artist").pack()
        self.entry_artist = tk.Entry(self.root, width=40)
        self.entry_artist.pack()

        tk.Label(self.root, text="Album").pack()
        self.entry_album = tk.Entry(self.root, width=40)
        self.entry_album.pack()

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Song", command=self.on_add_song).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="View Songs", command=self.on_view_songs).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Update Song", command=self.on_update_song).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete Song", command=self.on_delete_song).grid(row=1, column=1, padx=5, pady=5)

        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=10)

    def on_add_song(self):
        title = self.entry_title.get().strip()
        artist = self.entry_artist.get().strip()
        album = self.entry_album.get().strip()

        if title and artist:
            new_id = len(read_song_data()) + 1
            song = Song(new_id, title, artist, album)
            self.song_queue.enqueue_song(song)
            self.status_label.config(text=f" Queued '{title}' for addition.")
            self.entry_title.delete(0, tk.END)
            self.entry_artist.delete(0, tk.END)
            self.entry_album.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing Info", "Title and Artist are required.")

    def on_view_songs(self):
        if not self.bst_root:
            self.reload_bst()

        message = []

        def collect_inorder(node):
            if node:
                collect_inorder(node.left)
                song = node.value
                message.append(f"{song['title']} - {song['artist']}")
                collect_inorder(node.right)

        collect_inorder(self.bst_root)

        if not message:
            messagebox.showinfo("Songs", "No songs found.")
        else:
            messagebox.showinfo("All Songs", "\n".join(message))

    def on_update_song(self):
        song_id = simpledialog.askinteger("Update Song", "Enter Song ID:")
        if not song_id:
            return

        title = simpledialog.askstring("Update Title", "Enter new title (optional):")
        artist = simpledialog.askstring("Update Artist", "Enter new artist (optional):")
        album = simpledialog.askstring("Update Album", "Enter new album (optional):")

        success = self.song_table.update_song(song_id, title, artist, album)

        if success:
            self.status_label.config(text=f" Song {song_id} updated.")
        else:
            messagebox.showerror("Update Failed", f"Song ID {song_id} not found.")

    def on_delete_song(self):
        song_id = simpledialog.askinteger("Delete Song", "Enter Song ID to delete:")
        if not song_id:
            return

        song = self.song_table.table.get(song_id)
        if song:
            self.delete_stack.push_song(song)
            from src.db.database import delete_song_from_db
            delete_song_from_db(song_id)
            self.status_label.config(text=f" Song '{song.title}' deleted and pushed to stack.")
        else:
            messagebox.showerror("Not Found", f"Song ID {song_id} not found.")


