//--- START OF FILE: csrc/statemachine.c ---
#include "sentire_core.h"
#include <stdlib.h>
#include <stdio.h>

// Déclarations des fonctions de journal.c pour les lier
void journal_init(Journal* journal);
void journal_record(Journal* journal, const char* description);

/**
 * @brief Crée et initialise l'état complet du Guardian.
 * Le "Pourquoi" : Allouer en une seule fois toutes les ressources natives
 * pour garantir une gestion de la mémoire simple et centralisée.
 */
SENTIRE_API GuardianState* sentire_api_create(int cooldown_seconds) {
    GuardianState* state = (GuardianState*)malloc(sizeof(GuardianState));
    if (!state) {
        return NULL; // Échec de l'allocation
    }

    // Initialisation de la machine à états
    state->state_machine.last_action_time = 0;
    state->state_machine.cooldown_seconds = cooldown_seconds;

    // Initialisation du journal
    journal_init(&state->journal);

    return state;
}

/**
 * @brief Libère les ressources allouées pour l'état du Guardian.
 * Le "Pourquoi" : Empêcher les fuites de mémoire en fournissant un point
 * de sortie unique et propre pour les ressources natives.
 */
SENTIRE_API void sentire_api_destroy(GuardianState* state) {
    if (state) {
        free(state);
    }
}

/**
 * @brief Détermine si une nouvelle action peut être entreprise.
 * Le "Pourquoi" : Implémenter la logique de cooldown en C pour la performance
 * et pour éviter de surcharger le système avec des actions répétées.
 */
SENTIRE_API int sentire_api_can_act(GuardianState* state) {
    if (!state) return 0;
    time_t current_time = time(NULL);
    return (current_time - state->state_machine.last_action_time) >= state->state_machine.cooldown_seconds;
}

/**
 * @brief Enregistre une action et met à jour l'état.
 * Le "Pourquoi" : Centraliser la mise à jour de l'état (timestamp et journal)
 * en une seule opération atomique du point de vue du code appelant.
 */
SENTIRE_API void sentire_api_record_action(GuardianState* state, const char* description) {
    if (!state) return;
    state->state_machine.last_action_time = time(NULL);
    journal_record(&state->journal, description);
}
//--- END OF FILE: csrc/statemachine.c ---