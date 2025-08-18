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
    #print(item.title, item.TYPE)   # TYPE is 'photo' or 'clip'
    scanned_items = scanned_items + 1
    plex_rating = item.userRating

    # Avancement de la boucle
    if scanned_items % 1000 == 0:
        print(f"...{scanned_items} photos scanned, over {total_items}...")

    # Vérifie si la photo a une certaine notation
    if plex_rating is not None:
        metaRating = metadataLib.get_rating(PlexHelper.get_file_path(item))

        if plex_rating != metaRating:
            message = "⚠ Différence détectée !"
        else:
            message = ""
        print(f"{item.title},{plex_rating},{metaRating},{message}")

print(f"=========================================")

print(f"Finished ! {scanned_items} photos scanned")
