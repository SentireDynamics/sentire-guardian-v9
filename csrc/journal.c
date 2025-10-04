//--- START OF FILE: csrc/journal.c ---
#include "sentire_core.h"
#include <stdlib.h>
#include <string.h>

/**
 * @brief Initialise le journal (ring buffer).
 * @param journal Pointeur vers le journal à initialiser.
 */
void journal_init(Journal* journal) {
    if (!journal) return;
    journal->head = 0;
    journal->tail = 0;
    journal->count = 0;
    memset(journal->entries, 0, sizeof(journal->entries));
}

/**
 * @brief Enregistre une nouvelle entrée dans le journal.
 * @param journal Pointeur vers le journal.
 * @param description Description de l'action à enregistrer.
 */
void journal_record(Journal* journal, const char* description) {
    if (!journal) return;

    JournalEntry* entry = &journal->entries[journal->head];
    entry->timestamp = time(NULL);
    strncpy(entry->description, description, ACTION_DESC_MAX_LEN - 1);
    entry->description[ACTION_DESC_MAX_LEN - 1] = '\0'; // Assurer la terminaison null

    journal->head = (journal->head + 1) % JOURNAL_CAPACITY;

    if (journal->count < JOURNAL_CAPACITY) {
        journal->count++;
    } else {
        // Le buffer est plein, la queue avance avec la tête
        journal->tail = (journal->tail + 1) % JOURNAL_CAPACITY;
    }
}
//--- END OF FILE: csrc/journal.c ---