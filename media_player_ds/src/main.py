from src.db.database import init_db
from tkinter import Tk
from src.ui.interface import MediaPlayerUI

def main():
    init_db()  # Create DB if not exists
    root = Tk()
    app = MediaPlayerUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
