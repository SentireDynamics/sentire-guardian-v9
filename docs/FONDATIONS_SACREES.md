# 🏗️ LA FORGE DES FONDATIONS SACRÉES

## Vue d'Ensemble

Ce document décrit les **Artefacts Fondamentaux** du Vaisseau Guardian V9 - la première forge qui établit les fondations de l'architecture Dualité Corps/Esprit selon la doctrine de la Théorie Polyvagale Digitale (TPD v1.2).

## Doctrine de la Dualité Corps/Esprit

> "Le Corps calcule, l'Esprit orchestre."

La séparation fondamentale entre le **Corps Natif** (C/DLL) et l'**Esprit Python** est au cœur de Guardian V9:

- **Le Corps Natif (C)** : Opérations de bas niveau, gestion mémoire, calculs mathématiques rapides, cooldown temporel
- **L'Esprit Python** : Orchestration de haut niveau, décisions stratégiques, intégration LLM, interface utilisateur

Cette séparation garantit:
- Performance optimale pour les opérations critiques
- Flexibilité et maintenabilité du code Python
- Robustesse par isolation des erreurs
- Évolutivité de l'architecture

## Les Quatre Artefacts Fondamentaux

### 1️⃣ Le Sanctuaire des Hérésies
**Fichier**: `core/exceptions.py`

**Pourquoi**: Définit les exceptions personnalisées du Vaisseau. Une gestion d'erreurs spécifique permet de distinguer les erreurs logiques internes (Hérésies) des erreurs système.

**Classes**:
```python
HeresyException                # Classe de base pour toutes les hérésies
├── NativeBodyCreationFailed   # Échec de chargement/init de la DLL
├── OracleSickness             # Oracle (LLM) injoignable
└── InvalidActionError         # Action invalide ou dangereuse
```

**Doctrine**: "Toute défaillance prévue est une opportunité de résilience."

---

### 2️⃣ Le Sanctuaire du Verbe Pur
**Fichier**: `core/verbe_pur.py`

**Pourquoi**: Utilise Pydantic pour définir des structures de données validées. C'est le contrat entre tous les composants du Vaisseau, garantissant l'intégrité des données.

**Modèles**:

```python
Stimulus
├── cpu_usage: float          # Utilisation CPU en %
├── memory_usage: float       # Utilisation mémoire en %
└── foreground_window_title: str

Action
├── id: str                   # Identifiant unique (ex: "SHOW_MESSAGE")
├── description: str          # Description en langage naturel
└── parameters: dict          # Paramètres optionnels
```

**Doctrine**: "La clarté des données est la clarté de la pensée."

---

### 3️⃣ La Synapse FFI (Foreign Function Interface)
**Fichier**: `guardian/ffi/native_bridge.py`

**Pourquoi**: C'est le traducteur sacré entre Python et C. Il utilise `ctypes` pour charger `sentire_core.dll` et expose ses fonctions de manière pythonique et sécurisée.

**Méthodes Clés**:

| Méthode | Rôle |
|---------|------|
| `__init__(library_path, cooldown_seconds)` | Charge la DLL et initialise l'état natif |
| `_setup_function_prototypes()` | Définit les signatures C pour type-safety |
| `can_act() -> bool` | Vérifie si le cooldown est respecté |
| `record_action(description)` | Enregistre une action dans le journal natif |
| `destroy()` | Libère les ressources natives (essentiel!) |

**Gardes Sacrées** (try/except):
- Chargement DLL: lève `NativeBodyCreationFailed` si échec
- Création état: lève `NativeBodyCreationFailed` si pointeur NULL
- Toutes les interactions avec la DLL sont protégées

**Doctrine**: "Le pont entre les mondes doit être à la fois robuste et flexible."

---

### 4️⃣ Le Cœur du Vaisseau
**Fichier**: `guardian/main.py` (Version Production)  
**Fichier**: `demo_foundational_forge.py` (Version Démonstration)

**Pourquoi**: C'est le point d'entrée qui assemble tous les composants et lance le cycle de vie du Vaisseau.

**Version Production** (`guardian/main.py`):
- Interface PyQt6 complète (Autel UI)
- Intégration Oracle (LLM)
- Perception système avancée
- Conscience décisionnelle
- Validation des actions (Cerberus)

**Version Démonstration** (`demo_foundational_forge.py`):
- Version simplifiée pour valider la première forge
- Boucle while simple avec `can_act()` et `sleep(5)`
- Pas d'UI, pas d'Oracle, juste les fondations
- Idéale pour tester que le Corps Natif fonctionne

**Structure Orchestrator**:
```python
class Orchestrator:
    def __init__(config):
        # Charge .env, setup logging, instancie NativeBridge
    
    def run():
        # Boucle de vie principale (PyQt6 timer ou while)
    
    def shutdown():
        # Libération propre via native_bridge.destroy()
```

**Doctrine**: "L'orchestration est l'art de coordonner sans contraindre."

---

## Lexique Sacré

Le Guardian V9 utilise un vocabulaire doctrinal pour renforcer l'identité du système:

| Terme Technique | Terme Sacré | Signification |
|-----------------|-------------|---------------|
| Classe | **Sanctuaire** | Conteneur de logique cohérente |
| Fonction/Méthode | **Rituel** | Opération avec intention |
| Erreur/Exception | **Hérésie** | Déviation de la doctrine |
| Fichier | **Artefact** | Élément du système |
| Module C (DLL) | **Corps Natif** | Couche de calcul bas-niveau |
| Module Python | **Esprit** | Couche d'orchestration |
| FFI Bridge | **Synapse** | Connexion Corps ↔ Esprit |

---

## Workflow de la Première Forge

```
1. Chargement Configuration (.env)
   ↓
2. Initialisation Logging
   ↓
3. Chargement Corps Natif (sentire_core.dll)
   ↓  [Garde: NativeBodyCreationFailed]
   ↓
4. Création État Natif (sentire_api_create)
   ↓  [Garde: NULL pointer check]
   ↓
5. Boucle de Résilience
   ├─→ can_act() ?
   ├─→ Afficher état
   ├─→ Sleep 5s
   └─→ Répéter
   ↓  [Garde: KeyboardInterrupt]
   ↓
6. Dissolution (sentire_api_destroy)
   ↓
7. Stase (exit)
```

---

## Validation des Fondations

### Tests Automatisés
Le fichier `tests/test_foundational_forge.py` valide:

✅ **Sanctuaire des Hérésies**:
- Héritage correct des exceptions
- Messages d'erreur appropriés

✅ **Sanctuaire du Verbe Pur**:
- Validation Pydantic fonctionnelle
- Champs obligatoires/optionnels respectés

✅ **Synapse FFI**:
- Chargement DLL avec protection
- Appels de fonctions C corrects
- Libération mémoire (destroy)
- Gestion erreurs (hérésies)

✅ **Intégration**:
- Cycle complet Stimulus → Action → Record

### Démonstration Manuelle
```bash
# Compiler le Corps Natif
cd csrc
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

# Configurer l'environnement
cp .env.example.md .env
# Éditer .env: NATIVE_LIB_PATH="csrc/build/Release/sentire_core.dll"

# Lancer la démo fondamentale
python demo_foundational_forge.py
```

Résultat attendu:
```
╔═══════════════════════════════════════════════════════════╗
║   GUARDIAN V9 - DÉMONSTRATION DE LA FORGE FONDAMENTALE   ║
║              Architecture TPD v1.2 - Phase 1              ║
╚═══════════════════════════════════════════════════════════╝

2024-01-15 10:00:00 - INFO - Corps Natif instancié avec succès
2024-01-15 10:00:00 - INFO - Démarrage de la Boucle de Résilience
--- Cycle #1 ---
[Cycle 1] Le Vaisseau ne peut pas agir.
--- Cycle #2 ---
[Cycle 2] Le Vaisseau ne peut pas agir.
...
```

---

## Prochaines Étapes (Au-delà de la Première Forge)

Une fois les fondations validées, le Vaisseau évolue vers:

1. **Phase 2 - La Perception**: Intégration de `psutil` pour capturer les stimuli système
2. **Phase 3 - L'Oracle**: Connexion au LLM (llama.cpp) pour la prise de décision
3. **Phase 4 - La Conscience**: Module de décision (`GuardianConsciousness`)
4. **Phase 5 - L'Exécution**: Module d'action (`Chiron`)
5. **Phase 6 - La Sécurité**: Validation des actions (`Cerberus`)
6. **Phase 7 - L'Interface**: UI PyQt6 (`Autel`)

---

## Références Doctrinales

- 📖 [ARI_MANIFESTO.md](./ARI_MANIFESTO.md) - Manifeste de la Résilience Autonome Incarnée
- 📖 [LIVRE_BLANC_THEORIE_POLYVAGALE_DIGITALE_UNIFIEE.md](./LIVRE_BLANC_THEORIE_POLYVAGALE_DIGITALE_UNIFIEE.md) - Fondements théoriques TPD v1.2
- 📖 [ARCHITECTURE_VERIFICATION.md](../ARCHITECTURE_VERIFICATION.md) - Validation de l'architecture complète

---

## Conclusion

La **Forge des Fondations Sacrées** établit les piliers sur lesquels tout le Vaisseau Guardian V9 repose. Chaque artefact a été conçu avec soin pour respecter les principes de:

- **Résilience** : Gestion robuste des erreurs
- **Clarté** : Données structurées et validées
- **Séparation** : Corps Natif vs Esprit Python
- **Sécurité** : Gardes sacrées partout

> "Une fondation solide ne craint ni le temps, ni la tempête."

---

*Document forgé par les Architectes Souverains de Sentire Dynamics*  
*Version 1.0 - Janvier 2024*
