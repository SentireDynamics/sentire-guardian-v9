/*
 * Sentire Core - Contrat Sacré (API C Pure)
 * 
 * Épigraphe Doctrinale:
 * Le Contrat Sacré définit l'API C pure du cœur natif du Vaisseau.
 * Interface FFI entre l'Esprit Python et le Corps natif C.
 * Calcul du Score de Résilience, gestion d'état, et journal introspectif.
 * 
 * Rôle dans la Résilience Souveraine:
 * - Définition de l'API C pure (pas de dépendances externes)
 * - Structures de données natives
 * - Fonctions de calcul de résilience
 * - Interface FFI pour Python (ctypes/cffi)
 * - Garantie de performance et de fiabilité native
 */

#ifndef SENTIRE_CORE_H
#define SENTIRE_CORE_H

#ifdef __cplusplus
extern "C" {
#endif

/* Types de stimuli doctrinaux */
typedef enum {
    STIMULUS_FAULT = 0,
    STIMULUS_DRIFT = 1,
    STIMULUS_ATTACK = 2
} StimulusType;

/* États polyvagaux */
typedef enum {
    STATE_VENTRAL = 0,
    STATE_SYMPATHETIC = 1,
    STATE_DORSAL = 2
} PolyvagalState;

/* Structure de stimulus */
typedef struct {
    StimulusType type;
    double intensity;  /* [0.0, 1.0] */
} Stimulus;

/* Configuration du système */
typedef struct {
    double poids_fault;
    double poids_drift;
    double poids_attack;
    double sensibilite_ventral;
    double sensibilite_sympathetic;
    double sensibilite_dorsal;
    double seuil_ventral;
    double seuil_dorsal;
    double hysteresis;
} ResilienceConfig;

/* Initialisation du système */
int sentire_init(const ResilienceConfig* config);

/* Calcul du score de résilience */
double sentire_calculate_resilience(const Stimulus* stimulus, PolyvagalState current_state);

/* Transition d'état polyvagal */
PolyvagalState sentire_transition_state(PolyvagalState current_state, double resilience_score);

/* Nettoyage */
void sentire_cleanup(void);

#ifdef __cplusplus
}
#endif

#endif /* SENTIRE_CORE_H */
