import sqlite3
import os

# Configuration
DB_PATH = "XmpFixer\\xmp_inventory.db"

def rename_xmp_files():
    """Rename XMP files by removing the file_ext part from filenames."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch all records from digikam_xmp table
        cursor.execute("SELECT id, file_name, file_path FROM digikam_xmp")
        records = cursor.fetchall()
        
        for record_id, file_name, file_path in records:
            # Remove the middle file_ext part (name.ext.xmp -> name.xmp)
            if file_name.endswith('.xmp'):
                parts = file_name.rsplit('.', 2)  # Split from right: ['name', 'ext', 'xmp']
                if len(parts) == 3:
                    new_name = f"{parts[0]}.xmp"
                    
                    old_path = file_path
                    new_path = file_path.replace(file_name, new_name)
                    
                    if os.path.exists(old_path):
                        if os.path.exists(new_path):
                            print(f"⚠️  Target file already exists, skipping: {new_path}")
                            continue

                        os.rename(old_path, new_path)
                        #print(f"✓ Renamed: {file_name} -> {new_name}")
                        
                        # Update database
                        cursor.execute("UPDATE digikam_xmp SET renamed_xmp_file = ? WHERE id = ?", 
                                     (new_name, record_id))
                    else:
                        print(f"✗ File not found: {file_name}")
        
        conn.commit()
        conn.close()
        print("\nRenaming completed!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    rename_xmp_files()