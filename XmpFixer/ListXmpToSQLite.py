import os
import sqlite3
from pathlib import Path
import win32security



def get_file_owner_sid(filepath):
    security = win32security.GetFileSecurity(
        filepath,
        win32security.OWNER_SECURITY_INFORMATION
    )

    sid = security.GetSecurityDescriptorOwner()

    return win32security.ConvertSidToStringSid(sid)



DIGIKAM_SID = [
    get_file_owner_sid("\\\\[REDACTED]\\photo\\2020.06 - Guadeloupe\\Téléphone\\20200706_092520.xmp"),
    get_file_owner_sid("\\\\[REDACTED]\\photo\\01 - Autres Katya\\Fleurs\\2018.06.03 - Beau bouquet\\IMG_8565.xmp")
]
IMMICH_SID = get_file_owner_sid("\\\\[REDACTED]\\photo\\2020.06 - Guadeloupe\\Téléphone\\20200624_063419.jpg.xmp")


def get_file_owner(filepath):
    owner_sid = get_file_owner_sid(filepath)
    if owner_sid in DIGIKAM_SID:
        source = "digiKam"
    elif owner_sid == IMMICH_SID:
        source = "Immich"
    else:
        source = "Unknown"
    return source

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
            xmp_owner TEXT,
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
                    INSERT INTO xmp_files (
                        file_name,
                        file_path,
                        base_name,
                        xmp_type,
                        xmp_modified_time,
                        xmp_owner
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (filename, xmp_path, base_name, xmp_type, stat.st_mtime, get_file_owner(xmp_path)))
                count += 1
                
                # Log and commit every 250 files
                if count % 250 == 0:
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