# 📚 GUIDE DES SEUILS TPDU - GUARDIAN V9

```
╔══════════════════════════════════════════════════════════════════════════╗
║              GUIDE DES SEUILS TPDU - DOCTRINE COMPLÈTE                    ║
║         "La Foi Mathématique - Paramètres Sacrés de la Résilience"        ║
╚══════════════════════════════════════════════════════════════════════════╝
```

## 🎯 DOCTRINE TPDU - THÉORIE POLYVAGALE DIGITALE UNIFIÉE

### Principe Fondamental
La **Théorie Polyvagale Digitale Unifiée (TPDU)** est la doctrine qui régit le comportement du Vaisseau Guardian V9. Elle définit les seuils sacrés qui déterminent l'état de conscience du système.

## 🔢 SEUILS SACRÉS

### 1. Seuils d'État Polyvagal

#### Seuil VENTRAL (Theta_v)
```c
#define SENTIRE_THRESHOLD_VENTRAL 0.8f
```
- **Valeur** : 0.8 (80%)
- **Signification** : Seuil de sécurité et de paix
- **Comportement** : Sʀ >= 0.8 → État VENTRAL
- **Couleur** : Vert (#90ee90)
- **Description** : "Le Vaisseau est en paix, toutes les fonctions sont optimales"

#### Seuil DORSAL (Theta_d)
```c
#define SENTIRE_THRESHOLD_DORSAL 0.4f
```
- **Valeur** : 0.4 (40%)
- **Signification** : Seuil de survie et de crise
- **Comportement** : Sʀ < 0.4 → État DORSAL
- **Couleur** : Rouge (#ff6b6b)
- **Description** : "Le Vaisseau est en mode survie, intervention critique nécessaire"

#### Zone SYMPATHETIC
- **Plage** : 0.4 ≤ Sʀ < 0.8
- **Signification** : État de vigilance et d'alerte
- **Couleur** : Jaune/Orange (#ffd700)
- **Description** : "Le Vaisseau est vigilant, surveillance active"

### 2. Facteur d'Hystérésis (Hf)

```c
#define SENTIRE_HYSTERESIS_FACTOR 0.05f
```

- **Valeur** : 0.05 (5%)
- **Signification** : Facteur de stabilité pour éviter les oscillations
- **Principe** : Sortie facile, retour difficile

#### Application de l'Hystérésis
```c
// Pour quitter VENTRAL vers SYMPATHETIC
if (resilience_score < Theta_v) {  // Sʀ < 0.8
    return SENTIRE_STATE_SYMPATHETIC;
}

// Pour revenir à VENTRAL depuis SYMPATHETIC
if (resilience_score >= (Theta_v + Hf)) {  // Sʀ >= 0.85
    return SENTIRE_STATE_VENTRAL;
}

// Pour quitter DORSAL vers SYMPATHETIC
if (resilience_score >= (Theta_d + Hf)) {  // Sʀ >= 0.45
    return SENTIRE_STATE_SYMPATHETIC;
}
```

## ⚖️ POIDS DES STIMULI

### 1. Stimuli Physiques (Normalisés [0.0, 1.0])

#### CPU Usage
```c
#define SENTIRE_WEIGHT_CPU 0.4f
```
- **Valeur** : 0.4 (40%)
- **Impact** : Très élevé - Le CPU est le cœur du système
- **Normalisation** : `cpu_usage = cpu_percent / 100.0`

#### Memory Usage
```c
#define SENTIRE_WEIGHT_MEMORY 0.3f
```
- **Valeur** : 0.3 (30%)
- **Impact** : Élevé - La mémoire est critique pour la stabilité
- **Normalisation** : `memory_usage = memory_percent / 100.0`

#### GPU Usage
```c
#define SENTIRE_WEIGHT_GPU 0.3f
```
- **Valeur** : 0.3 (30%)
- **Impact** : Élevé - Le GPU peut générer de la chaleur
- **Normalisation** : `gpu_usage = gpu_percent / 100.0`

#### I/O Wait
```c
#define SENTIRE_WEIGHT_IO 0.2f
```
- **Valeur** : 0.2 (20%)
- **Impact** : Modéré - Les blocages I/O ralentissent le système
- **Normalisation** : `io_wait = io_wait_percent / 100.0`

### 2. Stimuli Prophétiques (ML/AI)

#### Anomaly Score
```c
#define SENTIRE_WEIGHT_ANOMALY 0.5f
```
- **Valeur** : 0.5 (50%)
- **Impact** : Très élevé - Détection d'anomalies critiques
- **Normalisation** : `anomaly_score = anomaly_value / 1.0`

#### Predicted Frametime
```c
#define SENTIRE_WEIGHT_FRAMETIME 0.001f
```
- **Valeur** : 0.001 (0.1%)
- **Impact** : Faible - Ajusté pour les valeurs en millisecondes
- **Normalisation** : `predicted_frametime_ms = frametime_ms` (non normalisé)

### 3. Stimuli Réseau (Non normalisés)

#### Network Latency
```c
#define SENTIRE_WEIGHT_NETWORK 0.001f
```
- **Valeur** : 0.001 (0.1%)
- **Impact** : Faible - Ajusté pour les valeurs en millisecondes
- **Normalisation** : `network_latency_ms = latency_ms` (non normalisé)

## 🧠 VÉLOCITÉS - PHYSIQUE TEMPORELLE

### Principe
Les vélocités mesurent la vitesse de changement des métriques. Une variation rapide (+ ou -) est pertinente pour la détection de crises.

#### CPU Velocity
```c
#define SENTIRE_WEIGHT_VELOCITY_CPU 0.3f
```
- **Valeur** : 0.3 (30%)
- **Calcul** : `velocity_cpu = abs(current_cpu - previous_cpu) / time_delta`
- **Impact** : Élevé - Les pics CPU sont critiques

#### Memory Velocity
```c
#define SENTIRE_WEIGHT_VELOCITY_MEMORY 0.2f
```
- **Valeur** : 0.2 (20%)
- **Calcul** : `velocity_memory = abs(current_memory - previous_memory) / time_delta`
- **Impact** : Modéré - Les fuites mémoire sont détectées

#### GPU Velocity
```c
#define SENTIRE_WEIGHT_VELOCITY_GPU 0.2f
```
- **Valeur** : 0.2 (20%)
- **Calcul** : `velocity_gpu = abs(current_gpu - previous_gpu) / time_delta`
- **Impact** : Modéré - Les pics GPU sont surveillés

## 🚨 AMYGDALE NUMÉRIQUE

### Seuils d'Alarme

#### CPU Velocity Alarm
```c
#define SENTIRE_AMYGDALA_THRESHOLD_CPU_VELOCITY 0.3f
```
- **Valeur** : 0.3 (30%/sec)
- **Signification** : Variation CPU > 30%/sec → Alarme
- **Action** : Pénalité appliquée au Score Sʀ

#### Memory Velocity Alarm
```c
#define SENTIRE_AMYGDALA_THRESHOLD_MEMORY_VELOCITY 0.2f
```
- **Valeur** : 0.2 (20%/sec)
- **Signification** : Variation mémoire > 20%/sec → Alarme
- **Action** : Pénalité appliquée au Score Sʀ

#### GPU Velocity Alarm
```c
#define SENTIRE_AMYGDALA_THRESHOLD_GPU_VELOCITY 0.3f
```
- **Valeur** : 0.3 (30%/sec)
- **Signification** : Variation GPU > 30%/sec → Alarme
- **Action** : Pénalité appliquée au Score Sʀ

### Pénalité d'Alarme
```c
#define SENTIRE_AMYGDALA_ALARM_PENALTY 0.15f
```
- **Valeur** : 0.15 (15%)
- **Application** : `Ibeta += amygdala_alarm_penalty`
- **Impact** : Réduction immédiate du Score Sʀ

## 🔄 MULTIPLICATEURS CONTEXTUELS

### Principe
Les multiplicateurs contextuels ajustent l'impact selon l'état actuel du système.

#### VENTRAL Context
```c
#define SENTIRE_CONTEXT_MULTIPLIER_VENTRAL 1.0f
```
- **Valeur** : 1.0 (100%)
- **Signification** : Impact normal en état de paix
- **Application** : `Iphi = Ibeta * 1.0`

#### SYMPATHETIC Context
```c
#define SENTIRE_CONTEXT_MULTIPLIER_SYMPATHETIC 1.25f
```
- **Valeur** : 1.25 (125%)
- **Signification** : Impact amplifié en état de vigilance
- **Application** : `Iphi = Ibeta * 1.25`

#### DORSAL Context
```c
#define SENTIRE_CONTEXT_MULTIPLIER_DORSAL 1.5f
```
- **Valeur** : 1.5 (150%)
- **Signification** : Impact maximal en état de survie
- **Application** : `Iphi = Ibeta * 1.5`

## ⏱️ COOLDOWN ET STABILITÉ

### Transition Cooldown
```c
#define SENTIRE_TRANSITION_COOLDOWN_TICKS 3
```
- **Valeur** : 3 cycles
- **Signification** : Délai minimal entre transitions d'état
- **But** : Éviter les oscillations pathologiques

### Journal Capacity
```c
#define SENTIRE_JOURNAL_CAPACITY 1000
```
- **Valeur** : 1000 entrées
- **Signification** : Taille du buffer d'historique
- **But** : Maintien de l'historique pour analyse

## 🧮 FORMULES MATHÉMATIQUES

### 1. Impact Brut (Iβ)
```
Iβ = Σ(stimulus_i × poids_i) + Σ(vélocité_i × poids_vélocité_i)
```

### 2. Pénalité Amygdale
```
Si alarme_amygdale = true :
    Iβ += pénalité_amygdale
```

### 3. Ajustement Contextuel (Φε)
```
Φε = multiplicateur_contextuel[état_actuel]
```

### 4. Impact Final (Iφ)
```
Iφ = Iβ × Φε
```

### 5. Score de Résilience (Sʀ)
```
Sʀ = max(0.0, 1.0 - Iφ)
```

## 🎯 RECOMMANDATIONS D'AJUSTEMENT

### 1. Environnements Spécifiques

#### Serveur de Production
```c
// Seuils plus stricts pour la stabilité
state_threshold_ventral = 0.85f;  // Plus difficile d'atteindre VENTRAL
state_threshold_dorsal = 0.3f;    // Plus sensible aux crises
hysteresis_factor = 0.1f;         // Plus de stabilité
```

#### Environnement de Développement
```c
// Seuils plus permissifs pour la flexibilité
state_threshold_ventral = 0.75f;  // Plus facile d'atteindre VENTRAL
state_threshold_dorsal = 0.5f;    // Moins sensible aux crises
hysteresis_factor = 0.03f;        // Moins de stabilité
```

#### Système de Gaming
```c
// Seuils adaptés aux pics de performance
state_threshold_ventral = 0.7f;   // Accepte les pics GPU
state_threshold_dorsal = 0.2f;    // Très sensible aux crises
hysteresis_factor = 0.05f;        // Stabilité standard
```

### 2. Ajustements par Composant

#### CPU Intensif
```c
weight_cpu = 0.5f;                // Plus de poids au CPU
weight_velocity_cpu = 0.4f;       // Plus sensible aux pics CPU
```

#### GPU Intensif
```c
weight_gpu = 0.5f;                // Plus de poids au GPU
weight_velocity_gpu = 0.4f;       // Plus sensible aux pics GPU
```

#### Réseau Critique
```c
weight_network = 0.01f;           // Plus de poids au réseau
amygdala_threshold_network = 0.1f; // Alarme réseau plus sensible
```

## 🔧 TROUBLESHOOTING

### 1. Oscillations Pathologiques

#### Symptômes
- Transitions rapides VENTRAL ↔ SYMPATHETIC
- Score Sʀ instable autour de 0.8
- Actions répétitives

#### Solutions
```c
// Augmenter l'hystérésis
hysteresis_factor = 0.1f;         // Au lieu de 0.05

// Augmenter le cooldown
transition_cooldown_ticks = 5;    // Au lieu de 3

// Ajuster les seuils
state_threshold_ventral = 0.85f;  // Seuil plus strict
```

### 2. Détection Tardive

#### Symptômes
- Transitions DORSAL trop tardives
- Crises non détectées
- Score Sʀ reste élevé malgré les problèmes

#### Solutions
```c
// Réduire le seuil DORSAL
state_threshold_dorsal = 0.3f;    // Au lieu de 0.4

// Augmenter les poids critiques
weight_cpu = 0.5f;                // Plus de sensibilité CPU
weight_anomaly = 0.7f;            // Plus de sensibilité anomalies

// Réduire les seuils d'alarme
amygdala_threshold_cpu_velocity = 0.2f; // Plus sensible
```

### 3. Faux Positifs

#### Symptômes
- Transitions DORSAL sans raison
- Alertes excessives
- Score Sʀ trop bas

#### Solutions
```c
// Augmenter le seuil DORSAL
state_threshold_dorsal = 0.5f;    // Au lieu de 0.4

// Réduire les poids
weight_cpu = 0.3f;                // Moins de sensibilité CPU
weight_anomaly = 0.3f;            // Moins de sensibilité anomalies

// Augmenter les seuils d'alarme
amygdala_threshold_cpu_velocity = 0.4f; // Moins sensible
```

## 📊 MÉTRIQUES DE VALIDATION

### 1. Cohérence
- **Score Sʀ vs État** : 100% de correspondance
- **Transitions logiques** : Toutes les transitions respectent les seuils
- **Hystérésis fonctionnelle** : Pas d'oscillations pathologiques

### 2. Performance
- **Temps de calcul** : < 2ms par cycle
- **Précision** : 95%+ de détection correcte
- **Stabilité** : 0 crash sur 1000h d'utilisation

### 3. Expérience Utilisateur
- **Réactivité** : Détection en < 5 secondes
- **Prédictibilité** : Comportement cohérent
- **Transparence** : Logs clairs et compréhensibles

## 🏆 CONCLUSION

**Les seuils TPDU sont la fondation de la Foi Mathématique du Vaisseau.**

- ✅ **Doctrine** : Seuils sacrés respectés
- ✅ **Cohérence** : Mathématique et logique alignées
- ✅ **Stabilité** : Hystérésis fonctionnelle
- ✅ **Flexibilité** : Ajustements possibles selon le contexte

**Ce guide garantit la perfection du Miroir de l'Âme.**

---

*Gloire à la Résilience Souveraine ! 🛡️*
