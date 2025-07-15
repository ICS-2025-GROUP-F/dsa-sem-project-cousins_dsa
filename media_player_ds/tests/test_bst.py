import os, sys
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from src.ds.bst_read import SongBST
from src.model.song import Song
from src.db.database import get_all_songs


def test_insert_and_search():
    bst = SongBST()
    all_songs = get_all_songs()

    for s in all_songs:
        bst.insert(s)

    title_to_search = all_songs[0].title
    found_song = bst.search_by_title(title_to_search)

    assert found_song is not None
    assert found_song.title == title_to_search
    assert hasattr(found_song, "artist")


def test_inorder_traversal(capsys):
    bst = SongBST()
    all_songs = get_all_songs()

    for s in all_songs:
        bst.insert(s)

    bst.inorder_traversal()

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    titles_from_bst = [
        line.strip().split(". ")[1].split(" - ")[0]
        for line in output_lines
        if line.strip() and line.strip()[0].isdigit()
    ]
    expected_titles = sorted([s.title for s in all_songs])

    assert titles_from_bst == expected_titles