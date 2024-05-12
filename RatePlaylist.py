import Connexion
from plexapi.server import PlexServer


########################################
## Paramètres à modifier 
########################################

playlistName = "2024.03 - Chine"
rating = 6.0 # sur 10, en float

########################################




plex = PlexServer(Connexion.baseurl, Connexion.token)

playlists = plex.playlists(playlistType='photo', title=playlistName)
for playlist in playlists:
  if (not playlist.smart):
    print("Start rating {playlistName} ({n} photos)".format(playlistName=playlist.title, n=playlist.leafCount))
    for photo in playlist.items():
      print("\n - {photoTitle} (rating {photoRating})".format(photoTitle=photo.title, photoRating=photo.userRating), end="")
      if (photo.userRating == None or photo.userRating < rating):
        print(" ==> update rating to {tgtRating} !".format(tgtRating=rating), end="")
        photo.rate(rating)
  else:
    print("Ignored smart playlist {playlistName}".format(playlistName=playlist.title))
