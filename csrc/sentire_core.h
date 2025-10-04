//--- START OF FILE: csrc/sentire_core.h ---
#ifndef SENTIRE_CORE_H
#define SENTIRE_CORE_H

#include <time.h>

#ifdef _WIN32
    #ifdef SENTIRE_CORE_EXPORTS
        #define SENTIRE_API __declspec(dllexport)
    #else
        #define SENTIRE_API __declspec(dllimport)
    #endif
#else
    #define SENTIRE_API
#endif

#define JOURNAL_CAPACITY 50
#define ACTION_DESC_MAX_LEN 256

// --- Journal d'Actions (Ring Buffer) ---
typedef struct {
    time_t timestamp;
    char description[ACTION_DESC_MAX_LEN];
} JournalEntry;

typedef struct {
    JournalEntry entries[JOURNAL_CAPACITY];
    int head;
    int tail;
    int count;
} Journal;

// --- Machine à États (Gestion du Cooldown) ---
typedef struct {
    time_t last_action_time;
    int cooldown_seconds;
} StateMachine;

// --- Structure Principale (Le Corps Natif) ---
typedef struct {
    StateMachine state_machine;
    Journal journal;
} GuardianState;

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Rituel de création du Corps Natif. Alloue et initialise l'état du Guardian.
 * @param cooldown_seconds Le temps de recharge entre les actions.
 * @return Un pointeur vers l'état alloué, ou NULL en cas d'échec.
 */
SENTIRE_API GuardianState* sentire_api_create(int cooldown_seconds);

/**
 * @brief Rituel de destruction du Corps Natif. Libère la mémoire.
 * @param state Le pointeur vers l'état à détruire.
 */
SENTIRE_API void sentire_api_destroy(GuardianState* state);

/**
 * @brief Vérifie si le Vaisseau est autorisé à agir (respect du cooldown).
 * @param state Le pointeur vers l'état.
 * @return 1 si l'action est autorisée, 0 sinon.
 */
SENTIRE_API int sentire_api_can_act(GuardianState* state);

/**
 * @brief Enregistre une action, mettant à jour le journal et le temps de la dernière action.
 * @param state Le pointeur vers l'état.
 * @param description Une chaîne de caractères décrivant l'action effectuée.
 */
SENTIRE_API void sentire_api_record_action(GuardianState* state, const char* description);

#ifdef __cplusplus
}
#endif

#endif // SENTIRE_CORE_H
//--- END OF FILE: csrc/sentire_core.h ---