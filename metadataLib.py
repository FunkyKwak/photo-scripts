import os
import xml.etree.ElementTree as ET
import subprocess

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
            ["exiftool", "-Rating", "-XMP:Rating", "-xmp:Label", photo_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
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