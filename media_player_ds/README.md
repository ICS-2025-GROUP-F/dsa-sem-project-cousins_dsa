# Media Player with Data Structures

A Python desktop application demonstrating practical implementation of data structures (Queue, Binary Search Tree, Hash Table, Stack) through a music library management system with complete CRUD operations.

## Project Overview

This Data Structures and Algorithms semester project implements a media player that uses different data structures for specific CRUD operations:

- **Queue (FIFO)**: CREATE operations - Add new songs to library
- **Binary Search Tree**: READ operations - Search and display songs alphabetically
- **Hash Table**: UPDATE operations - Modify song metadata with O(1) access
- **Stack (LIFO)**: DELETE operations - Remove songs with undo functionality

## Features

- Complete CRUD operations with verbose data structure logging
- SQLite database persistence
- Tkinter GUI with real-time song display
- Advanced delete session management with flush capability
- Search functionality across multiple fields
- Data structure operation visualization in console
- Comprehensive testing suite

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd dsa-sem-project-cousins_dsa
   ```

2. **Set up Python environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   cd media_player_ds
   pip install -r requirements.txt
   ```

## Branch Information

This project uses a collaborative Git workflow with feature branches:

### Main Branches
- **main**: Base template and integrated codebase
- **integration-prep**: Integration testing branch

### Feature Branches (by team member)
- **regNO_170469_Read**: Binary Search Tree implementation for read operations
- **regNo_190118_queue**: Queue implementation for create operations  
- **regNo_192231_Stack**: Stack implementation for delete operations
- **regNo_178616_update**: Hash Table implementation for update operations
- **regNo_192108_GUI**: Complete GUI integration and user interface

### Branch Conversion Instructions

To work with different implementations:

1. **List all branches:**
   ```bash
   git branch -a
   ```

2. **Switch to a specific feature branch:**
   ```bash
   git checkout regNO_170469_Read    # For BST implementation
   git checkout regNo_190118_queue   # For Queue implementation
   git checkout regNo_192231_Stack   # For Stack implementation
   git checkout regNo_178616_update  # For Hash Table implementation
   git checkout regNo_192108_GUI     # For GUI implementation
   ```

3. **Return to main integrated version:**
   ```bash
   git checkout main
   ```

4. **View branch commit history:**
   ```bash
   git log --oneline --graph --all
   ```

## Quick Start

### 1. Basic Application Launch

```bash
# Navigate to project directory
cd media_player_ds

# Run the main application
python main.py
```

### 2. Testing Individual Data Structures

```bash
# Test Queue operations (FIFO)
python src/ds/queue_create.py

# Test BST operations (Search/Traversal)
python src/ds/bst_read.py

# Test Hash Table operations (Updates)
python src/ds/hashtable_update.py

# Test Stack operations (LIFO/Delete)
python src/ds/stack_delete.py
```

### 3. Database Operations

```bash
# Test database functionality
python src/db/database.py

# View database contents (if SQLite CLI installed)
sqlite3 songs.db ".tables"
sqlite3 songs.db "SELECT * FROM songs;"
```

### 4. Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python -m pytest tests/test_bst.py
python -m pytest tests/test_hashtable.py
python -m pytest tests/test_queue.py
python -m pytest tests/test_stack.py
```

## Application Usage

### GUI Operations

1. **Adding Songs (Queue/CREATE):**
   - Fill in song details (Title, Artist, Album, Genre, Year)
   - Click "Add to Queue" to add songs to processing queue
   - Click "Process Queue" to insert all queued songs into database

2. **Viewing Songs (BST/READ):**
   - Song list is automatically displayed on the right panel
   - Click "View All Songs" for BST in-order traversal popup
   - Use "Search Song" for finding specific songs

3. **Updating Songs (Hash Table/UPDATE):**
   - Note the Song ID from the right panel
   - Click "Update Song" and enter the ID
   - Modify desired fields (leave blank to keep current values)

4. **Deleting Songs (Stack/DELETE):**
   - Note the Song ID from the right panel
   - Click "Delete Song" and enter the ID
   - Song is immediately deleted from database but tracked in delete session
   - Use "View Delete Stack" to see deleted songs
   - Use "Flush Delete Session" to finalize deletions
   - Use "View Deleted History" for complete audit trail

### Console Output

The application provides verbose logging for all data structure operations:

- **Queue operations**: Shows FIFO processing, queue state changes
- **BST operations**: Displays tree building, search paths, traversal steps
- **Hash Table operations**: Shows O(1) access, collision handling, updates
- **Stack operations**: Demonstrates LIFO processing, session management

## Project Structure

```
media_player_ds/
├── src/
│   ├── main.py              # Application entry point
│   ├── model/
│   │   └── song.py          # Song data model
│   ├── db/
│   │   └── database.py      # SQLite database operations
│   ├── ds/                  # Data structure implementations
│   │   ├── queue_create.py  # Queue for CREATE operations
│   │   ├── bst_read.py      # BST for READ operations
│   │   ├── hashtable_update.py # Hash Table for UPDATE operations
│   │   └── stack_delete.py  # Stack for DELETE operations
│   ├── ui/
│   │   └── interface.py     # Tkinter GUI interface
│   └── utils/
│       └── logger.py        # Logging utilities
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technical Details

### Data Structure Implementations

- **Queue**: Uses `collections.deque` for O(1) enqueue/dequeue operations
- **Binary Search Tree**: Custom implementation with recursive operations
- **Hash Table**: Python dictionary with song ID as key for O(1) access
- **Stack**: Python list with LIFO operations for delete session management

### Database Schema

```sql
CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT,
    duration INTEGER DEFAULT 0,
    file_path TEXT,
    genre TEXT,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Time Complexity

- **Queue operations**: O(1) for enqueue/dequeue
- **BST operations**: O(log n) average for search/insert
- **Hash Table operations**: O(1) average for updates
- **Stack operations**: O(1) for push/pop

## Troubleshooting

### Common Issues

1. **Import Errors:**
   ```bash
   # Ensure you're in the correct directory
   cd media_player_ds
   python main.py
   ```

2. **Database Not Found:**
   ```bash
   # Initialize database
   python src/db/database.py
   ```

3. **GUI Not Displaying:**
   ```bash
   # Check Tkinter installation
   python -c "import tkinter; print('Tkinter available')"
   ```

4. **Module Not Found:**
   ```bash
   # Ensure __init__.py files exist
   find . -name "__init__.py"
   ```

### Performance Notes

- Application is optimized for educational demonstration
- Database operations include verbose logging which may affect performance
- For production use, consider disabling verbose output

## Development

### Adding New Features

1. Create feature branch following naming convention: `regNo_XXXXXX_feature`
2. Implement feature with comprehensive logging
3. Add corresponding tests
4. Create pull request for review

### Testing

- Each data structure has corresponding test file
- Tests include functionality and edge case validation
- Run tests before committing changes

## Contributing

This is an academic project developed collaboratively by team members. Each branch represents individual contributions that are integrated into the main application.

## License

This project is developed for educational purposes as part of a Data Structures and Algorithms course.
