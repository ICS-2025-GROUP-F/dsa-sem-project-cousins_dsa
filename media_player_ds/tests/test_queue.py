import pytest
from src.ds.queue_create import SongQueue
from src.model.song import Song


class MockDatabase:
    """Mock database for simulating insertions"""
    def __init__(self):
        self.songs = {}

    def insert_song(self, song: Song) -> bool:
        if not song or song.duration <= 0:
            return False
        if song.id in self.songs:
            return False
        self.songs[song.id] = song
        return True


@pytest.fixture
def queue_with_songs():
    queue = SongQueue()
    songs = [
        Song(song_id="song_001", title="Song 1", artist="Artist 1", duration=200),
        Song(song_id="song_002", title="Song 2", artist="Artist 2", duration=220),
        Song(song_id="song_003", title="Song 3", artist="Artist 3", duration=180)
    ]
    for song in songs:
        queue.enqueue_song(song)
    return queue, songs


def test_enqueue_and_peek():
    queue = SongQueue()
    song = Song(song_id="s123", title="Test Song", artist="Tester", duration=210)
    queue.enqueue_song(song)

    assert queue.get_queue_size() == 1
    assert not queue.is_empty()

    peeked = queue.peek_next()
    assert peeked is not None
    assert peeked.title == "Test Song"
    assert peeked.artist == "Tester"


def test_dequeue_fifo(queue_with_songs):
    queue, songs = queue_with_songs

    first = queue.dequeue_song()
    second = queue.dequeue_song()

    assert first.title == songs[0].title
    assert second.title == songs[1].title
    assert queue.get_queue_size() == 1


def test_process_queue_with_mock(monkeypatch):
    queue = SongQueue()
    db = MockDatabase()

    songs = [
        Song(song_id="s1", title="A", artist="X", duration=100),
        Song(song_id="s2", title="B", artist="Y", duration=150)
    ]

    for song in songs:
        queue.enqueue_song(song)

    # Monkeypatch the insert_song_to_db import to use the mock
    monkeypatch.setitem(__import__("sys").modules, "src.db.database", type("mock_module", (), {
        "insert_song_to_db": db.insert_song
    }))

    # Process queue, internally uses db.insert_song
    queue.process_queue()

    assert db.songs["s1"].title == "A"
    assert db.songs["s2"].title == "B"
    assert queue.is_empty()


def test_clear_queue():
    queue = SongQueue()
    queue.enqueue_song(Song(song_id="x1", title="Clear Me", artist="A", duration=200))
    assert queue.get_queue_size() == 1
    queue.clear_queue()
    assert queue.is_empty()


def test_queue_edge_cases():
    queue = SongQueue()

    # Dequeue and peek from empty queue
    assert queue.dequeue_song() is None
    assert queue.peek_next() is None

    # Clear already empty queue
    queue.clear_queue()
    assert queue.get_queue_size() == 0

    # Process empty queue
    queue.process_queue()  # Should not crash


def test_view_queue_output(queue_with_songs, capsys):
    queue, songs = queue_with_songs
    queue.view_queue()
    output = capsys.readouterr().out
    for song in songs:
        assert song.title in output
        assert song.artist in output


def test_enqueue_multiple_and_order():
    queue = SongQueue()
    s1 = Song(song_id="sA", title="Alpha", artist="A", duration=100)
    s2 = Song(song_id="sB", title="Beta", artist="B", duration=110)
    s3 = Song(song_id="sC", title="Gamma", artist="C", duration=120)

    queue.enqueue_song(s1)
    queue.enqueue_song(s2)
    queue.enqueue_song(s3)

    assert queue.get_queue_size() == 3
    assert queue.peek_next().title == "Alpha"

    assert queue.dequeue_song().title == "Alpha"
    assert queue.dequeue_song().title == "Beta"
    assert queue.dequeue_song().title == "Gamma"
    assert queue.is_empty()
