import connexion
from plexapi.server import PlexServer

plex = PlexServer(connexion.baseurl, connexion.token)

playlist = plex.playlist("2024.03 - Chine")

foreach(photo in playlist.items()):
  print(photo.title)
  #photo.rate(6.0)
