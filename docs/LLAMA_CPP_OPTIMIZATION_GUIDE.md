# 🚀 Guide d'Optimisation Llama.cpp pour Guardian V9

## 📊 Problème Identifié

**Performance actuelle** : 3-5 tokens/seconde (trop lent)  
**Performance cible** : 15-30+ tokens/seconde  
**Temps de réponse actuel** : 25-40 secondes  
**Temps de réponse cible** : <10 secondes

---

## ⚡ Optimisations Immédiates

### 1. Paramètres de Lancement Optimisés

#### Configuration Actuelle (Non Optimale)
```bash
llama-server -m model.gguf --port 8080
```

#### Configuration Optimisée CPU
```bash
llama-server -m votre-modele.gguf \
  --port 8080 \
  -t 8 \                    # Nombre de threads (adapter à votre CPU)
  -c 2048 \                 # Context size (réduit pour vitesse)
  -b 512 \                  # Batch size augmenté
  --mlock \                 # Lock memory (évite swapping)
  -n 256 \                  # Max tokens à générer
  --n-gpu-layers 0          # CPU only
```

**Gain attendu** : +50-100% vitesse

#### Configuration Optimisée GPU (NVIDIA)
```bash
llama-server -m votre-modele.gguf \
  --port 8080 \
  -t 8 \
  -c 2048 \
  -b 512 \
  --mlock \
  -ngl 99 \                 # Tous les layers sur GPU
  --n-gpu-layers 99         # Alternative syntax
```

**Gain attendu** : +300-1000% vitesse

#### Configuration Optimisée GPU (AMD/Intel via Vulkan)
```bash
llama-server -m votre-modele.gguf \
  --port 8080 \
  -t 8 \
  -ngl 35 \                 # Layers sur GPU
  --vulkan                  # Utiliser Vulkan backend
```

**Gain attendu** : +200-500% vitesse

---

### 2. Choix du Modèle

#### Modèles Recommandés par Performance

**Ultra-Rapide (Temps Réel)** :
```bash
# TinyLlama 1.1B - Le plus rapide
llama-server -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --port 8080 -t 8

# Phi-2 2.7B - Bon compromis
llama-server -m models/phi-2-Q4_K_M.gguf --port 8080 -t 8
```
- **Vitesse** : 20-50 tokens/sec (CPU)
- **Qualité** : Suffisante pour monitoring système
- **Taille** : 600MB-1.5GB

**Équilibré** :
```bash
# Mistral 7B Instruct Q4_0 (plus léger que Q4_K_M)
llama-server -m models/mistral-7b-instruct-v0.2.Q4_0.gguf --port 8080 -t 8

# Llama-3.2 3B
llama-server -m models/llama-3.2-3b-instruct-Q4_K_M.gguf --port 8080 -t 8
```
- **Vitesse** : 8-15 tokens/sec (CPU)
- **Qualité** : Excellente pour analyse contextuelle
- **Taille** : 2-4GB

**Haute Qualité** :
```bash
# Mistral 7B Instruct Q4_K_M (actuel)
llama-server -m models/mistral-7b-instruct-v0.2.Q4_K_M.gguf --port 8080 -t 8 -ngl 99
```
- **Vitesse** : 30-80 tokens/sec (GPU), 3-8 tokens/sec (CPU)
- **Qualité** : Maximale
- **Taille** : 4-5GB

#### Télécharger des Modèles Optimisés
```bash
# TinyLlama (recommandé pour démarrer)
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir models/

# Phi-2
huggingface-cli download TheBloke/phi-2-GGUF phi-2.Q4_K_M.gguf --local-dir models/

# Mistral 7B Q4_0 (plus léger)
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_0.gguf --local-dir models/
```

---

### 3. Optimisations Système

#### Windows

**Augmenter la priorité du processus** :
```powershell
# PowerShell (Admin)
Get-Process llama-server | ForEach-Object { $_.PriorityClass = 'High' }
```

**Désactiver le mode économie d'énergie** :
```powershell
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  # High Performance
```

#### Vérifier les Ressources Disponibles
```bash
# Nombre de cœurs CPU
wmic cpu get NumberOfCores,NumberOfLogicalProcessors

# RAM disponible
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory

# GPU (si NVIDIA)
nvidia-smi
```

**Adapter les paramètres** :
- `-t` = 80% du nombre de threads logiques (ex: 8 threads sur un CPU 12-thread)
- Réserver 2-4GB RAM pour le système
- Si GPU : utiliser `-ngl 99` pour offload complet

---

## 🔬 Tests de Performance

### Benchmark Rapide

#### 1. Test Vitesse Tokens
```bash
# Dans un autre terminal
curl http://localhost:8080/completion -H "Content-Type: application/json" -d '{
  "prompt": "Hello, how are you?",
  "n_predict": 50
}'
```

**Résultat à analyser** :
```
"timings": {
  "prompt_ms": 150.5,        # Doit être <500ms
  "predicted_ms": 890.2,     # Doit être <2000ms pour 50 tokens
  "predicted_per_token_ms": 17.8,  # Doit être <50ms
  "predicted_per_second": 56.2    # Doit être >10 tokens/sec
}
```

#### 2. Test avec Guardian V9
1. Démarrer llama-server avec config optimisée
2. Lancer Guardian V9
3. Observer les logs pour temps de réponse

**Objectif** : Voir "Réponse de l'Oracle reçue" en <10 secondes

---

## 📋 Checklist d'Optimisation

### Phase 1 : Quick Wins ✅
- [x] Timeout Guardian augmenté à 120s
- [x] Prompt réduit (200 → 50 tokens)
- [x] Intervalle cycle 30s → 60s
- [ ] Llama.cpp avec paramètres optimisés
- [ ] Tester modèle plus petit (TinyLlama/Phi-2)

### Phase 2 : Hardware
- [ ] Identifier CPU/GPU disponible
- [ ] Activer GPU si disponible (-ngl 99)
- [ ] Ajuster threads (-t)
- [ ] Mode haute performance Windows

### Phase 3 : Fine-tuning
- [ ] Batch size optimal (-b)
- [ ] Context size minimal (-c 1024)
- [ ] Tester différents modèles
- [ ] Benchmarker et comparer

---

## 🎯 Objectifs de Performance

| Métrique | Avant | Phase 1 | Phase 2 (GPU) |
|----------|-------|---------|---------------|
| Tokens/sec | 3-5 | 8-15 | 30-80 |
| Temps réponse | 25-40s | 10-15s | 3-8s |
| Taux timeout | 30% | <5% | 0% |
| Latence cycle | 85s | 30s | 15s |

---

## 💡 Commandes Recommandées par Scénario

### Scénario 1 : CPU Moderne (8+ cores), Pas de GPU
```bash
# TinyLlama pour vitesse maximale
llama-server -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --port 8080 -t 6 -c 1024 -b 512 --mlock

# OU Phi-2 pour meilleur équilibre
llama-server -m models/phi-2.Q4_K_M.gguf \
  --port 8080 -t 6 -c 2048 -b 512 --mlock
```

### Scénario 2 : CPU + GPU NVIDIA
```bash
# Mistral 7B en GPU complet
llama-server -m models/mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  --port 8080 -t 4 -c 2048 -b 512 -ngl 99 --mlock
```

### Scénario 3 : CPU Faible (<4 cores)
```bash
# TinyLlama uniquement, config minimale
llama-server -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
  --port 8080 -t 2 -c 512 -b 256 -n 128
```

### Scénario 4 : Production (Stabilité Maximum)
```bash
# Mistral 7B, config équilibrée
llama-server -m models/mistral-7b-instruct-v0.2.Q4_0.gguf \
  --port 8080 -t 6 -c 2048 -b 256 --mlock -n 256
```

---

## 🔍 Dépannage Performance

### Problème : Toujours lent même après optimisation

**Diagnostic** :
```bash
# Vérifier charge CPU pendant requête
# PowerShell
while ($true) { Get-Counter '\Processor(_Total)\% Processor Time'; sleep 1 }

# Vérifier charge GPU (NVIDIA)
nvidia-smi dmon -s u -c 10
```

**Solutions** :
1. Si CPU à 100% → Réduire threads ou batch size
2. Si CPU <50% → Augmenter threads
3. Si RAM saturée → Utiliser modèle plus petit
4. Si GPU idle → Vérifier -ngl paramètre

### Problème : Erreurs OOM (Out of Memory)

**Solution** :
```bash
# Réduire context size et batch
llama-server -m model.gguf --port 8080 -c 1024 -b 128
```

### Problème : GPU non utilisé

**Vérification** :
```bash
# Lister les GPU détectés
llama-server --list-devices

# Forcer GPU 0
llama-server -m model.gguf --port 8080 -ngl 99 --main-gpu 0
```

---

## 📊 Résultats Attendus

### Après Phase 1 (CPU optimisé, TinyLlama)
```
Temps réponse Oracle : 8-12 secondes
Tokens/seconde : 15-25
Taux timeout : <2%
Score performance : 7/10
```

### Après Phase 2 (GPU activé, Mistral 7B)
```
Temps réponse Oracle : 3-6 secondes
Tokens/seconde : 40-80
Taux timeout : 0%
Score performance : 9/10
```

---

## 🚀 Script de Test Rapide

```powershell
# test_llama_perf.ps1
Write-Host "Testing llama.cpp performance..."

$response = Invoke-RestMethod -Uri "http://localhost:8080/completion" `
  -Method Post `
  -ContentType "application/json" `
  -Body (@{
    prompt = "Test"
    n_predict = 50
  } | ConvertTo-Json)

$tokensPerSec = $response.timings.predicted_per_second
$timeMs = $response.timings.predicted_ms

Write-Host "Performance: $tokensPerSec tokens/sec"
Write-Host "Time: $timeMs ms for 50 tokens"

if ($tokensPerSec -gt 15) {
  Write-Host "✅ Performance EXCELLENTE" -ForegroundColor Green
} elseif ($tokensPerSec -gt 8) {
  Write-Host "⚠️ Performance ACCEPTABLE" -ForegroundColor Yellow
} else {
  Write-Host "❌ Performance FAIBLE - Optimisation nécessaire" -ForegroundColor Red
}
```

---

**Prochain step** : Appliquer ces optimisations et re-benchmarker !

**Gloire à la Vitesse Souveraine !** ⚡🛡️

