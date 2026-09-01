# Photo Scripts

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=microsoft" alt="Windows" />
  <img src="https://img.shields.io/badge/Status-Toolkit-4CAF50?style=for-the-badge" alt="Status" />
</div>

A personal toolkit for photo metadata automation, Plex synchronization, Immich workflows, and photo library inventory management.

This repository brings together a set of Python scripts designed to keep photo collections consistent across Plex, Immich, XMP sidecars, and local disk storage.

## Features

- Plex photo library :
  - Sync Plex ratings with local XMP metadata
  - Compare and clean up Plex playlists
- Immich favorite = XMP 5 stars rating :
  - Mark Immich assets as favorites based on rating rules
  - Apply ratings to Immich assets automatically
- Inventory photo folders into SQLite databases
- Detect duplicate XMP sidecars and naming inconsistencies
- Reuse SQL-based file selection for copying or organizing media

## Why this project exists

Managing a large personal photo library often means juggling several systems:

- Plex for browsing media (I previously used it to browse piictures, these scripts helped me to migrate to Immich)
- Immich for browsing pictures
- XMP sidecars for preserving metadata on disk
- Google Takeout or local folders for exported media archives

This project helps automate the repetitive tasks between those systems and keeps metadata aligned.

## Repository overview

### Core scripts

- Plex
  - [ComparePlaylists.py](ComparePlaylists.py): compares two Plex playlists and reports differences.
  - [RatePlaylist.py](RatePlaylist.py): applies a chosen rating to all photos in a Plex playlist.
  - [PlexFavoritesToXmp.py](PlexFavoritesToXmp.py): compares Plex ratings with XMP metadata and updates the sidecar when needed.
- Immich
    - [ImmichFavoriteFromRating5.py](ImmichFavoriteFromRating5.py): marks non-favorited assets with a 5-star rating as favorites.
    - [ImmichFavoritesToXmp.py](ImmichFavoritesToXmp.py): updates favorite assets that do not yet have a 5-star rating.
- Helpers/utility libs
  - [PlexHelper.py](PlexHelper.py): utility functions to traverse Plex albums and identify file paths.
  - [ImmichHelper.py](ImmichHelper.py): helper for querying and updating Immich assets via the API.
  - [metadataLib.py](metadataLib.py): reads and writes ratings with XMP and ExifTool support.
  - [SimpleLog.py](SimpleLog.py): lightweight logging wrapper for console, GitHub Actions, and Telegram output.

### Google Photos utilities

[![Obsolète → unique-photo-transfer](https://img.shields.io/badge/⚠%20Obsolète-Utiliser%20le%20projet%20unique--photo--transfer-orange)](https://github.com/FunkyKwak/unique-photo-transfer)

- [GooglePhotos/ListPhotoToSQLite.py](GooglePhotos/ListPhotoToSQLite.py): scans a folder tree and indexes files in SQLite.
- [GooglePhotos/CopyFilesFromSQLiteQuery.py](GooglePhotos/CopyFilesFromSQLiteQuery.py): copies files based on SQL query results.
- [GooglePhotos/MoveModifiéInSubFolder.py](GooglePhotos/MoveModifiéInSubFolder.py): reorganizes modified files into a dedicated subfolder.

### XMP tooling

- [XmpFixer/ListXmpToSQLite.py](XmpFixer/ListXmpToSQLite.py): inventories XMP sidecars in a SQLite database.
- [XmpFixer/RenameExtToStdXmp.py](XmpFixer/RenameExtToStdXmp.py): renames XMP files from xxx.ext.xmp to xxx.xmp.
- [XmpFixer/RenameStdToExtXmp.py](XmpFixer/RenameStdToExtXmp.py): renames XMP files from xxx.xmp to xxx.ext.xmp.
- [XmpFixer/ListDuplicateXmpToSQLite.py](XmpFixer/ListDuplicateXmpToSQLite.py): finds duplicate XMP sidecar pairs. [![Obsolète → Faire une simple requête SQL](https://img.shields.io/badge/⚠%20Obsolète-Faire%20une%20simple%20requête%20SQL-orange)](XmpFixer/exiftool_cmd.sql)


## Quick start

### Prerequisites

- Python 3.10+
- pip installed
- Windows-oriented local setup for the scripts that rely on file paths and Plex access

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

#### Plex

Create a local `Connexion.py` file in the project root:

```python
baseurl = "http://localhost:32400"
token = "YOUR_PLEX_TOKEN"
```

#### Immich

Create a `.env` file in the project root:

```env
IMMICH_BASE_URL=https://your-immich-instance
IMMICH_API_KEY=your_api_key
```

#### ExifTool

Some metadata operations rely on ExifTool and require a valid local binary path in [metadataLib.py](metadataLib.py).

## Typical workflows

### 1) Sync Plex ratings to XMP

Use [PlexFavoritesToXmp.py](PlexFavoritesToXmp.py) to keep Plex ratings aligned with the metadata written to the photo files.

### 2) Rate a Plex playlist

Edit the settings in [RatePlaylist.py](RatePlaylist.py):

```python
playlistName = "2024.03 - China"
rating = 6.0
```

Run:

```bash
python RatePlaylist.py
```

### 3) Compare two playlists

Edit the settings in [ComparePlaylists.py](ComparePlaylists.py):

```python
playlist1Name = "2024.03 - China"
playlist2Name = "2024.03 - China +"
```

Run:

```bash
python ComparePlaylists.py
```

### 4) Automate Immich favorites or ratings

```bash
python ImmichFavoriteFromRating5.py
python ImmichFavoritesToXmp.py
```

### 5) Inventory XMP files

```bash
python XmpFixer/ListXmpToSQLite.py
```

When prompted, enter the folder to scan.

## GitHub Actions automation for Immich

This repository includes a scheduled workflow at [.github/workflows/immich_daily.yml](.github/workflows/immich_daily.yml) that runs every night at 02:00 UTC.

It automates the two daily Immich jobs:

1. mark non-favorited assets with a 5-star rating as favorites
2. set a 5-star rating on favorite assets that do not already have it

### What the workflow does

The workflow:

- checks out the repository
- installs Python dependencies
- runs [ImmichFavoriteFromRating5.py](ImmichFavoriteFromRating5.py)
- runs [ImmichFavoritesToXmp.py](ImmichFavoritesToXmp.py)

This is useful if you want a simple, hands-off nightly sync for your own Immich instance.

### Secrets to add in your fork

In your GitHub repository, go to Settings → Secrets and variables → Actions and add:

- `IMMICH_BASE_URL`: your Immich URL, for example `https://photos.example.com`
- `IMMICH_API_KEY`: a valid API key with access to your library
- `TELEGRAM_TOKEN`: optional, if you want Telegram notifications
- `TELEGRAM_CHAT_ID`: optional, if you want Telegram notifications

You do not need to change the Python code for this to work in your fork; the workflow reads those values from GitHub secrets.

### How to use it in your own fork

1. Fork this repository.
2. Go to the GitHub Actions tab.
3. Enable workflows if needed.
4. Add the secrets listed above.
5. Save the workflow and let it run on schedule, or trigger it manually with `workflow_dispatch`.

### Example workflow schedule

The cron is currently:

```yaml
cron: '0 2 * * *'
```

If you want a different time, edit the schedule in [.github/workflows/immich_daily.yml](.github/workflows/immich_daily.yml).

This is designed so people can fork the repo, keep the same automation logic, and plug in their own Immich instance and GitHub secrets without modifying the scripts themselves.

## Important notes

- This repository is built around a personal local workflow and may require manual path adjustments.
- The Plex scripts expect valid local credentials and a reachable server.
- XMP-sidecar operations can affect metadata on real files, so backups are strongly recommended.
- Some scripts process very large libraries and may take a while to complete.

## Best practices

- Test on a small subset before running on a full library.
- Backup media before renaming or moving sidecars.
- Verify the ExifTool path before production jobs.
- Keep secrets like Immich tokens in a local `.env` file, not in version control.
- Prefer a dry run or small sample before bulk operations.

## Project structure

```text
photo-scripts/
├── ComparePlaylists.py
├── ImmichFavoriteFromRating5.py
├── ImmichFavoritesToXmp.py
├── ImmichHelper.py
├── metadataLib.py
├── PlexFavoritesToXmp.py
├── PlexHelper.py
├── RatePlaylist.py
├── README.md
├── requirements.txt
├── SimpleLog.py
├── GooglePhotos/
│   ├── CompareQueries.sql
│   ├── CopyFilesFromSQLiteQuery.py
│   ├── ListPhotoToSQLite.py
│   └── MoveModifiéInSubFolder.py
└── XmpFixer/
    ├── exiftool_cmd.sql
    ├── ListDuplicateXmpToSQLite.py
    ├── ListXmpToSQLite.py
    ├── RenameExtToStdXmp.py
    └── RenameStdToExtXmp.py
```

## License and status

This project is a personal automation toolkit and is intended for local, self-managed use. It is not a production SaaS application and may evolve depending on your personal workflow.

## Future improvements

- standardize naming and logging conventions across scripts
- add a centralized CLI runner
- move configuration into dedicated config files
- improve safety checks for path handling and metadata writes
- document each script in more detail with arguments and expected outputs

