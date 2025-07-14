

import tkinter as tk
from tkinter import messagebox, simpledialog

from src.model.song import Song
from src.ds.queue_create import SongQueue
from src.ds.bst_read import SongBST, read_song_data, insert, inorder
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
        try:
            all_songs = read_song_data()
            song_objects = []
            for song_dict in all_songs:
                song_obj = Song(
                    song_id=song_dict.get('id'),
                    title=song_dict.get('title', ''),
                    artist=song_dict.get('artist', ''),
                    album=song_dict.get('album', ''),
                    year=song_dict.get('year')
                )
                song_objects.append(song_obj)
            self.song_table.load_from_list(song_objects)
        except:
            print("Could not load songs into hash table")
        
        self.setup_widgets()
    
    def reload_bst(self):
        """Rebuild BST from DB"""
        self.bst_root = None
        try:
            songs = read_song_data()
            for song in songs:
                self.bst_root = insert(self.bst_root, song)
        except:
            print("Could not load BST")
    
    def setup_widgets(self):
        """Initialize UI widgets and layout"""
        tk.Label(self.root, text="🎶 Media Player", font=("Helvetica", 18)).pack(pady=10)
        
        # Input fields
        tk.Label(self.root, text="Title").pack()
        self.entry_title = tk.Entry(self.root, width=40)
        self.entry_title.pack()
        
        tk.Label(self.root, text="Artist").pack()
        self.entry_artist = tk.Entry(self.root, width=40)
        self.entry_artist.pack()
        
        tk.Label(self.root, text="Album").pack()
        self.entry_album = tk.Entry(self.root, width=40)
        self.entry_album.pack()
        
        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Song", command=self.on_add_song).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Process Queue", command=self.on_process_queue).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="View Songs", command=self.on_view_songs).grid(row=1, column=0, padx=5)
        tk.Button(btn_frame, text="Update Song", command=self.on_update_song).grid(row=1, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Song", command=self.on_delete_song).grid(row=1, column=2, padx=5)
        
        self.status_label = tk.Label(self.root, text="Ready", fg="green")
        self.status_label.pack(pady=10)
    
    def on_add_song(self):
        """Handler for adding a new song (enqueue)"""
        title = self.entry_title.get().strip()
        artist = self.entry_artist.get().strip()
        album = self.entry_album.get().strip()
        
        if title and artist:
            song = Song(title=title, artist=artist, album=album)
            self.song_queue.enqueue_song(song)
            self.status_label.config(text=f"✅ Queued '{title}' for addition.")
            self.entry_title.delete(0, tk.END)
            self.entry_artist.delete(0, tk.END)
            self.entry_album.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing Info", "Title and Artist are required.")
    
    def on_process_queue(self):
        """Process all songs in queue"""
        if self.song_queue.is_empty():
            messagebox.showinfo("Empty Queue", "No songs to process.")
            return
        
        self.song_queue.process_queue()
        self.reload_bst()
        self.song_table.load_from_database()
        self.status_label.config(text="✅ Queue processed successfully.")
    
    def on_view_songs(self):
        """Handler for listing songs (BST traversal)"""
        if not self.bst_root:
            self.reload_bst()
        
        if not self.bst_root:
            messagebox.showinfo("Songs", "No songs found.")
            return
        
        # Create window to show songs
        view_window = tk.Toplevel(self.root)
        view_window.title("All Songs")
        view_window.geometry("400x300")
        
        text_widget = tk.Text(view_window)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Capture inorder traversal output
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            inorder(self.bst_root)
            output = captured_output.getvalue()
            text_widget.insert("1.0", output)
        finally:
            sys.stdout = old_stdout
    
    def on_update_song(self):
        """Handler for updating song metadata"""
        song_id = simpledialog.askinteger("Update Song", "Enter Song ID:")
        if not song_id:
            return
        
        title = simpledialog.askstring("Update Title", "Enter new title (optional):")
        artist = simpledialog.askstring("Update Artist", "Enter new artist (optional):")
        album = simpledialog.askstring("Update Album", "Enter new album (optional):")
        
        success = self.song_table.update_song(song_id, title, artist, album)
        
        if success:
            self.status_label.config(text=f"✅ Song {song_id} updated.")
            self.reload_bst()  # Refresh BST
        else:
            messagebox.showerror("Update Failed", f"Song ID {song_id} not found.")
    
    def on_delete_song(self):
        """Handler for deleting a song"""
        song_id = simpledialog.askinteger("Delete Song", "Enter Song ID to delete:")
        if not song_id:
            return
        
        song = self.song_table.get_song(song_id)
        if song:
            self.delete_stack.push_song(song)
            self.status_label.config(text=f"✅ Song '{song.title}' moved to delete stack.")
        else:
            messagebox.showerror("Not Found", f"Song ID {song_id} not found.")

