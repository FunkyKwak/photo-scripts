import os
import xml.etree.ElementTree as ET
import subprocess
import json
from pathlib import Path


def load_config():
    config_file = Path(__file__).parent / "../config.json"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Fichier de configuration introuvable : {config_file}"
        )

    with config_file.open("r", encoding="utf-8") as file:
        return json.load(file)

config = load_config()

def find_exiftool():
    exiftool_path = Path(config["exiftool_path"])

    # Si le chemin est relatif, il est relatif au dossier du programme.
    if not exiftool_path.is_absolute():
        exiftool_path = Path(__file__).parent / exiftool_path

    if not exiftool_path.exists():
        raise FileNotFoundError(
            f"ExifTool introuvable : {exiftool_path}"
        )

    return str(exiftool_path)


exiftool = find_exiftool()


def get_rating(photo_path):
    """
    Récupère la notation depuis le fichier XMP associé,
    ou depuis les métadonnées EXIF si pas de XMP.
    Retourne None si aucune note trouvée.
    """
    base, _ = os.path.splitext(photo_path)
    xmp_file = base + ".xmp"

    # 1) Vérifier si un fichier XMP existe
    if os.path.exists(xmp_file):
        try:
            tree = ET.parse(xmp_file)
            root = tree.getroot()
            for elem in root.iter():
                if 'Rating' in elem.tag:
                    try:
                        return int(elem.text)
                    except:
                        return None
        except Exception as e:
            print(f"Erreur lecture {xmp_file}: {e}")

    # 2) Sinon, lire directement dans les métadonnées du fichier image avec ExifTool
    try:
        # ExifTool doit être installé sur la machine
        result = subprocess.run(
            [exiftool,
            "-Rating", "-XMP:Rating", "-xmp:Label", photo_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        output = result.stdout.strip()

        # Exemple de sortie: "Rating : 4"
        for line in output.splitlines():
            if "Rating" in line:
                try:
                    return int(line.split(":")[1].strip())
                except:
                    pass
    except Exception as e:
        print(f"Erreur lecture EXIF pour {photo_path}: {e}")

    return None



def set_xmp_rating(photo_path, rating):
    """
    Write rating to XMP sidecar for photo_path.
    Creates the .xmp if missing.
    """
    try:
        result = subprocess.run(
            [
                exiftool,
                "-overwrite_original",
                f"-Rating={rating}",
                "-o", "%d%f.xmp",
                photo_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        if result.returncode != 0:
            print(f"ExifTool error on {photo_path}: {result.stderr}")
            return False
        else:
            print(f"Updated rating {rating} for {photo_path}")
            return True
    except Exception as e:
        print(f"Failed to update {photo_path}: {e}")
        return False
