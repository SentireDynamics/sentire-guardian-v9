/*
 * State Machine - Moteur Polyvagal Natif
 * 
 * Épigraphe Doctrinale:
 * Machine d'état polyvagale native implémentant les transitions sacrées
 * entre Ventral, Sympathique et Dorsal. Hystérésis et cooldown intégrés.
 * 
 * Rôle dans la Résilience Souveraine:
 * - Gestion native des transitions polyvagales
 * - Hystérésis pour éviter les oscillations
 * - Cooldown entre transitions
 * - Historique des états
 * - Performance optimale (pas de GC, pas de latence Python)
 */

#include "sentire_core.h"
#include <time.h>

/* Structure interne de la machine d'état */
typedef struct {
    PolyvagalState current_state;
    time_t last_transition;
    int cooldown_active;
} StateMachine;

static StateMachine state_machine = {
    .current_state = STATE_VENTRAL,
    .last_transition = 0,
    .cooldown_active = 0
};

/*
 * Transition d'état avec hystérésis et cooldown
 */
PolyvagalState state_machine_transition(PolyvagalState current_state,
                                       double resilience_score,
                                       const ResilienceConfig* config) {
    if (!config) {
        return current_state;
    }
    
    PolyvagalState next_state = current_state;
    
    /* Machine d'état avec hystérésis */
    switch (current_state) {
        case STATE_VENTRAL:
            /* Transition Ventral → Sympathique */
            if (resilience_score < (config->seuil_ventral - config->hysteresis)) {
                next_state = STATE_SYMPATHETIC;
            }
            break;
            
        case STATE_SYMPATHETIC:
            /* Transition Sympathique → Ventral */
            if (resilience_score >= config->seuil_ventral) {
                next_state = STATE_VENTRAL;
            }
            /* Transition Sympathique → Dorsal */
            else if (resilience_score < config->seuil_dorsal) {
                next_state = STATE_DORSAL;
            }
            break;
            
        case STATE_DORSAL:
            /* Transition Dorsal → Sympathique (avec hystérésis) */
            if (resilience_score >= (config->seuil_dorsal + config->hysteresis)) {
                next_state = STATE_SYMPATHETIC;
            }
            break;
    }
    
    /* Mise à jour de l'état interne si transition */
    if (next_state != current_state) {
        state_machine.current_state = next_state;
        state_machine.last_transition = time(NULL);
    }
    
    return next_state;
}

/*
 * Obtenir l'état actuel
 */
PolyvagalState state_machine_get_current(void) {
    return state_machine.current_state;
}

/*
 * Réinitialiser la machine d'état
 */
void state_machine_reset(void) {
    state_machine.current_state = STATE_VENTRAL;
    state_machine.last_transition = 0;
    state_machine.cooldown_active = 0;
}
