import pytest
from src.ds.hashtable_update import SongTable
from src.model.song import Song

@pytest.fixture
def song_table():
    """Prepare a SongTable with preloaded songs"""
    songs = [
        Song("S001", "Imagine", "John Lennon", "Imagine"),
        Song("S002", "Bohemian Rhapsody", "Queen", "Opera")
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
