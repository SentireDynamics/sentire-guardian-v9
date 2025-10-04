/*
 * Resilience Core - Calcul du Score de Résilience
 * 
 * Épigraphe Doctrinale:
 * Module natif dédié au calcul précis du Score de Résilience selon la TPDU.
 * Implémentation optimisée de l'équation sacrée: SR = max(0, 1 - Iφ)
 * 
 * Rôle dans la Résilience Souveraine:
 * - Calcul haute précision du Score de Résilience
 * - Application des pondérations doctrinales
 * - Ajustement contextuel selon l'état
 * - Optimisations pour performance native
 */

#include "sentire_core.h"

/*
 * Calcul avancé du score de résilience avec extensions TPDU
 * 
 * Équation:
 * 1. Impact brut: Iβ = ι × ω_τ
 * 2. Impact contextualisé: Iφ = Iβ × Φ_ε
 * 3. Score: SR = max(0, 1 - Iφ)
 */
double calculate_resilience_advanced(const Stimulus* stimulus, 
                                    PolyvagalState state,
                                    const ResilienceConfig* config) {
    if (!stimulus || !config) {
        return 0.0;
    }
    
    /* Étape 1: Sélection du poids selon le type de stimulus */
    double poids = 0.0;
    switch (stimulus->type) {
        case STIMULUS_FAULT:
            poids = config->poids_fault;
            break;
        case STIMULUS_DRIFT:
            poids = config->poids_drift;
            break;
        case STIMULUS_ATTACK:
            poids = config->poids_attack;
            break;
        default:
            return 1.0;  /* Stimulus invalide = pas d'impact */
    }
    
    /* Étape 2: Calcul de l'impact brut */
    double impact_brut = stimulus->intensity * poids;
    
    /* Étape 3: Sélection de la sensibilité selon l'état */
    double sensibilite = 1.0;
    switch (state) {
        case STATE_VENTRAL:
            sensibilite = config->sensibilite_ventral;
            break;
        case STATE_SYMPATHETIC:
            sensibilite = config->sensibilite_sympathetic;
            break;
        case STATE_DORSAL:
            sensibilite = config->sensibilite_dorsal;
            break;
    }
    
    /* Étape 4: Impact contextualisé */
    double impact_final = impact_brut * sensibilite;
    
    /* Étape 5: Score de résilience */
    double resilience_score = 1.0 - impact_final;
    
    /* Contrainte: SR ∈ [0, 1] */
    if (resilience_score < 0.0) {
        resilience_score = 0.0;
    } else if (resilience_score > 1.0) {
        resilience_score = 1.0;
    }
    
    return resilience_score;
}
