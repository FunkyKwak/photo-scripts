import os
import sqlite3
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import datetime
import time

DB_FILE = "GooglePhotos\\photo_inventory.db"

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".heic"}
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv"}
BATCH_SIZE = 1000  # commit tous les 1000 fichiers

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA synchronous=NORMAL;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        filename TEXT,
        size INTEGER,
        date_taken TEXT,
        path TEXT,
        UNIQUE(source, path)
    )
    """)
    conn.commit()
    return conn, cur

def get_exif_date(path):
    try:
        with Image.open(path) as img:
            exif = img._getexif()
            if not exif:
                return None
            for tag, value in exif.items():
                if TAGS.get(tag, tag) == "DateTimeOriginal":
                    return value
    except:
        return None
    return None

def get_file_date(path):
    timestamp = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(timestamp).isoformat()

def process_folder(root_path, source_name):
    conn, cur = init_db()
    count = 0
    start_time = time.time()
    total_files = sum(len(files) for _, _, files in os.walk(root_path))
    processed_files = 0
    print(f"{processed_files}/{total_files} fichiers traités")

    for root, _, files in os.walk(root_path):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in IMAGE_EXT and ext not in VIDEO_EXT:
                continue

            full_path = os.path.join(root, file)

            try:
                size = os.path.getsize(full_path)

                date_taken = None
                if ext in IMAGE_EXT:
                    date_taken = get_exif_date(full_path)
                if not date_taken:
                    date_taken = get_file_date(full_path)

                # Insert en ignorant les doublons déjà présents
                cur.execute("""
                    INSERT OR IGNORE INTO files (source, filename, size, date_taken, path)
                    VALUES (?, ?, ?, ?, ?)
                """, (source_name, file, size, date_taken, full_path))

                count += 1
                processed_files += 1

                if count >= BATCH_SIZE:
                    conn.commit()
                    count = 0
                    elapsed = time.time() - start_time
                    speed = processed_files / elapsed
                    remaining = (total_files - processed_files) / speed
                    print(f"{processed_files}/{total_files} fichiers traités "
                          f"({speed:.1f}/s), ~{remaining/60:.1f} min restants")

            except Exception as e:
                print(f"Erreur sur {full_path}: {e}")

    # Commit final
    conn.commit()
    conn.close()
    print(f"Traitement de {source_name} terminé, {processed_files} fichiers analysés.")

if __name__ == "__main__":

    print("Extraction Google Takeout...")
    #process_folder("F:\\TEMP\\Takeout", "google")

    print("Extraction NAS...")
#    process_folder("P:\\", "nas")
    process_folder("S:\\", "syncthings")

    print("Inventaire terminé.")
