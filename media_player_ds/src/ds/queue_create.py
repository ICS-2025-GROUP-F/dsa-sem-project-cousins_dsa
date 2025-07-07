from collections import deque


class SongQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue_song(self, song):
        """Add song to the queue (FIFO)"""
        self.queue.append(song)
        print(f"Added '{song}' to queue")

    def dequeue_song(self):
        """Remove and return the next song from queue"""
        if self.queue:
            song = self.queue.popleft()
            print(f"Now playing: '{song}'")
            return song
        else:
            print("Queue is empty")
            return None

    def peek_next(self):
        """View the next song without removing it"""
        if self.queue:
            return self.queue[0]
        return None

    def get_queue_size(self):
        """Return the number of songs in queue"""
        return len(self.queue)

    def is_empty(self):
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

        songs_to_insert = list(self.queue)

        print("Inserting songs into database:")
        for song in songs_to_insert:
            print(f"  - Inserted: {song}")

        self.clear_queue()
        print(f"Processed {len(songs_to_insert)} songs")


if __name__ == "__main__":
    player_queue = SongQueue()

    player_queue.enqueue_song("Bohemian Rhapsody - Queen")
    player_queue.enqueue_song("Hotel California - Eagles")
    player_queue.enqueue_song("Imagine - John Lennon")

    player_queue.view_queue()

    player_queue.dequeue_song()

    next_song = player_queue.peek_next()
    if next_song:
        print(f"Up next: {next_song}")

    player_queue.enqueue_song("Yesterday - The Beatles")

    player_queue.process_queue()