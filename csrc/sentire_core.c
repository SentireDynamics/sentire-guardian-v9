/*
 * Sentire Core - Implémentation du Cœur Natif
 * 
 * Épigraphe Doctrinale:
 * Implémentation C du cœur natif du Vaisseau Guardian V9.
 * Orchestration des modules natifs: résilience, machine d'état, journal.
 * 
 * Rôle dans la Résilience Souveraine:
 * - Implémentation de l'API définie dans sentire_core.h
 * - Coordination des modules natifs
 * - Gestion de l'état global du système
 * - Interface FFI vers Python
 */

#include "sentire_core.h"
#include <stdlib.h>
#include <string.h>

/* État global du système */
static ResilienceConfig global_config;
static int initialized = 0;

/* Initialisation du système */
int sentire_init(const ResilienceConfig* config) {
    if (!config) {
        return -1;
    }
    
    memcpy(&global_config, config, sizeof(ResilienceConfig));
    initialized = 1;
    
    return 0;
}

/* Calcul du score de résilience */
double sentire_calculate_resilience(const Stimulus* stimulus, PolyvagalState current_state) {
    if (!initialized || !stimulus) {
        return 0.0;
    }
    
    /* Voir resilience_core.c pour l'implémentation complète */
    double poids = 0.0;
    
    switch (stimulus->type) {
        case STIMULUS_FAULT:
            poids = global_config.poids_fault;
            break;
        case STIMULUS_DRIFT:
            poids = global_config.poids_drift;
            break;
        case STIMULUS_ATTACK:
            poids = global_config.poids_attack;
            break;
    }
    
    double impact_brut = stimulus->intensity * poids;
    
    double sensibilite = 0.0;
    switch (current_state) {
        case STATE_VENTRAL:
            sensibilite = global_config.sensibilite_ventral;
            break;
        case STATE_SYMPATHETIC:
            sensibilite = global_config.sensibilite_sympathetic;
            break;
        case STATE_DORSAL:
            sensibilite = global_config.sensibilite_dorsal;
            break;
    }
    
    double impact_final = impact_brut * sensibilite;
    double resilience_score = 1.0 - impact_final;
    
    if (resilience_score < 0.0) {
        resilience_score = 0.0;
    }
    
    return resilience_score;
}

/* Transition d'état polyvagal */
PolyvagalState sentire_transition_state(PolyvagalState current_state, double resilience_score) {
    if (!initialized) {
        return current_state;
    }
    
    /* Voir statemachine.c pour l'implémentation complète */
    PolyvagalState next_state = current_state;
    
    switch (current_state) {
        case STATE_VENTRAL:
            if (resilience_score < (global_config.seuil_ventral - global_config.hysteresis)) {
                next_state = STATE_SYMPATHETIC;
            }
            break;
            
        case STATE_SYMPATHETIC:
            if (resilience_score >= global_config.seuil_ventral) {
                next_state = STATE_VENTRAL;
            } else if (resilience_score < global_config.seuil_dorsal) {
                next_state = STATE_DORSAL;
            }
            break;
            
        case STATE_DORSAL:
            if (resilience_score >= (global_config.seuil_dorsal + global_config.hysteresis)) {
                next_state = STATE_SYMPATHETIC;
            }
            break;
    }
    
    return next_state;
}

/* Nettoyage */
void sentire_cleanup(void) {
    initialized = 0;
}
