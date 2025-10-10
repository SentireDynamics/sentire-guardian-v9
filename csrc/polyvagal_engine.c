/*
 * ******************************************************************************
 * *                    SENTIRE CORE SDK V2                                     *
 * *           Le Moteur Polyvagal - Le Juge de la Résilience                   *
 * ******************************************************************************
 * 
 * POURQUOI : Le Saint des Saints. Le Moteur Polyvagal est le siège de la décision
 * finale. Il calcule l'Impact, le Score de Résilience, et détermine l'état
 * polyvagal du Vaisseau.
 * 
 * DOCTRINE (TPDU Section IV) :
 * 
 * 1. IMPACT BRUT (Ibeta) :
 *    Ibeta = SUM (stimulus_i * poids_i) + SUM (velocite_i * poids_velocite_i)
 * 
 * 2. PENALITE AMYGDALE :
 *    Si alarme levée : Ibeta += penalite
 * 
 * 3. AJUSTEMENT CONTEXTUEL (Phi_epsilon) :
 *    - VENTRAL : Phi_epsilon = 1.0
 *    - SYMPATHETIC : Phi_epsilon = 1.25
 *    - DORSAL : Phi_epsilon = 1.5
 * 
 * 4. IMPACT FINAL (Iphi) :
 *    Iphi = Ibeta * Phi_epsilon
 * 
 * 5. SCORE DE RESILIENCE (Sr) :
 *    Sr = max(0.0, 1.0 - Iphi)
 * 
 * 6. MACHINE D'ETAT avec HYSTERESIS :
 *    - VENTRAL <-> SYMPATHETIC : seuil Theta_v +/- Hf
 *    - SYMPATHETIC <-> DORSAL : seuil Theta_d +/- Hf
 *    - COOLDOWN : délai minimal entre transitions
 */

#include "sentire_core_internal.h"
#include <math.h> // Pour fabsf et fmaxf

/* *******************************************************************************
 * HELPER : Calcule l'Ajustement Contextuel (Phi_epsilon)
 * ******************************************************************************* */
static float get_context_multiplier(const sentire_internal_state_t* state) {
    switch (state->current_state) {
        case SENTIRE_STATE_VENTRAL:
            return state->config.context_multiplier_ventral;
        case SENTIRE_STATE_SYMPATHETIC:
            return state->config.context_multiplier_sympathetic;
        case SENTIRE_STATE_DORSAL:
            return state->config.context_multiplier_dorsal;
        default:
            return 1.0f;
    }
}

/* *******************************************************************************
 * HELPER : Détermine le Nouvel État avec Hystérésis
 * *******************************************************************************
 * ALGORITHME :
 * - Si en COOLDOWN : pas de transition
 * - Sinon : applique les seuils avec hystérésis selon l'état actuel
 */
static sentire_state_t determine_new_state(
    const sentire_internal_state_t* state,
    float resilience_score
) {
    sentire_state_t current = state->current_state;
    float Theta_v = state->config.state_threshold_ventral;
    float Theta_d = state->config.state_threshold_dorsal;
    float Hf = state->config.hysteresis_factor;
    
    // Cooldown actif : pas de transition
    if (state->cooldown_ticks > 0) {
        return current;
    }
    
    // --- Machine d'Etat avec Hysteresis ---
    switch (current) {
        case SENTIRE_STATE_VENTRAL:
            // Pour quitter VENTRAL vers SYMPATHETIC : Sr < Theta_v - Hf
            if (resilience_score < (Theta_v - Hf)) {
                if (resilience_score < Theta_d) {
                    return SENTIRE_STATE_DORSAL;
                }
                return SENTIRE_STATE_SYMPATHETIC;
            }
            return SENTIRE_STATE_VENTRAL;
            
        case SENTIRE_STATE_SYMPATHETIC:
            // Pour monter vers VENTRAL : Sr >= Theta_v + Hf
            if (resilience_score >= (Theta_v + Hf)) {
                return SENTIRE_STATE_VENTRAL;
            }
            // Pour descendre vers DORSAL : Sr < Theta_d - Hf
            if (resilience_score < (Theta_d - Hf)) {
                return SENTIRE_STATE_DORSAL;
            }
            return SENTIRE_STATE_SYMPATHETIC;
            
        case SENTIRE_STATE_DORSAL:
            // Pour quitter DORSAL vers SYMPATHETIC : Sr >= Theta_d + Hf
            if (resilience_score >= (Theta_d + Hf)) {
                if (resilience_score >= Theta_v) {
                    return SENTIRE_STATE_VENTRAL;
                }
                return SENTIRE_STATE_SYMPATHETIC;
            }
            return SENTIRE_STATE_DORSAL;
            
        default:
            return SENTIRE_STATE_SYMPATHETIC; // Fallback sur
    }
}

/* *******************************************************************************
 * polyvagal_engine_process - Rituel du Jugement Suprême
 * ******************************************************************************* */
void polyvagal_engine_process(
    sentire_internal_state_t* state,
    const sentire_stimulus_t* stimulus
) {
    if (!state || !stimulus) {
        return;
    }
    
    const sentire_config_t* cfg = &state->config;
    
    /* -----------------------------------------------------------------------
     * ETAPE 1 : Calcul de l'Impact Brut (Ibeta)
     * ----------------------------------------------------------------------- */
    float Ibeta = 0.0f;
    
    // Contribution des stimuli physiques
    Ibeta += stimulus->cpu_usage * cfg->weight_cpu;
    Ibeta += stimulus->memory_usage * cfg->weight_memory;
    Ibeta += stimulus->gpu_usage * cfg->weight_gpu;
    Ibeta += stimulus->io_wait * cfg->weight_io;
    Ibeta += stimulus->network_latency_ms * cfg->weight_network;
    Ibeta += stimulus->thread_contention * cfg->weight_threads;
    Ibeta += stimulus->disk_io_rate * cfg->weight_disk;
    Ibeta += stimulus->power_consumption * cfg->weight_power;
    
    // Contribution des stimuli prophétiques
    Ibeta += stimulus->anomaly_score * cfg->weight_anomaly;
    Ibeta += stimulus->predicted_frametime_ms * cfg->weight_frametime;
    
    // Contribution des velocites (physique temporelle)
    // On utilise la valeur absolue car une variation rapide (+ ou -) est pertinente
    Ibeta += fabsf(state->velocities.cpu) * cfg->weight_velocity_cpu;
    Ibeta += fabsf(state->velocities.memory) * cfg->weight_velocity_memory;
    Ibeta += fabsf(state->velocities.gpu) * cfg->weight_velocity_gpu;
    Ibeta += fabsf(state->velocities.io) * cfg->weight_velocity_io;
    
    /* -----------------------------------------------------------------------
     * ETAPE 2 : Penalite de l'Amygdale
     * ----------------------------------------------------------------------- */
    if (state->amygdala.alarm_fired) {
        Ibeta += cfg->amygdala_alarm_penalty;
    }
    
    state->last_impact_base = Ibeta;
    
    /* -----------------------------------------------------------------------
     * ETAPE 3 : Ajustement Contextuel (Phi_epsilon)
     * ----------------------------------------------------------------------- */
    float Phi_epsilon = get_context_multiplier(state);
    
    /* -----------------------------------------------------------------------
     * ETAPE 4 : Impact Final (Iphi)
     * ----------------------------------------------------------------------- */
    float Iphi = Ibeta * Phi_epsilon;
    state->last_impact_score = Iphi;
    
    /* -----------------------------------------------------------------------
     * ETAPE 5 : Score de Resilience (Sr)
     * ----------------------------------------------------------------------- */
    float Sr = fmaxf(0.0f, 1.0f - Iphi);
    state->last_resilience_score = Sr;
    
    /* -----------------------------------------------------------------------
     * ETAPE 6 : Machine d'Etat avec Hysteresis
     * ----------------------------------------------------------------------- */
    sentire_state_t old_state = state->current_state;
    sentire_state_t new_state = determine_new_state(state, Sr);
    
    // Transition detectee
    if (new_state != old_state) {
        state->current_state = new_state;
        // Reinitialise le cooldown
        state->cooldown_ticks = cfg->transition_cooldown_ticks;
    } else {
        // Decremente le cooldown si actif
        if (state->cooldown_ticks > 0) {
            state->cooldown_ticks--;
        }
    }
}