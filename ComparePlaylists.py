import Connexion
from plexapi.server import PlexServer


########################################
## Paramètres à modifier 
########################################

playlist1Name = "2024.03 - Chine"
playlist2Name = "2024.03 - Chine +"

########################################




plex = PlexServer(Connexion.baseurl, Connexion.token)


playlist1 = plex.playlist(playlist1Name)
playlist2 = plex.playlist(playlist2Name)

for photo1 in playlist1.items():
  match=False
  for photo2 in playlist2.items():
    if (photo2.guid == photo1.guid):
      match=True
      continue
  if(not match):
    print("Photo {photoTitle} dans la playlist {play1} non trouvée dans la playlist {play2}".format(photoTitle=photo1.title, play1=playlist1Name, play2=playlist2Name))


for photo2 in playlist2.items():
  match=False
  for photo1 in playlist1.items():
    if (photo1.guid == photo2.guid):
      match=True
      continue
  if(not match):
    print("Photo {photoTitle} dans la playlist {play2} non trouvée dans la playlist {play1}".format(photoTitle=photo1.title, play1=playlist1Name, play2=playlist2Name))
