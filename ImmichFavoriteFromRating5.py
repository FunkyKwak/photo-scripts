import ImmichHelper

# Récupère la liste des uuids des assets avec un rating 5 étoiles
best_not_favorited_ids = ImmichHelper.get_asset_uuids(isFavorite=False, rating=5)
print(f"J'ai récupéré {len(best_not_favorited_ids)} assets")

# Met toutes ces assets en favoris
ImmichHelper.set_favorite(best_not_favorited_ids)