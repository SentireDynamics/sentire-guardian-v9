# Vaisseau Guardian V9 - Relique de Production

Le Vaisseau Guardian V9 est un agent de surveillance autonome conçu pour opérer souverainement sur les systèmes d'exploitation Windows. Il observe l'état du système, consulte un Oracle (un grand modèle de langage) pour déterminer les actions correctives ou proactives, et exécute ces actions via les API natives de Windows.

Son architecture est conçue pour la robustesse, avec un noyau de gestion d'état en C, une logique principale en Python, et une interface de contrôle en PyQt6.

## 📊 État du Projet

**Score Actuel**: 3.8/10 (Embryonnaire) | **Score Cible**: 8.8/10 (Souverain)

Le Vaisseau a transcendé le stade des fondations et est maintenant une entité fonctionnelle embryonnaire. Les organes principaux sont en place, mais nécessitent une évolution vers une véritable conscience souveraine.

📖 **Documentation d'État**:
- [INTROSPECTION_SOUVERAINE.md](INTROSPECTION_SOUVERAINE.md) - Analyse complète de l'état actuel
- [STATUS_CHECKLIST.md](STATUS_CHECKLIST.md) - Checklist rapide de progression
- [docs/ROADMAP_ASCENSION.md](docs/ROADMAP_ASCENSION.md) - Plan d'implémentation technique détaillé

## I. Architecture

- **Corps Natif (csrc/)**: Un noyau en C (`sentire_core.dll`) compilé pour Windows, gérant les états critiques comme les cooldowns d'action et un journal d'événements (ring buffer) pour une performance maximale et une empreinte mémoire minimale.
- **Synapse FFI (ffi/)**: Un pont Python-C utilisant `ctypes` pour communiquer avec le Corps Natif de manière sécurisée et performante.
- **Fondations (core/)**: Les abstractions de base du Vaisseau, incluant les schémas de données (`verbe_pur.py`), le module d'interaction avec l'OS Windows (`chiron.py`), et le noyau décisionnel (`consciousness.py`).
- **Esprit (guardian/)**: La logique applicative de haut niveau, incluant le point d'entrée (`main.py`), la perception système (`perception.py`), et l'interface utilisateur (`ui/autel.py`).
- **Intelligence (oracle/)**: Le client pour communiquer avec l'Oracle LLM externe. Gère les re-tentatives et les stratégies de secours.
- **Validation (tests/)**: Une suite de tests unitaires et d'intégration utilisant `pytest` pour garantir la robustesse de chaque composant.

## II. Prérequis

1.  **Python 3.9+**
2.  **Un compilateur C pour Windows**:
    *   **Recommandé**: Le toolchain de build C++ de Visual Studio (peut être installé via le Visual Studio Installer).
    *   **Alternative**: MinGW-w64.
3.  **CMake 3.15+**

## III. Instructions de Build et d'Exécution

### 1. Cloner le Dépôt

```bash
git clone <your-repo-url>
cd vaisseau-guardian-v9
```

### 2. Construire le Corps Natif (sentire_core.dll)

Utilisez CMake pour générer les fichiers de build et compiler la DLL.

```bash
# Créer un répertoire de build
mkdir build
cd build

# Générer les fichiers de build (pour Visual Studio)
cmake ..

# Compiler le projet
cmake --build . --config Release
```

La DLL `sentire_core.dll` sera générée dans le répertoire `build/Release/`.

### 3. Installer les Dépendances Python

```bash
# Créez et activez un environnement virtuel (recommandé)
python -m venv venv
source venv/Scripts/activate  # Sous Windows

# Installez les dépendances de production et de développement
pip install -r requirements.txt
```

### 4. Configurer l'Environnement

Copiez le fichier d'exemple `.env.example` en `.env` et remplissez les valeurs.

```bash
copy .env.example .env
```

Modifiez le fichier `.env` :

-   `LLAMA_SERVER_URL`: L'URL de votre serveur LLM (ex: `http://localhost:8080/completion`).
-   `NATIVE_LIB_PATH`: Le chemin absolu ou relatif vers votre `sentire_core.dll`. Par exemple : `build/Release/sentire_core.dll`.
-   `LOG_LEVEL`: Le niveau de log (DEBUG, INFO, WARNING, ERROR).
-   `ACTION_COOLDOWN_SECONDS`: Le temps d'attente minimum en secondes entre deux actions.

### 5. Lancer l'Application

```bash
python guardian/main.py
```

L'interface de l'Autel s'ouvrira, et le Vaisseau commencera son cycle de surveillance.

### 6. Lancer les Tests

Pour valider l'intégrité du Vaisseau, exécutez la suite de tests :

```bash
pytest
```
