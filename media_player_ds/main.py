import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from src/
sys.path.insert(0, project_root)

# Imports should now work
from src.db.database import init_db
from tkinter import Tk
from src.ui.interface import MediaPlayerUI


def main():
    try:
        print("Initializing database...")
        init_db()

        print("Starting GUI...")
        root = Tk()
        app = MediaPlayerUI(root)
        root.mainloop()

    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required files are present.")
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()