# 🚨 ACTIVATION GPU URGENTE - Guardian V9

## ⚠️ PROBLÈME CRITIQUE DÉTECTÉ

**Votre RTX 4070 12GB est DORMANTE !**

```
Performance Actuelle : 0.75 tokens/sec (CPU-only) ❌
Performance Possible : 50-80 tokens/sec (GPU) ✅
Temps Oracle Actuel : 59 secondes
Temps Oracle Possible : 2-5 secondes

PERTE : 54 secondes par cycle gaspillées !
```

---

## ⚡ SOLUTION IMMÉDIATE (5 minutes)

### Étape 1 : Arrêter llama-server actuel

**PowerShell (Administrateur)** :
```powershell
# Trouver et tuer le processus
Stop-Process -Name llama-server -Force
```

**OU manuellement** :
- Ctrl+C dans la fenêtre PowerShell où tourne llama-server
- Ou fermer la fenêtre

---

### Étape 2 : Relancer avec GPU ACTIVÉ

#### Option A : Configuration Optimale RTX 4070
```powershell
llama-server -m chemin/vers/votre-modele.gguf `
  --port 8080 `
  -ngl 99 `              # ← ACTIVER GPU (tous les layers)
  -t 6 `                 # 6 threads CPU
  -c 2048 `              # Context size
  -b 512 `               # Batch size
  --main-gpu 0           # Utiliser GPU 0
```

#### Option B : Si vous utilisez Mistral 7B
```powershell
llama-server -m models/mistral-7b-instruct-v0.2.Q4_K_M.gguf `
  --port 8080 `
  -ngl 99 `
  -t 6 `
  -c 2048 `
  -b 512
```

#### Option C : Mode Simple (GPU auto-détecté)
```powershell
llama-server -m votre-modele.gguf --port 8080 -ngl 99
```

---

### Étape 3 : Vérifier l'Activation GPU

**Test rapide** :
```powershell
# Envoyer une requête test
$response = Invoke-RestMethod -Uri "http://localhost:8080/completion" `
  -Method Post `
  -ContentType "application/json" `
  -Body (@{prompt="Test GPU";n_predict=50} | ConvertTo-Json)

# Afficher la vitesse
$response.timings.predicted_per_second
```

**Résultat attendu** :
```
50-80   ← ✅ GPU ACTIF !
0.5-3   ← ❌ GPU non actif, vérifier -ngl flag
```

---

### Étape 4 : Relancer Guardian V9

```powershell
python -m guardian.main
```

**Observer les logs** :
```
✅ AVANT GPU : 16:29:34 → 16:30:33 (59 secondes)
✅ APRÈS GPU : 16:29:34 → 16:29:39 (5 secondes) ← ATTENDU
```

---

## 🔍 VÉRIFICATION NVIDIA

### Vérifier que le GPU est détecté

```powershell
# Vérifier GPU NVIDIA
nvidia-smi
```

**Sortie attendue** :
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 581.15                 Driver Version: 581.15         CUDA Version: 12.x    |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  TCC/WDDM     | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4070    WDDM    | 00000000:01:00.0  On  |                  N/A |
|  0%   48C    P8              15W / 200W |   1234MiB / 12288MiB   |      5%      Default |
+-----------------------------------------+------------------------+----------------------+
```

### Vérifier que llama.cpp utilise le GPU

**Pendant que llama-server tourne, dans les logs, chercher** :
```
llm_load_tensors: offloading 32 layers to GPU  ← ✅ GPU ACTIF
llm_load_tensors: using CUDA backend           ← ✅ CUDA détecté
```

**Si vous voyez** :
```
llm_load_tensors: offloading 0 layers to GPU   ← ❌ GPU NON ACTIF
```
→ Vérifier que vous avez bien mis `-ngl 99` ou `--n-gpu-layers 99`

---

## 🚨 DÉPANNAGE

### Problème : "CUDA not available"

**Solution 1** : Vérifier drivers NVIDIA
```powershell
nvidia-smi
```
Si erreur → Installer/mettre à jour drivers : https://www.nvidia.com/drivers

**Solution 2** : Utiliser build CUDA de llama.cpp
```bash
# Télécharger llama.cpp avec support CUDA
# Depuis : https://github.com/ggerganov/llama.cpp/releases
# Chercher : llama-*-cuda.zip
```

### Problème : Toujours lent même avec -ngl 99

**Diagnostic** :
```powershell
# Vérifier charge GPU pendant requête
nvidia-smi dmon -s u -c 10
```

**Si GPU à 0%** :
1. Vérifier version llama.cpp (doit avoir CUDA)
2. Vérifier CUDA installé : `nvcc --version`
3. Essayer Vulkan backend : `llama-server ... --vulkan`

### Problème : "Out of memory"

**Solution** : Réduire layers sur GPU
```powershell
llama-server -m model.gguf --port 8080 -ngl 35  # Au lieu de 99
```

---

## 📊 RÉSULTATS ATTENDUS

### Logs llama.cpp AVANT (CPU)
```
prompt eval time = 4086 ms / 97 tokens (42 ms per token, 23 tokens per second)
  eval time      = 54449 ms / 41 tokens (1328 ms per token, 0.75 tokens per second) ❌
  total time     = 58536 ms
```

### Logs llama.cpp APRÈS (GPU)
```
prompt eval time = 150 ms / 97 tokens (1.5 ms per token, 650 tokens per second) ✅
  eval time      = 820 ms / 41 tokens (20 ms per token, 50 tokens per second) ✅
  total time     = 970 ms
```

### Guardian V9 AVANT (CPU)
```
16:29:34 - Consultation de l'Oracle
16:30:33 - Réponse reçue (59 secondes) ❌
```

### Guardian V9 APRÈS (GPU)
```
16:29:34 - Consultation de l'Oracle
16:29:36 - Réponse reçue (2 secondes) ✅
```

---

## 🎯 SCORE DE PERFORMANCE

### Score Actuel (CPU-only)
```
Temps Oracle : 59s
Score        : 7.5/10 ⚠️
```

### Score Attendu (GPU activé)
```
Temps Oracle : 2-5s
Score        : 9.5/10 ✅
```

**Gain** : +27% de performance globale pour 1 commande !

---

## ✅ CHECKLIST D'ACTIVATION

- [ ] Arrêter llama-server actuel
- [ ] Vérifier GPU détecté (`nvidia-smi`)
- [ ] Relancer llama-server avec `-ngl 99`
- [ ] Vérifier logs : "offloading X layers to GPU"
- [ ] Test vitesse : >40 tokens/sec
- [ ] Relancer Guardian V9
- [ ] Vérifier temps Oracle <5 secondes
- [ ] Célébrer le x50 speedup ! 🎉

---

## 📝 COMMANDE RECOMMANDÉE FINALE

### Pour votre configuration (RTX 4070)

```powershell
# Ajuster le chemin vers votre modèle
llama-server -m "C:\chemin\vers\votre-modele.gguf" `
  --port 8080 `
  -ngl 99 `
  -t 6 `
  -c 2048 `
  -b 512 `
  --main-gpu 0 `
  --mlock
```

**Copier-coller cette commande et remplacer le chemin du modèle !**

---

## 🚀 APRÈS ACTIVATION

**Relancer Guardian** :
```powershell
python -m guardian.main
```

**Observer la magie** :
- ⚡ Cycles rapides (<10s)
- 🧠 Décisions instantanées
- 🏆 Score 9.5/10 atteint

---

**URGENT** : Exécuter maintenant pour débloquer x50 performance ! 🔥

**Gloire à la Puissance du GPU !** 🛡️⚡

