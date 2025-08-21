import requests
import json
import os
import logging
from dotenv import load_dotenv

# charge les variables du fichier .env si présent (secret github sinon)
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


base_url = os.environ["IMMICH_BASE_URL"]
api_key = os.environ["IMMICH_API_KEY"]




def get_asset_info(info, **filters) -> list[str]:
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': api_key
    }
    page = 1
    size = int(filters.pop("size", 1000))  # max 1000 selon la doc
    returns = []

    while True:
        payload = {"page": page, "size": size, **filters}
        r = requests.post(f"{base_url}/api/search/metadata", json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()

        assets = data.get("assets", [])
        #print(assets["items"][0].keys())
        #print(assets["items"][0])

        returns.extend(a[info] for a in assets["items"])

        # arrêt si on a tout récupéré ou s'il n'y a plus de page suivante
        next_page = assets.get("nextPage")
        if next_page is None:
            next_page = 0
        else:
            next_page = int(next_page)

        if next_page <= page:
            break

        # nextPage peut être une chaîne, donc on essaie de la convertir
        try:
            page = int(next_page)
        except (TypeError, ValueError):
            page += 1

    logging.info(f"J'ai récupéré {len(returns)} assets")
    
    return returns

## Unit test
best_not_favorited_ids = get_asset_info(info="id", isFavorite=False, rating=5)
print(f"J'ai récupéré {len(best_not_favorited_ids)} assets")
print(best_not_favorited_ids[:10])  # affiche les 10 premiers UUID

best_not_favorited_ids = get_asset_info(info="originalPath", isFavorite=True, originalFileName="IMG_2525.JPG")
print(f"J'ai récupéré {len(best_not_favorited_ids)} assets")
print(best_not_favorited_ids[:10])  # affiche les 10 premiers UUID


def set_favorite(uuids):

    payload = json.dumps({
    "ids": uuids,
    "isFavorite": True
    })
    headers = {
    'Content-Type': 'application/json',
    'x-api-key': api_key
    }

    resp = requests.request("PUT", f"{base_url}/api/assets", headers=headers, data=payload)

    if resp.status_code == 204:
        logging.info(f"Succès : update effectué sur {len(uuids)} assets")
        print(f"::notice::Job terminé avec succès – {len(uuids)} assets passées en favoris")
    else:
        logging.error("Erreur :", resp.status_code, resp.text)
        print(f"::error::Méthode set_favorite a retourné le code erreur {resp.status_code}, message dans les logs")

    print(resp.text)


## Unit test
#set_favorite(["8a34c963-4075-4f0b-b49a-e9f870055784", "07673d4a-a3e1-4d1c-aa10-0812ff95e1da"])
