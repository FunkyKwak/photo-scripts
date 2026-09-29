from tkinter import messagebox
import matplotlib.pyplot as plt
from Helpers import DigikamHelper, metadataLib



def create_chart(results):
    results = sorted(
        results,
        key=lambda item: item["name"],
        reverse=False
    )

    # Hauteur proportionnelle au nombre de répertoires
    height_per_directory = 0.25
    min_height = 6

    height = max(
        min_height,
        len(results) * height_per_directory
    )

    fig, ax = plt.subplots(
        figsize=(12, height)
    )

    names = [item["name"] for item in results]
    counts = [item["count"] for item in results]

    bars = ax.barh(names, counts)

    ax.invert_yaxis()

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f" {count}",
            va="center"
        )

    ax.set_xlabel("Photos 5★")
    ax.set_ylabel("Répertoire")
    ax.set_title("Photos 5★ par répertoire")

    plt.tight_layout()

    plt.savefig(
        "photos_5_etoiles.png",
        dpi=150,
        bbox_inches="tight"
    )


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