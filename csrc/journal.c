/*
 * Journal - Journal Introspectif Natif
 * 
 * Épigraphe Doctrinale:
 * Journal introspectif natif pour l'enregistrement de tous les cycles de résilience.
 * Persistance sur disque, performance optimale, format binaire compact.
 * 
 * Rôle dans la Résilience Souveraine:
 * - Enregistrement natif des cycles de résilience
 * - Persistence sur disque (format binaire)
 * - Accès rapide à l'historique
 * - Statistiques et métriques
 * - Support de la mémoire adaptative
 */

#include "sentire_core.h"
#include <stdio.h>
#include <time.h>

/* Entrée du journal */
typedef struct {
    time_t timestamp;
    StimulusType stimulus_type;
    double stimulus_intensity;
    double resilience_score;
    PolyvagalState state;
    int transition;  /* 1 si changement d'état, 0 sinon */
} JournalEntry;

/* Buffer du journal (en mémoire) */
#define JOURNAL_BUFFER_SIZE 10000
static JournalEntry journal_buffer[JOURNAL_BUFFER_SIZE];
static int journal_count = 0;

/*
 * Enregistrer un cycle dans le journal
 */
int journal_record_cycle(const Stimulus* stimulus,
                        double resilience_score,
                        PolyvagalState state,
                        int transition) {
    if (!stimulus || journal_count >= JOURNAL_BUFFER_SIZE) {
        return -1;
    }
    
    JournalEntry entry = {
        .timestamp = time(NULL),
        .stimulus_type = stimulus->type,
        .stimulus_intensity = stimulus->intensity,
        .resilience_score = resilience_score,
        .state = state,
        .transition = transition
    };
    
    journal_buffer[journal_count++] = entry;
    
    return 0;
}

/*
 * Obtenir le nombre d'entrées
 */
int journal_get_count(void) {
    return journal_count;
}

/*
 * Obtenir une entrée du journal
 */
const JournalEntry* journal_get_entry(int index) {
    if (index < 0 || index >= journal_count) {
        return NULL;
    }
    return &journal_buffer[index];
}

/*
 * Sauvegarder le journal sur disque
 */
int journal_save_to_disk(const char* filepath) {
    if (!filepath || journal_count == 0) {
        return -1;
    }
    
    FILE* file = fopen(filepath, "wb");
    if (!file) {
        return -1;
    }
    
    fwrite(journal_buffer, sizeof(JournalEntry), journal_count, file);
    fclose(file);
    
    return 0;
}

/*
 * Charger le journal depuis le disque
 */
int journal_load_from_disk(const char* filepath) {
    if (!filepath) {
        return -1;
    }
    
    FILE* file = fopen(filepath, "rb");
    if (!file) {
        return -1;
    }
    
    journal_count = fread(journal_buffer, sizeof(JournalEntry), 
                         JOURNAL_BUFFER_SIZE, file);
    fclose(file);
    
    return journal_count;
}

/*
 * Réinitialiser le journal
 */
void journal_reset(void) {
    journal_count = 0;
}
