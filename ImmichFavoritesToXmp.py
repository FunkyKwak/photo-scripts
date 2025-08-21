import ImmichHelper
import metadataLib
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# Récupère la liste des uuids des assets favoris avec un rating 5 étoiles
favorited_paths = ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=-1)
favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=0))
favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=1))
favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=2))
favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=3))
favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=4))
#favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=''))
#favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=5))
#favorited_paths.extend(ImmichHelper.get_asset_info(info="originalPath", isFavorite=True))

# On dirait que les photos sans rating ne remonte dans aucun des filtres : 





nb_total = len(favorited_paths)
logging.info(f"{nb_total} favorite assets without a 5 stars rating")

nb_ok = 0
nb_ko = 0
for favorited_path in favorited_paths :
    favorited_path = "//[REDACTED]/" + favorited_path
    # if (metadataLib.set_xmp_rating(favorited_path, 5)):
    #     nb_ok = nb_ok + 1
    # else:
    #     nb_ko = nb_ko + 1


if (nb_ko == 0):
    print(f"::notice::Job terminé avec succès – {nb_ok} assets favoris marqués 5 étoiles")
else:
    print(f"::error::Impossible de mettre à jour le rating pour {nb_ko} fichiers sur {nb_total}, plus de détails dans les logs")
