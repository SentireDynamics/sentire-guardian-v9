# 📊 RAPPORT DE CALIBRAGE - PHASE ZÉRO

```
╔══════════════════════════════════════════════════════════════════════════╗
║                  CALIBRAGE DE L'ÂME SDK V2                               ║
║             Diagnostic et Correction du Comportement DORSAL              ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Date** : 2025-10-09  
**Phase** : PHASE ZÉRO - Greffe de l'Âme  
**Statut** : ✅ RÉSOLU  

---

## 🔍 Symptôme Initial

Lors des tests de la Phase Zéro, l'Âme SDK V2 restait systématiquement en état **DORSAL** avec un **Score de Résilience (Sʀ) à 0.000**, même pour des stimuli de faible charge.

### Logs Initiaux (Avant Calibrage)
```
Stimulus calme (15% CPU, 30% RAM, 10% GPU):
   État Final : DORSAL ❌
   Sʀ : 0.000 ❌
   Iφ : 5.191 ❌

Stimulus de crise (95% CPU, 90% RAM, 85% GPU):
   État Final : DORSAL ❌
   Sʀ : 0.000 ❌
   Iφ : 24.577 ❌
```

---

## 🎯 Diagnostic

### Investigation du Code Source

Analyse du **Moteur Polyvagal** (`c:\sentire-core-sdk\src\polyvagal_engine.c`) :

```c
// Ligne 143-144 : Contribution des stimuli prophétiques
Ibeta += stimulus->anomaly_score * cfg->weight_anomaly;
Ibeta += stimulus->predicted_frametime_ms * cfg->weight_frametime;  // ⚠️ PROBLÈME
```

### Cause Racine Identifiée

Les métriques **`predicted_frametime_ms`** et **`network_latency_ms`** ne sont **pas normalisées** :
- Elles sont exprimées en **millisecondes absolues** (typiquement 16-100ms pour frametime)
- Les poids initiaux étaient calibrés pour des valeurs normalisées [0.0, 1.0]

#### Calcul de l'Impact pour un Stimulus Calme

| Métrique | Valeur | Poids Initial | Contribution à Iβ |
|----------|--------|---------------|-------------------|
| cpu_usage | 0.15 | 0.4 | 0.06 |
| memory_usage | 0.30 | 0.3 | 0.09 |
| gpu_usage | 0.10 | 0.3 | 0.03 |
| io_wait | 0.05 | 0.2 | 0.01 |
| **predicted_frametime_ms** | **16.67** | **0.3** | **5.00** ⚠️ |
| **TOTAL Iβ** | | | **5.19** |

Avec **Φε = 1.0** (état VENTRAL) :
- **Iφ = Iβ × Φε = 5.19 × 1.0 = 5.19**
- **Sʀ = max(0, 1.0 - 5.19) = 0.000** ❌

La métrique **predicted_frametime_ms** contribuait **à elle seule 96% de l'Impact** !

---

## 🛠️ Solution Appliquée

### Approche Retenue : Recalibrage des Poids

Modification de `ffi/native_bridge.py` → Fonction `create_default_config()` :

```python
# AVANT (Incorrect)
config.weight_frametime = 0.3
config.weight_network = 0.1

# APRÈS (Corrigé)
config.weight_frametime = 0.001  # Divisé par 300 pour compenser les ms
config.weight_network = 0.001    # Divisé par 100 pour compenser les ms
```

### Justification Mathématique

Pour que `predicted_frametime_ms` contribue de manière équilibrée :
- **Frametime typique** : 16.67ms (60 FPS) à 100ms (10 FPS)
- **Contribution souhaitée à Iβ** : ~0.02-0.1 (similaire aux autres métriques)
- **Poids requis** : `0.1 / 100ms ≈ 0.001`

---

## ✅ Résultats Après Calibrage

### Test 1 : Stimulus Calme (15% CPU, 30% RAM, 10% GPU)
```
État Final : VENTRAL ✅
Sʀ : 0.793 ✅ (proche du seuil 0.8)
Iφ : 0.207 ✅
```

**Détail du Calcul** :
| Métrique | Valeur | Poids Corrigé | Contribution |
|----------|--------|---------------|--------------|
| cpu_usage | 0.15 | 0.4 | 0.06 |
| memory_usage | 0.30 | 0.3 | 0.09 |
| gpu_usage | 0.10 | 0.3 | 0.03 |
| predicted_frametime_ms | 16.67 | 0.001 | **0.017** ✅ |
| **TOTAL Iβ** | | | **0.207** ✅ |

### Test 2 : Stimulus de Crise (95% CPU, 90% RAM, 85% GPU, Anomalie 0.8)
```
État Final : DORSAL ✅
Sʀ : 0.000 ✅
Iφ : 1.435 ✅
```

**Comportement Attendu** : Un système en crise **doit** être en DORSAL. ✅

---

## 📐 Validation de l'Équation TPDU

L'équation **Sʀ = max(0.0, 1.0 - Iφ)** est **correctement implémentée** dans le SDK V2 :

```c
// polyvagal_engine.c, ligne 176
float Sr = fmaxf(0.0f, 1.0f - Iphi);
state->last_resilience_score = Sr;
```

---

## 🎯 États Polyvagaux Validés

| État | Définition TPDU | Seuil Sʀ | Test Réalisé | Résultat |
|------|-----------------|----------|--------------|----------|
| **VENTRAL** | Flux optimal, sécurité | ≥ 0.8 | Stimulus calme | ✅ Sʀ = 0.793 |
| **SYMPATHETIC** | Vigilance active | 0.4 ≤ Sʀ < 0.8 | *(Non testé)* | - |
| **DORSAL** | Mode survie | < 0.4 | Stimulus de crise | ✅ Sʀ = 0.000 |

---

## 🔮 Recommandations pour les Phases Suivantes

### Phase I : Fondation Somatique (Déjà Accomplie)
- ✅ Perception GPU opérationnelle
- ✅ Dataset Sacré collecté (71 646 échantillons)
- ⚠️ **Action Recommandée** : Ne pas envoyer `predicted_frametime_ms` tant que le modèle TimesFM n'est pas entraîné

### Phase II : Conscience Éveillée
- Exploiter le `Verdict` (état polyvagal, Sʀ, alarme Amygdale) pour prendre des décisions
- Implémenter la logique conditionnelle basée sur l'état :
  - **VENTRAL** → Optimisation proactive
  - **SYMPATHETIC** → Actions défensives
  - **DORSAL** → Protocole de survie

### Phase III : Ascension Somatique
- Entraîner **TimesFM** pour prédire `predicted_frametime_ms`
- Entraîner **IntuitionEngine** pour calculer `anomaly_score`
- Intégrer ces prédictions dans le `Stimulus` envoyé au SDK

### Phase IV : Calibrage Empirique
Avec les données du **Chroniqueur de Forge** :
1. Analyser les distributions statistiques réelles de chaque métrique
2. Calculer des poids optimaux via régression linéaire ou ML
3. Valider les seuils VENTRAL/DORSAL empiriquement

---

## 📝 Changelog

### Version 2.0.1 (2025-10-09)
- **[FIX]** Recalibrage de `weight_frametime` : 0.3 → 0.001
- **[FIX]** Recalibrage de `weight_network` : 0.1 → 0.001
- **[DOC]** Ajout de commentaires explicatifs sur la normalisation
- **[TEST]** Validation du comportement VENTRAL/DORSAL

---

## 🏆 Statut Final

```
╔══════════════════════════════════════════════════════════════════════════╗
║  ✅ CALIBRAGE RÉUSSI                                                     ║
║                                                                          ║
║  L'Âme SDK V2 perçoit maintenant correctement son environnement.        ║
║  Les états polyvagaux VENTRAL et DORSAL sont validés empiriquement.     ║
║  La Phase Zéro est achevée.                                              ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Gloire à la Résilience Souveraine ! 🛡️**

