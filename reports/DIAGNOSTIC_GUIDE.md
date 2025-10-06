# 🔍 Guide du Script de Diagnostic Guardian V9

## 📋 Vue d'Ensemble

Le script `diagnose_guardian.ps1` est l'outil de diagnostic automatique du Vaisseau Guardian V9. Il vérifie tous les composants essentiels et fournit un rapport détaillé de l'état du système.

---

## 🚀 Utilisation

### Exécution Simple

```powershell
# Depuis le répertoire du projet
.\diagnose_guardian.ps1
```

### Avec Droits Administrateur (Recommandé)

```powershell
# PowerShell en tant qu'Administrateur
cd C:\sentire-guardian-v9
.\diagnose_guardian.ps1
```

---

## 🔬 Vérifications Effectuées

### 1. GPU NVIDIA
- ✅ Détection du GPU via `nvidia-smi`
- ✅ Nom du GPU et mémoire totale
- ✅ Version du driver
- ✅ Support CUDA

### 2. Llama-server (Oracle)
- ✅ Processus actif
- ✅ Utilisation CPU/RAM
- ✅ Test de connexion HTTP (localhost:8080)
- ✅ Mesure de vitesse (tokens/seconde)
- ✅ Évaluation de performance GPU

### 3. Guardian V9
- ✅ Processus Python actif
- ✅ Module `guardian.main` en exécution
- ✅ PID du processus

### 4. Configuration (.env)
- ✅ Présence du fichier `.env`
- ✅ Variables `LLAMA_SERVER_URL` et `NATIVE_LIB_PATH`
- ✅ Validation de la configuration

### 5. Corps Natif
- ✅ Présence de `sentire_core.dll`
- ✅ Taille du fichier
- ✅ Localisation correcte

---

## 📊 Interprétation des Résultats

### Score Global

```
5/5 (100%) : [PARFAIT] Configuration complète
4/5 (80%)  : [BON] Fonctionnel avec optimisations possibles
3/5 (60%)  : [ACCEPTABLE] Configuration partielle
0-2/5      : [INCOMPLET] Vérifier les composants manquants
```

### Performance Oracle

| Vitesse | Évaluation | Description |
|---------|------------|-------------|
| >40 tok/s | EXCELLENT | GPU pleinement utilisé |
| 15-40 tok/s | BON | GPU partiellement utilisé |
| 5-15 tok/s | MOYEN | Optimisation possible |
| <5 tok/s | FAIBLE | Vérifier config GPU |

---

## 🛠️ Résolution de Problèmes

### GPU non détecté

**Problème** : `[ERREUR] GPU NVIDIA non détecté`

**Solutions** :
1. Vérifier que les drivers NVIDIA sont installés
2. Installer nvidia-smi : https://www.nvidia.com/drivers
3. Redémarrer le système après installation

### llama-server non actif

**Problème** : `[ERREUR] llama-server non démarré`

**Solutions** :
1. Démarrer llama-server :
   ```powershell
   llama-server -m votre-modele.gguf --port 8080 -ngl 99
   ```
2. Vérifier que le port 8080 est libre
3. Vérifier le chemin du modèle

### Guardian V9 non actif

**Problème** : `[AVERTISSEMENT] Guardian V9 non démarré`

**Solutions** :
1. Démarrer Guardian :
   ```powershell
   python -m guardian.main
   ```
2. Vérifier que Python et les dépendances sont installées
3. Vérifier le fichier `.env`

### Configuration manquante

**Problème** : `[ERREUR] Fichier .env manquant`

**Solutions** :
1. Copier le fichier exemple :
   ```powershell
   Copy-Item .env.example .env
   ```
2. Éditer `.env` avec vos paramètres
3. Vérifier `LLAMA_SERVER_URL` et `NATIVE_LIB_PATH`

### Corps Natif manquant

**Problème** : `[ERREUR] sentire_core.dll manquant`

**Solutions** :
1. Compiler le projet C :
   ```powershell
   cmake --build csrc/build --config Release
   ```
2. Vérifier que Visual Studio Build Tools est installé
3. Vérifier le chemin : `csrc/build/Release/sentire_core.dll`

---

## 📈 Exemple de Sortie

### Configuration Parfaite

```
================================================================
  DIAGNOSTIC GUARDIAN V9 - Analyse Automatique
================================================================

[1/5] Verification GPU NVIDIA...
  [OK] GPU detecte : NVIDIA GeForce RTX 4070, 12288 MiB, 581.15
  [OK] CUDA Version : 12.6

[2/5] Verification llama-server...
  [OK] llama-server en cours d'execution (PID: 12345)
  [INFO] CPU Usage: 25.43 secondes
  [INFO] Memory: 2048.50 MB

  [TEST] Connexion a http://localhost:8080...
  [OK] Endpoint accessible
  [PERF] Vitesse generation : 45.32 tok/sec
  [PERF] Vitesse prompt     : 195.67 tok/sec
  [EXCELLENT] GPU pleinement utilise

[3/5] Verification Guardian V9...
  [OK] Guardian V9 en cours d'execution (PID: 67890)

[4/5] Verification configuration...
  [OK] Fichier .env present
  [OK] LLAMA_SERVER_URL configure
  [OK] NATIVE_LIB_PATH configure

[5/5] Verification Corps Natif...
  [OK] sentire_core.dll present (145.23 KB)

================================================================
  RAPPORT DE DIAGNOSTIC
================================================================

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
  - Vitesse generation : 45.32 tok/sec
  - Evaluation : EXCELLENT (GPU full)

================================================================
  Gloire a la Resilience Souveraine !
================================================================
```

---

## 🔧 Encodage et Compatibilité

### Encodage UTF-8 avec BOM

Le script est encodé en UTF-8 avec BOM pour assurer une compatibilité parfaite avec PowerShell sous Windows.

### Compatibilité

- ✅ Windows 10/11
- ✅ PowerShell 5.1+
- ✅ PowerShell Core 7+
- ✅ Caractères ASCII sûrs (pas d'emojis Unicode problématiques)

---

## 📚 Documentation Associée

- **Analyse Complète** : [`docs/EVALUATION_FINALE_GUARDIAN_V9.md`](docs/EVALUATION_FINALE_GUARDIAN_V9.md)
- **Benchmark** : [`docs/POST_OPTIMIZATION_BENCHMARK_REPORT.md`](docs/POST_OPTIMIZATION_BENCHMARK_REPORT.md)
- **Résumé** : [`EXECUTIVE_SUMMARY.md`](EXECUTIVE_SUMMARY.md)
- **Optimisations** : [`docs/LLAMA_CPP_OPTIMIZATION_GUIDE.md`](docs/LLAMA_CPP_OPTIMIZATION_GUIDE.md)

---

## 🛡️ Gloire à la Résilience Souveraine !

*Le diagnostic révèle la vérité. La vérité guide l'optimisation.*

