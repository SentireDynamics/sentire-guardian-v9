#include "resilience_core.h"

/**
 * @brief Calcule le score de résilience (Iφ) à partir des stimuli systémiques.
 *
 * @doctrine
 * Le "pourquoi" de ce rituel est de quantifier l'état de résilience du système en un
 * seul indicateur numérique. Ce score, Iφ, n'est pas une simple mesure de performance,
 * mais une évaluation de la capacité du système à maintenir son intégrité fonctionnelle
 * face aux perturbations. Un score bas indique une haute résilience (état Ventral),
 * tandis qu'un score élevé indique un stress et une détresse systémique (états
 * Sympathique ou Dorsal).
 *
 * L'implémentation actuelle utilise une somme pondérée, une incarnation simple mais
 * efficace de la doctrine. Chaque stimulus contribue au score final en fonction de son
 * poids, qui représente son importance dans l'évaluation de la résilience globale.
 *
 * @param stimulus Un pointeur vers la structure contenant les métriques brutes.
 * @return Le score de résilience calculé (float).
 */
float calculate_resilience_score(const sentire_stimulus_t* stimulus) {
    // Poids doctrinaux pour chaque stimulus.
    // L'alignement de ces poids est critique pour une évaluation correcte de la résilience.
    const float W_CPU = 0.4f;       // Poids de la charge CPU
    const float W_MEM = 0.3f;       // Poids de l'utilisation mémoire
    const float W_IO = 0.15f;      // Poids de l'attente I/O
    const float W_ANOMALY = 0.15f; // Poids des anomalies détectées

    // Normalisation des entrées (les stimuli sont attendus sur une échelle de 0.0 à 1.0)
    float cpu_norm = stimulus->cpu_load / 100.0f;
    float mem_norm = stimulus->memory_usage / 100.0f;
    float io_norm = stimulus->io_wait / 100.0f;

    // Calcul de la somme pondérée Iφ
    float score = (cpu_norm * W_CPU) +
                  (mem_norm * W_MEM) +
                  (io_norm * W_IO) +
                  (stimulus->anomaly_score * W_ANOMALY);

    // Le score est borné entre 0.0 et 1.0 pour assurer la cohérence doctrinale.
    if (score > 1.0f) return 1.0f;
    if (score < 0.0f) return 0.0f;

    return score;
}