# BoxVoyage

Application de gestion des lieux de voyage avec calcul de distances géographiques et optimisation de trajets.

## Installation

```bash
pip install -r requirements.txt
```

## Démarrage

```bash
python main.py
```

## Fonctionnalités

- **S'inscrire** : Créer un compte utilisateur
- **Se connecter** : Accéder à votre profil sécurisé
- **Ajouter un lieu** : Enregistrer une destination avec ses coordonnées GPS
- **Voir mes lieux** : Consulter tous vos lieux sauvegardés
- **Supprimer un lieu** : Supprimer une destination
- **Calcul de distances** : Distance réelle entre deux points (formule Haversine)

## Architecture

### 3 Couches

```
┌─────────────────────────────┐
│  UI (console.py)            │
├─────────────────────────────┤
│  Core (auth, places, algo)  │
├─────────────────────────────┤
│  Data (storage.py)          │
└─────────────────────────────┘
```

### Modules

| Module | Responsabilité |
|--------|-----------------|
| `core/auth.py` | Authentification et gestion utilisateurs |
| `core/places.py` | Gestion des lieux et géocodage |
| `core/algorithm.py` | Calculs géographiques (distance, tours) |
| `data/storage.py` | Sauvegarde en JSON |
| `ui/console.py` | Interface utilisateur |

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

**Couverture :** 23 tests (algorithm, auth, places)

## Structure

```
src/
  core/      # Logique métier
  data/      # Persistance
  ui/        # Interface
tests/       # Tests unitaires
dataBase/    # Données JSON
```

## Sécurité

- Mots de passe hashés (SHA256)
- Isolation des données par utilisateur
- Validation des entrées

## Technologies

- Python 3.10+
- geopy (géocodage Nominatim)
- unittest (tests)
- JSON (base de données)