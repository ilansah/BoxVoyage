from src.core.auth import AuthManager
from src.core.places import PlaceManager
from src.core.tours import TourManager
from src.core.algorithm import DistanceCalculator, GeoPoint, TourOptimiszer
from src.data.storage import JsonStorage


def display_menu_login():
    print("\n=== BoxVoyage ===")
    print("1. S'inscrire")
    print("2. Se connecter")
    print("3. Quitter")


def display_menu_tours():
    print(f"\n=== Mes Voyages ===")
    print("1. Voir les voyages")
    print("2. Ajouter un voyage")
    print("3. Supprimer un voyage")
    print("Q. Se déconnecter")


def display_menu_in_tour(tour):
    print(f"\n=== Voyage: {tour.name} ===")
    print(f"Villes: {len(tour.places)}")
    print("\n1. Ajouter une ville")
    print("2. Voir les villes du voyage")
    print("3. Supprimer une ville")
    print("4. Lancer l'algorithme optimal")
    print("5. Retour aux voyages")


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
            
            display_menu_tours()
            choice = input("\nChoix: ").strip().lower()
            
            if choice == "q":
                auth.logout()
                print("✓ Déconnexion réussie")
            
            elif choice == "1":
                # Voir les voyages
                if tours:
                    print(f"\n=== Voir mes voyages ({len(tours)}) ===")
                    for i, tour in enumerate(tours, 1):
                        nb_places = len(tour.places)
                        print(f"  {i}. {tour.name} ({nb_places} villes)")
                    idx_str = input("\nSélectionner un voyage (numéro): ")
                    if idx_str.isdigit():
                        idx = int(idx_str) - 1
                        if 0 <= idx < len(tours):
                            selected_tour = tours[idx]
                            print(f"✓ Voyage sélectionné: {selected_tour.name}")
                        else:
                            print("✗ Numéro invalide")
                else:
                    print("✗ Vous n'avez pas de voyage")
            
            elif choice == "2":
                # Ajouter un voyage
                tour_name = input("Nom du voyage: ")
                try:
                    tour = tour_manager.create_tour(tour_name, [])
                    selected_tour = tour
                    print(f"✓ Voyage '{tour_name}' créé!")
                except Exception as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "3":
                # Supprimer un voyage
                if tours:
                    print(f"\n=== Supprimer un voyage ({len(tours)}) ===")
                    for i, tour in enumerate(tours, 1):
                        nb_places = len(tour.places)
                        print(f"  {i}. {tour.name} ({nb_places} villes)")
                    idx_str = input("\nSélectionner un voyage à supprimer (numéro): ")
                    if idx_str.isdigit():
                        idx = int(idx_str) - 1
                        if 0 <= idx < len(tours):
                            tour_to_delete = tours[idx]
                            tour_manager.delete_tour(tour_to_delete.id)
                            print(f"✓ Voyage '{tour_to_delete.name}' supprimé!")
                        else:
                            print("✗ Numéro invalide")
                else:
                    print("✗ Vous n'avez pas de voyage")
            
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
                        added = tour_manager.add_place_to_tour(selected_tour.id, place)
                        if added:
                            selected_tour.places.append(place.to_dict())
                            print(f"✓ {place.name} ajouté au voyage!")
                        else:
                            print(f"✗ {place.name} est déjà dans ce voyage")
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
                    
                    # Utiliser la méthode qui fait tous les calculs
                    result = TourOptimiszer.optimize_places_with_distances(selected_tour.places)
                    
                    # Mettre à jour le tour avec les places optimisées
                    selected_tour.places = result['optimized_places']
                    tour_manager.update_tour_places(selected_tour.id, result['optimized_places'])
                    
                    # Afficher les résultats
                    print(f"\n✓ Voyage optimisé:")
                    for i, segment in enumerate(result['segments']):
                        if i == 0:
                            print(f"  {i+1}. {segment['to']}")
                        else:
                            if segment.get('is_return'):
                                print(f"  → Retour à {segment['to']} (+{segment['distance']:.1f} km)")
                            else:
                                print(f"  {i+1}. {segment['to']} (+{segment['distance']:.1f} km)")
                    
                    print(f"\nDistance totale: {result['total_distance']:.1f} km")
            
            elif choice == "5":
                # Retour aux voyages
                selected_tour = None
            
            else:
                print("Option invalide")

if __name__ == "__main__":
    main()
