import os
import sqlite3
from pathlib import Path

def create_database(db_path):
    """Create SQLite database if it doesn't exist"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS xmp_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            xmp_type TEXT NOT NULL CHECK(xmp_type IN ('std', 'ext')),
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            base_name TEXT NOT NULL,
            xmp_modified_time REAL,
            renamed_xmp_file TEXT,
            UNIQUE(file_path)
        )
    ''')
    conn.commit()
    return conn

def scan_directory(directory, db_path):
    """Scan directory for .xmp files and add them to SQLite database"""
    conn = create_database(db_path)
    cursor = conn.cursor()
    
    # Répertoires à exclure
    excluded_dirs = {'#recycle', '#snapshot', '.dtrash'}
    
    count = 0
    
    for root, dirs, files in os.walk(directory):
        
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for filename in files:
            if filename.endswith('.xmp'):
                # Extract base filename (without .xmp)
                base_name = Path(filename).stem
                xmp_type = 'std' if '.' not in base_name else 'ext'
                
                xmp_path = os.path.join(root, filename)

                stat = os.stat(xmp_path)

                
                cursor.execute('''
                    INSERT INTO xmp_files (file_name, file_path, base_name, xmp_type, xmp_modified_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (filename, xmp_path, base_name, xmp_type, stat.st_mtime))
                count += 1
                
                # Log and commit every 1000 files
                if count % 1000 == 0:
                    conn.commit()
                    print(f"Progress: {count} XMP files processed and committed...")
    
    conn.commit()
    conn.close()
    print(f"Database updated: {db_path} - Total: {count} XMP files")

if __name__ == "__main__":
    directory = input("Enter directory path: ")
    db_path = "XmpFixer\\xmp_inventory.db"
    
    if os.path.isdir(directory):
        scan_directory(directory, db_path)
    else:
        print("Invalid directory path")