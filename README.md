# BoxVoyage

Application de gestion des lieux de voyage avec calcul de distances géographiques et optimisation de trajets.

**Repository:** [github.com/ilansah/BoxVoyage](https://github.com/ilansah/BoxVoyage)

## Installation

### Prérequis
- Python 3.11+
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner ou télécharger le projet**
```bash
cd BoxVoyage
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

Cela va installer :
- `requests` — pour les appels HTTP
- `geopy` — pour le géocodage (convertir "Paris" → coordonnées GPS)

3. **Démarrer l'application**
```bash
python main.py
```

L'application affiche le menu principal

---

## Guide d'Utilisation

### 1. S'inscrire (Première fois)

Au démarrage, vous voyez :
```
=== BoxVoyage ===
1. S'inscrire
2. Se connecter
3. Quitter
```

**Tapez `1` pour créer votre compte :**
```
Nom d'utilisateur: alice
Mot de passe: monMotDePass123
✓ Inscription réussie !
```

→ Votre compte est créé. Vous devez maintenant **vous connecter**.

### 2. Se connecter

**Tapez `2` :**
```
Nom d'utilisateur: alice
Mot de passe: monMotDePass123
✓ Connexion réussie !
```

→ Vous arrivez au menu principal des voyages.

---

### 3. Ajouter des lieux (Destinations)

Menu principal :
```
=== Mes Voyages ===
1. Voir les voyages
2. Ajouter un voyage
3. Supprimer un voyage
Q. Se déconnecter
```

**Tapez `2` pour créer un voyage :**
```
Nom du voyage: Tour de France
Rendre public ? (O/N): N
```

→ Votre voyage est créé ! Maintenant ajoutez des lieux.

**Menu du voyage :**
```
Tour de France:
1. Ajouter un lieu
2. Voir les lieux
3. Optimiser le voyage
4. Voir les hôtels
5. Retour aux voyages
```

### 4. Ajouter un lieu au voyage

**Tapez `1` :**
```
Nom du lieu: Paris
```

**L'application géolocalise automatiquement :**
```
✓ Paris trouvé ! (Lat: 48.8566, Lon: 2.3522)
✓ Lieu ajouté au voyage
```

**Répétez avec d'autres villes :**
- Versailles
- Lyon
- Marseille

→ Elles sont sauvegardées automatiquement en JSON.

---

### 5. Voir vos lieux

**Tapez `2` :**
```
Lieux dans le voyage (4):
1. Paris (48.8566, 2.3522) - 343 km
2. Versailles (48.8049, 2.1204) - 15 km
3. Lyon (45.7640, 4.8357) - 391 km
4. Marseille (43.2965, 5.3698) - 660 km
```

→ Chaque lieu affiche :
- Ses coordonnées GPS
- Sa distance avec le lieu précédent

---

### 6. Optimiser votre voyage (Shortest Path)

**Tapez `3` :**

L'algorithme **Nearest Neighbor + 2-opt** calcule le meilleur ordre :

```
⏳ Optimisation du voyage...

✓ Voyage optimisé:
1. Paris
2. Versailles (+15 km)
3. Lyon (+391 km)
4. Marseille (+308 km)
→ Retour à Paris (+660 km)

Distance totale: 1374 km
```

**Avant optimisation :** Vous auriez pu faire Paris → Marseille → Versailles → Lyon = beaucoup plus long

**Après optimisation :** Paris → Versailles (proche) → Lyon → Marseille (retour) = moins cher en essence !

---

### 7. Utiliser les hôtels (Aller-Retours)

Si vous avez identifié un **hôtel** (ville avec ≥2 villes proches à <60km) :

**Tapez `4` :**

```
⏳ Recherche des hôtels...

✓ Hôtels trouvés:

PARIS (hôtel):
   • Versailles (15 km)
   • Fontainebleau (48 km)

LYON (hôtel):
   • Grenoble (102 km) — Trop loin !
```

**Votre itinéraire devient :**
```
Jour 1: Paris
Jour 2: Paris → Versailles → Paris (excursion)
Jour 3: Paris → Fontainebleau → Paris (excursion)
Jour 4: Paris → Lyon → Marseille → Paris (retour)
```

→ Vous restez à l'hôtel et faites des **excursions à la journée**

---

## Exemples Réels

### Exemple 1: Weekend à Paris

```
Voyage: "Weekend Découverte"
Lieux:
  • Paris
  • Versailles
  • Fontainebleau

Résultat optimisé:
  1. Paris (hôtel)
  2. Versailles (15 km)
  3. Fontainebleau (50 km)
  4. Retour Paris (60 km)
  
Total: 125 km (facile à pied/RER !)
```

### Exemple 2: Grand Tour Europe

```
Voyage: "Europe 2 semaines"
Lieux:
  • Paris
  • Lyon
  • Genève
  • Zurich
  • Munich
  • Vienne

Avant optimisation: 3200 km (trajet aléatoire)
Après optimisation: 2100 km (Nearest Neighbor)

Économies: 1100 km ≈ 90€ d'essence !
```

---

## Fonctionnalités Avancées

### Calcul de Distance

L'app utilise la **formule Haversine** (grande distance entre 2 points sur une sphère) :

```
Distance = R × arccos(sin(lat₁) × sin(lat₂) + cos(lat₁) × cos(lat₂) × cos(lon₂ - lon₁))
R = 6378.197 km (rayon Terre)
```

**C'est exact !** Pas une ligne droite sur une carte plate.

### Optimisation de Trajet

**Nearest Neighbor** :
- Complexité : O(n²)
- Résultat : tour optimal (ou très proche)
- Utilisé pour les GPS, drones, logistique

**2-opt (amélioration)** :
- Teste tous les échanges d'arêtes
- Complexité : O(n³)
- Réduit distance de 10-30%

---

## Données Sauvegardées

Tout est sauvegardé en **JSON** (pas de base de données complexe) :

### `dataBase/users.json`
```json
{
  "alice": {
    "password": "hash_sécurisé",
    "places": ["Paris", "Versailles"]
  }
}
```

### `dataBase/places.json`
```json
{
  "alice": [
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "owner": "alice"},
    {"name": "Versailles", "lat": 48.8049, "lon": 2.1204, "owner": "alice"}
  ]
}
```

→ **Simple, portable, sans serveur** ✓

---

## Architecture

### 3 Couches

```
┌─────────────────────────────┐
│  UI (console.py)            │  ← Ce que vous voyez
├─────────────────────────────┤
│  Core (auth, places, algo)  │  ← La logique (calculs)
├─────────────────────────────┤
│  Data (storage.py)          │  ← Sauvegarde (JSON)
└─────────────────────────────┘
```

### Modules

| Module | Responsabilité |
|--------|-----------------|
| `core/auth.py` | Inscription, connexion, authentification |
| `core/places.py` | Ajout/suppression de lieux, géocodage |
| `core/algorithm.py` | Distance, optimisation (Nearest Neighbor + 2-opt), hotels |
| `core/tours.py` | Création/gestion de voyages |
| `core/hotel.py` | Identification d'hôtels et excursions |
| `data/storage.py` | Lecture/écriture JSON |
| `ui/console.py` | Menus, affichage, interaction utilisateur |

---

## Dépannage

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