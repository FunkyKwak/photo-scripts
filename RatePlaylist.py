import connexion
from plexapi.server import PlexServer


########################################
## Paramètres à modifier 
########################################

playlistName = "2024.03 - Chine"
rating = 6.0 # sur 10, en float

########################################




plex = PlexServer(connexion.baseurl, connexion.token)

playlists = plex.playlists(playlistType: "photo", title: playlistName)
foreach(playlist in playlists):
  if (not playlist.smart)
    print("Start rating " + playlist.title + " (" + playlist.leafCount + " photos)")
    foreach(photo in playlist.items()):
      print(photo.title + " (rating " + photo.userRating + ")")
      if (photo.userRating == None):
        print("update rating")
        #photo.rate(rating)
  else:
    print("Ignored smart playlist " + playlist.title)
