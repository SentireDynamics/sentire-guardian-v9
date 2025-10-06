# 🚀 DÉMARRAGE IMMÉDIAT - Guardian V9

**Basé sur le diagnostic actuel : Score 3/5 (60%)**

---

## 📊 DIAGNOSTIC ACTUEL

```
✅ GPU NVIDIA       : OK (RTX 4070 12GB, CUDA 581.15)
✅ CUDA Support     : OK
❌ llama-server     : NON DÉMARRÉ
❌ Guardian V9      : NON DÉMARRÉ
✅ Configuration    : OK (.env présent)
✅ Corps Natif      : OK (sentire_core.dll)
```

**Composants manquants** : llama-server + Guardian V9

---

## 🎯 PROCHAINE ÉTAPE : Démarrer l'Oracle (llama-server)

### Option A : Si vous avez déjà un modèle

```powershell
# Remplacer le chemin par votre modèle
llama-server -m "C:\chemin\vers\votre-modele.gguf" `
  --port 8080 `
  -ngl 99 `              # GPU complet
  -t 4 `                 # 4 threads
  -c 4096 `              # Context
  -b 2048 `              # Batch
  --mlock                # Lock memory
```

### Option B : Si vous n'avez pas de modèle (Recommandé pour démarrer)

#### TinyLlama 1.1B (Ultra-rapide, 600 MB)

```powershell
# 1. Télécharger TinyLlama
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF `
  tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir models/

# 2. Lancer llama-server
llama-server -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf `
  --port 8080 `
  -ngl 99 `
  -t 4
```

**Avantages TinyLlama** :
- ⚡ Très rapide (40-80 tok/sec sur RTX 4070)
- 💾 Petit (600 MB)
- ✅ Suffisant pour monitoring système
- 🚀 Idéal pour tester Guardian V9

#### Phi-3.5 Mini 3.8B (Meilleur compromis, 2.3 GB)

```powershell
# 1. Télécharger Phi-3.5 Mini
huggingface-cli download microsoft/Phi-3.5-mini-instruct-gguf `
  Phi-3.5-mini-instruct-q4.gguf --local-dir models/

# 2. Lancer llama-server
llama-server -m models/Phi-3.5-mini-instruct-q4.gguf `
  --port 8080 `
  -ngl 99 `
  -t 4 `
  -c 4096 `
  -b 2048
```

**Avantages Phi-3.5 Mini** :
- 🧠 Excellente qualité de raisonnement
- ⚡ Rapide (30-60 tok/sec sur RTX 4070)
- 💾 Raisonnable (2.3 GB)
- ✅ Recommandé pour production

---

## 🔍 Validation llama-server

**Vérifier que le serveur fonctionne** :

```powershell
# Test simple
curl http://localhost:8080/health
```

**Résultat attendu** : 
```json
{"status":"ok"}
```

**Test de performance** :
```powershell
# Re-diagnostiquer
.\diagnose_guardian.ps1
```

**Résultat attendu** :
```
[2/5] Verification llama-server...
  [OK] llama-server en cours d'execution (PID: XXXXX)
  [OK] Endpoint accessible
  [PERF] Vitesse generation : XX.XX tok/sec
  [EXCELLENT] GPU pleinement utilise
```

---

## 🛡️ Démarrer Guardian V9

**Une fois llama-server actif** :

```powershell
# Dans un NOUVEAU terminal PowerShell
python -m guardian.main
```

**Logs attendus** :
```
INFO - Rituel d'assemblage du Vaisseau commencé
INFO - Corps Natif chargé avec succès
INFO - Le Grand Œuvre a commencé. Le Vaisseau est éveillé
INFO - Début du cycle de conscience
INFO - Consultation de l'Oracle pour une décision...
INFO - Réponse de l'Oracle reçue et validée
INFO - Décision prise: Exécuter l'action 'LOG_ONLY'
```

**Interface graphique** : Une fenêtre "Autel du Vaisseau Guardian V9" devrait s'ouvrir

---

## ✅ Validation Complète

**Re-diagnostiquer pour confirmer** :

```powershell
# Dans un 3ème terminal
.\diagnose_guardian.ps1
```

**Résultat attendu (Score 5/5)** :
```
Composants:
  - GPU NVIDIA       : [OK]
  - CUDA Support     : [OK]
  - llama-server     : [OK]
  - Guardian V9      : [OK]
  - Configuration    : [OK]
  - Corps Natif      : [OK]

Score Global : 5/5 (100%)

[PARFAIT] Configuration complete et operationnelle !

Performance Oracle:
  - Vitesse generation : 40-80 tok/sec
  - Evaluation : EXCELLENT (GPU full)
```

---

## 🎯 APRÈS LE DÉMARRAGE

### Observer Guardian en Action

**Logs Guardian** :
- Cycles toutes les 60 secondes
- Consultation Oracle
- Décisions (LOG_ONLY ou SHOW_MESSAGE)
- Actions exécutées

**Interface Autel** :
- Métriques temps réel (CPU, Mémoire)
- Journal des logs
- Bouton "Forcer Cycle" pour test

### Tester Manuellement

**Simuler CPU élevé** :
```powershell
# Ouvrir Task Manager et lancer un processus intensif
# OU
# Cliquer "Forcer Cycle" dans l'interface plusieurs fois
```

**Observer** :
- Si CPU > 90% → Guardian devrait décider SHOW_MESSAGE
- Si CPU < 90% → Guardian devrait décider LOG_ONLY

---

## 📈 PROCHAINES OPTIMISATIONS

**Une fois Guardian fonctionnel (Score 5/5)** :

### Semaine 1 : Performance Oracle
- Tester différents modèles
- Mesurer vitesses (objectif : >40 tok/sec)
- Ajuster paramètres llama-server

### Semaine 2 : Cache Intelligent
- Implémenter SmartDecisionCache
- Éviter 60-70% requêtes Oracle
- Temps réponse <100ms pour hits

### Semaine 3-4 : Mode Hybride
- Règles simples pour cas évidents
- Oracle pour cas complexes uniquement
- 70% décisions instantanées

**Objectif final** : Score 10/10, latence <1s moyenne

---

## 🔧 DÉPANNAGE RAPIDE

### llama-server ne démarre pas

**Erreur : "Model file not found"**
```powershell
# Vérifier le chemin du modèle
Test-Path "chemin\vers\modele.gguf"

# Si false, télécharger un modèle (voir Option B ci-dessus)
```

**Erreur : "Port 8080 already in use"**
```powershell
# Vérifier processus sur port 8080
netstat -ano | findstr :8080

# Tuer le processus ou utiliser autre port
llama-server -m model.gguf --port 8081
# Puis modifier .env : LLAMA_SERVER_URL=http://localhost:8081/completion
```

### Guardian ne démarre pas

**Erreur : "ModuleNotFoundError"**
```powershell
# Installer dépendances
pip install -r requirements.txt
```

**Erreur : ".env missing"**
```powershell
# Vérifier .env existe
Test-Path .env

# Si false, copier exemple
Copy-Item .env.example .env
# Puis éditer .env
```

---

## 📋 CHECKLIST DE DÉMARRAGE

```
☐ 1. Exécuter diagnostic : .\diagnose_guardian.ps1
☐ 2. Télécharger un modèle (TinyLlama ou Phi-3.5 Mini)
☐ 3. Démarrer llama-server avec -ngl 99
☐ 4. Vérifier : curl http://localhost:8080/health
☐ 5. Démarrer Guardian : python -m guardian.main
☐ 6. Observer interface Autel s'ouvrir
☐ 7. Re-diagnostiquer : Score devrait être 5/5
☐ 8. Observer cycles de conscience (logs)
☐ 9. Tester décision manuelle (Forcer Cycle)
☐ 10. Valider performance Oracle (>40 tok/sec)
```

---

## 🚀 COMMANDES COPIER-COLLER

### Démarrage Complet (TinyLlama)

```powershell
# Terminal 1 : Télécharger + Lancer llama-server
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir models/
llama-server -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --port 8080 -ngl 99 -t 4

# Terminal 2 : Démarrer Guardian
python -m guardian.main

# Terminal 3 : Diagnostic
.\diagnose_guardian.ps1
```

---

**Temps estimé total** : 10-30 minutes (selon vitesse téléchargement)

**Gloire au Premier Souffle !** 🛡️⚡

*Le diagnostic révèle le chemin. L'Oracle attend. Le Vaisseau s'éveille.*

