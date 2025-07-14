from src.model.song import Song
from typing import Optional

class DeleteStack:
    def __init__(self):
        self.stack = []
    
    def push_song(self, song: Song):
        """Add a deleted song to the top of the stack"""
        self.stack.append(song)
        print(f"Song '{song.title}' added to delete stack.")
    
    def pop_and_delete(self) -> Optional[Song]:
        """Permanently delete the most recently deleted song"""
        if self.stack:
            deleted_song = self.stack.pop()
            
            # Try to permanently delete from database
            try:
                from src.db.database import delete_song_from_db
                if delete_song_from_db(deleted_song.id):
                    print(f"Song '{deleted_song.title}' permanently deleted from database.")
                    return deleted_song
                else:
                    # If database deletion fails, put it back on stack
                    self.stack.append(deleted_song)
                    print(f"Failed to permanently delete '{deleted_song.title}' from database")
                    return None
            except ImportError:
                print(f"Database module not available - removed '{deleted_song.title}' from stack only")
                return deleted_song
        else:
            print("Delete stack is empty. No song to delete.")
            return None
    
    def peek(self) -> Optional[Song]:
        """Return the most recent song added to the stack without removing it"""
        if self.stack:
            return self.stack[-1]
        else:
            return None
    
    def is_empty(self) -> bool:
        """Return True if the stack has no songs, False otherwise"""
        return len(self.stack) == 0
    
    def restore_song(self) -> Optional[Song]:
        """Remove song from delete stack (undo delete operation)"""
        if self.stack:
            restored_song = self.stack.pop()
            print(f"Song '{restored_song.title}' removed from delete stack (restored).")
            return restored_song
        else:
            print("Delete stack is empty. No song to restore.")
            return None
    
    def view_stack(self):
        """Display all songs in delete stack"""
        if not self.stack:
            print("Delete stack is empty.")
        else:
            print("Delete stack (most recent first):")
            for i, song in enumerate(reversed(self.stack), 1):
                print(f"{i}. {song.title} - {song.artist}")
    
    def __str__(self):
        """Return a string showing the stack contents from top to bottom"""
        if not self.stack:
            return "Delete stack is empty."
        return "Delete stack (top to bottom):\n" + "\n".join(
            [song.title for song in reversed(self.stack)]
        )

# Test functionality if run directly
if __name__ == "__main__":
    delete_stack = DeleteStack()
    
    # Create test songs
    song1 = Song(song_id=1, title="Test Song 1", artist="Test Artist 1")
    song2 = Song(song_id=2, title="Test Song 2", artist="Test Artist 2")
    
    delete_stack.push_song(song1)
    delete_stack.push_song(song2)
    delete_stack.view_stack()
    
    restored = delete_stack.restore_song()
    print(f"Restored: {restored}")
    
    deleted = delete_stack.pop_and_delete()
    print(f"Permanently deleted: {deleted}")
