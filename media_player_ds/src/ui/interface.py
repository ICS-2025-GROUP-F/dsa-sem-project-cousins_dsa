import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import io
import sys

from src.model.song import Song
from src.ds.queue_create import SongQueue
from src.ds.bst_read import SongBST, read_song_data, insert, inorder
from src.ds.hashtable_update import SongTable
from src.ds.stack_delete import DeleteStack

class MediaPlayerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player with Data Structures")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # DATA STRUCTURE INITIALIZATION
        self.song_queue = SongQueue()
        self.song_table = SongTable()
        self.delete_stack = DeleteStack()
        
        # For viewing songs
        self.bst_root = None
        self.songs_listbox = None  # Will store reference to songs display
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
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50")
        title_frame.pack(fill="x", pady=(0, 10))
        
        title_label = tk.Label(title_frame, text="🎵 Media Player with Data Structures", 
                              font=("Arial", 18, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left side - Input and Controls
        left_frame = tk.LabelFrame(main_frame, text="Song Management", 
                                  font=("Arial", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Input fields
        self.setup_input_fields(left_frame)
        
        # Buttons
        self.setup_buttons(left_frame)
        
        # Status label
        self.status_label = tk.Label(left_frame, text="Ready", fg="green", 
                                   font=("Arial", 10), bg="#f0f0f0")
        self.status_label.pack(pady=10)
        
        # Right side - Song Display
        right_frame = tk.LabelFrame(main_frame, text="Song Library", 
                                   font=("Arial", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True)
        
        self.setup_song_display(right_frame)
        
        # Load initial songs
        self.refresh_song_display()
    
    def setup_input_fields(self, parent):
        """Setup input fields for song information"""
        # Title input
        tk.Label(parent, text="Title:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.entry_title = tk.Entry(parent, width=30, font=("Arial", 10))
        self.entry_title.pack(pady=(0, 10), fill="x")
        
        # Artist input
        tk.Label(parent, text="Artist:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.entry_artist = tk.Entry(parent, width=30, font=("Arial", 10))
        self.entry_artist.pack(pady=(0, 10), fill="x")
        
        # Album input
        tk.Label(parent, text="Album:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.entry_album = tk.Entry(parent, width=30, font=("Arial", 10))
        self.entry_album.pack(pady=(0, 10), fill="x")
        
        # Genre input
        tk.Label(parent, text="Genre:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.entry_genre = tk.Entry(parent, width=30, font=("Arial", 10))
        self.entry_genre.pack(pady=(0, 10), fill="x")
        
        # Year input
        tk.Label(parent, text="Year:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
        self.entry_year = tk.Entry(parent, width=30, font=("Arial", 10))
        self.entry_year.pack(pady=(0, 15), fill="x")
    
    def setup_buttons(self, parent):
        """Setup control buttons"""
        # Button frame
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(fill="x", pady=10)
        
        # Row 1 - CRUD Operations
        tk.Button(btn_frame, text="Add to Queue\n(CREATE)", command=self.on_add_song, 
                 bg="#27ae60", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Process Queue", command=self.on_process_queue, 
                 bg="#3498db", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=0, column=1, padx=2, pady=2)
        
        # Row 2
        tk.Button(btn_frame, text="View All Songs\n(READ)", command=self.on_view_songs, 
                 bg="#e67e22", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Search Song", command=self.on_search_song, 
                 bg="#9b59b6", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=1, column=1, padx=2, pady=2)
        
        # Row 3
        tk.Button(btn_frame, text="Update Song\n(UPDATE)", command=self.on_update_song, 
                 bg="#f39c12", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=2, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="Delete Song\n(DELETE)", command=self.on_delete_song, 
                 bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=2, column=1, padx=2, pady=2)
        
        # Row 4 - Utility
        tk.Button(btn_frame, text="View Queue", command=self.on_view_queue, 
                 bg="#95a5a6", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=3, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="View Delete Stack", command=self.on_view_stack, 
                 bg="#34495e", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=3, column=1, padx=2, pady=2)
        
        # Row 5 - Delete Management
        tk.Button(btn_frame, text="Flush Delete Session\n(Finalize)", command=self.on_flush_delete_session, 
                 bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=4, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="View Deleted History\n(All Time)", command=self.on_view_deleted_history, 
                 bg="#2c3e50", fg="white", font=("Arial", 9, "bold"), width=15, height=2).grid(row=4, column=1, padx=2, pady=2)
        
        # Row 6 - Clear
        tk.Button(btn_frame, text="Clear Fields", command=self.clear_fields, 
                 bg="#7f8c8d", fg="white", font=("Arial", 9, "bold"), width=32).grid(row=5, column=0, columnspan=2, padx=2, pady=10)
    
    def setup_song_display(self, parent):
        """Setup the song display area with Song IDs visible"""
        # Instructions
        instructions = tk.Label(parent, text="All songs with their IDs (for Update/Delete operations):", 
                               font=("Arial", 10, "bold"), bg="#f0f0f0")
        instructions.pack(anchor="w", pady=(0, 10))
        
        # Create frame for listbox and scrollbar
        display_frame = tk.Frame(parent, bg="#f0f0f0")
        display_frame.pack(fill="both", expand=True)
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.songs_listbox = tk.Listbox(display_frame, yscrollcommand=scrollbar.set, 
                                       font=("Courier", 10), height=20, selectmode=tk.SINGLE)
        self.songs_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.songs_listbox.yview)
        
        # Bind double-click to fill form
        self.songs_listbox.bind('<Double-Button-1>', self.on_song_double_click)
        
        # Refresh button
        refresh_btn = tk.Button(parent, text="🔄 Refresh Song List", command=self.refresh_song_display,
                               bg="#16a085", fg="white", font=("Arial", 10, "bold"))
        refresh_btn.pack(pady=10)
    
    def refresh_song_display(self):
        """Refresh the song display with current database contents"""
        if not self.songs_listbox:
            return
            
        # Clear current contents
        self.songs_listbox.delete(0, tk.END)
        
        try:
            # Get songs from database
            songs = read_song_data()
            
            if not songs:
                self.songs_listbox.insert(tk.END, "No songs in library")
                return
            
            # Sort songs by ID for consistent display
            songs_sorted = sorted(songs, key=lambda x: x.get('id', 0))
            
            # Add header
            header = f"{'ID':<4} | {'Title':<25} | {'Artist':<20} | {'Album':<20}"
            self.songs_listbox.insert(tk.END, header)
            self.songs_listbox.insert(tk.END, "-" * 75)
            
            # Add each song with clear ID display
            for song in songs_sorted:
                song_id = song.get('id', 'N/A')
                title = song.get('title', 'Unknown')[:25]
                artist = song.get('artist', 'Unknown')[:20]
                album = song.get('album', 'Unknown')[:20]
                
                song_line = f"{song_id:<4} | {title:<25} | {artist:<20} | {album:<20}"
                self.songs_listbox.insert(tk.END, song_line)
                
        except Exception as e:
            self.songs_listbox.insert(tk.END, f"Error loading songs: {e}")
    
    def on_song_double_click(self, event):
        """Handle double-click on song to fill form"""
        selection = self.songs_listbox.curselection()
        if not selection:
            return
            
        # Get selected line
        line = self.songs_listbox.get(selection[0])
        
        # Skip header lines
        if line.startswith("ID") or line.startswith("-") or "No songs" in line or "Error" in line:
            return
        
        try:
            # Parse the song ID from the line
            song_id = int(line.split("|")[0].strip())
            
            # Get full song data
            songs = read_song_data()
            selected_song = None
            
            for song in songs:
                if song.get('id') == song_id:
                    selected_song = song
                    break
            
            if selected_song:
                # Fill the form with song data
                self.clear_fields()
                self.entry_title.insert(0, selected_song.get('title', ''))
                self.entry_artist.insert(0, selected_song.get('artist', ''))
                self.entry_album.insert(0, selected_song.get('album', ''))
                self.entry_genre.insert(0, selected_song.get('genre', ''))
                if selected_song.get('year'):
                    self.entry_year.insert(0, str(selected_song.get('year')))
                
                self.status_label.config(text=f"Loaded song ID {song_id} into form")
                
        except (ValueError, IndexError):
            messagebox.showwarning("Selection Error", "Could not parse selected song")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.entry_title.delete(0, tk.END)
        self.entry_artist.delete(0, tk.END)
        self.entry_album.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
    
    def get_song_from_inputs(self):
        """Create Song object from input fields"""
        title = self.entry_title.get().strip()
        artist = self.entry_artist.get().strip()
        album = self.entry_album.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        
        if not title or not artist:
            messagebox.showwarning("Missing Info", "Title and Artist are required.")
            return None
        
        year = None
        if year_str:
            try:
                year = int(year_str)
            except ValueError:
                messagebox.showwarning("Invalid Year", "Year must be a number.")
                return None
        
        return Song(
            title=title,
            artist=artist,
            album=album,
            genre=genre,
            year=year,
            duration=0,
            file_path=""
        )
    
    def on_add_song(self):
        """Handler for adding a new song (enqueue)"""
        song = self.get_song_from_inputs()
        if song:
            self.song_queue.enqueue_song(song)
            self.status_label.config(text=f"✅ Queued '{song.title}' for addition.")
            self.clear_fields()
    
    def on_process_queue(self):
        """Process all songs in queue"""
        if self.song_queue.is_empty():
            messagebox.showinfo("Empty Queue", "No songs to process.")
            return
        
        queue_size = self.song_queue.get_queue_size()
        self.song_queue.process_queue()
        self.reload_bst()
        self.song_table.load_from_database()
        self.refresh_song_display()  # Refresh the display
        self.status_label.config(text=f"✅ Processed {queue_size} songs from queue.")
    
    def on_view_songs(self):
        """Handler for viewing all songs using BST"""
        # The song display is always visible, just refresh it
        self.refresh_song_display()
        self.status_label.config(text="✅ Song list refreshed (sorted by ID)")
        
        # Also show BST traversal in a popup for educational purposes
        if not self.bst_root:
            self.reload_bst()
        
        if not self.bst_root:
            messagebox.showinfo("BST Traversal", "No songs found for BST traversal.")
            return
        
        # Create window to show BST traversal
        bst_window = tk.Toplevel(self.root)
        bst_window.title("BST In-Order Traversal (Alphabetical by Title)")
        bst_window.geometry("500x400")
        
        text_widget = tk.Text(bst_window, font=("Courier", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Capture BST traversal output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            print("BST IN-ORDER TRAVERSAL (Alphabetical by Title):")
            print("=" * 50)
            inorder(self.bst_root)
            output = captured_output.getvalue()
            text_widget.insert("1.0", output)
        finally:
            sys.stdout = old_stdout
    
    def on_search_song(self):
        """Handler for searching songs"""
        search_term = simpledialog.askstring("Search Songs", "Enter title, artist, or album to search for:")
        if not search_term:
            return
        
        try:
            from src.db.database import search_songs
            results = search_songs(search_term)
            
            if not results:
                messagebox.showinfo("Search Results", f"No songs found matching '{search_term}'")
                return
            
            # Create window to show search results
            search_window = tk.Toplevel(self.root)
            search_window.title(f"Search Results for '{search_term}'")
            search_window.geometry("600x400")
            
            # Create listbox for results
            result_listbox = tk.Listbox(search_window, font=("Courier", 10))
            result_listbox.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Add header
            header = f"{'ID':<4} | {'Title':<25} | {'Artist':<20} | {'Album':<15}"
            result_listbox.insert(tk.END, header)
            result_listbox.insert(tk.END, "-" * 70)
            
            # Add search results
            for song in results:
                song_line = f"{song.id:<4} | {song.title[:25]:<25} | {song.artist[:20]:<20} | {song.album[:15]:<15}"
                result_listbox.insert(tk.END, song_line)
            
            self.status_label.config(text=f"Found {len(results)} songs matching '{search_term}'")
            
        except ImportError:
            messagebox.showerror("Error", "Search functionality not available")
    
    def on_update_song(self):
        """Handler for updating song metadata"""
        # Show current songs first
        self.refresh_song_display()
        
        song_id = simpledialog.askinteger("Update Song", 
                                         "Enter Song ID (see the list on the right):\n\n" +
                                         "Tip: Double-click a song to load it into the form first!")
        if not song_id:
            return
        
        # Check if song exists
        song = self.song_table.get_song(song_id)
        if not song:
            messagebox.showerror("Update Failed", f"Song ID {song_id} not found.\n\nPlease check the song list on the right.")
            return
        
        # Get update values
        title = simpledialog.askstring("Update Title", f"Current title: '{song.title}'\nEnter new title (or press Cancel to keep current):")
        artist = simpledialog.askstring("Update Artist", f"Current artist: '{song.artist}'\nEnter new artist (or press Cancel to keep current):")
        album = simpledialog.askstring("Update Album", f"Current album: '{song.album}'\nEnter new album (or press Cancel to keep current):")
        genre = simpledialog.askstring("Update Genre", f"Current genre: '{song.genre}'\nEnter new genre (or press Cancel to keep current):")
        
        year_str = simpledialog.askstring("Update Year", f"Current year: {song.year}\nEnter new year (or press Cancel to keep current):")
        year = None
        if year_str:
            try:
                year = int(year_str)
            except ValueError:
                messagebox.showwarning("Invalid Year", "Year must be a number. Keeping current year.")
        
        success = self.song_table.update_song(song_id, title, artist, album, genre, year)
        
        if success:
            self.status_label.config(text=f"✅ Song {song_id} updated successfully.")
            self.reload_bst()
            self.refresh_song_display()
        else:
            messagebox.showerror("Update Failed", f"Failed to update song ID {song_id}")
    
    def on_delete_song(self):
        """Handler for deleting a song - IMMEDIATE database deletion"""
        # Show current songs first
        self.refresh_song_display()
        
        song_id = simpledialog.askinteger("Delete Song", 
                                         "Enter Song ID to delete (see the list on the right):\n\n" +
                                         "WARNING: Song will be immediately deleted from database!\n" +
                                         "(But tracked in delete session for history)")
        if not song_id:
            return
        
        song = self.song_table.get_song(song_id)
        if song:
            # Confirm deletion with clear warning
            confirm = messagebox.askyesno("Confirm Immediate Delete", 
                                         f"IMMEDIATE DATABASE DELETION:\n\n" +
                                         f"ID: {song.id}\n" +
                                         f"Title: {song.title}\n" +
                                         f"Artist: {song.artist}\n\n" +
                                         f"This will IMMEDIATELY delete the song from database\n" +
                                         f"and add it to the delete session for tracking.\n\n" +
                                         f"Continue with deletion?")
            
            if confirm:
                # Use the new push_song method that immediately deletes from database
                success = self.delete_stack.push_song(song)
                
                if success:
                    # Remove from hash table as well since it's deleted from DB
                    if song_id in self.song_table.table:
                        del self.song_table.table[song_id]
                    
                    self.status_label.config(text=f"✅ Song '{song.title}' deleted from database and added to delete session.")
                    self.refresh_song_display()  # Will show song is gone
                else:
                    messagebox.showerror("Delete Failed", f"Failed to delete '{song.title}' from database.")
        else:
            messagebox.showerror("Not Found", f"Song ID {song_id} not found.\n\nPlease check the song list on the right.")
    
    def on_view_queue(self):
        """Display current queue contents"""
        queue_window = tk.Toplevel(self.root)
        queue_window.title("Current Queue (FIFO)")
        queue_window.geometry("500x400")
        
        text_widget = tk.Text(queue_window, font=("Courier", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Capture queue output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            self.song_queue.view_queue()
            output = captured_output.getvalue()
            text_widget.insert("1.0", output)
        finally:
            sys.stdout = old_stdout
    
    def on_view_stack(self):
        """Display current delete stack contents"""
        stack_window = tk.Toplevel(self.root)
        stack_window.title("Delete Stack (LIFO)")
        stack_window.geometry("500x400")
        
        text_widget = tk.Text(stack_window, font=("Courier", 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add restore button
        restore_btn = tk.Button(stack_window, text="Restore Top Song (Undo Delete)", 
                               command=self.restore_top_song, bg="#27ae60", fg="white")
        restore_btn.pack(pady=5)
        
        # Capture stack output
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            self.delete_stack.view_stack()
            output = captured_output.getvalue()
            text_widget.insert("1.0", output)
        finally:
            sys.stdout = old_stdout
    
    def restore_top_song(self):
        """Restore the top song from delete stack"""
        if self.delete_stack.is_empty():
            messagebox.showinfo("Nothing to Restore", "The delete session is empty.")
            return
            
        # Get the top song
        top_song = self.delete_stack.peek()
        if not top_song:
            return
            
        # Confirm restoration
        confirm = messagebox.askyesno("Confirm Restore", 
                                     f"Restore song to database?\n\n" +
                                     f"Title: {top_song.title}\n" +
                                     f"Artist: {top_song.artist}\n\n" +
                                     f"This will re-add the song to the database.")
        
        if confirm:
            # Remove from stack first
            restored_song = self.delete_stack.pop_song()
            
            if restored_song:
                # Try to restore to database
                success = self.delete_stack.restore_song_to_database(restored_song)
                
                if success:
                    # Add back to hash table
                    self.song_table.table[restored_song.id] = restored_song
                    
                    messagebox.showinfo("Song Restored", f"'{restored_song.title}' has been restored to the database!")
                    self.refresh_song_display()
                    self.status_label.config(text=f"✅ Restored '{restored_song.title}' to database.")
                else:
                    # Put it back on stack if restoration failed
                    self.delete_stack.stack.append(restored_song)
                    messagebox.showerror("Restore Failed", f"Failed to restore '{restored_song.title}' to database.")
    
    def on_flush_delete_session(self):
        """Flush the delete session - finalize all deletions"""
        if self.delete_stack.is_empty():
            messagebox.showinfo("Nothing to Flush", "The delete session is empty.")
            return
            
        # Get current session songs
        current_session = self.delete_stack.get_current_delete_session()
        
        # Confirm flush
        confirm = messagebox.askyesno("Confirm Flush Delete Session", 
                                     f"Finalize deletion of {len(current_session)} songs?\n\n" +
                                     "Songs in current session:\n" +
                                     "\n".join([f"• {song.title} - {song.artist}" for song in current_session[:5]]) +
                                     (f"\n... and {len(current_session)-5} more" if len(current_session) > 5 else "") +
                                     "\n\nThis will finalize all deletions and clear the session.\n" +
                                     "Songs are already deleted from database.")
        
        if confirm:
            flushed_songs = self.delete_stack.flush_delete_session()
            
            messagebox.showinfo("Delete Session Flushed", 
                               f"Successfully finalized deletion of {len(flushed_songs)} songs.\n\n" +
                               f"These songs have been permanently removed and\n" +
                               f"moved to the deletion history.")
            
            self.status_label.config(text=f"✅ Flushed {len(flushed_songs)} songs from delete session.")
    
    def on_view_deleted_history(self):
        """View complete history of all deleted songs"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Complete Deletion History (All Time)")
        history_window.geometry("700x500")
        
        # Create frame for content
        content_frame = tk.Frame(history_window)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(content_frame, text="Complete Deletion History", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Get deletion history
        deleted_history = self.delete_stack.get_deleted_songs_history()
        current_session = self.delete_stack.get_current_delete_session()
        
        # Statistics
        stats_text = f"Total Permanently Deleted: {len(deleted_history)} songs\n" + \
                    f"Current Delete Session: {len(current_session)} songs\n" + \
                    f"Grand Total Deletions: {len(deleted_history) + len(current_session)} songs"
        
        stats_label = tk.Label(content_frame, text=stats_text, font=("Arial", 10), 
                              justify="left", bg="#ecf0f1")
        stats_label.pack(fill="x", pady=(0, 10))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill="both", expand=True)
        
        # Tab 1: Permanently Deleted (Flushed)
        flushed_frame = tk.Frame(notebook)
        notebook.add(flushed_frame, text=f"Permanently Deleted ({len(deleted_history)})")
        
        if deleted_history:
            flushed_listbox = tk.Listbox(flushed_frame, font=("Courier", 10))
            flushed_listbox.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Add header
            flushed_listbox.insert(tk.END, "Permanently Deleted Songs (Flushed Sessions):")
            flushed_listbox.insert(tk.END, "=" * 50)
            
            for i, song in enumerate(deleted_history, 1):
                song_line = f"{i:3d}. ID:{song.id:<4} | {song.title[:30]:<30} | {song.artist[:20]:<20}"
                flushed_listbox.insert(tk.END, song_line)
        else:
            no_history_label = tk.Label(flushed_frame, text="No permanently deleted songs yet.\n\n" +
                                       "Songs will appear here after flushing delete sessions.", 
                                       font=("Arial", 12), fg="gray")
            no_history_label.pack(expand=True)
        
        # Tab 2: Current Session
        session_frame = tk.Frame(notebook)
        notebook.add(session_frame, text=f"Current Session ({len(current_session)})")
        
        if current_session:
            session_listbox = tk.Listbox(session_frame, font=("Courier", 10))
            session_listbox.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Add header
            session_listbox.insert(tk.END, "Current Delete Session (Not Yet Flushed):")
            session_listbox.insert(tk.END, "=" * 50)
            
            for i, song in enumerate(reversed(current_session), 1):  # Show most recent first
                song_line = f"{i:3d}. ID:{song.id:<4} | {song.title[:30]:<30} | {song.artist[:20]:<20}"
                session_listbox.insert(tk.END, song_line)
            
            # Add restore button for current session
            restore_frame = tk.Frame(session_frame)
            restore_frame.pack(fill="x", padx=5, pady=5)
            
            restore_btn = tk.Button(restore_frame, text="Restore Top Song from Session", 
                                   command=self.restore_top_song, bg="#27ae60", fg="white", 
                                   font=("Arial", 10, "bold"))
            restore_btn.pack(side="left", padx=5)
            
            flush_btn = tk.Button(restore_frame, text="Flush Session (Finalize All)", 
                                 command=self.on_flush_delete_session, bg="#8e44ad", fg="white", 
                                 font=("Arial", 10, "bold"))
            flush_btn.pack(side="right", padx=5)
        else:
            no_session_label = tk.Label(session_frame, text="No songs in current delete session.\n\n" +
                                       "Deleted songs will appear here before being flushed.", 
                                       font=("Arial", 12), fg="gray")
            no_session_label.pack(expand=True)
        
        # Add refresh button
        refresh_btn = tk.Button(content_frame, text="Refresh History", 
                               command=lambda: self.refresh_history_window(history_window), 
                               bg="#3498db", fg="white", font=("Arial", 10, "bold"))
        refresh_btn.pack(pady=10)
    
    def refresh_history_window(self, window):
        """Refresh the history window"""
        window.destroy()
        self.on_view_deleted_history()
