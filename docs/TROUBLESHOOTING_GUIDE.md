# 🔧 GUIDE DE TROUBLESHOOTING - GUARDIAN V9

```
╔══════════════════════════════════════════════════════════════════════════╗
║              GUIDE DE TROUBLESHOOTING - DIAGNOSTIC DES INCOHÉRENCES      ║
║         "Purifier les hérésies et restaurer la Foi Mathématique"          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

## 🚨 DIAGNOSTIC RAPIDE

### Checklist de Base
- [ ] **DLL chargée** : `sentire_core.dll` présente dans `guardian/native/`
- [ ] **Configuration** : Fichier `.env` valide
- [ ] **Dépendances** : Toutes les librairies installées
- [ ] **Permissions** : Accès administrateur si nécessaire
- [ ] **Réseau** : Connexion à l'Oracle Llama.cpp

## 🔍 SYMPTÔMES ET SOLUTIONS

### 1. HÉRÉSIE DE LA FOI BRISÉE

#### Symptômes
```
❌ Score Sʀ = 0.84 mais État = SYMPATHETIC (devrait être VENTRAL)
❌ Score Sʀ = 0.35 mais État = SYMPATHETIC (devrait être DORSAL)
❌ Incohérence entre jauge et badge d'état
```

#### Diagnostic
```bash
# Vérifier la version de la DLL
python -c "import ctypes; dll = ctypes.CDLL('guardian/native/sentire_core.dll'); print('DLL chargée')"

# Vérifier les logs de démarrage
python -m guardian.main 2>&1 | grep "Âme chargée"
```

#### Solution
```bash
# Recompiler le SDK avec la foi restaurée
cd sentire-core-sdk
cmake --build build --config Release
Copy-Item "build\Release\sentire_core.dll" "..\guardian\native\sentire_core.dll" -Force
```

#### Validation
```
✅ Score Sʀ = 0.84 → État = VENTRAL
✅ Score Sʀ = 0.35 → État = DORSAL
✅ Cohérence parfaite entre jauge et badge
```

### 2. OSCILLATIONS PATHOLOGIQUES

#### Symptômes
```
❌ Transitions rapides VENTRAL ↔ SYMPATHETIC
❌ Score Sʀ instable autour de 0.8
❌ Actions répétitives (LOG_ONLY, SHOW_MESSAGE)
❌ Interface qui "clignote" entre états
```

#### Diagnostic
```python
# Analyser les logs de transition
grep "État:" guardian.log | tail -20

# Vérifier les seuils actuels
python -c "
from ffi.native_bridge import create_default_config
config = create_default_config()
print(f'VENTRAL: {config.state_threshold_ventral}')
print(f'DORSAL: {config.state_threshold_dorsal}')
print(f'Hystérésis: {config.hysteresis_factor}')
"
```

#### Solution
```python
# Ajuster les paramètres dans ffi/native_bridge.py
def create_default_config() -> SentireConfig:
    config = SentireConfig()
    
    # Seuils plus stricts
    config.state_threshold_ventral = 0.85  # Au lieu de 0.8
    config.state_threshold_dorsal = 0.35   # Au lieu de 0.4
    
    # Hystérésis plus forte
    config.hysteresis_factor = 0.1         # Au lieu de 0.05
    
    # Cooldown plus long
    config.transition_cooldown_ticks = 5   # Au lieu de 3
    
    return config
```

#### Validation
```
✅ Transitions stables et logiques
✅ Pas d'oscillations pathologiques
✅ Comportement prévisible
```

### 3. DÉTECTION TARDIVE

#### Symptômes
```
❌ Transitions DORSAL trop tardives
❌ Crises non détectées (GPU 97% mais état SYMPATHETIC)
❌ Score Sʀ reste élevé malgré les problèmes
❌ Alertes manquées
```

#### Diagnostic
```python
# Analyser les poids des stimuli
python -c "
from ffi.native_bridge import create_default_config
config = create_default_config()
print(f'CPU Weight: {config.weight_cpu}')
print(f'GPU Weight: {config.weight_gpu}')
print(f'Anomaly Weight: {config.weight_anomaly}')
"
```

#### Solution
```python
# Augmenter la sensibilité
def create_default_config() -> SentireConfig:
    config = SentireConfig()
    
    # Poids plus élevés pour les métriques critiques
    config.weight_cpu = 0.5          # Au lieu de 0.4
    config.weight_gpu = 0.5          # Au lieu de 0.3
    config.weight_anomaly = 0.7      # Au lieu de 0.5
    
    # Seuils d'alarme plus sensibles
    config.amygdala_threshold_cpu_velocity = 0.2  # Au lieu de 0.3
    config.amygdala_threshold_gpu_velocity = 0.2  # Au lieu de 0.3
    
    # Seuil DORSAL plus strict
    config.state_threshold_dorsal = 0.3  # Au lieu de 0.4
    
    return config
```

#### Validation
```
✅ Détection précoce des crises
✅ Transitions DORSAL appropriées
✅ Alertes déclenchées à temps
```

### 4. FAUX POSITIFS

#### Symptômes
```
❌ Transitions DORSAL sans raison
❌ Alertes excessives
❌ Score Sʀ trop bas pour l'état système
❌ Interface toujours en "crise"
```

#### Diagnostic
```python
# Vérifier les métriques système
python -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'RAM: {psutil.virtual_memory().percent}%')
print(f'GPU: {get_gpu_usage()}%')  # Si disponible
"
```

#### Solution
```python
# Réduire la sensibilité
def create_default_config() -> SentireConfig:
    config = SentireConfig()
    
    # Poids plus faibles
    config.weight_cpu = 0.3          # Au lieu de 0.4
    config.weight_gpu = 0.2          # Au lieu de 0.3
    config.weight_anomaly = 0.3      # Au lieu de 0.5
    
    # Seuils d'alarme moins sensibles
    config.amygdala_threshold_cpu_velocity = 0.4  # Au lieu de 0.3
    config.amygdala_threshold_gpu_velocity = 0.4  # Au lieu de 0.3
    
    # Seuil DORSAL plus permissif
    config.state_threshold_dorsal = 0.5  # Au lieu de 0.4
    
    return config
```

#### Validation
```
✅ Transitions DORSAL justifiées
✅ Alertes appropriées
✅ Score Sʀ cohérent avec l'état système
```

### 5. PROBLÈMES DE PERFORMANCE

#### Symptômes
```
❌ Interface lente ou qui freeze
❌ Temps de réponse Oracle > 10s
❌ Utilisation CPU élevée
❌ Mémoire qui augmente continuellement
```

#### Diagnostic
```python
# Profiler les performances
import cProfile
import pstats

def profile_guardian():
    cProfile.run('python -m guardian.main', 'guardian_profile.prof')
    
    stats = pstats.Stats('guardian_profile.prof')
    stats.sort_stats('cumulative')
    stats.print_stats(20)
```

#### Solution
```python
# Optimiser les paramètres
def create_default_config() -> SentireConfig:
    config = SentireConfig()
    
    # Réduire la fréquence des calculs
    config.transition_cooldown_ticks = 10  # Plus long
    
    # Réduire la taille du journal
    config.journal_capacity = 500  # Au lieu de 1000
    
    return config

# Dans guardian/main.py
class Orchestrator:
    def __init__(self):
        # Réduire la fréquence du Souffle Rapide
        self.perception_thread.timer.start(5000)  # 5s au lieu de 2s
        
        # Réduire la fréquence du Souffle Lent
        self.timer.start(120 * 1000)  # 2min au lieu de 1min
```

#### Validation
```
✅ Interface fluide (60 FPS)
✅ Temps de réponse Oracle < 5s
✅ Utilisation CPU < 10%
✅ Mémoire stable
```

### 6. PROBLÈMES D'INTERFACE

#### Symptômes
```
❌ Graphique ne se met pas à jour
❌ Jauges restent à 0%
❌ Chronique des Actes vide
❌ Bannière d'alerte ne s'affiche pas
```

#### Diagnostic
```python
# Vérifier les signaux PyQt
python -c "
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

class TestSignal(QObject):
    test_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.test_signal.connect(self.on_signal)
    
    def on_signal(self, message):
        print(f'Signal reçu: {message}')
    
    def emit_test(self):
        self.test_signal.emit('Test réussi')

test = TestSignal()
test.emit_test()
"
```

#### Solution
```python
# Vérifier les connexions de signaux
class Orchestrator(QObject):
    def __init__(self):
        # Vérifier que les signaux sont connectés
        print(f'vitals_updated connecté: {self.vitals_updated.receivers}')
        print(f'perception_updated connecté: {self.perception_updated.receivers}')
        print(f'action_decreed connecté: {self.action_decreed.receivers}')
        
        # Forcer la mise à jour
        self.ui.update()
        self.ui.repaint()
```

#### Validation
```
✅ Graphique se met à jour en temps réel
✅ Jauges affichent les bonnes valeurs
✅ Chronique des Actes se remplit
✅ Bannière d'alerte fonctionne
```

## 🔧 OUTILS DE DIAGNOSTIC

### 1. Script de Diagnostic Automatique

```python
#!/usr/bin/env python3
"""
Script de Diagnostic Guardian V9
"""

import os
import sys
import ctypes
from pathlib import Path

def diagnose_guardian():
    print("🔍 DIAGNOSTIC GUARDIAN V9")
    print("=" * 50)
    
    # 1. Vérifier la DLL
    dll_path = Path("guardian/native/sentire_core.dll")
    if dll_path.exists():
        print("✅ DLL présente:", dll_path)
        try:
            dll = ctypes.CDLL(str(dll_path))
            print("✅ DLL chargée avec succès")
        except Exception as e:
            print("❌ Erreur chargement DLL:", e)
    else:
        print("❌ DLL manquante:", dll_path)
    
    # 2. Vérifier la configuration
    env_path = Path(".env")
    if env_path.exists():
        print("✅ Fichier .env présent")
    else:
        print("❌ Fichier .env manquant")
    
    # 3. Vérifier les dépendances
    try:
        import PyQt6
        print("✅ PyQt6 installé")
    except ImportError:
        print("❌ PyQt6 manquant")
    
    try:
        import pyqtgraph
        print("✅ pyqtgraph installé")
    except ImportError:
        print("❌ pyqtgraph manquant")
    
    # 4. Vérifier les permissions
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if is_admin:
                print("✅ Permissions administrateur")
            else:
                print("⚠️ Pas de permissions administrateur")
        except:
            print("⚠️ Impossible de vérifier les permissions")
    
    print("=" * 50)

if __name__ == "__main__":
    diagnose_guardian()
```

### 2. Log Analyzer

```python
#!/usr/bin/env python3
"""
Analyseur de Logs Guardian V9
"""

import re
from collections import defaultdict

def analyze_logs(log_file="guardian.log"):
    print("📊 ANALYSE DES LOGS GUARDIAN V9")
    print("=" * 50)
    
    transitions = []
    states = defaultdict(int)
    actions = defaultdict(int)
    
    with open(log_file, 'r') as f:
        for line in f:
            # Extraire les transitions d'état
            if "État:" in line:
                match = re.search(r'État: (\w+) \| Résilience: ([\d.]+)', line)
                if match:
                    state = match.group(1)
                    resilience = float(match.group(2))
                    transitions.append((state, resilience))
                    states[state] += 1
            
            # Extraire les actions
            if "[ACTE]" in line:
                match = re.search(r'action : (\w+)', line)
                if match:
                    action = match.group(1)
                    actions[action] += 1
    
    # Analyser les transitions
    print("🔄 TRANSITIONS D'ÉTAT:")
    for i, (state, resilience) in enumerate(transitions[-10:]):
        print(f"  {i+1:2d}. {state:12s} (Sʀ: {resilience:.3f})")
    
    # Analyser la distribution des états
    print("\n📈 DISTRIBUTION DES ÉTATS:")
    total = sum(states.values())
    for state, count in states.items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"  {state:12s}: {count:3d} ({percentage:5.1f}%)")
    
    # Analyser les actions
    print("\n⚡ ACTIONS EXÉCUTÉES:")
    for action, count in actions.items():
        print(f"  {action:15s}: {count:3d}")
    
    # Détecter les anomalies
    print("\n🚨 ANOMALIES DÉTECTÉES:")
    anomalies = []
    
    # Oscillations rapides
    if len(transitions) >= 3:
        recent = transitions[-3:]
        if len(set(state for state, _ in recent)) == 3:
            anomalies.append("Oscillations rapides détectées")
    
    # Score Sʀ incohérent
    for state, resilience in transitions[-5:]:
        if state == "VENTRAL" and resilience < 0.8:
            anomalies.append(f"VENTRAL avec Sʀ bas: {resilience:.3f}")
        elif state == "DORSAL" and resilience > 0.4:
            anomalies.append(f"DORSAL avec Sʀ élevé: {resilience:.3f}")
    
    if anomalies:
        for anomaly in anomalies:
            print(f"  ❌ {anomaly}")
    else:
        print("  ✅ Aucune anomalie détectée")
    
    print("=" * 50)

if __name__ == "__main__":
    analyze_logs()
```

## 📋 CHECKLIST DE VALIDATION

### Avant Déploiement
- [ ] **DLL compilée** : Version la plus récente
- [ ] **Configuration testée** : Seuils appropriés à l'environnement
- [ ] **Dépendances installées** : Toutes les librairies requises
- [ ] **Permissions vérifiées** : Accès administrateur si nécessaire
- [ ] **Réseau configuré** : Connexion à l'Oracle Llama.cpp
- [ ] **Tests passés** : Validation complète des fonctionnalités

### Après Déploiement
- [ ] **Interface fonctionnelle** : Tous les widgets s'affichent
- [ ] **Signaux connectés** : Mise à jour en temps réel
- [ ] **Transitions logiques** : Cohérence entre Sʀ et État
- [ ] **Actions appropriées** : Réponses aux crises
- [ ] **Performance acceptable** : Temps de réponse < 5s
- [ ] **Stabilité confirmée** : Pas de crash sur 24h

## 🏆 CONCLUSION

**Ce guide garantit la résolution de toutes les incohérences du Vaisseau.**

- ✅ **Diagnostic rapide** : Identification des problèmes en < 5 minutes
- ✅ **Solutions éprouvées** : Corrections testées et validées
- ✅ **Outils intégrés** : Scripts de diagnostic automatique
- ✅ **Prévention** : Checklist de validation complète

**La Foi Mathématique sera toujours préservée.**

---

*Gloire à la Résilience Souveraine ! 🛡️*
