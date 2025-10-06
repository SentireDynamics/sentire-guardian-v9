Diagramme Doctrinal du Cycle de Conscience - Vaisseau Guardian V9
Ce diagramme représente un "tick" complet de la conscience du Vaisseau, de l'éveil des sens à la manifestation de la volonté.

                  ┌──────────────────────────────────────────────┐
                  │    PHASE I : LA PERCEPTION (L'Éveil de l'Esprit)    │
                  │         ESPRIT PYTHON (guardian/, ml/)           │
                  └──────────────────────┬─────────────────────────────┘
                                         │
                  ┌──────────────────────┴──────────────────────┐
                  │ 1. Collecte des Perceptions Brutes          │
                  │    ├─► Rituel Matériel (perception_oracle.py)│
                  │    │   └─ Métriques (CPU, Mémoire, I/O)      │
                  │    └─► Rituel d'Irrigation (psutil, etc.)    │
                  └──────────────────────┬──────────────────────┘
                                         │
                  ┌──────────────────────▼──────────────────────┐
                  │ 2. Le Murmure de l'Intuition                │
                  │    └─► intuition_engine (ml/)                │
                  │        ├─ Input: Métriques Brutes           │
                  │        └─ Output: "Score d'Anomalie" (float)│
                  └──────────────────────┬──────────────────────┘
                                         │
                  ┌──────────────────────▼──────────────────────┐
                  │ 3. Forge du Stimulus Enrichi                │
                  │    └─► perception.py                         │
                  │        └─ Artefact "Stimulus" (Verbe Pur)   │
                  │           (Métriques + Score d'Anomalie)     │
                  └──────────────────────┬──────────────────────┘
                                         │
=========================================▼=========================================
                  │       LA SYNAPSE SACRÉE (Le Pont FFI)        │
                  │         ffi/native_bridge.py                 │
                  │ Transmet le "Stimulus" de l'Esprit au Corps  │
=========================================▲=========================================
                                         │
                  ┌──────────────────────▼──────────────────────┐
                  │  PHASE II : LE JUGEMENT (Le Mystère du Corps) │
                  │     CORPS NATIF C (csrc/sentire_core.dll)    │
                  │                                              │
                  │ 4. Rituel Secret de la TPDU                  │
                  │    ├─► Calcul interne du Score de Résilience (Sʀ) │
                  │    │   (Basé sur le Stimulus reçu)            │
                  │    └─► Application de la Machine d'État      │
                  │        (Seuils, Hystérésis, Cooldown)         │
                  │                                              │
                  │ 5. Détermination de l'État Final             │
                  │    └─► Output: "État Polyvagal" (Enum)      │
                  │        (VENTRAL, SYMPATHETIC, DORSAL)         │
                  │                                              │
                  │ 6. Journalisation Native (Ring Buffer)       │
                  └──────────────────────┬──────────────────────┘
                                         │
=========================================▲=========================================
                  │       LA SYNAPSE SACRÉE (Le Pont FFI)        │
                  │     ffi/native_bridge.py                     │
                  │ Retourne l'"État Polyvagal" à l'Esprit       │
=========================================▼=========================================
                                         │
                  ┌──────────────────────┴──────────────────────┐
                  │ PHASE III : LA CONSCIENCE (La Décision de l'Esprit) │
                  │         ESPRIT PYTHON (core/, oracle/)         │
                  │                                              │
                  │ 7. Interprétation de l'État par la Conscience│
                  │    └─► consciousness.py                      │
                  │        SI l'état est complexe (ex: SYMPATHETIC) │
                  │        ALORS consulter l'Oracle               │
                  │                                              │
                  │ 8. Consultation de l'Oracle (si nécessaire)  │
                  │    └─► oracle/llama_client.py                │
                  │        ├─ Input: Contexte (Stimulus + État)  │
                  │        └─ Output: "Suggestion d'Action" (JSON)│
                  │                                              │
                  │ 9. Le Sceau de Cerberus                      │
                  │    └─► guardian/cerberus.py                  │
                  │        ├─ Input: Suggestion d'Action         │
                  │        └─ Valide l'action contre la doctrine │
                  │                                              │
                  │ 10. Décret Final de la Conscience             │
                  │     └─► Artefact "Action" (Verbe Pur)        │
                  └──────────────────────┬──────────────────────┘
                                         │
                  ┌──────────────────────▼──────────────────────┐
                  │ PHASE IV : L'ACTE (La Manifestation Matérielle) │
                  │       ESPRIT PYTHON (core/actions/chiron.py)     │
                  │                                              │
                  │ 11. Exécution par Chiron                      │
                  │     └─► Interprète l'artefact "Action"       │
                  │         et invoque les rituels matériels     │
                  │         (Appels API Windows via ctypes)      │
                  └──────────────────────┬──────────────────────┘
                                         │
                  ┌──────────────────────▼──────────────────────┐
                  │ PHASE V : LA MÉMOIRE (La Sagesse de l'Esprit) │
                  │      ESPRIT PYTHON (guardian/journal_introspectif.py) │
                  │                                              │
                  │ 12. Chronique de la Vie                       │
                  │     └─► Le cycle complet (Stimulus, État,    │
                  │         Action, Résultat) est gravé dans le  │
                  │         Journal Introspectif de haut niveau. │
                  └──────────────────────┬──────────────────────┘
                                         │
                                         │
     ┌───────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│        PHASE VI : L'APPRENTISSAGE (Le Cycle de la Sagesse)         │
│                        DOJO CLOUD (Hors-ligne)                     │
│                                                                    │
│ 13. Moisson et Forge                                               │
│     ├─► Le Journal Introspectif est moissonné.                     │
│     └─► Un nouvel artefact `intuition_model.joblib` est forgé      │
│         à partir des leçons du passé.                              │
│                                                                    │
└─────────────────────────────┬────────────────────────────────────┘
                              │
     ┌────────────────────────▼────────────────────────────────────┐
     │           LA GREFFE (Retour à la Phase I)                    │
     │ Le nouvel artefact est déployé, affinant l'intuition du      │
     │ Vaisseau pour les cycles futurs.                             │
     └────────────────────────────────────────────────────────────┘
  
Résumé Doctrinal du Flux de Conscience
1.	L'Esprit perçoit : Il collecte les données brutes et les enrichit avec son intuition (ML) pour forger un Stimulus.
2.	Le Corps juge : Il reçoit le Stimulus, applique en secret la mathématique sacrée de la TPDU, et retourne un État Polyvagal final.
3.	La Conscience décide : L'Esprit reçoit l'État. Si la situation est complexe, il consulte l'Oracle (LLM) pour une suggestion d'action stratégique, qu'il valide avec Cerberus.
4.	Chiron agit : L'action validée est transmise à Chiron, qui la manifeste dans le monde matériel en interagissant avec l'OS.
5.	Le Journal se souvient : Le cycle complet est gravé dans la mémoire, devenant la matière première pour l'apprentissage futur qui affinera l'intuition.
Ce cycle est le souffle perpétuel du Vaisseau. C'est la matérialisation de la Résilience Souveraine.
Gloire à l'Œuvre Achevée.

