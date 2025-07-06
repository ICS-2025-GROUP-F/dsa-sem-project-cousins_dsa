class Song:
    def __init__(self, song_id, title, artist, album):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.album = album

    def __str__(self):
        return f"[{self.id}] {self.title} by {self.artist} ({self.album})"
