from tkinter import messagebox
import matplotlib.pyplot as plt
from Helpers import DigikamHelper, metadataLib



def create_chart(results):
    """
    Crée et affiche le graphique.
    """

    if not results:
        messagebox.showinfo(
            "Aucun résultat",
            "Le dossier ne contient aucun sous-répertoire."
        )
        return

    # Tri décroissant du nombre de photos 5 étoiles.
    results = sorted(
        results,
        key=lambda item: item["name"],
        reverse=False
    )

    names = [
        item["name"]
        for item in results
    ]

    counts = [
        item["count"]
        for item in results
    ]

    # Hauteur adaptée au nombre de répertoires.
    height = max(
        5,
        len(results) * 0.55
    )

    fig, ax = plt.subplots(
        figsize=(12, height)
    )

    bars = ax.barh(
        names,
        counts
    )

    # Le plus grand en haut.
    ax.invert_yaxis()

    ax.set_title(
        f"Photos 5 étoiles",
        fontsize=16,
        pad=15
    )

    ax.set_xlabel(
        "Nombre de photos avec XMP:Rating = 5"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.3
    )

    # Affiche la valeur à droite de chaque barre.
    max_count = max(counts, default=0)

    for bar, value in zip(bars, counts):

        # Petit espace après la barre.
        offset = max_count * 0.01 if max_count else 0.1

        ax.text(
            bar.get_width() + offset,
            bar.get_y() + bar.get_height() / 2,
            str(value),
            va="center"
        )

    plt.tight_layout()

    # Enregistre automatiquement le graphique.
    output_file = "photos_5_etoiles.png"

    fig.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight"
    )

    print()
    print(f"Graphique enregistré :")
    print(output_file)
    print()

    plt.show()


def main():

    print("=== Photos 5 étoiles — digiKam ===")
    print()

    database_path = metadataLib.config.get("digikam_database")

    print(f"Base digiKam : {database_path}")

    print()
    print("Analyse de la base digiKam...")

    try:

        results = DigikamHelper.get_five_star_counts(
            database_path=database_path,
            excluded_dirs=metadataLib.config.get("excluded_dirs", [])
        )

    except Exception as error:

        messagebox.showerror(
            "Erreur",
            str(error)
        )

        return

    print()

    for result in results:

        print(
            f"{result['name']}: "
            f"{result['count']} photos 5★"
        )

    print()

    create_chart(results)


if __name__ == "__main__":
    main()