import sqlite3
from pathlib import Path


def _get_connection(database_path):
    database_path = Path(database_path)

    if not database_path.exists():
        raise FileNotFoundError(
            f"Base digiKam introuvable : {database_path}"
        )

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA query_only = ON")

    return connection


def _normalize_path(path):
    path = str(path)
    path = path.replace("/", "\\")
    path = path.rstrip("\\")
    return path.casefold()


def _get_albums(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            Albums.id,
            Albums.albumRoot,
            AlbumRoots.specificPath,
            Albums.relativePath
        FROM Albums
        INNER JOIN AlbumRoots
            ON Albums.albumRoot = AlbumRoots.id
    """)

    albums = []

    for album_id, album_root, specific_path, relative_path in cursor.fetchall():
        if not specific_path:
            continue

        relative_path = str(relative_path or "").replace("\\", "/")
        relative_path = relative_path.strip("/")

        if relative_path:
            parts = relative_path.split("/")
            top_level = parts[0]
        else:
            # L'album racine lui-même n'a pas de niveau supérieur.
            top_level = None

        albums.append({
            "id": album_id,
            "album_root": album_root,
            "specific_path": specific_path,
            "relative_path": relative_path,
            "top_level": top_level,
        })

    return albums


def _get_five_star_count_by_album(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            Images.album,
            COUNT(*)
        FROM Images
        INNER JOIN ImageInformation
            ON Images.id = ImageInformation.imageid
        WHERE
            Images.status = 1
            AND ImageInformation.rating = 5
        GROUP BY Images.album
    """)

    return {
        album_id: count
        for album_id, count in cursor.fetchall()
    }


def get_five_star_counts(database_path, excluded_dirs=None):
    excluded_dirs = {
        name.casefold()
        for name in (excluded_dirs or [])
    }

    connection = _get_connection(database_path)

    try:
        albums = _get_albums(connection)
        five_star_by_album = _get_five_star_count_by_album(connection)
    finally:
        connection.close()

    results = {}

    for album in albums:
        top_level = album["top_level"]

        if not top_level:
            continue

        if top_level.casefold() in excluded_dirs:
            continue

        count = five_star_by_album.get(album["id"], 0)

        #if count == 0:
        #    continue

        # On distingue les collections digiKam.
        key = (
            album["album_root"],
            top_level.casefold()
        )

        if key not in results:
            results[key] = {
                "name": top_level,
                "count": 0,
            }

        results[key]["count"] += count

    return sorted(
        results.values(),
        key=lambda item: item["name"].casefold()
    )