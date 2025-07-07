import tkinter as tk
from tkinter import messagebox, simpledialog

class MediaPlayerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Media Player DS")
        self.root.geometry("500x500")
        self.setup_widgets()

    def setup_widgets(self):
        """Initialize UI widgets and layout"""
        # Header
        tk.Label(self.root, text="🎶 Media Player", font=("Helvetica", 18)).pack(pady=10)

        # Song Title Entry
        tk.Label(self.root, text="Song Title:").pack()
        self.entry_title = tk.Entry(self.root, width=40)
        self.entry_title.pack(pady=5)

        # Artist Entry
        tk.Label(self.root, text="Artist:").pack()
        self.entry_artist = tk.Entry(self.root, width=40)
        self.entry_artist.pack(pady=5)

        # Album Entry
        tk.Label(self.root, text="Album:").pack()
        self.entry_album = tk.Entry(self.root, width=40)
        self.entry_album.pack(pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Song", command=self.on_add_song, width=15).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="View Songs", command=self.on_view_songs, width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Update Song", command=self.on_update_song, width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete Song", command=self.on_delete_song, width=15).grid(row=1, column=1, padx=5, pady=5)

        # Status Label
        self.status_label = tk.Label(self.root, text="", fg="green")
        self.status_label.pack(pady=10)

    def on_add_song(self):
        """Handler for adding a new song (enqueue)"""
        title = self.entry_title.get().strip()
        artist = self.entry_artist.get().strip()
        album = self.entry_album.get().strip()

        if title and artist:
            self.status_label.config(text=f"Song added: {title} by {artist}")
            self.entry_title.delete(0, tk.END)
            self.entry_artist.delete(0, tk.END)
            self.entry_album.delete(0, tk.END)
        else:
            messagebox.showwarning("Missing Info", "Title and artist are required.")

    def on_view_songs(self):
        """Handler for listing songs (BST traversal)"""
        messagebox.showinfo("Songs", "Songs will be listed here from the backend (BST).")

    def on_update_song(self):
        """Handler for updating song metadata"""
        song_id = simpledialog.askinteger("Update Song", "Enter song ID to update:")
        if song_id:
            messagebox.showinfo("Update", f"This would update song ID {song_id} (via Hash Table).")

    def on_delete_song(self):
        """Handler for deleting a song"""
        song_id = simpledialog.askinteger("Delete Song", "Enter song ID to delete:")
        if song_id:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete song ID {song_id}?")
            if confirm:
                messagebox.showinfo("Deleted", f"Song ID {song_id} will be deleted (via Stack).")
