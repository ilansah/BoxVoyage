# test_manual.py — fichier temporaire, à supprimer après vérification

from src.core.algorithm import GeoPoint
from src.core.places import Place, GeocodingService
from src.data.storage import JsonStorage

print("=== GeoPoint ===")
tokyo = GeoPoint(lat=35.682, lon=139.762)
print(tokyo)
print(f"lat_rad: {tokyo.lat_rad:.6f}")  # attendu : 0.622837
print(f"lon_rad: {tokyo.lon_rad:.6f}")  # attendu : 2.439199

print("\n=== JsonStorage ===")
storage = JsonStorage("data/test_temp.json")
storage.save({"test": "ok", "valeur": 42})
data = storage.load()
print(data)  # attendu : {'test': 'ok', 'valeur': 42}

print("\n=== GeocodingService ===")
service = GeocodingService()
point = service.get_coordinates("Tokyo")
print(point)  # attendu : GeoPoint(lat=~35.68, lon=~139.76)

print("\n=== Place to_dict / from_dict ===")
place = Place(name="Tokyo", point=point, owner="alice")
d = place.to_dict()
print(d)
place2 = Place.from_dict(d)
print(place2)  # attendu : même nom, mêmes coordonnées
print(f"Aller-retour OK : {place.name == place2.name and place.point.lat == place2.point.lat}")