from src.core.auth import AuthManager
from src.core.places import PlaceManager
from src.data.storage import JsonStorage

def main():
    storage_users = JsonStorage("dataBase/users.json")
    storage_places = JsonStorage("dataBase/places.json")
    auth = AuthManager(storage_users)
    place_manager = None
    
    while True:
        if auth.get_current_user() is None:
            # Menu non connecté
            print("\n1. S'inscrire")
            print("2. Se connecter")
            print("3. Quitter")
            choice = input("Choix: ")
            
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
                    print(f"✓ Bonjour {username}!")
                    place_manager = PlaceManager(storage_places, username)
                except Exception as e:
                    print(f"✗ Erreur: {e}")
            
            elif choice == "3":
                print("Au revoir!")
                break
            else:
                print("Option invalide")
        else:
            # Menu connecté
            user = auth.get_current_user()
            print(f"\nBonjour {user.username}!")
            print("1. Ajouter un lieu")
            print("2. Voir mes lieux")
            print("3. Supprimer un lieu")
            print("4. Se déconnecter")
            choice = input("Choix: ")
            
            if choice == "1":
                name = input("Nom du lieu: ")
                place = place_manager.search_and_add(name)
                if place:
                    print(f"✓ {place.name} ajouté!")
            
            elif choice == "2":
                places = place_manager.list_places()
                if places:
                    print("\nVos lieux:")
                    for i, place in enumerate(places, 1):
                        print(f"  {i}. {place.name} ({place.point.lat}, {place.point.lon})")
                else:
                    print("Vous n'avez pas de lieux")
            
            elif choice == "3":
                name = input("Nom du lieu à supprimer: ")
                if place_manager.remove_place(name):
                    print(f"✓ {name} supprimé!")
                else:
                    print(f"✗ {name} non trouvé")
            
            elif choice == "4":
                auth.logout()
                print("✓ Déconnexion réussie")
            
            else:
                print("Option invalide")

if __name__ == "__main__":
    main()
