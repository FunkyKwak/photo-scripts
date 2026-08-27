import os
import shutil
from pathlib import Path

source_dir = "R:\\Google Takeout\\"
dest_dir = "R:\\Google Takeout\\_modifiés"

# Créer le répertoire destination s'il n'existe pas
os.makedirs(dest_dir, exist_ok=True)

# Parcourir tous les fichiers et sous-répertoires
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # Vérifier si le nom du fichier se termine par "modifié"
        if Path(file).stem.endswith("-modifié"):
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, file)
            
            # Déplacer le fichier
            shutil.move(src_path, dest_path)
            print(f"Déplacé: {src_path} → {dest_path}")

print("Terminé!")