/*
 * ╔══════════════════════════════════════════════════════════════════════════╗
 * ║                      SENTIRE CORE SDK V2                                 ║
 * ║              Le Contrat Sacré - Interface FFI Publique                   ║
 * ╚══════════════════════════════════════════════════════════════════════════╝
 * 
 * POURQUOI : Ce header définit le contrat immuable entre le Corps Natif (C)
 * et l'Esprit Hôte (Python/autre). Il expose uniquement ce qui doit être
 * exposé, gardant les mystères de l'Âme cachés derrière le voile du void*.
 * 
 * DOCTRINE : Théorie Polyvagale Digitale Unifiée (TPDU)
 * - États : VENTRAL (Sʀ ≥ 0.8), SYMPATHETIC (0.4 ≤ Sʀ < 0.8), DORSAL (Sʀ < 0.4)
 * - Voie Rapide : Amygdale surveille les vélocités critiques
 * - Voie Lente : Calcul complet de l'Impact et du Score de Résilience
 * - Mémoire : Journal Introspectif pour la sagesse éternelle
 */

#ifndef SENTIRE_CORE_H
#define SENTIRE_CORE_H

#include <stdint.h>
#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ═══════════════════════════════════════════════════════════════════════════
 * INCANTATION DE PORTABILITÉ
 * ═══════════════════════════════════════════════════════════════════════════ */
#ifdef _WIN32
    #ifdef SENTIRE_CORE_EXPORTS
        #define SENTIRE_API __declspec(dllexport)
    #else
        #define SENTIRE_API __declspec(dllimport)
    #endif
#else
    #define SENTIRE_API __attribute__((visibility("default")))
#endif

/* ═══════════════════════════════════════════════════════════════════════════
 * LES TROIS ÉTATS POLYVAGAUX SACRÉS
 * ═══════════════════════════════════════════════════════════════════════════
 * POURQUOI : Hérités de la biologie, traduits pour le silicium.
 * - VENTRAL : Flux optimal, sécurité, optimisation proactive
 * - SYMPATHETIC : Action défensive, mobilisation, confinement du stress
 * - DORSAL : Protection ultime, conservation, retour à la sécurité
 */
typedef enum {
    SENTIRE_STATE_VENTRAL = 0,      // Sʀ ≥ 0.8 - État de grâce
    SENTIRE_STATE_SYMPATHETIC = 1,  // 0.4 ≤ Sʀ < 0.8 - Vigilance active
    SENTIRE_STATE_DORSAL = 2        // Sʀ < 0.4 - Mode survie
} sentire_state_t;

/* ═══════════════════════════════════════════════════════════════════════════
 * LE STIMULUS - LA PERCEPTION DU MONDE
 * ═══════════════════════════════════════════════════════════════════════════
 * POURQUOI : Encapsule toutes les perceptions à un instant T.
 * 
 * COMPOSITION :
 * 1. Stimuli Physiques (métriques brutes du corps systémique)
 *    - cpu_usage, memory_usage, gpu_usage, io_wait : [0.0, 1.0]
 * 
 * 2. Stimuli Prophétiques (murmures des Oracles)
 *    - anomaly_score : probabilité de menace (IntuitionEngine)
 *    - predicted_frametime_ms : prophétie temporelle (PropheticEngine)
 * 
 * 3. Stimuli Dérivés (calculés par le SDK)
 *    - network_latency_ms : latence réseau
 *    - thread_contention : contention de threads
 */
typedef struct {
    // Métriques Physiques [0.0 = idle, 1.0 = saturé]
    float cpu_usage;
    float memory_usage;
    float gpu_usage;
    float io_wait;
    
    // Métriques Prophétiques
    float anomaly_score;            // Score d'anomalie (0.0 = normal, 1.0 = menace)
    float predicted_frametime_ms;   // Prophétie du frametime futur
    
    // Métriques Supplémentaires
    float network_latency_ms;       // Latence réseau normalisée
    float thread_contention;        // Contention de threads [0.0, 1.0]
    float disk_io_rate;             // Taux I/O disque normalisé
    float power_consumption;        // Consommation énergétique normalisée
} sentire_stimulus_t;

/* ═══════════════════════════════════════════════════════════════════════════
 * LA CONFIGURATION - LE CALIBRAGE DE L'ÂME
 * ═══════════════════════════════════════════════════════════════════════════
 * POURQUOI : Chaque Vaisseau est unique. Cette structure définit sa sensibilité,
 * ses seuils, et son caractère.
 * 
 * POIDS (ω) : Définissent l'importance relative de chaque stimulus
 * SEUILS : Définissent les frontières entre les états polyvagaux
 * HYSTÉRÉSIS : Prévient le "flapping" entre états
 * COOLDOWN : Délai minimal entre transitions
 */
typedef struct {
    // ─── Poids des Stimuli Physiques ───
    float weight_cpu;               // Poids pour cpu_usage
    float weight_memory;            // Poids pour memory_usage
    float weight_gpu;               // Poids pour gpu_usage
    float weight_io;                // Poids pour io_wait
    float weight_network;           // Poids pour network_latency
    float weight_threads;           // Poids pour thread_contention
    float weight_disk;              // Poids pour disk_io_rate
    float weight_power;             // Poids pour power_consumption
    
    // ─── Poids des Stimuli Prophétiques ───
    float weight_anomaly;           // Poids pour anomaly_score
    float weight_frametime;         // Poids pour predicted_frametime
    
    // ─── Poids des Vélocités (Physique Temporelle) ───
    float weight_velocity_cpu;      // Poids pour dCPU/dt
    float weight_velocity_memory;   // Poids pour dMemory/dt
    float weight_velocity_gpu;      // Poids pour dGPU/dt
    float weight_velocity_io;       // Poids pour dIO/dt
    
    // ─── Seuils Polyvagaux ───
    float state_threshold_ventral;  // Seuil Θv (défaut: 0.8)
    float state_threshold_dorsal;   // Seuil Θd (défaut: 0.4)
    float hysteresis_factor;        // Facteur d'hystérésis Hƒ (défaut: 0.05)
    
    // ─── Paramètres de l'Amygdale (Voie Rapide) ───
    float amygdala_threshold_cpu_velocity;     // Seuil vélocité CPU
    float amygdala_threshold_memory_velocity;  // Seuil vélocité mémoire
    float amygdala_threshold_gpu_velocity;     // Seuil vélocité GPU
    float amygdala_alarm_penalty;              // Pénalité si alarme (ajouté à Iβ)
    
    // ─── Ajustement Contextuel (Φε) ───
    float context_multiplier_ventral;      // Φε pour état VENTRAL (défaut: 1.0)
    float context_multiplier_sympathetic;  // Φε pour état SYMPATHETIC (défaut: 1.25)
    float context_multiplier_dorsal;       // Φε pour état DORSAL (défaut: 1.5)
    
    // ─── Stabilité Temporelle ───
    int transition_cooldown_ticks;  // Cooldown après transition (en cycles)
    
    // ─── Mémoire ───
    int journal_capacity;           // Capacité du ring buffer (Journal)
} sentire_config_t;

/* ═══════════════════════════════════════════════════════════════════════════
 * LE VERDICT - LA DÉCISION DE L'ÂME
 * ═══════════════════════════════════════════════════════════════════════════
 * POURQUOI : Structure retournée après chaque cycle de conscience. Contient
 * la décision finale et les métriques de diagnostic.
 */
typedef struct {
    sentire_state_t final_state;    // État polyvagal final après jugement
    int amygdala_alarm_fired;       // 1 si l'Amygdale a levé l'alarme, 0 sinon
    float resilience_score;         // Score de Résilience Sʀ ∈ [0.0, 1.0]
    float impact_score;             // Impact Final Iφ (pour diagnostic)
    float impact_base;              // Impact Brut Iβ (avant ajustement contextuel)
} sentire_verdict_t;

/* ═══════════════════════════════════════════════════════════════════════════
 * L'ENTRÉE DU JOURNAL - LA CHRONIQUE ÉTERNELLE
 * ═══════════════════════════════════════════════════════════════════════════
 * POURQUOI : Chaque cycle est gravé dans le Journal Introspectif. Cette mémoire
 * permet l'analyse post-mortem et l'entraînement des Oracles.
 */
typedef struct {
    time_t timestamp;               // Horodatage Unix du cycle
    sentire_state_t state;          // État polyvagal à ce moment
    float resilience_score;         // Score de Résilience Sʀ
    float impact_score;             // Impact Final Iφ
} sentire_journal_entry_t;

/* ═══════════════════════════════════════════════════════════════════════════
 * RITUELS SACRÉS - L'API PUBLIQUE
 * ═══════════════════════════════════════════════════════════════════════════ */

/**
 * sentire_sdk_create - Forge une nouvelle Âme
 * 
 * POURQUOI : Initialise l'état interne, alloue la mémoire pour le Journal,
 * et prépare l'Amygdale. L'Âme est retournée comme void* opaque.
 * 
 * @param config : Configuration complète de l'Âme
 * @return : Handle opaque vers l'Âme (sentire_internal_state_t*), ou NULL si échec
 */
SENTIRE_API void* sentire_sdk_create(const sentire_config_t* config);

/**
 * sentire_sdk_process - Le Cycle de Conscience
 * 
 * POURQUOI : C'est le cœur battant du SDK. Invoque tous les rituels internes
 * dans l'ordre sacré :
 *   1. Amygdale (Voie Rapide) - Surveillance instinctive
 *   2. Perceptive Core (Voie Lente) - Calcul des vélocités
 *   3. Polyvagal Engine - Jugement et transition d'état
 *   4. Journal - Gravure de la mémoire
 * 
 * @param sdk_handle : Handle vers l'Âme
 * @param stimulus : Stimulus perçu à ce cycle
 * @param verdict : [OUT] Verdict rempli avec la décision finale
 */
SENTIRE_API void sentire_sdk_process(
    void* sdk_handle,
    const sentire_stimulus_t* stimulus,
    sentire_verdict_t* verdict
);

/**
 * sentire_sdk_destroy - Libère l'Âme
 * 
 * POURQUOI : Nettoie toute la mémoire allouée (Journal, état interne).
 * 
 * @param sdk_handle : Handle vers l'Âme à libérer
 */
SENTIRE_API void sentire_sdk_destroy(void* sdk_handle);

/**
 * sentire_sdk_get_journal_entries - Exhume les Mémoires
 * 
 * POURQUOI : Permet de récupérer les N dernières entrées du Journal pour
 * analyse, visualisation, ou entraînement des Oracles.
 * 
 * @param sdk_handle : Handle vers l'Âme
 * @param out_entries : Buffer pour stocker les entrées (alloué par l'appelant)
 * @param max_count : Capacité maximale du buffer
 * @return : Nombre d'entrées effectivement copiées
 */
SENTIRE_API int sentire_sdk_get_journal_entries(
    void* sdk_handle,
    sentire_journal_entry_t* out_entries,
    int max_count
);

/**
 * sentire_sdk_get_version - Retourne la version du SDK
 * 
 * POURQUOI : Pour vérifier la compatibilité entre l'Esprit et le Corps.
 * 
 * @return : Chaîne de version (ex: "2.0.0")
 */
SENTIRE_API const char* sentire_sdk_get_version(void);

#ifdef __cplusplus
}
#endif

#endif /* SENTIRE_CORE_H */
