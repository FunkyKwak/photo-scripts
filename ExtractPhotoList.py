import os
import sqlite3
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import datetime

DB_FILE = "photo_inventory.db"

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".heic"}
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv"}


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        filename TEXT,
        size INTEGER,
        date_taken TEXT,
        path TEXT
    )
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_source ON files(source)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_filename ON files(filename)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_size ON files(size)")

    conn.commit()
    return conn


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


def extract_to_db(root_path, source_name):
    conn = init_db()
    cur = conn.cursor()

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

                cur.execute("""
                    INSERT INTO files (source, filename, size, date_taken, path)
                    VALUES (?, ?, ?, ?, ?)
                """, (source_name, file, size, date_taken, full_path))

            except Exception as e:
                print(f"Erreur sur {full_path}: {e}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    #print("Extraction Google...")
    #extract_to_db("F:\\TEMP\\Takeout", "google")

    print("Extraction NAS...")
    extract_to_db("P:\\", "nas")

    print("Terminé.")