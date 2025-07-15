import os
import sys
import pytest
from datetime import datetime

# Adjust path for importing local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.ds.hashtable_update import SongTable
from src.model.song import Song


@pytest.fixture
def song_table():
    """Fixture to initialize a hash table with test songs"""
    songs = [
        Song(
            song_id="S001",
            title="Imagine",
            artist="John Lennon",
            album="Imagine",
            genre="Rock",
            year=1971,
            duration=183,
            file_path="/music/imagine.mp3",
            created_at=datetime(2020, 1, 1)
        ),
        Song(
            song_id="S002",
            title="Bohemian Rhapsody",
            artist="Queen",
            album="A Night at the Opera",
            genre="Rock",
            year=1975,
            duration=354,
            file_path="/music/bohemian.mp3",
            created_at=datetime(2020, 1, 2)
        )
    ]
    table = SongTable()
    table.load_from_list(songs)
    return table


def test_update_existing_song(song_table):
    result = song_table.update_song("S002", artist="Freddie Mercury")
    assert result is True
    assert song_table.table["S002"].artist == "Freddie Mercury"


def test_update_nonexistent_song(song_table):
    result = song_table.update_song("S999", title="Fake Song")
    assert result is False


def test_update_multiple_fields(song_table):
    result = song_table.update_song(
        "S001",
        title="Imagine (Remastered)",
        artist="John Lennon",
        album="Greatest Hits",
        genre="Pop Rock",
        year=1972,
        duration=200,
        file_path="/music/imagine-remastered.mp3"
    )
    assert result is True

    updated = song_table.table["S001"]
    assert updated.title == "Imagine (Remastered)"
    assert updated.album == "Greatest Hits"
    assert updated.genre == "Pop Rock"
    assert updated.year == 1972
    assert updated.duration == 200
    assert updated.file_path == "/music/imagine-remastered.mp3"
    assert updated.artist == "John Lennon"


def test_noop_update(song_table):
    """Update with no fields should return True but not change data"""
    original = song_table.table["S002"]
    result = song_table.update_song("S002")  # no fields
    assert result is True
    # Ensure nothing changed
    current = song_table.table["S002"]
    assert current.title == original.title
    assert current.artist == original.artist
    assert current.album == original.album
    assert current.genre == original.genre
    assert current.duration == original.duration
    assert current.file_path == original.file_path


def test_get_song(song_table):
    song = song_table.get_song("S001")
    assert song is not None
    assert song.title == "Imagine"
    assert song.year == 1971


def test_get_nonexistent_song(song_table):
    song = song_table.get_song("BAD_ID")
    assert song is None


def test_table_structure(song_table):
    """Ensure all songs are in the table with correct structure"""
    assert len(song_table.table) == 2
    for key, song in song_table.table.items():
        assert isinstance(song, Song)
        assert hasattr(song, "title")
        assert hasattr(song, "artist")
        assert hasattr(song, "duration")
