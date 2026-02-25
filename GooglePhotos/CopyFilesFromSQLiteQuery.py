import sqlite3
import shutil
import os
from pathlib import Path
import time

# ==============================
# CONFIGURATION
# ==============================

DB_FILE = "photo_inventory.db"

# Ta requête SQL ici :
SQL_QUERY = """
with approx as (
    SELECT
        google.id as google_id,
        (select nas_approx.id
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source = 'nas'
        LIMIT 1
        ) as nas_approx_id,
        (select count(distinct nas_approx.id)
        from files nas_approx
        WHERE google.filename = nas_approx.filename
        AND nas_approx.source = 'nas'
        ) as nas_approx_count
    FROM files google
    LEFT JOIN files nas_exact
        ON google.filename = nas_exact.filename
        AND google.date_taken = nas_exact.date_taken
        AND google.size <= nas_exact.size
        AND nas_exact.source = 'nas'
    WHERE google.source = 'google'
    AND nas_exact.id IS NULL
), googlenasdiff as (
    SELECT
        google.id as google_id, google.filename as google_filename, google.size as google_size, google.date_taken as google_date_taken, google.path as google_path,
        approx.nas_approx_count,
        nas.id    as nas_id   , nas.filename    as nas_filename   , nas.size    as nas_size   , nas.date_taken    as nas_date_taken   , nas.path as nas_path
    FROM approx
    LEFT JOIN files nas ON approx.nas_approx_id = nas.id
    INNER JOIN files google ON approx.google_id = google.id
)
select * 
from googlenasdiff
where nas_approx_count = 0
and google_path NOT LIKE '%\Archiver\%';
"""

# Racine d'origine (celle utilisée dans la base)
SOURCE_ROOT = "F:\\TEMP\\Takeout"

# Nouvelle racine de destination
DEST_ROOT = "F:\\TEMP\\Missings"

# ==============================


def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(SQL_QUERY)
    rows = cursor.fetchall()

    total = len(rows)
    print(f"{total} fichiers à copier.\n")

    start_time = time.time()

    for i, (source_path,) in enumerate(rows, 1):

        try:
            source_path = Path(source_path)

            # Construire le chemin relatif par rapport à SOURCE_ROOT
            relative_path = source_path.relative_to(SOURCE_ROOT)

            # Construire le nouveau chemin
            dest_path = Path(DEST_ROOT) / relative_path

            # Créer les dossiers si nécessaires
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copier le fichier (avec métadonnées)
            shutil.copy2(source_path, dest_path)

        except Exception as e:
            print(f"Erreur avec {source_path}: {e}")
            continue

        # Affichage progression
        if i % 100 == 0 or i == total:
            elapsed = time.time() - start_time
            speed = i / elapsed
            remaining = (total - i) / speed if speed > 0 else 0
            print(f"{i}/{total} copiés "
                  f"({speed:.1f}/s) - ~{remaining/60:.1f} min restantes")

    conn.close()
    print("\nCopie terminée.")


if __name__ == "__main__":
    main()