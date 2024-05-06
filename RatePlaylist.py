import connexion
from plexapi.server import PlexServer


########################################
## Paramètres à modifier 
########################################

playlistName = "2024.03 - Chine"
rating = 6.0 # sur 10, en float

########################################




plex = PlexServer(connexion.baseurl, connexion.token)

playlist = plex.playlist(playlistName)
foreach(photo in playlist.items()):
  print(photo.title)
  #photo.rate(rating)
