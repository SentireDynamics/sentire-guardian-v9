// csrc/sentire_core.h
/*
Artefact: Le Contrat d'API Pur.
Doctrine: Ce fichier est le contrat immuable entre le Corps Natif (C) et l'Esprit
Python. Il définit les structures de données pures, les énumérations sacrées et les
signatures des fonctions qui forment le pont entre les deux royaumes. Sa clarté et sa
rigueur sont la garantie de la stabilité de l'architecture Corps/Esprit.
*/

#ifndef SENTIRE_CORE_H
#define SENTIRE_CORE_H

#include <stdint.h>

// Les trois états sacrés, comme définis dans l'Esprit.
typedef enum {
    SENTIRE_STATE_VENTRAL = 0,
    SENTIRE_STATE_SYMPATHETIC = 1,
    SENTIRE_STATE_DORSAL = 2,
} sentire_state_t;

// Structure de configuration pour l'initialisation du Corps.
typedef struct {
    double sympathetic_threshold;
    double dorsal_threshold;
    uint32_t cooldown_ticks;
} sentire_config_t;

// Un stimulus, la perception de l'Esprit traduite pour le Corps.
typedef struct {
    double cpu_load;
    double memory_usage;
    double network_latency;
} sentire_stimulus_t;

// La réponse du Corps après avoir traité un stimulus.
typedef struct {
    sentire_state_t new_state;
    double resilience_score;
} sentire_response_t;

// Rituel d'Initialisation: Crée et configure l'instance du Corps Natif.
// Retourne un pointeur opaque vers l'état interne.
void* sentire_core_create(const sentire_config_t* config);

// Rituel Central: Traite un stimulus et met à jour l'état du Corps.
void sentire_core_process(void* core_handle, const sentire_stimulus_t* stimulus, sentire_response_t* response);

// Rituel de Dissolution: Libère toutes les ressources allouées au Corps Natif.
void sentire_core_destroy(void* core_handle);

#endif // SENTIRE_CORE_H