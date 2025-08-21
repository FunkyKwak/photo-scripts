import ImmichHelper

# Récupère la liste des uuids des assets avec un rating 5 étoiles
best_not_favorited_ids = ImmichHelper.get_asset_info(info="id", isFavorite=False, rating=5)

# Met toutes ces assets en favoris
ImmichHelper.set_favorite(best_not_favorited_ids)