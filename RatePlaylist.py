import connexion
from plexapi.server import PlexServer

plex = PlexServer(connexion.baseurl, connexion.token)
