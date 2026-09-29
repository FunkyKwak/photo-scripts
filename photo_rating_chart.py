import json
import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt

from Helpers import metadataLib


import os
from pathlib import Path


def get_photo_files(folder):
    extensions = (
        set(metadataLib.config["photo_extensions"])
        | set(metadataLib.config["raw_extensions"])
        | set(metadataLib.config["video_extensions"])
    )

    files = []

    for root, dirs, filenames in os.walk(folder):
        # Empêche os.walk() d'entrer dans les répertoires exclus
        dirs[:] = [
            d for d in dirs
            if d not in metadataLib.config["excluded_dirs"]
        ]

        for filename in filenames:
            path = Path(root) / filename

            if path.suffix.lower() in extensions:
                files.append(path)

    return files


def count_five_star_photos(files):
    """
    Utilise ExifTool pour récupérer XMP:Rating.

    Retourne le nombre de photos ayant exactement Rating = 5.
    """

    if not files:
        return 0

    count = 0

    # On traite les fichiers par lots afin d'éviter une commande
    # gigantesque avec une très grosse photothèque.
    batch_size = 500

    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]

        command = [
            metadataLib.exiftool,
            "-XMP:Rating",
            "-j",
            "-n",
            *[str(file) for file in batch],
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )

        if result.returncode != 0:
            print("Erreur ExifTool :")
            print(result.stderr)
            continue

        try:
            metadata = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("Impossible de lire la sortie JSON d'ExifTool.")
            continue

        for photo in metadata:
            rating = photo.get("Rating")

            try:
                if float(rating) == 5:
                    count += 1
            except (TypeError, ValueError):
                pass

    return count


def analyze_folder(root_folder):
    """
    Analyse les sous-dossiers directs du dossier racine.

    Chaque ligne du graphique représente un sous-dossier direct,
    mais le comptage est récursif.
    """

    directories = [
        path
        for path in root_folder.iterdir()
        if path.is_dir()
    ]

    if not directories:
        messagebox.showinfo(
            "Aucun sous-dossier",
            "Le dossier sélectionné ne contient aucun sous-dossier."
        )
        return []

    results = []

    for index, directory in enumerate(sorted(directories), start=1):
        if (directory.name in metadataLib.config["excluded_dirs"]):
            continue


        print(f"[{index}/{len(directories)}] Analyse de : {directory.name}")

        photos = get_photo_files(directory)

        print(f"    {len(photos)} photos trouvées")

        five_stars = count_five_star_photos(photos)

        print(f"    {five_stars} photos 5★")

        results.append(
            {
                "name": directory.name,
                "count": five_stars,
                "total": len(photos),
            }
        )

    return results


def create_chart(results, root_folder):
    """
    Génère et affiche le graphique.
    """

    # Tri décroissant par nombre de photos 5 étoiles.
    results = sorted(
        results,
        key=lambda x: x["count"],
        reverse=True,
    )

    names = [item["name"] for item in results]
    counts = [item["count"] for item in results]

    # Hauteur adaptée au nombre de répertoires.
    height = max(5, len(results) * 0.55)

    fig, ax = plt.subplots(figsize=(12, height))

    bars = ax.barh(names, counts)

    # Le plus grand en haut.
    ax.invert_yaxis()

    ax.set_title(
        f"Photos 5 étoiles — {root_folder.name}",
        fontsize=16,
        pad=15,
    )

    ax.set_xlabel("Nombre de photos avec XMP:Rating = 5")

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3,
    )

    # Affichage de la valeur au bout de chaque barre.
    for bar, value in zip(bars, counts):
        ax.text(
            bar.get_width() + max(counts, default=1) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            str(value),
            va="center",
        )

    plt.tight_layout()

    # Sauvegarde automatique à côté du dossier analysé.
    output_file = root_folder / "photos_5_etoiles.png"

    fig.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight",
    )

    print()
    print(f"Graphique enregistré :")
    print(output_file)

    plt.show()


def main():
    print("=== Photos 5 étoiles ===")
    print()

    # Fenêtre de sélection du dossier.
    root = tk.Tk()
    root.withdraw()

    selected_folder = filedialog.askdirectory(
        title="Sélectionne le dossier racine de ta photothèque"
    )

    root.destroy()

    if not selected_folder:
        return

    root_folder = Path(selected_folder)

    print(f"Dossier sélectionné : {root_folder}")
    print()

    results = analyze_folder(root_folder)

    if not results:
        return

    create_chart(results, root_folder)


if __name__ == "__main__":
    main()
