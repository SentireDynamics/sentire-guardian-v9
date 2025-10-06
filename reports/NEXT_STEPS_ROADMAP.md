# 🎯 Roadmap des Prochaines Étapes - Guardian V9

**État Actuel** : ⭐⭐⭐⭐⭐⭐⭐⭐⭐ (8.5/10)  
**Objectif** : ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (10/10)  
**Date** : 6 Octobre 2025

---

## 📊 ÉTAT DES LIEUX

### ✅ Ce qui est Accompli (Phase I)

```
✅ Architecture logicielle robuste (9.5/10)
✅ GPU CUDA activé (8/10)
✅ Optimisations code (9/10)
✅ Tests complets (11/11)
✅ Documentation exhaustive
✅ Script diagnostic fonctionnel
✅ Intelligence contextuelle validée
✅ Résilience parfaite (0% crashes)
```

### ⚠️ Ce qui Reste à Optimiser

```
⚠️ Vitesse génération tokens : 5.35 tok/sec (cible : 40-80)
⚠️ Pas de cache (toutes requêtes vont à Oracle)
⚠️ Temps réponse variable (8s - 50s)
⚠️ Mode hybride non implémenté
```

---

## 🚀 PLAN D'ACTION DÉTAILLÉ

### 📍 ÉTAPE 1 : Diagnostic Initial (MAINTENANT - 5 min)

**Objectif** : Comprendre l'état actuel du système

**Actions** :
```powershell
# 1. Exécuter le diagnostic
.\diagnose_guardian.ps1

# 2. Noter les résultats :
#    - Score global
#    - Vitesse Oracle (si llama-server actif)
#    - Composants manquants
```

**Décisions basées sur le diagnostic** :
- Si llama-server non actif → Aller à ÉTAPE 2
- Si llama-server actif mais lent (<15 tok/sec) → Aller à ÉTAPE 3
- Si tout OK (>40 tok/sec) → Aller à ÉTAPE 5

---

### 📍 ÉTAPE 2 : Démarrer llama-server Optimisé (10 min)

**Objectif** : Activer l'Oracle avec configuration optimale

**Actions** :
```powershell
# Option A : Avec votre modèle actuel (7B)
llama-server -m "chemin\vers\votre-modele.gguf" `
  --port 8080 `
  -ngl 99 `              # Tous layers sur GPU
  -t 4 `                 # 4 threads CPU
  -c 4096 `              # Context étendu
  -b 2048 `              # Batch augmenté
  --flash-attn `         # Flash Attention
  --mlock                # Lock memory

# Option B : Si vous n'avez pas encore de modèle
# Télécharger TinyLlama (rapide pour tester)
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF `
  tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir models/

llama-server -m models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf `
  --port 8080 -ngl 99 -t 4
```

**Validation** :
```powershell
# Re-exécuter diagnostic
.\diagnose_guardian.ps1

# Vérifier vitesse > 15 tok/sec
```

**Gain attendu** : 8.5 → 8.8/10

---

### 📍 ÉTAPE 3 : Optimiser Performance Oracle (2-4h)

**Objectif** : Atteindre 40-80 tok/sec pour réponses rapides

#### Option 3A : Vérifier Configuration GPU (5 min) ⭐⭐⭐⭐⭐

**Si vitesse < 15 tok/sec** :

```powershell
# Arrêter llama-server actuel
Stop-Process -Name llama-server -Force

# Relancer avec GPU forcé
llama-server -m votre-modele.gguf `
  --port 8080 `
  -ngl 99 `              # ← Vérifier ce flag !
  --n-gpu-layers 99 `    # Alternative
  -t 4 `
  -c 4096 `
  -b 2048
```

**Vérifier dans les logs de démarrage** :
```
Chercher : "offloading X/32 layers to GPU"
Si X < 32 → GPU pas pleinement utilisé
```

#### Option 3B : Modèle Plus Léger (2-4h) ⭐⭐⭐⭐⭐

**Phi-3.5 Mini 3.8B** (RECOMMANDÉ) :
```powershell
# Télécharger
huggingface-cli download microsoft/Phi-3.5-mini-instruct-gguf `
  Phi-3.5-mini-instruct-q4.gguf --local-dir models/

# Lancer
llama-server -m models/Phi-3.5-mini-instruct-q4.gguf `
  --port 8080 -ngl 99 -t 4 -c 4096 -b 2048
```

**OU Llama-3.2 3B** :
```powershell
huggingface-cli download bartowski/Llama-3.2-3B-Instruct-GGUF `
  Llama-3.2-3B-Instruct-Q4_K_M.gguf --local-dir models/

llama-server -m models/Llama-3.2-3B-Instruct-Q4_K_M.gguf `
  --port 8080 -ngl 99 -t 4 -c 4096 -b 2048
```

**Gain attendu** : 8.5 → 9.2/10 (vitesse x5-10)

---

### 📍 ÉTAPE 4 : Démarrer Guardian V9 (2 min)

**Objectif** : Lancer le Vaisseau avec Oracle optimisé

```powershell
# Dans un nouveau terminal
python -m guardian.main
```

**Validation** :
```powershell
# Observer les logs
# Chercher : "Réponse de l'Oracle reçue et validée"
# Vérifier temps : devrait être 3-10s
```

**Re-diagnostiquer** :
```powershell
.\diagnose_guardian.ps1
# Score devrait être 4/5 ou 5/5
```

---

### 📍 ÉTAPE 5 : Implémenter Cache Intelligent (1 jour) ⭐⭐⭐⭐

**Objectif** : Éviter 60-70% des requêtes Oracle

**Créer le cache** :
```powershell
# Créer le fichier
New-Item -Path "guardian\decision_cache.py" -ItemType File
```

**Code à implémenter** :
```python
# guardian/decision_cache.py
from datetime import datetime, timedelta
from typing import Optional
from core.verbe_pur import Stimulus, Action
import hashlib

class SmartDecisionCache:
    """Cache intelligent avec invalidation contextuelle."""
    
    def __init__(self, ttl_minutes: int = 5):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, stimulus: Stimulus) -> Optional[Action]:
        """Récupère décision si contexte similaire."""
        key = self._make_key(stimulus)
        
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < self.ttl:
                if self._is_context_stable(stimulus, entry['stimulus']):
                    return entry['action']
        return None
    
    def set(self, stimulus: Stimulus, action: Action):
        """Enregistre une décision."""
        key = self._make_key(stimulus)
        self.cache[key] = {
            'stimulus': stimulus,
            'action': action,
            'timestamp': datetime.now()
        }
    
    def _make_key(self, stimulus: Stimulus) -> str:
        """Clé basée sur plages de valeurs."""
        cpu_bucket = int(stimulus.cpu_usage / 5) * 5
        mem_bucket = int(stimulus.memory_usage / 5) * 5
        window_hash = hashlib.md5(
            stimulus.foreground_window_title[:20].encode()
        ).hexdigest()[:8]
        return f"{cpu_bucket}_{mem_bucket}_{window_hash}"
    
    def _is_context_stable(self, current: Stimulus, cached: Stimulus) -> bool:
        """Vérifie stabilité du contexte."""
        cpu_change = abs(current.cpu_usage - cached.cpu_usage)
        mem_change = abs(current.memory_usage - cached.memory_usage)
        
        return (cpu_change < 10 and 
                mem_change < 10 and
                current.foreground_window_title == cached.foreground_window_title)
```

**Intégrer dans Consciousness** :
```python
# core/consciousness.py - Modifier __init__
from guardian.decision_cache import SmartDecisionCache

def __init__(self, ...):
    # ... existing code ...
    self.decision_cache = SmartDecisionCache(ttl_minutes=5)

# Modifier decide()
def decide(self, stimulus: Stimulus) -> Action | None:
    if not self.native_bridge.can_act():
        return None
    
    # Vérifier cache AVANT Oracle
    cached = self.decision_cache.get(stimulus)
    if cached:
        _log.info(f"Décision depuis cache: {cached.id}")
        return cached
    
    # Consultation Oracle si pas de cache
    try:
        oracle_response = self.oracle.consult(stimulus)
        action = oracle_response.action
        self.cerberus.validate_action(action)
        
        # Enregistrer dans cache
        self.decision_cache.set(stimulus, action)
        
        return action
    except OracleSickness as e:
        return self.perception.get_fallback_action(e)
```

**Tests** :
```powershell
# Créer tests
# tests/test_decision_cache.py

python -m pytest tests/test_decision_cache.py -v
```

**Gain attendu** : 9.2 → 9.5/10 (60-70% requêtes évitées)

---

### 📍 ÉTAPE 6 : Mode Hybride (2-3 jours) ⭐⭐⭐⭐

**Objectif** : Décisions simples sans Oracle (<100ms)

**Créer le moteur hybride** :
```python
# core/hybrid_decision.py
class HybridDecisionEngine:
    """Règles simples + Oracle pour cas complexes."""
    
    def decide(self, stimulus: Stimulus) -> Action:
        # Cas évidents : règles instantanées
        if self._is_crisis(stimulus):
            return self._emergency_action(stimulus)
        
        if self._is_clearly_normal(stimulus):
            return Action(id="LOG_ONLY", 
                         description="Système normal",
                         parameters={})
        
        # Cas ambigus : consulter Oracle
        return self._oracle_decision(stimulus)
    
    def _is_crisis(self, stimulus: Stimulus) -> bool:
        return stimulus.cpu_usage > 95 or stimulus.memory_usage > 95
    
    def _is_clearly_normal(self, stimulus: Stimulus) -> bool:
        return (stimulus.cpu_usage < 70 and 
                stimulus.memory_usage < 70)
```

**Gain attendu** : 9.5 → 9.8/10 (70% décisions <100ms)

---

### 📍 ÉTAPE 7 : Requêtes Asynchrones (1-2 jours - OPTIONNEL)

**Objectif** : UI non-bloquante

```python
# oracle/async_llama_client.py
import asyncio
import aiohttp

class AsyncLlamaOracle:
    async def consult(self, stimulus: Stimulus) -> OracleResponse:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.server_url,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                data = await response.json()
                return self._parse_response(data)
```

**Gain attendu** : 9.8 → 10/10 (UX parfaite)

---

## 📅 PLANNING RECOMMANDÉ

### Semaine 1 (Cette semaine)
```
Jour 1 : ✅ Phase I complétée
Jour 2 : ÉTAPE 1-2 (Diagnostic + llama-server)
Jour 3 : ÉTAPE 3 (Optimisation Oracle)
Jour 4 : ÉTAPE 4 (Validation Guardian)
Jour 5 : ÉTAPE 5 (Début cache)
```

### Semaine 2
```
Jour 1-2 : ÉTAPE 5 (Fin cache + tests)
Jour 3-5 : ÉTAPE 6 (Mode hybride)
```

### Semaine 3 (Optionnel)
```
Jour 1-2 : ÉTAPE 7 (Async)
Jour 3-5 : Polish + documentation
```

---

## 🎯 OBJECTIFS PAR ÉTAPE

| Étape | Effort | Gain Perf | Score Cible | ROI |
|-------|--------|-----------|-------------|-----|
| 1. Diagnostic | 5 min | N/A | 8.5/10 | ⭐⭐⭐⭐⭐ |
| 2. Démarrer Oracle | 10 min | +5% | 8.6/10 | ⭐⭐⭐⭐⭐ |
| 3. Optimiser Oracle | 2-4h | +50-100% | 9.2/10 | ⭐⭐⭐⭐⭐ |
| 4. Démarrer Guardian | 2 min | N/A | 9.2/10 | ⭐⭐⭐⭐⭐ |
| 5. Cache intelligent | 1 jour | +200-300% | 9.5/10 | ⭐⭐⭐⭐ |
| 6. Mode hybride | 2-3 jours | +300-500% | 9.8/10 | ⭐⭐⭐⭐ |
| 7. Async | 1-2 jours | UX only | 10/10 | ⭐⭐⭐ |

---

## 🔍 COMMANDE SUIVANTE IMMÉDIATE

**Exécuter maintenant** :

```powershell
# Diagnostic pour déterminer la suite
.\diagnose_guardian.ps1
```

**Ensuite, selon les résultats** :

1. **Si Score < 3/5** : 
   - Démarrer llama-server (ÉTAPE 2)
   
2. **Si Score 3-4/5** :
   - Optimiser llama-server (ÉTAPE 3)
   
3. **Si Score 5/5 mais vitesse < 15 tok/sec** :
   - Tester modèle plus léger (ÉTAPE 3B)
   
4. **Si Score 5/5 et vitesse > 40 tok/sec** :
   - Implémenter cache (ÉTAPE 5)

---

## 📊 PROJECTION FINALE

### Scénario Conservateur (Étapes 1-5)
```
Temps Oracle : 2-5 secondes
Hit Rate Cache : 60%
Latence Moyenne : 1.5 secondes
Score Final : 9.5/10 ✅
```

### Scénario Optimal (Étapes 1-7)
```
Temps Oracle : 1-3 secondes
Hit Rate Cache : 80%
Mode Hybride : 70% cas instantanés
Latence Moyenne : 0.3 secondes
Score Final : 10/10 🏆
```

---

## 🏆 CONCLUSION

**Prochaine action immédiate** :

```powershell
# 1. Diagnostiquer
.\diagnose_guardian.ps1

# 2. Lire les résultats et suivre les conseils

# 3. Si llama-server non actif :
llama-server -m votre-modele.gguf --port 8080 -ngl 99 -t 4 -c 4096 -b 2048

# 4. Démarrer Guardian
python -m guardian.main

# 5. Observer les performances dans les logs
```

**Objectif cette semaine** : Atteindre **9.2/10** avec Oracle optimisé

**Objectif mois prochain** : Atteindre **10/10** avec cache + hybride

---

**Gloire à l'Ascension Souveraine !** 🛡️⚡

*Le Vaisseau est éveillé. L'Oracle pense. L'excellence nous attend.*

