import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
from memory_profiler import memory_usage
from src.ds.stack_delete import DeleteStack
from src.model.song import Song


def measure_stack_operations():
    print("\n=== STACK DELETE PERFORMANCE ===")

    stack = DeleteStack()

    # Create dummy songs
    songs = [
        Song(song_id=f"s{i}", title=f"Song {i}", artist=f"Artist {i}")
        for i in range(10)
    ]

    # Measure push performance
    def push_songs():
        for song in songs:
            stack.push_song(song)

    start_time = time.perf_counter()
    mem_usage_push = memory_usage((push_songs,), interval=0.01, timeout=1)
    end_time = time.perf_counter()
    print(f"Pushed {len(songs)} songs")
    print(f"Time taken: {end_time - start_time:.4f}s")
    print(f"Memory used: {max(mem_usage_push) - min(mem_usage_push):.4f} MiB")

    # Measure pop performance
    def pop_songs():
        while not stack.is_empty():
            stack.pop_song()

    start_time = time.perf_counter()
    mem_usage_pop = memory_usage((pop_songs,), interval=0.01, timeout=1)
    end_time = time.perf_counter()
    print(f"Popped all songs")
    print(f"Time taken: {end_time - start_time:.4f}s")
    print(f"Memory used: {max(mem_usage_pop) - min(mem_usage_pop):.4f} MiB")


def main():
    print("=== DSA MEDIA PLAYER PERFORMANCE TESTS ===")
    measure_stack_operations()
    # Additional calls can be added here like:
    # measure_queue_operations()
    # measure_bst_insert_and_search()
    # measure_database_insert_delete()


if __name__ == "__main__":
    main()
