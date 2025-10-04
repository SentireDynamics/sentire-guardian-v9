#include "resilience_core.h"
#include "statemachine.h"
#include "sentire_core.h"

/**
 * @brief Point d'entrée principal pour le traitement des stimuli par le Corps Natif.
 *
 * @doctrine
 * Ce rituel orchestre le flux de traitement au sein du Corps Natif. Il est le
 * gardien de l'ordre séquentiel sacré :
 * 1. Invocation de `calculate_resilience_score` pour distiller la complexité des
 *    stimuli en un unique score de vérité, Iφ.
 * 2. Invocation de `update_state` pour traduire ce score en un état de conscience
 *    discret et actionnable.
 * Cette séparation assure que le calcul brut reste pur et que la logique de transition
 * est appliquée de manière cohérente. C'est l'incarnation de la dualité Esprit/Corps,
 * où le Corps fournit la sensation brute et l'Esprit (ici, la machine à états) l'interprète.
 *
 * @param stimulus La structure contenant les données des capteurs.
 * @return Le nouvel état du Gardien après traitement.
 */
guardian_state_t sentire_core_process(const sentire_stimulus_t* stimulus, guardian_state_t current_state) {
    // 1. Quantifier la résilience à partir des stimuli.
    float score = calculate_resilience_score(stimulus);

    // 2. Mettre à jour l'état en fonction du nouveau score.
    guardian_state_t new_state = update_state(current_state, score);

    return new_state;
}