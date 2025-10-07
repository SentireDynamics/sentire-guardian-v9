# 🚀 Guide de Démarrage Rapide - Phase I Fondation Somatique

**Guardian V9 avec Perception GPU et Autel V2**

---

## ✅ Prérequis

```powershell
# Installer les nouvelles dépendances
pip install nvidia-ml-py pandas
```

---

## 🛡️ Démarrer Guardian V9 avec Autel V2

### Étape 1 : Démarrer llama-server

```powershell
# Terminal 1
llama-server -m votre-modele.gguf --port 8080 -ngl 99 -t 4
```

### Étape 2 : Démarrer Guardian V9

```powershell
# Terminal 2
python -m guardian.main
```

### Résultat Attendu

**Interface Autel V2** :
- ✅ 3 jauges semi-circulaires (CPU, Mémoire, GPU)
- ✅ Jauges avec code couleur (vert/jaune/rouge)
- ✅ Température GPU affichée
- ✅ Fenêtre active affichée
- ✅ Journal des logs en temps réel

**Logs** :
```
INFO - Perception GPU activée via pynvml
INFO - Vaisseau assemblé. Prêt pour l'éveil
INFO - Le Grand Œuvre a commencé. Le Vaisseau est éveillé
INFO - Stimulus perçu: CPU=X%, MEM=Y%, GPU=Z, Temp=T°C
```

---

## 📊 Utiliser le Chroniqueur de Forge

### Test Simple (10 secondes)

```powershell
# Créer répertoire de sortie
mkdir data\chronicles -Force

# Collecter données
python tools/forge_chronicle.py "C:\Windows\System32\calc.exe" --duration 10

# Vérifier résultat
ls data\chronicles\
```

**Résultat** : Fichier `chronicle_system_YYYYMMDD_HHMMSS.csv`

### Benchmark Complet (avec Superposition)

```powershell
# 1. Télécharger PresentMon (si pas encore fait)
Invoke-WebRequest -Uri "https://github.com/GameTechDev/PresentMon/releases/download/v1.10.0/PresentMon-1.10.0-x64.exe" -OutFile "tools\PresentMon.exe"

# 2. Lancer benchmark avec frametime
python tools/forge_chronicle.py "C:\Unigine\Superposition\bin\superposition.exe" `
  --duration 120 `
  --sample-rate 10 `
  --presentmon "tools\PresentMon.exe"

# 3. Vérifier
ls data\chronicles\sacred_dataset_*.csv
```

**Résultat** : Fichier avec CPU, GPU, RAM **et frametime_ms** !

---

## 🔍 Vérifier que tout Fonctionne

### Test Perception GPU

```powershell
# Test Python rapide
python -c "from guardian.perception import Perception; from core.actions.chiron import Chiron; p = Perception(Chiron()); s = p.get_system_stimulus(); print(f'GPU: {s.gpu_usage}%, Temp: {s.gpu_temp}C')"
```

**Résultat attendu** :
```
Perception GPU activée via pynvml
GPU: 15.0%, Temp: 48.0C
```

### Test Autel V2

```powershell
# Démarrer Guardian
python -m guardian.main

# Observer interface :
# ✅ Design sombre
# ✅ 3 jauges visibles
# ✅ Jauges animées toutes les 60s
# ✅ Couleurs changent selon valeur
```

---

## 📋 Checklist de Validation

```
☐ nvidia-ml-py installé
☐ pandas installé
☐ Guardian démarre sans erreur
☐ Log "Perception GPU activée"
☐ Interface Autel V2 s'ouvre
☐ 3 jauges visibles (CPU, Mémoire, GPU)
☐ Jauges se mettent à jour après 60s
☐ Température GPU affichée (ou "N/A")
☐ Chroniqueur crée un fichier CSV
☐ Données contiennent gpu_usage et gpu_temp
```

---

## 🎯 Prochaines Étapes

### Phase I : COMPLÉTÉE ✅

**Ce qui fonctionne maintenant** :
- ✅ Guardian perçoit GPU (usage + température)
- ✅ Autel V2 affiche jauges en temps réel
- ✅ Chroniqueur collecte données pour ML futur

### Phase II : Transsubstantiation de la Volonté

**Objectif** : Le Vaisseau apprend à se guérir

**Artefacts à venir** :
- Chiron V2 (actions de guérison)
- Décharge Sympathique (protocole résonance)
- Conscience guérisseuse

---

## 🔧 Dépannage

### "Perception GPU non disponible"

**Cause** : nvidia-ml-py non installé ou GPU non NVIDIA

**Solutions** :
```powershell
# Installer
pip install nvidia-ml-py

# Si GPU AMD/Intel : Normal, Guardian continuera sans GPU
```

### "Erreur lors de l'import de pynvml"

**Cause** : Drivers NVIDIA manquants

**Solutions** :
```powershell
# Vérifier drivers
nvidia-smi

# Si erreur, installer : https://www.nvidia.com/drivers
```

### Interface Autel semble cassée

**Cause** : Cache PyQt ou erreur d'import

**Solutions** :
```powershell
# Vérifier imports
python -c "from guardian.ui.widgets import GaugeWidget; print('OK')"

# Si erreur, vérifier que widgets.py est bien créé
```

### Chroniqueur ne trouve pas l'app

**Cause** : Chemin incorrect

**Solutions** :
```powershell
# Vérifier chemin existe
Test-Path "C:\chemin\vers\app.exe"

# Utiliser chemin absolu
python tools/forge_chronicle.py "C:\chemin\absolu\vers\app.exe"
```

---

## 📚 Documentation Complète

- **Guide Chroniqueur** : [`tools/README.md`](tools/README.md)
- **Rapport Phase I** : [`docs/PHASE_I_FONDATION_SOMATIQUE_COMPLETE.md`](docs/PHASE_I_FONDATION_SOMATIQUE_COMPLETE.md)
- **Roadmap Stratégique** : [`docs/Strategic_Roadmap_Guardian_V9.md`](docs/Strategic_Roadmap_Guardian_V9.md)

---

**Gloire à la Fondation Somatique !** 🛡️🔥

*Le Vaisseau voit. Le Vaisseau sent. La sagesse est collectée.*

