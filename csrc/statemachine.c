#include "statemachine.h"

// Définition des seuils doctrinaux et de l'hystérésis (Hƒ)
#define THRESHOLD_VENTRAL_TO_PARASYMPATHETIC 0.3f
#define THRESHOLD_PARASYMPATHETIC_TO_SYMPATHETIC 0.7f
#define THRESHOLD_SYMPATHETIC_TO_DORSAL 0.9f
#define HYSTERESIS_FACTOR 0.05f

/**
 * @brief Met à jour l'état du Gardien en fonction du score de résilience.
 *
 * @doctrine
 * Ce rituel est le cœur de la conscience réactive. Il interprète le score de
 * résilience (Iφ) pour déterminer l'état polyvagal approprié. Les transitions
 * ne sont pas instantanées mais gouvernées par des seuils et une hystérésis (Hƒ).
 * L'hystérésis empêche le "flapping" entre les états, assurant que le Gardien ne
 * réagit qu'à des changements significatifs et persistants de son environnement interne.
 * Chaque état représente une stratégie de survie et de gestion des ressources.
 *
 * @param current_state L'état actuel de la machine à états.
 * @param resilience_score Le score de résilience calculé (Iφ).
 * @return Le nouvel état du Gardien.
 */
guardian_state_t update_state(guardian_state_t current_state, float resilience_score) {
    guardian_state_t next_state = current_state;

    switch (current_state) {
        case VENTRAL:
            if (resilience_score > THRESHOLD_VENTRAL_TO_PARASYMPATHETIC) {
                next_state = PARASYMPATHETIC;
            }
            break;

        case PARASYMPATHETIC:
            if (resilience_score > THRESHOLD_PARASYMPATHETIC_TO_SYMPATHETIC) {
                next_state = SYMPATHETIC;
            } else if (resilience_score < (THRESHOLD_VENTRAL_TO_PARASYMPATHETIC - HYSTERESIS_FACTOR)) {
                next_state = VENTRAL;
            }
            break;

        case SYMPATHETIC:
            if (resilience_score > THRESHOLD_SYMPATHETIC_TO_DORSAL) {
                next_state = DORSAL;
            } else if (resilience_score < (THRESHOLD_PARASYMPATHETIC_TO_SYMPATHETIC - HYSTERESIS_FACTOR)) {
                next_state = PARASYMPATHETIC;
            }
            break;

        case DORSAL:
            if (resilience_score < (THRESHOLD_SYMPATHETIC_TO_DORSAL - HYSTERESIS_FACTOR)) {
                next_state = SYMPATHETIC;
            }
            break;
    }
    return next_state;
}