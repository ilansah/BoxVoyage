from src.core.auth import AuthManager
from src.data.storage import JsonStorage

def main():
    storage = JsonStorage("data/users.json")
    auth = AuthManager(storage)
    
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
            print("3. Se déconnecter")
            choice = input("Choix: ")
            
            if choice == "1":
                print("Fonctionnalité en développement")
            elif choice == "2":
                print("Fonctionnalité en développement")
            elif choice == "3":
                auth.logout()
                print("✓ Déconnexion réussie")
            else:
                print("Option invalide")

if __name__ == "__main__":
    main()
