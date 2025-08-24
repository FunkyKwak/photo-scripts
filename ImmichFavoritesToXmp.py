import ImmichHelper
import SimpleLog
import metadataLib
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# Récupère la liste des uuids des assets favoris avec un rating 5 étoiles
favorited_paths = ImmichHelper.get_asset_info(info="originalPath", isFavorite=True)
favorited_5s_paths = ImmichHelper.get_asset_info(info="originalPath", isFavorite=True, rating=5)

logging.info(f"{len(favorited_paths)} favorite assets in total")
logging.info(f"{len(favorited_5s_paths)} favorite assets with a 5 stars rating")

paths_to_rate5 = list(set(favorited_paths) - set(favorited_5s_paths))

nb_total = len(paths_to_rate5)
logging.info(f"{nb_total} favorite assets without a 5 stars rating")

nb_ok = 0
nb_ko = 0
for favorited_path in paths_to_rate5 :
    favorited_path = "//[REDACTED]/" + favorited_path
    favorited_path = favorited_path.replace("/", "\\")
    if (metadataLib.set_xmp_rating(favorited_path, 5)):
        nb_ok = nb_ok + 1
    else:
        nb_ko = nb_ko + 1



if (nb_ko == 0):
    print(f"::notice::Job terminé avec succès – {nb_ok} assets favoris marqués 5 étoiles")
    if (nb_ok > 0):
        SimpleLog.send_telegram_message(f"{nb_ok} assets favoris marqués 5 étoiles")
else:
    print(f"::error::Impossible de mettre à jour le rating pour {nb_ko} fichiers sur {nb_total}, plus de détails dans les logs")
    SimpleLog.send_telegram_message(f"Impossible de mettre à jour le rating pour {nb_ko} fichiers sur {nb_total}, plus de détails dans les logs")
