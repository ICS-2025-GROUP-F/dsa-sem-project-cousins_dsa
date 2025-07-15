import pytest
from src.ds.stack_delete import DeleteStack
from src.model.song import Song

import sys

@pytest.fixture(autouse=True)
def mock_delete(monkeypatch):
    """Auto-mock delete_song_from_db to always succeed for tests"""
    monkeypatch.setitem(
        sys.modules,
        "src.db.database",
        type("MockDB", (), {"delete_song_from_db": lambda song_id: True})
    )


@pytest.fixture
def delete_stack_with_songs():
    stack = DeleteStack()
    s1 = Song(song_id="s1", title="Song A", artist="Artist A", duration=180)
    s2 = Song(song_id="s2", title="Song B", artist="Artist B", duration=200)
    s3 = Song(song_id="s3", title="Song C", artist="Artist C", duration=210)

    for song in [s1, s2, s3]:
        stack.push_song(song)

    return stack, [s1, s2, s3]


def test_push_and_pop_behavior():
    stack = DeleteStack()
    song1 = Song(song_id="a1", title="Go Easy", artist="Odeal", duration=90)
    song2 = Song(song_id="a2", title="On Bended Knee", artist="Boyz II Men", duration=255)
    song3 = Song(song_id="a3", title="Lost Me", artist="Giveon", duration=165)

    stack.push_song(song1)
    stack.push_song(song2)
    stack.push_song(song3)

    assert not stack.is_empty()

    assert stack.pop_song().title == "Lost Me"
    assert stack.pop_song().title == "On Bended Knee"
    assert stack.pop_song().title == "Go Easy"

    # Stack should now be empty
    assert stack.pop_song() is None
    assert stack.is_empty()


def test_peek_returns_top_song():
    stack = DeleteStack()
    s1 = Song(song_id="s123", title="Peek Song", artist="Z", duration=180)
    s2 = Song(song_id="s456", title="Top Song", artist="X", duration=190)

    stack.push_song(s1)
    stack.push_song(s2)

    top = stack.peek()
    assert top.title == "Top Song"
    assert stack.get_current_delete_session()[-1].title == "Top Song"


def test_flush_stack_and_history_tracking(delete_stack_with_songs):
    stack, songs = delete_stack_with_songs

    flushed = stack.flush_delete_session()

    # Songs flushed in LIFO order
    assert [s.id for s in flushed] == ["s3", "s2", "s1"]
    assert stack.is_empty()

    history = stack.get_deleted_songs_history()
    assert len(history) == 3
    assert [s.id for s in history] == ["s3", "s2", "s1"]


def test_clear_session_resets_stack():
    stack = DeleteStack()
    stack.push_song(Song(song_id="s001", title="Temp", artist="Temp", duration=120))

    assert not stack.is_empty()
    stack.clear_session()
    assert stack.is_empty()
    assert stack.get_current_delete_session() == []


def test_get_current_delete_session_order(delete_stack_with_songs):
    stack, songs = delete_stack_with_songs
    current = stack.get_current_delete_session()
    assert len(current) == 3
    assert current[0].id == "s1"
    assert current[-1].id == "s3"


def test_restore_song_to_database_simulation(monkeypatch):
    stack = DeleteStack()
    song = Song(song_id="abc123", title="Resurrect", artist="Phantom", duration=150)

    # Patch insert_song_to_db to return True
    monkeypatch.setitem(__import__("sys").modules, "src.db.database", type("mockmod", (), {
        "insert_song_to_db": lambda s: True
    }))

    result = stack.restore_song_to_database(song)
    assert result is True
