from collections import deque
from src.model.song import Song
from typing import Optional

class SongQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue_song(self, song: Song):
        """Add song to the queue (FIFO)"""
        self.queue.append(song)
        print(f"Added '{song}' to queue")

    def dequeue_song(self) -> Optional[Song]:
        """Remove and return the next song from queue"""
        if self.queue:
            song = self.queue.popleft()
            print(f"Dequeued: '{song}'")
            return song
        else:
            print("Queue is empty")
            return None

def peek_next(self) -> Optional[Song]:
        """View the next song without removing it"""
        if self.queue:
            return self.queue[0]
        return None

    def get_queue_size(self) -> int:
        """Return the number of songs in queue"""
        return len(self.queue)

    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.queue) == 0

    def clear_queue(self):
        """Remove all songs from queue"""
        self.queue.clear()
        print("Queue cleared")
    def view_queue(self):
        """Display all songs in queue"""
        if self.queue:
            print("Current queue:")
            for i, song in enumerate(self.queue, 1):
                print(f"{i}. {song}")
        else:
            print("Queue is empty")

    def process_queue(self):
        """Insert all songs in queue to database and clear queue"""
        if not self.queue:
            print("No songs to process")
            return
# Import here to avoid circular imports
        try:
            from src.db.database import insert_song_to_db
            songs_processed = 0

            while not self.is_empty():
                song = self.dequeue_song()
                if insert_song_to_db(song):
                    songs_processed += 1
                else:
                    print(f"Failed to insert song: {song}")

            print(f"Processed {songs_processed} songs successfully")
        except ImportError:
            print("Database module not available - clearing queue without saving")
            self.clear_queue()
# Test functionality if run directly
if __name__ == "__main__":
    player_queue = SongQueue()

    # Create test songs
    song1 = Song(title="Bohemian Rhapsody", artist="Queen", album="A Night at the Opera")
    song2 = Song(title="Hotel California", artist="Eagles", album="Hotel California")

    player_queue.enqueue_song(song1)
    player_queue.enqueue_song(song2)
    player_queue.view_queue()

    next_song = player_queue.peek_next()
    if next_song:
        print(f"Up next: {next_song}")

    player_queue.process_queue()
