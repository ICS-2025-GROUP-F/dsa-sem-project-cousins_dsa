import pytest
from src.ds.stack_delete import DeleteStack
from src.model.song import Song

def test_push_and_pop():
    # Create an instance of the DeleteStack
    stack = DeleteStack()

    # Create sample Song objects
    song1 = Song("Go Easy", "Odeal", "1:30")
    song2 = Song("On Bended Knee", "Boyz II Men", "4:15")
    song3 = Song("Lost Me", "Giveon", "2:45")
    song4 = Song("Neu Roses", "Daniel Caesar", "2:45")

    # Push the songs to the stack 
    stack.push_song(song1)
    stack.push_song(song2)
    stack.push_song(song3)
    stack.push_song(song4)

    # Pop songs from the stack and verify LIFO order
    popped_song1 = stack.pop_and_delete()
    assert popped_song1 == song3, "Expected Song C to be popped first"

    popped_song2 = stack.pop_and_delete()
    assert popped_song2 == song2, "Expected Song B to be popped second"

    popped_song3 = stack.pop_and_delete()
    assert popped_song3 == song1, "Expected Song A to be popped last"

    # Stack should now be empty
    assert stack.pop_and_delete() is None, "Expected None when popping from empty stack"
