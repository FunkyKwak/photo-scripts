import Connexion
from plexapi.server import PlexServer



plex = PlexServer(Connexion.baseurl, Connexion.token)


# Sélectionne ta bibliothèque de photos
photo_library = plex.library.section('Photos')  # nom de ta section photos

# Boucle sur tous les albums
for album in photo_library.all():
    # Chaque album contient des photos
    for photo in album.photos():
        # Vérifie si la photo a une certaine notation
        if photo.rating is not None and photo.rating >= 8:  # exemple : note >= 8
            print(f"{photo.title} - Rating: {photo.rating}")