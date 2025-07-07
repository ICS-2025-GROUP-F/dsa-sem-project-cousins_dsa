class DeleteStack:
    def __init__(self):
        # This list will store deleted songs temporarily, like a recycle bin.
        self.stack = []

    def push_song(self, song):
        # Add a deleted song to the top of the stack.
        self.stack.append(song)
        print(f"Song '{song}' added to delete stack.")

    def pop_and_delete(self):
        # If there are songs in the stack, remove the most recent one.
        if self.stack:
            deleted_song = self.stack.pop()
            print(f"Song '{deleted_song}' permanently deleted.")
            return deleted_song
        else:
            # If the stack is empty, there's nothing to delete.
            print("Delete stack is empty. No song to delete.")
            return None

    def peek(self):
        # Return the most recent song added to the stack without removing it.
        if self.stack:
            return self.stack[-1]
        else:
            # If the stack is empty, return None.
            return None

    def is_empty(self):
        # Return True if the stack has no songs, False otherwise.
        return len(self.stack) == 0

    def __str__(self):
        # Return a string showing the stack contents from top to bottom.
        if not self.stack:
            return "Delete stack is empty."
        return "Delete stack (top to bottom):\n" + "\n".join(reversed(self.stack))
