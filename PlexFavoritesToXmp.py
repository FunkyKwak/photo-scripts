import Connexion
import PlexHelper
import metadataLib
from plexapi.server import PlexServer



plex = PlexServer(Connexion.baseurl, Connexion.token)




# Sélectionne ta bibliothèque de photos
photo_library = plex.library.section('Photos')  # nom de ta section photos

all_items = list(PlexHelper.iter_all_media(photo_library))
scanned_items = 0
total_items = len(all_items)
print(f"Total media items to scan: {total_items}")

print(f"=========================================")
print(f"Title,Plex Rating,Metadata Rating,Message")
for item in all_items:

    # Avancement de la boucle
    scanned_items = scanned_items + 1
    if scanned_items % 1000 == 0:
        print(f"...{scanned_items} photos scanned, over {total_items}...")

    # Vérifie si la photo a une certaine notation
    if item.userRating is not None:
        plex_rating = round(item.userRating/2)

        photo_path = PlexHelper.get_file_path(item)
        metaRating = metadataLib.get_rating(photo_path)

        print(f"{item.title},{plex_rating},{metaRating},", end="")

        if metaRating is None:
            metaRating = 0
        
        if plex_rating > metaRating:
            print(f"⚠ Différence détectée ! ", end="")
            metadataLib.set_xmp_rating(photo_path, plex_rating)
        elif plex_rating == metaRating:
            print(f"Already set")
        elif plex_rating < metaRating:
            print(f"Already higher than Plex rating")
        else:
            print(f"")

print(f"=========================================")

print(f"Finished ! {scanned_items} photos scanned")
