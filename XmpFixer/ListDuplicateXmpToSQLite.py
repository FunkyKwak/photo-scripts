import os
import sqlite3
from pathlib import Path
from collections import defaultdict

def find_duplicate_xmp_pairs(directory):
    """Parcourt le répertoire et identifie les paires de fichiers XMP doublons dans le même répertoire"""
    pairs = []
    total_standard = 0
    total_digikam = 0
    total_xmp_found = 0
    
    # Répertoires à exclure
    excluded_dirs = {'#recycle', '#snapshot', '.dtrash'}
    
    for root, dirs, files in os.walk(directory):
        # Exclure les répertoires indésirables
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        xmp_files = [f for f in files if f.endswith('.xmp')]
        total_xmp_found += len(xmp_files)
        
        # Log tous les 1000 fichiers XMP trouvés
        if total_xmp_found // 1000 > (total_xmp_found - len(xmp_files)) // 1000:
            print(f"Progression : {total_xmp_found} fichiers XMP trouvés...")
        
        # Grouper par nom de base
        grouped = defaultdict(list)
        for f in xmp_files:
            if f.count('.') == 1:  # format standard : nom.xmp
                base = f[:-4]
                grouped[base].append(('standard', f))
                total_standard += 1
            elif f.count('.') >= 2:  # format digikam : nom.ext.xmp
                base = f.rsplit('.', 2)[0]  # enlever .ext.xmp
                grouped[base].append(('digikam', f))
                total_digikam += 1
        
        # Pour chaque groupe avec exactement 2 fichiers (un standard et un digikam)
        for base, files in grouped.items():
            if len(files) == 2:
                file_types = [ft for ft, fn in files]
                if 'standard' in file_types and 'digikam' in file_types:
                    standard_file = next(fn for ft, fn in files if ft == 'standard')
                    digikam_file = next(fn for ft, fn in files if ft == 'digikam')
                    pairs.append({
                        'directory': root,
                        'base_name': base,
                        'standard_filename': standard_file,
                        'standard_path': os.path.join(root, standard_file),
                        'digikam_filename': digikam_file,
                        'digikam_path': os.path.join(root, digikam_file)
                    })
    
    return pairs, total_standard, total_digikam

def create_database(db_path):
    """Crée la base de données SQLite"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS xmp_duplicates (
            id INTEGER PRIMARY KEY,
            directory TEXT,
            base_name TEXT,
            standard_filename TEXT,
            standard_path TEXT,
            digikam_filename TEXT,
            digikam_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def insert_pairs(conn, pairs):
    """Insère les paires dans la base de données"""
    cursor = conn.cursor()
    for i, pair in enumerate(pairs, 1):
        cursor.execute('''
            INSERT INTO xmp_duplicates (directory, base_name, standard_filename, standard_path, digikam_filename, digikam_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pair['directory'], pair['base_name'], pair['standard_filename'], pair['standard_path'], pair['digikam_filename'], pair['digikam_path']))
        
        # Commit toutes les 1000 insertions
        if i % 1000 == 0:
            conn.commit()
            print(f"Progression insertion : {i} paires insérées...")
    
    # Commit final si nécessaire
    conn.commit()

def main():
    directory = input("Entrez le chemin du répertoire à analyser: ")
    db_path = "XmpFixer\\xmp_inventory.db"
    
    if not os.path.isdir(directory):
        print(f"Erreur: {directory} n'est pas un répertoire valide")
        return
    
    print("Recherche des paires de doublons XMP...")
    pairs, total_standard, total_digikam = find_duplicate_xmp_pairs(directory)
    
    print(f"Fichiers XMP trouvés : {total_standard} standard, {total_digikam} digikam")
    
    if not pairs:
        print("Aucune paire de doublons trouvée")
        return
    
    print(f"Trouvé {len(pairs)} paire(s) de doublons")
    
    conn = create_database(db_path)
    insert_pairs(conn, pairs)
    conn.close()
    
    print(f"Résultats insérés dans {db_path}")

if __name__ == '__main__':
    main()