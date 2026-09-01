import ImmichHelper
import SimpleLog
import metadataLib
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# Récupère la liste des uuids des assets favoris avec un rating 5 étoiles
favorited = ImmichHelper.get_asset_info(info="id", isFavorite=True)
favorited_5s = ImmichHelper.get_asset_info(info="id", isFavorite=True, rating=5)

logging.info(f"{len(favorited)} favorite assets in total")
logging.info(f"{len(favorited_5s)} favorite assets with a 5 stars rating")

to_rate5 = list(set(favorited) - set(favorited_5s))

nb_total = len(to_rate5)
logging.info(f"{nb_total} favorite assets without a 5 stars rating")

nb_ok = 0
nb_ko = 0
for asset_id in to_rate5 :
    if (ImmichHelper.set_rating(asset_id, 5).type == "SUCCESS"):
        nb_ok = nb_ok + 1
    else:
        nb_ko = nb_ko + 1


# Envoi de log
s = ""
if (nb_ko == 0):
    if nb_ok > 1:
        s = "s"
    print(f"::notice::Job terminé avec succès – {nb_ok} asset{s} favori{s} marqué{s} 5 étoiles")
    if (nb_ok > 0):
        SimpleLog.send_telegram_message(f"{nb_ok} asset{s} favori{s} marqué{s} 5 étoiles")
    if (nb_ok == 6):
        asset_ids = ','.join(to_rate5)
        print(f"::debug::Liste des ID traités : {asset_ids}")
else:
    if nb_ko > 1:
        s = "s"
    print(f"::error::Impossible de mettre à jour le rating pour {nb_ko} fichier{s} sur {nb_total}, plus de détails dans les logs")
    SimpleLog.send_telegram_message(f"Impossible de mettre à jour le rating pour {nb_ko} fichier{s} sur {nb_total}, plus de détails dans les logs")
