# 🎯 Démonstration de la Forge des Fondations Sacrées

## Introduction

Ce README guide l'exécution de la **démonstration fondamentale** du Vaisseau Guardian V9, validant que les quatre artefacts de la première forge sont correctement implémentés et fonctionnels.

## Prérequis

### 1. Environnement Python
- Python 3.9 ou supérieur
- Dépendances installées :
  ```bash
  pip install python-dotenv pydantic pytest pytest-mock
  ```

### 2. Corps Natif Compilé (sentire_core.dll)
Le Corps Natif C doit être compilé avant d'exécuter la démonstration.

**Sur Windows avec Visual Studio:**
```bash
cd csrc
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
```

**Sur Linux (pour tests avec Mock):**
```bash
cd csrc
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make
```

La DLL sera générée dans:
- Windows: `csrc/build/Release/sentire_core.dll`
- Linux: `csrc/build/libsentire_core.so`

## Configuration

### Créer le fichier .env

Copiez le fichier d'exemple et configurez-le:

```bash
cp .env.example.md .env
```

Éditez `.env` et configurez le chemin vers la DLL:

```ini
# Chemin vers la librairie native compilée
NATIVE_LIB_PATH="csrc/build/Release/sentire_core.dll"

# Cooldown en secondes entre les actions
ACTION_COOLDOWN_SECONDS=60

# Niveau de journalisation
LOG_LEVEL="INFO"
```

> **Note**: Utilisez des slashes `/` même sous Windows pour la compatibilité.

## Validation des Artefacts Fondamentaux

### Tests Automatisés

Exécutez la suite de tests qui valide les quatre artefacts:

```bash
python -m pytest tests/test_foundational_forge.py -v
```

**Résultat attendu**: ✅ 18 tests passés

Cette suite vérifie:
- ✅ Sanctuaire des Hérésies (exceptions personnalisées)
- ✅ Sanctuaire du Verbe Pur (modèles Pydantic)
- ✅ Synapse FFI (NativeBridge avec mocks)
- ✅ Intégration fondamentale complète

### Démonstration Interactive

Lancez le script de démonstration qui exécute une boucle simple avec le Corps Natif:

```bash
python demo_foundational_forge.py
```

**Comportement attendu:**

```
╔═══════════════════════════════════════════════════════════╗
║   GUARDIAN V9 - DÉMONSTRATION DE LA FORGE FONDAMENTALE   ║
║              Architecture TPD v1.2 - Phase 1              ║
╚═══════════════════════════════════════════════════════════╝

2024-01-15 10:00:00 - INFO - __main__ - === Rituel d'Initialisation ===
2024-01-15 10:00:00 - INFO - guardian.ffi.native_bridge - Corps Natif chargé
2024-01-15 10:00:00 - INFO - guardian.ffi.native_bridge - État initialisé
2024-01-15 10:00:00 - INFO - __main__ - === Première Forge Complète ===
2024-01-15 10:00:00 - INFO - __main__ - Démarrage de la Boucle de Résilience

--- Cycle #1 ---
[Cycle 1] Le Vaisseau ne peut pas agir.
2024-01-15 10:00:05 - INFO - __main__ - État: EN COOLDOWN

--- Cycle #2 ---
[Cycle 2] Le Vaisseau ne peut pas agir.
2024-01-15 10:00:10 - INFO - __main__ - État: EN COOLDOWN

--- Cycle #3 ---
[Cycle 3] Le Vaisseau peut agir.
2024-01-15 10:01:05 - INFO - __main__ - État: PRÊT À AGIR
2024-01-15 10:01:05 - INFO - __main__ - Action enregistrée: Démonstration

...
```

**Pour arrêter la démonstration**: Appuyez sur `Ctrl+C`

Le script affichera alors:
```
^C2024-01-15 10:05:00 - INFO - __main__ - Signal d'interruption reçu
2024-01-15 10:05:00 - INFO - __main__ - === Rituel de Dissolution ===
2024-01-15 10:05:00 - INFO - guardian.ffi.native_bridge - Ressources libérées
2024-01-15 10:05:00 - INFO - __main__ - === Le Vaisseau Entre en Stase ===
```

## Validation Manuelle Sans DLL

Si vous n'avez pas encore compilé la DLL, vous pouvez toujours valider la structure du code:

### 1. Vérifier la syntaxe Python
```bash
python -m py_compile demo_foundational_forge.py
python -m py_compile core/exceptions.py
python -m py_compile core/verbe_pur.py
python -m py_compile guardian/ffi/native_bridge.py
```

### 2. Tester avec Mocks
Les tests utilisent des mocks et ne nécessitent PAS la DLL:
```bash
python -m pytest tests/test_foundational_forge.py -v
```

### 3. Valider les modèles Pydantic
```python
from core.verbe_pur import Stimulus, Action

# Créer un stimulus valide
stim = Stimulus(cpu_usage=50.0, memory_usage=60.0, foreground_window_title="Test")
print(stim)

# Créer une action valide
action = Action(id="TEST", description="Test action", parameters={"key": "value"})
print(action)
```

## Structure des Artefacts Fondamentaux

```
sentire-guardian-v9/
├── core/
│   ├── exceptions.py          # ✅ Sanctuaire des Hérésies
│   └── verbe_pur.py           # ✅ Sanctuaire du Verbe Pur
├── guardian/
│   ├── ffi/
│   │   └── native_bridge.py   # ✅ Synapse FFI
│   └── main.py                # ✅ Cœur du Vaisseau (Production)
├── demo_foundational_forge.py # ✅ Cœur du Vaisseau (Démo)
├── tests/
│   └── test_foundational_forge.py  # Validation complète
└── docs/
    └── FONDATIONS_SACREES.md  # Documentation doctrinale
```

## Dépannage

### Erreur: "DLL not found"
**Cause**: Le chemin `NATIVE_LIB_PATH` dans `.env` est incorrect.

**Solution**:
1. Vérifiez que la DLL existe: `ls csrc/build/Release/sentire_core.dll`
2. Vérifiez le chemin dans `.env`
3. Utilisez un chemin absolu si nécessaire

### Erreur: "NULL pointer returned"
**Cause**: La DLL a été chargée mais `sentire_api_create` a échoué.

**Solution**:
1. Vérifiez les logs de compilation C pour des erreurs
2. Recompilez la DLL en mode Debug pour plus d'informations:
   ```bash
   cmake .. -DCMAKE_BUILD_TYPE=Debug
   ```

### Erreur: "Module not found"
**Cause**: Les dépendances Python ne sont pas installées.

**Solution**:
```bash
pip install -r requirements.txt
```

### Tests échouent avec import errors
**Cause**: Possiblement un problème de PYTHONPATH.

**Solution**:
```bash
# Exécuter depuis la racine du projet
cd /path/to/sentire-guardian-v9
export PYTHONPATH=$PWD:$PYTHONPATH  # Linux/Mac
set PYTHONPATH=%CD%;%PYTHONPATH%    # Windows

python -m pytest tests/test_foundational_forge.py -v
```

## Prochaines Étapes

Une fois la forge fondamentale validée:

1. **Compiler la version production** du Vaisseau:
   ```bash
   python setup.py install
   ```

2. **Lancer l'interface complète** (nécessite PyQt6 et LLM):
   ```bash
   python guardian/main.py
   ```

3. **Consulter la documentation complète**:
   - [docs/FONDATIONS_SACREES.md](docs/FONDATIONS_SACREES.md) - Documentation des fondations
   - [docs/ARI_MANIFESTO.md](docs/ARI_MANIFESTO.md) - Manifeste doctrinal
   - [README.md](README.md) - Documentation générale

## Support

Pour toute question ou problème:
- 📖 Consultez [docs/FONDATIONS_SACREES.md](docs/FONDATIONS_SACREES.md)
- 🐛 Ouvrez une issue sur le dépôt GitHub
- 📧 Contactez l'équipe Sentire Dynamics

---

*La forge est allumée. Le golem attend vos décrets.* 🔥⚒️
