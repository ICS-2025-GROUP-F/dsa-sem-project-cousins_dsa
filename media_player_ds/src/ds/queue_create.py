from collections import deque
from src.model.song import Song
from typing import Optional

class SongQueue:
    def __init__(self):
        self.queue = deque()
        self.total_enqueued = 0
        self.total_dequeued = 0
        print("QUEUE: Initialized empty song queue (FIFO - First In, First Out)")
        self._print_queue_status()

    def enqueue_song(self, song: Song):
        """Add song to the queue (FIFO) with verbose logging"""
        print(f"\nQUEUE ENQUEUE: Adding '{song.title}' by {song.artist}")
        
        # Show queue state before
        print(f"QUEUE: Queue size before enqueue: {len(self.queue)}")
        if self.queue:
            print(f"QUEUE: Current front of queue: '{self.queue[0].title}'")
            print(f"QUEUE: Current back of queue: '{self.queue[-1].title}'")
        else:
            print("QUEUE: Queue is currently empty")
        
        # Perform enqueue
        self.queue.append(song)
        self.total_enqueued += 1
        
        print(f"QUEUE: Song added to BACK of queue (position {len(self.queue)})")
        print(f"QUEUE: Queue size after enqueue: {len(self.queue)}")
        print(f"QUEUE: Total songs enqueued so far: {self.total_enqueued}")
        
        self._print_queue_contents()
        self._print_queue_status()

    def dequeue_song(self) -> Optional[Song]:
        """Remove and return the next song from queue with verbose logging"""
        print(f"\nQUEUE DEQUEUE: Attempting to remove song from FRONT of queue")
        
        if not self.queue:
            print("QUEUE: Cannot dequeue - Queue is EMPTY!")
            return None
        
        # Show queue state before
        print(f"QUEUE: Queue size before dequeue: {len(self.queue)}")
        front_song = self.queue[0]
        print(f"QUEUE: Song at FRONT (to be removed): '{front_song.title}'")
        
        if len(self.queue) > 1:
            print(f"QUEUE: Next song in line: '{self.queue[1].title}'")
        else:
            print("QUEUE: This is the last song in queue")
        
        # Perform dequeue - FIFO operation
        song = self.queue.popleft()
        self.total_dequeued += 1
        
        print(f"QUEUE: Successfully dequeued: '{song.title}' by {song.artist}")
        print(f"QUEUE: Queue size after dequeue: {len(self.queue)}")
        print(f"QUEUE: Total songs dequeued so far: {self.total_dequeued}")
        
        if self.queue:
            print(f"QUEUE: New front of queue: '{self.queue[0].title}'")
        else:
            print("QUEUE: Queue is now EMPTY")
        
        self._print_queue_contents()
        self._print_queue_status()
        
        return song

    def peek_next(self) -> Optional[Song]:
        """View the next song without removing it with verbose logging"""
        print(f"\nQUEUE PEEK: Checking front of queue without removing")
        
        if self.queue:
            front_song = self.queue[0]
            print(f"QUEUE: Front song: '{front_song.title}' by {front_song.artist}")
            print(f"QUEUE: This song will be next to dequeue")
            print(f"QUEUE: Position in queue: 1 (front)")
            return front_song
        else:
            print("QUEUE: Queue is empty - nothing to peek")
            return None

    def get_queue_size(self) -> int:
        """Return the number of songs in queue with verbose logging"""
        size = len(self.queue)
        print(f"QUEUE SIZE: Current queue contains {size} songs")
        if size > 0:
            print(f"QUEUE SIZE: Songs waiting to be processed: {size}")
            print(f"QUEUE SIZE: Estimated processing time: {size * 2} seconds")
        return size

    def is_empty(self) -> bool:
        """Check if queue is empty with verbose logging"""
        empty = len(self.queue) == 0
        print(f"QUEUE EMPTY CHECK: Queue is {'EMPTY' if empty else 'NOT EMPTY'}")
        if not empty:
            print(f"QUEUE EMPTY CHECK: {len(self.queue)} songs still in queue")
        return empty

    def clear_queue(self):
        """Remove all songs from queue with verbose logging"""
        print(f"\nQUEUE CLEAR: Removing all {len(self.queue)} songs from queue")
        
        if self.queue:
            print("QUEUE CLEAR: Songs being cleared:")
            for i, song in enumerate(self.queue, 1):
                print(f"   {i}. {song.title} - {song.artist}")
        
        cleared_count = len(self.queue)
        self.queue.clear()
        print(f"QUEUE CLEAR: Successfully cleared {cleared_count} songs")
        print("QUEUE CLEAR: Queue is now empty")
        self._print_queue_status()

    def view_queue(self):
        """Display all songs in queue with verbose logging"""
        print(f"\nQUEUE VIEW: Displaying complete queue contents")
        print(f"QUEUE VIEW: Total songs in queue: {len(self.queue)}")
        print(f"QUEUE VIEW: Queue follows FIFO principle (First In, First Out)")
        
        if self.queue:
            print("QUEUE VIEW: Songs in FIFO order (front -> back):")
            for i, song in enumerate(self.queue, 1):
                position_desc = "FRONT" if i == 1 else "BACK" if i == len(self.queue) else f"Position {i}"
                processing_order = f"Will be processed #{i}"
                print(f"   {i}. [{position_desc}] {song.title} - {song.artist} ({processing_order})")
                
            print(f"QUEUE VIEW: Next to process: '{self.queue[0].title}'")
            print(f"QUEUE VIEW: Last to process: '{self.queue[-1].title}'")
        else:
            print("QUEUE VIEW: Queue is empty - no songs to display")

    def process_queue(self):
        """Insert all songs in queue to database and clear queue with verbose logging"""
        print(f"\nQUEUE PROCESS: Starting batch processing of {len(self.queue)} songs")
        
        if not self.queue:
            print("QUEUE PROCESS: No songs to process - queue is empty")
            return

        songs_to_process = list(self.queue)  # Create copy for logging
        print("QUEUE PROCESS: Songs to be processed (in FIFO order):")
        for i, song in enumerate(songs_to_process, 1):
            print(f"   {i}. {song.title} - {song.artist}")

        # Import here to avoid circular imports
        try:
            from src.db.database import insert_song_to_db
            songs_processed = 0
            failed_songs = []

            print("\nQUEUE PROCESS: Beginning database insertion process...")
            print("QUEUE PROCESS: Processing songs in FIFO order (first enqueued = first processed)")
            
            while not self.is_empty():
                song = self.dequeue_song()
                print(f"\nQUEUE PROCESS: Processing song #{songs_processed + 1}: {song.title}")
                print(f"QUEUE PROCESS: Attempting database insertion...")
                
                if insert_song_to_db(song):
                    songs_processed += 1
                    print(f"QUEUE PROCESS: Successfully inserted '{song.title}' to database")
                else:
                    failed_songs.append(song)
                    print(f"QUEUE PROCESS: Failed to insert '{song.title}' to database")

            print(f"\nQUEUE PROCESS COMPLETE:")
            print(f"   Successfully processed: {songs_processed} songs")
            print(f"   Failed to process: {len(failed_songs)} songs")
            print(f"   Processing efficiency: {(songs_processed/(songs_processed + len(failed_songs)))*100:.1f}%")
            
            if failed_songs:
                print("   Failed songs:")
                for song in failed_songs:
                    print(f"     - {song.title} - {song.artist}")
            
            print("QUEUE PROCESS: All songs have been dequeued from queue")
            self._print_queue_status()
            
        except ImportError:
            print("QUEUE PROCESS: Database module not available - clearing queue without saving")
            print("QUEUE PROCESS: Simulating processing by clearing queue...")
            processed_songs = list(self.queue)
            self.clear_queue()
            print(f"QUEUE PROCESS: Simulated processing of {len(processed_songs)} songs")

    def _print_queue_contents(self):
        """Internal method to print current queue contents"""
        if not self.queue:
            print("QUEUE STATE: []")
            return
            
        if len(self.queue) <= 5:
            queue_display = " -> ".join([f"'{song.title}'" for song in self.queue])
            print(f"QUEUE STATE: [FRONT: {queue_display} :BACK]")
        else:
            front_songs = [f"'{song.title}'" for song in list(self.queue)[:2]]
            back_songs = [f"'{song.title}'" for song in list(self.queue)[-2:]]
            print(f"QUEUE STATE: [FRONT: {' -> '.join(front_songs)} -> ... -> {' -> '.join(back_songs)} :BACK]")

    def _print_queue_status(self):
        """Internal method to print queue statistics"""
        print(f"QUEUE STATS: Size={len(self.queue)}, Total Enqueued={self.total_enqueued}, Total Dequeued={self.total_dequeued}")
        if self.total_enqueued > 0:
            efficiency = (self.total_dequeued / self.total_enqueued) * 100
            print(f"QUEUE STATS: Processing Efficiency={efficiency:.1f}%")

# Test functionality with verbose output
if __name__ == "__main__":
    print("=" * 60)
    print("QUEUE DEMONSTRATION: Testing with verbose output")
    print("=" * 60)
    
    player_queue = SongQueue()

    # Create test songs
    song1 = Song(title="Hotel California", artist="Eagles", album="Hotel California")
    song2 = Song(title="Bohemian Rhapsody", artist="Queen", album="A Night at the Opera")
    song3 = Song(title="Imagine", artist="John Lennon", album="Imagine")
    song4 = Song(title="Yesterday", artist="The Beatles", album="Help!")

    print("\nTesting QUEUE ENQUEUE operations (FIFO - First In, First Out):")
    player_queue.enqueue_song(song1)
    player_queue.enqueue_song(song2)
    player_queue.enqueue_song(song3)
    player_queue.enqueue_song(song4)

    print("\nTesting QUEUE PEEK operation:")
    player_queue.peek_next()

    print("\nTesting QUEUE VIEW operation:")
    player_queue.view_queue()

    print("\nTesting QUEUE DEQUEUE operations:")
    first_dequeued = player_queue.dequeue_song()
    second_dequeued = player_queue.dequeue_song()

    print("\nTesting QUEUE SIZE operation:")
    player_queue.get_queue_size()

    print("\nTesting QUEUE PROCESS operation:")
    player_queue.process_queue()

    print("\nTesting QUEUE EMPTY CHECK:")
    player_queue.is_empty()
    
    print("\n" + "=" * 60)
    print("QUEUE DEMONSTRATION COMPLETE")
    print("FIFO Principle Demonstrated: First song enqueued was first to be processed")
    print("=" * 60)
