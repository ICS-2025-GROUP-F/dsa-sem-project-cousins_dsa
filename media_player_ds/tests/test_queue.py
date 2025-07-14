import pytest
from src.ds.queue_create import SongQueue
from src.model.song import Song

def test_enqueue_song():
    """Test enqueueing a single song to the queue"""
    queue = SongQueue()

    # Verify queue is initially empty
    assert queue.size() == 0
    assert queue.is_empty() == True

    # Create a song with sample data
    song = Song(
        id="song_001",
        title="Test Song",
        artist="Test Artist",
        album="Test Album",
        duration=180,
        file_path="/music/test_song.mp3"
    )

    # Enqueue the song
    queue.enqueue(song)

    # Assert queue size increased
    assert queue.size() == 1
    assert queue.is_empty() == False

    # Verify the song can be peeked at without removing it
    peeked_song = queue.peek()
    assert peeked_song.id == "song_001"
    assert peeked_song.title == "Test Song"
    assert peeked_song.artist == "Test Artist"

    # Verify queue size hasn't changed after peek
    assert queue.size() == 1


def test_enqueue_multiple_songs():
    """Test enqueueing multiple songs"""
    queue = SongQueue()

    # Create multiple songs
    songs = [
        Song(id="song_001", title="Song 1", artist="Artist 1", album="Album 1", duration=120,
             file_path="/music/song1.mp3"),
        Song(id="song_002", title="Song 2", artist="Artist 2", album="Album 2", duration=150,
             file_path="/music/song2.mp3"),
        Song(id="song_003", title="Song 3", artist="Artist 3", album="Album 3", duration=200,
             file_path="/music/song3.mp3")
    ]

    # Enqueue all songs
    for song in songs:
        queue.enqueue(song)

    # Verify queue size
    assert queue.size() == 3

    # Verify FIFO order (first song added should be first to peek)
    first_song = queue.peek()
    assert first_song.id == "song_001"


def test_process_queue():
    """Test processing queue with multiple songs and simulating DB insertion"""
    # Create queue and mock database
    queue = SongQueue()
    mock_db = MockDatabase()

    # Create multiple songs to process
    songs_to_add = [
        Song(id="song_001", title="Rock Song", artist="Rock Artist", album="Rock Album", duration=240,
             file_path="/music/rock.mp3"),
        Song(id="song_002", title="Pop Song", artist="Pop Artist", album="Pop Album", duration=180,
             file_path="/music/pop.mp3"),
        Song(id="song_003", title="Jazz Song", artist="Jazz Artist", album="Jazz Album", duration=300,
             file_path="/music/jazz.mp3"),
        Song(id="song_004", title="Classical Song", artist="Classical Artist", album="Classical Album", duration=420,
             file_path="/music/classical.mp3")
    ]

    # Enqueue all songs
    for song in songs_to_add:
        queue.enqueue(song)

    # Verify initial state
    assert queue.size() == 4
    assert len(mock_db.songs) == 0

    # Process the queue (simulate database insertions)
    processed_songs = []
    insertion_results = []

    while not queue.is_empty():
        # Dequeue song
        song = queue.dequeue()
        processed_songs.append(song)

        # Simulate database insertion
        success = mock_db.insert_song(song)
        insertion_results.append(success)

        # Simulate processing delay (in real scenario)
        # time.sleep(0.1)  # Commented out for test speed

    # Verify queue is now empty
    assert queue.size() == 0
    assert queue.is_empty() == True

    # Verify all songs were processed
    assert len(processed_songs) == 4
    assert all(insertion_results)  # All insertions should succeed

    # Verify songs were processed in FIFO order
    expected_order = ["song_001", "song_002", "song_003", "song_004"]
    actual_order = [song.id for song in processed_songs]
    assert actual_order == expected_order

    # Verify database contains all songs
    assert len(mock_db.songs) == 4
    assert all(song.id in mock_db.songs for song in songs_to_add)


def test_process_queue_with_failures():
    """Test processing queue with simulated database failures"""
    queue = SongQueue()
    mock_db = MockDatabase()

    # Create songs, including one that will fail insertion
    songs = [
        Song(id="song_001", title="Valid Song 1", artist="Artist 1", album="Album 1", duration=180,
             file_path="/music/valid1.mp3"),
        Song(id="invalid_song", title="Invalid Song", artist="Artist 2", album="Album 2", duration=0,
             file_path="/music/invalid.mp3"),  # Invalid duration
        Song(id="song_003", title="Valid Song 2", artist="Artist 3", album="Album 3", duration=240,
             file_path="/music/valid2.mp3")
    ]

    # Enqueue songs
    for song in songs:
        queue.enqueue(song)

    # Process queue with error handling
    processed_count = 0
    failed_count = 0

    while not queue.is_empty():
        song = queue.dequeue()

        try:
            success = mock_db.insert_song(song)
            if success:
                processed_count += 1
            else:
                failed_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to insert song {song.id}: {e}")

    # Verify results
    assert processed_count == 2  # Two valid songs
    assert failed_count == 1  # One invalid song
    assert len(mock_db.songs) == 2  # Only valid songs in database


def test_queue_edge_cases():
    """Test edge cases for queue operations"""
    queue = SongQueue()

    # Test dequeue on empty queue
    with pytest.raises(IndexError):
        queue.dequeue()

    # Test peek on empty queue
    with pytest.raises(IndexError):
        queue.peek()

    # Test enqueue None
    with pytest.raises(ValueError):
        queue.enqueue(None)

    # Test enqueue invalid object
    with pytest.raises(TypeError):
        queue.enqueue("not a song object")


class MockDatabase:
    """Mock database for testing"""

    def __init__(self):
        self.songs = {}

    def insert_song(self, song: Song) -> bool:
        """Simulate database insertion"""
        # Simulate validation failure
        if song.duration <= 0:
            raise ValueError(f"Invalid song duration: {song.duration}")

        # Simulate duplicate key error
        if song.id in self.songs:
            return False

        # Simulate successful insertion
        self.songs[song.id] = {
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'duration': song.duration,
            'file_path': song.file_path
        }
        return True

    def get_song(self, song_id: str) -> dict:
        """Retrieve song from mock database"""
        return self.songs.get(song_id)

    def get_all_songs(self) -> dict:
        """Get all songs from mock database"""
        return self.songs.copy()


# Additional helper test for queue operations
def test_queue_operations():
    """Test basic queue operations (enqueue, dequeue, peek)"""
    queue = SongQueue()

    # Test with single song
    song1 = Song(id="test_1", title="Test 1", artist="Artist 1", album="Album 1", duration=120, file_path="/test1.mp3")
    queue.enqueue(song1)

    assert queue.size() == 1
    assert queue.peek().id == "test_1"

    dequeued = queue.dequeue()
    assert dequeued.id == "test_1"
    assert queue.size() == 0

    # Test FIFO behavior with multiple songs
    song2 = Song(id="test_2", title="Test 2", artist="Artist 2", album="Album 2", duration=150, file_path="/test2.mp3")
    song3 = Song(id="test_3", title="Test 3", artist="Artist 3", album="Album 3", duration=180, file_path="/test3.mp3")

    queue.enqueue(song2)
    queue.enqueue(song3)

    # First in, first out
    assert queue.dequeue().id == "test_2"
    assert queue.dequeue().id == "test_3"
    assert queue.is_empty()


if __name__ == "__main__":
    # Run tests if file is executed directly
    pytest.main([__file__, "-v"])