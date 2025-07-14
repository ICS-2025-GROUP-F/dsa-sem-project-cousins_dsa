from src.model.song import Song
from typing import Optional, List

class DeleteStack:
    def __init__(self):
        self.stack = []
        self.total_pushes = 0
        self.total_pops = 0
        self.total_permanent_deletes = 0
        self.max_size_reached = 0
        self.deleted_songs_history = []  # Track all permanently deleted songs
        print("STACK: Initialized delete stack with flush session capability")
        print("STACK: Functions as a staging area before permanent database deletion")
        self._print_stack_status()
    
    def push_song(self, song: Song):
        """Add a deleted song to the stack and remove from database immediately"""
        print(f"\nSTACK PUSH: Adding '{song.title}' by {song.artist} to delete stack")
        
        # Show stack state before push
        print(f"STACK: Stack size before push: {len(self.stack)}")
        if self.stack:
            print(f"STACK: Current top of stack: '{self.stack[-1].title}'")
        else:
            print("STACK: Stack is currently empty")
        
        # IMMEDIATE DATABASE DELETION - This is the key change
        print(f"DATABASE DELETE: Immediately removing '{song.title}' from database...")
        try:
            from src.db.database import delete_song_from_db
            
            if delete_song_from_db(song.id):
                print(f"DATABASE DELETE: Successfully removed '{song.title}' from database")
                
                # Add to stack for tracking and potential restoration
                self.stack.append(song)
                self.total_pushes += 1
                
                # Update maximum size tracking
                if len(self.stack) > self.max_size_reached:
                    self.max_size_reached = len(self.stack)
                
                print(f"STACK PUSH: Song added to delete stack for session tracking")
                print(f"STACK: Stack size after push: {len(self.stack)}")
                print(f"STACK: Total songs in delete session: {self.total_pushes}")
                
                self._print_stack_contents()
                self._print_stack_status()
                return True
            else:
                print(f"DATABASE DELETE: Failed to remove '{song.title}' from database")
                print(f"STACK: Song NOT added to delete stack due to database error")
                return False
                
        except ImportError:
            print(f"DATABASE DELETE: Database module not available")
            print(f"STACK: Adding to stack for simulation (no actual database deletion)")
            
            # Still add to stack for demonstration purposes
            self.stack.append(song)
            self.total_pushes += 1
            
            if len(self.stack) > self.max_size_reached:
                self.max_size_reached = len(self.stack)
            
            self._print_stack_contents()
            self._print_stack_status()
            return True
    
    def pop_song(self) -> Optional[Song]:
        """Remove song from delete stack (for potential restoration)"""
        print(f"\nSTACK POP: Attempting to remove song from TOP of delete stack")
        
        if not self.stack:
            print("STACK POP: Cannot pop - Delete stack is EMPTY!")
            return None
        
        # Show stack state before pop
        print(f"STACK: Stack size before pop: {len(self.stack)}")
        top_song = self.stack[-1]
        print(f"STACK: Song at TOP (to be removed from session): '{top_song.title}'")
        
        # Perform LIFO pop operation
        popped_song = self.stack.pop()
        self.total_pops += 1
        
        print(f"STACK POP: Removed '{popped_song.title}' from delete session")
        print(f"STACK: Stack size after pop: {len(self.stack)}")
        print(f"STACK: Note - Song was already deleted from database!")
        
        if self.stack:
            print(f"STACK: New top of stack: '{self.stack[-1].title}'")
        else:
            print("STACK: Delete stack is now EMPTY")
        
        self._print_stack_contents()
        self._print_stack_status()
        
        return popped_song
    
    def flush_delete_session(self) -> List[Song]:
        """Flush the entire delete session - finalize all deletions using LIFO stack operations"""
        print(f"\nSTACK FLUSH: Flushing delete session with {len(self.stack)} songs")
        print("STACK FLUSH: This will finalize all deletions using LIFO (Last In, First Out) order")
        print("STACK FLUSH: Songs will be permanently deleted in reverse order of deletion")
        
        if not self.stack:
            print("STACK FLUSH: No songs in delete session to flush")
            return []
        
        # Show songs before flushing
        songs_to_flush = list(self.stack)  # Copy for return
        
        print("STACK FLUSH: Songs to be permanently deleted (LIFO order):")
        for i, song in enumerate(reversed(self.stack), 1):
            print(f"   {i}. {song.title} - {song.artist} (ID: {song.id}) [Will be deleted #{i}]")
        
        print("\nSTACK FLUSH: Beginning LIFO flush process...")
        flushed_songs = []
        flush_count = 0
        
        # Pop each song individually to demonstrate LIFO
        while self.stack:
            flush_count += 1
            
            # Pop from top of stack (LIFO)
            song_to_flush = self.stack.pop()
            self.total_pops += 1
            
            print(f"\nSTACK FLUSH #{flush_count}: Popping '{song_to_flush.title}' from top of stack")
            print(f"STACK FLUSH: Stack size before pop: {len(self.stack) + 1}")
            print(f"STACK FLUSH: Stack size after pop: {len(self.stack)}")
            
            # Add to permanent delete history
            flushed_songs.append(song_to_flush)
            self.deleted_songs_history.append(song_to_flush)
            self.total_permanent_deletes += 1
            
            print(f"STACK FLUSH: '{song_to_flush.title}' moved to permanent deletion history")
            
            # Show remaining stack contents
            if self.stack:
                print(f"STACK FLUSH: Remaining in stack: {len(self.stack)} songs")
                print(f"STACK FLUSH: Next to be flushed: '{self.stack[-1].title}' (top of stack)")
            else:
                print("STACK FLUSH: Stack is now empty - all songs flushed")
        
        print(f"\nSTACK FLUSH COMPLETE:")
        print(f"STACK FLUSH: Successfully flushed {len(flushed_songs)} songs using LIFO order")
        print(f"STACK FLUSH: Total permanent deletions (all-time): {self.total_permanent_deletes}")
        print("STACK FLUSH: All songs moved to permanent deletion history")
        print("STACK FLUSH: Delete session cleared - ready for new deletions")
        
        print("\nSTACK FLUSH: Final flush order (LIFO - Last In, First Out):")
        for i, song in enumerate(flushed_songs, 1):
            print(f"   Flush #{i}: {song.title} - {song.artist}")
        
        self._print_stack_status()
        
        return flushed_songs
    
    def get_deleted_songs_history(self) -> List[Song]:
        """Get complete history of all permanently deleted songs"""
        print(f"\nSTACK HISTORY: Retrieving complete deletion history")
        print(f"STACK HISTORY: Total permanently deleted songs: {len(self.deleted_songs_history)}")
        
        if self.deleted_songs_history:
            print("STACK HISTORY: All permanently deleted songs:")
            for i, song in enumerate(self.deleted_songs_history, 1):
                print(f"   {i}. {song.title} - {song.artist} (ID: {song.id})")
        else:
            print("STACK HISTORY: No songs have been permanently deleted yet")
        
        return self.deleted_songs_history.copy()
    
    def get_current_delete_session(self) -> List[Song]:
        """Get songs in current delete session (not yet flushed)"""
        print(f"\nSTACK SESSION: Current delete session contains {len(self.stack)} songs")
        
        if self.stack:
            print("STACK SESSION: Songs in current session (LIFO order):")
            for i, song in enumerate(reversed(self.stack), 1):
                stack_position = len(self.stack) - i + 1
                print(f"   {i}. [Position {stack_position}] {song.title} - {song.artist} (ID: {song.id})")
        else:
            print("STACK SESSION: Current delete session is empty")
        
        return self.stack.copy()
    
    def peek(self) -> Optional[Song]:
        """Return the most recent song added to the stack without removing it"""
        print(f"\nSTACK PEEK: Checking top of delete stack without removing")
        
        if self.stack:
            top_song = self.stack[-1]
            print(f"STACK PEEK: Top song: '{top_song.title}' by {top_song.artist}")
            print(f"STACK PEEK: This song was most recently deleted")
            print(f"STACK PEEK: Stack position: {len(self.stack)} (top)")
            return top_song
        else:
            print("STACK PEEK: Delete stack is empty - no recent deletions")
            return None
    
    def is_empty(self) -> bool:
        """Return True if the delete stack has no songs"""
        empty = len(self.stack) == 0
        print(f"STACK EMPTY CHECK: Delete stack is {'EMPTY' if empty else 'NOT EMPTY'}")
        if not empty:
            print(f"STACK EMPTY CHECK: {len(self.stack)} songs in current delete session")
        return empty
    
    def restore_song_to_database(self, song: Song) -> bool:
        """Restore a song back to the database (undo deletion)"""
        print(f"\nSTACK RESTORE: Attempting to restore '{song.title}' to database")
        
        try:
            from src.db.database import insert_song_to_db
            
            if insert_song_to_db(song):
                print(f"STACK RESTORE: Successfully restored '{song.title}' to database")
                return True
            else:
                print(f"STACK RESTORE: Failed to restore '{song.title}' to database")
                return False
                
        except ImportError:
            print(f"STACK RESTORE: Database module not available for restoration")
            return False
    
    def view_stack(self):
        """Display all songs in delete stack with verbose logging"""
        print(f"\nSTACK VIEW: Displaying complete delete session")
        print(f"STACK VIEW: Current session contains {len(self.stack)} songs")
        print(f"STACK VIEW: Stack follows LIFO principle (Last In, First Out)")
        print(f"STACK VIEW: Songs shown were deleted from database but tracked in session")
        
        if not self.stack:
            print("STACK VIEW: Current delete session is empty")
        else:
            print("STACK VIEW: Songs in current delete session (LIFO order):")
            
            for i, song in enumerate(reversed(self.stack), 1):
                stack_position = len(self.stack) - i + 1
                age_desc = "MOST RECENT" if i == 1 else "OLDEST" if i == len(self.stack) else f"Position {stack_position}"
                
                print(f"   {i}. [TOP-{i}] [{age_desc}] {song.title} - {song.artist} (ID: {song.id})")
            
            print(f"STACK VIEW: Most recently deleted: '{self.stack[-1].title}' (top)")
            print(f"STACK VIEW: First deleted this session: '{self.stack[0].title}' (bottom)")
        
        print(f"STACK VIEW: Session stats - Added: {self.total_pushes}, Removed: {self.total_pops}")
        print(f"STACK VIEW: Total permanent deletions (all time): {self.total_permanent_deletes}")
    
    def clear_session(self):
        """Clear current delete session without flushing"""
        print(f"\nSTACK CLEAR: Clearing current delete session ({len(self.stack)} songs)")
        print("STACK CLEAR: Warning - This will lose track of deleted songs in current session")
        
        if self.stack:
            print("STACK CLEAR: Songs being cleared from session tracking:")
            for i, song in enumerate(self.stack, 1):
                print(f"   {i}. {song.title} - {song.artist}")
        
        cleared_count = len(self.stack)
        self.stack.clear()
        
        print(f"STACK CLEAR: Cleared {cleared_count} songs from session tracking")
        print("STACK CLEAR: Note - Songs were already deleted from database")
        self._print_stack_status()
    
    def _print_stack_contents(self):
        """Internal method to print current stack contents"""
        if not self.stack:
            print("STACK STATE: [] (empty session)")
            return
        
        if len(self.stack) <= 4:
            stack_display = " | ".join([f"'{song.title}'" for song in reversed(self.stack)])
            print(f"STACK STATE: [TOP: {stack_display} :BOTTOM]")
        else:
            top_songs = [f"'{song.title}'" for song in reversed(self.stack[:2])]
            bottom_songs = [f"'{song.title}'" for song in reversed(self.stack[-2:])]
            print(f"STACK STATE: [TOP: {' | '.join(top_songs)} | ... | {' | '.join(bottom_songs)} :BOTTOM]")
    
    def _print_stack_status(self):
        """Internal method to print stack statistics"""
        print(f"STACK STATS: Current Session={len(self.stack)}, Total Pushes={self.total_pushes}, Total Pops={self.total_pops}")
        print(f"STACK STATS: Permanent Deletions={self.total_permanent_deletes}, Max Session Size={self.max_size_reached}")
    
    def __str__(self):
        """Return a string showing the current delete session"""
        if not self.stack:
            return "Delete session is empty."
        
        result = f"Current Delete Session ({len(self.stack)} songs):\n"
        for i, song in enumerate(reversed(self.stack), 1):
            result += f"  {i}. {song.title} - {song.artist} (ID: {song.id})\n"
        
        result += f"\nSession Stats: {self.total_pushes} deleted, {self.total_permanent_deletes} permanent deletions (all-time)"
        return result.strip()

# Test functionality with verbose output
if __name__ == "__main__":
    print("=" * 60)
    print("DELETE STACK DEMONSTRATION: Testing flush session functionality")
    print("=" * 60)
    
    delete_stack = DeleteStack()
    
    # Create test songs
    songs = [
        Song(song_id=1, title="Hotel California", artist="Eagles"),
        Song(song_id=2, title="Bohemian Rhapsody", artist="Queen"),
        Song(song_id=3, title="Imagine", artist="John Lennon"),
        Song(song_id=4, title="Yesterday", artist="The Beatles")
    ]
    
    print("\nTesting DELETE operations (immediate database deletion):")
    for song in songs:
        delete_stack.push_song(song)
    
    print("\nTesting VIEW current delete session:")
    delete_stack.view_stack()
    
    print("\nTesting GET current session:")
    current_session = delete_stack.get_current_delete_session()
    
    print("\nTesting POP operation (remove from session tracking):")
    popped_song = delete_stack.pop_song()
    
    print("\nTesting FLUSH delete session (LIFO processing):")
    print("Note: Songs will be flushed in LIFO order (Last In, First Out)")
    print("Expected order: Yesterday -> Imagine -> Bohemian Rhapsody (reverse of addition)")
    flushed_songs = delete_stack.flush_delete_session()
    
    print("\nTesting DELETION HISTORY:")
    history = delete_stack.get_deleted_songs_history()
    
    print("\nAdding more songs to new session:")
    new_song = Song(song_id=5, title="Stairway to Heaven", artist="Led Zeppelin")
    delete_stack.push_song(new_song)
    
    print("\nCurrent session after new additions:")
    delete_stack.view_stack()
    
    print("\n" + "=" * 60)
    print("DELETE STACK DEMONSTRATION COMPLETE")
    print("Key Features Demonstrated:")
    print("- Immediate database deletion on push")
    print("- Session tracking with LIFO stack")
    print("- Flush session to finalize deletions")
    print("- Complete deletion history tracking")
    print("=" * 60)
