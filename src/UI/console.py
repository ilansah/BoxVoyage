from core.auth import AuthManager
from core.places import PlaceManager
from data.storage import JsonStorage


def display_menu_login():
    print("\n=== BoxVoyage ===")
    print("1. S'inscrire")
    print("2. Se connecter")
    print("3. Quitter")


def display_menu_tours(tours):
    print(f"\n=== Mes Voyages ({len(tours)}) ===")
    if tours:
        for i, tour in enumerate(tours, 1):
            nb_places = len(tour.places)
            print(f"  {i}. {tour.name} ({nb_places} villes)")
    print(f"\n  N. Créer un nouveau voyage")
    print(f"  Q. Se déconnecter")


def display_menu_in_tour(tour):
    print(f"\n=== Voyage: {tour.name} ===")
    print(f"Villes: {len(tour.places)}")
    print("\n1. Ajouter une ville")
    print("2. Voir les villes du voyage")
    print("3. Supprimer une ville")
    print("4. Lancer l'algorithme optimal")
    print("5. Retour aux voyages")


def optimize_tour_order(places):
    """Réorganise les villes pour trouver un ordre optimal (nearest neighbor)."""
    if len(places) <= 1:
        return places
    
    from src.core.algorithm import GeoPoint
    
    # Convertir les dicts en objets Place si nécessaire
    from src.core.places import Place
    place_objs = []
    for p in places:
        if isinstance(p, dict):
            place_objs.append(Place(p["name"], GeoPoint(p["lat"], p["lon"]), p["owner"]))
        else:
            place_objs.append(p)
    
    # Nearest neighbor: commencer par le premier, puis ajouter le plus proche
    ordered = [place_objs[0]]
    remaining = set(range(1, len(place_objs)))
    
    while remaining:
        last = ordered[-1]
        nearest_idx = min(remaining, 
                         key=lambda i: DistanceCalculator.distance(last.point, place_objs[i].point))
        ordered.append(place_objs[nearest_idx])
        remaining.remove(nearest_idx)
    
    # Retourner en format dict
    return [p.to_dict() for p in ordered]


def main():
    storage_users = JsonStorage("dataBase/users.json")
    storage_places = JsonStorage("dataBase/places.json")
    storage_tours = JsonStorage("dataBase/tours.json")
    
    auth = AuthManager(storage_users)
    place_manager = None
    tour_manager = None
    
    selected_tour = None
    
    while True:
        # ============ MENU LOGIN ============
        if auth.get_current_user() is None:
            display_menu_login()
            choice = input("\nChoix: ").strip().lower()
            
            if choice == "1":
                username = input("Username: ")
                password = input("Password: ")
                try:
                    auth.register(username, password)
                    print("✓ Inscrit!")
                except Exception as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "2":
                username = input("Username: ")
                password = input("Password: ")
                try:
                    auth.login(username, password)
                    print(f"✓ Bienvenue {username}!")
                    place_manager = PlaceManager(storage_places, username)
                    tour_manager = TourManager(storage_tours, username)
                except Exception as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "3":
                print("Au revoir!")
                break
            else:
                print("Option invalide")
        
        # ============ MENU VOYAGES ============
        elif selected_tour is None:
            user = auth.get_current_user()
            tours = tour_manager.list_tours()
            
            display_menu_tours(tours)
            choice = input(f"\nChoix (1-{len(tours)} / N / Q): ").strip().lower()
            
            if choice == "q":
                auth.logout()
                print("✓ Déconnexion réussie")
            
            elif choice == "n":
                tour_name = input("Nom du voyage: ")
                try:
                    tour = tour_manager.create_tour(tour_name, [])
                    selected_tour = tour
                    print(f"✓ Voyage '{tour_name}' créé!")
                except Exception as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(tours):
                    selected_tour = tours[idx]
                    print(f"✓ Voyage sélectionné: {selected_tour.name}")
                else:
                    print("✗ Choix invalide")
            
            else:
                print("Option invalide")
        
        # ============ MENU DANS UN VOYAGE ============
        else:
            display_menu_in_tour(selected_tour)
            choice = input("\nChoix: ").strip()
            
            if choice == "1":
                # Ajouter une ville
                print("\nAjouter une ville au voyage:")
                city_name = input("Nom de la ville (ou adresse): ")
                try:
                    # Utiliser le geocoding SANS ajouter à la liste personnelle
                    place = place_manager.geocode_place(city_name)
                    if place:
                        # Ajouter au tour
                        tour_manager.add_place_to_tour(selected_tour.id, place)
                        selected_tour.places.append(place.to_dict())
                        print(f"✓ {place.name} ajouté au voyage!")
                    else:
                        print("✗ Ville non trouvée")
                except Exception as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "2":
                # Voir les villes du voyage
                if selected_tour.places:
                    print(f"\nVilles du voyage '{selected_tour.name}':")
                    for i, place in enumerate(selected_tour.places, 1):
                        print(f"  {i}. {place['name']}")
                else:
                    print("Le voyage est vide")
            
            elif choice == "3":
                # Supprimer une ville
                if not selected_tour.places:
                    print("✗ Le voyage est vide")
                else:
                    print(f"\nVilles du voyage:")
                    for i, place in enumerate(selected_tour.places, 1):
                        print(f"  {i}. {place['name']}")
                    idx_str = input("Numéro de la ville à supprimer: ")
                    if idx_str.isdigit():
                        idx = int(idx_str) - 1
                        if 0 <= idx < len(selected_tour.places):
                            removed = selected_tour.places.pop(idx)
                            tour_manager.update_tour_places(selected_tour.id, selected_tour.places)
                            print(f"✓ {removed['name']} supprimé du voyage")
                        else:
                            print("✗ Numéro invalide")
            
            elif choice == "4":
                # Lancer l'algorithme optimal
                if len(selected_tour.places) < 2:
                    print("✗ Il faut au moins 2 villes pour optimiser")
                else:
                    print(f"\n⏳ Optimisation du voyage...")
                    optimized = optimize_tour_order(selected_tour.places)
                    selected_tour.places = optimized
                    tour_manager.update_tour_places(selected_tour.id, optimized)
                    
                    # Calculer la distance totale
                    from src.core.places import Place
                    from src.core.algorithm import GeoPoint
                    place_objs = [Place(p["name"], GeoPoint(p["lat"], p["lon"]), p["owner"]) 
                                 for p in optimized]
                    
                    total_dist = 0.0
                    print(f"\n✓ Voyage optimisé:")
                    for i, place in enumerate(place_objs, 1):
                        if i > 1:
                            dist = DistanceCalculator.distance(place_objs[i-2].point, place.point)
                            total_dist += dist
                            print(f"  {i}. {place.name} (+{dist:.1f} km)")
                        else:
                            print(f"  {i}. {place.name}")
                    print(f"\nDistance totale: {total_dist:.1f} km")
            
            elif choice == "5":
                # Retour aux voyages
                selected_tour = None
            
            else:
                print("Option invalide")

if __name__ == "__main__":
    main()
