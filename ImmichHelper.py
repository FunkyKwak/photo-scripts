import requests
import json
import os


base_url = os.environ["IMMICH_BASE_URL"]
api_key = os.environ["IMMICH_API_KEY"]


def get_asset_uuids(**filters) -> list[str]:
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'x-api-key': api_key
    }
    page = 1
    size = int(filters.pop("size", 1000))  # max 1000 selon la doc
    uuids = []
    total = None

    while True:
        payload = {"page": page, "size": size, **filters}
        r = requests.post(f"{base_url}/api/search/metadata", json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()

        assets = data.get("assets", [])

        print(type(assets), assets.keys())
        #print(assets["items"][1]["id"])

        uuids.extend(a["id"] for a in assets["items"])

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

    return uuids

## Unit test
# best_not_favorited_ids = get_asset_uuids(isFavorite=False, rating=5)
# print(f"J'ai récupéré {len(best_not_favorited_ids)} assets")
# print(best_not_favorited_ids[:10])  # affiche les 10 premiers UUID


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
        print(f"Succès : update effectué sur {len(uuids)} assets")
    else:
        print("Erreur :", resp.status_code, resp.text)

    print(resp.text)


## Unit test
#set_favorite(["8a34c963-4075-4f0b-b49a-e9f870055784", "07673d4a-a3e1-4d1c-aa10-0812ff95e1da"])