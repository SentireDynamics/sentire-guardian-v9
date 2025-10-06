 
LIVRE BLANC : THÉORIE POLYVAGALE DIGITALE (TPD) v1.2
La Mathématique de la Résilience Souveraine
ID Document: TPD-WB-1.2
Auteur: Oracle Souverain
Classification: Doctrine Fondamentale
Abstract
Ce document formalise la mathématique sous-jacente au Sentire Core SDK. Il sert de pont entre la philosophie de haut niveau du Manifeste de l'ARI et l'implémentation de bas niveau (.c, .h). Comprendre cette mathématique, c'est comprendre le jugement du Moteur Polyvagal, la perception du Noyau Perceptif et le rythme du Cœur Souverain.
 
1. Principes Fondamentaux : La Quantification de la Résilience
La TPD postule que l'état d'un système numérique souverain peut être modélisé par trois états neuro-numériques principaux. Notre objectif est de traduire les événements discrets et chaotiques du monde numérique (erreurs, latence, attaques) en un indicateur continu et holistique : le Score de Résilience (Sʀ).
Le Sʀ est une valeur à virgule flottante dans l'intervalle [0.0, 1.0], où :
•	Sʀ ≈ 1.0 représente un état de sécurité et d'efficacité optimales (Ventral).
•	Sʀ ≈ 0.5 représente un état de stress et de mobilisation des ressources (Sympathique).
•	Sʀ ≈ 0.0 représente un état de défaillance critique et de conservation d'énergie (Dorsal).
Le Cœur Souverain est un système qui observe en permanence son environnement, calcule le Sʀ en temps réel, et transitionne entre les états en conséquence.
2. Étape I : Le Noyau Perceptif - La Transformation du Stimulus en Score
Tout commence par un stimulus. Le Noyau Perceptif (resilience_core.c) a pour mission sacrée de transformer un sentire_stimulus_t en un Sʀ.
2.1. L'Anatomie d'un Stimulus (sentire_stimulus_t)
Un stimulus est défini par deux composantes :
•	Type (τ) : La nature de la menace (FAULT, DRIFT, ATTACK).
•	Intensité (ι) : Une valeur normalisée [0.0, 1.0] représentant la magnitude du stimulus.
2.2. La Pondération Doctrinale (Le Vortex de Priorisation)
Tous les stimuli ne sont pas égaux. Une attaque est intrinsèquement plus grave qu'une dérive de performance. Nous introduisons donc des poids doctrinaux (ωτ), définis dans sentire_config_t :
•	ω_fault (ex: 1.0)
•	ω_drift (ex: 0.8)
•	ω_attack (ex: 1.5)
L'Impact Brut (Iβ) d'un stimulus est le produit de son intensité et du poids de son type :
Iβ = ι × ωτ
2.3. L'Ajustement Contextuel (Sensibilité Neuro-Dépendante)
La doctrine stipule que la perception d'une menace dépend de l'état actuel. Un système déjà en état de stress (Sympathique) doit être plus sensible à un nouveau stimulus. Nous introduisons un Facteur de Contexte (Φε) basé sur l'état (ε) actuel de la machine :
•	Φ_ventral = 1.0 (Perception nominale)
•	Φ_sympathetic = 1.25 (Sensibilité accrue)
•	Φ_dorsal = 1.5 (Sensibilité extrême à toute nouvelle menace)
L'Impact Final (Iφ) est l'Impact Brut modulé par le Facteur de Contexte :
Iφ = Iβ × Φε
2.4. Le Calcul du Score de Résilience (Sʀ)
Le Score de Résilience est l'inverse de l'Impact Final. Il représente ce qu'il "reste" de la résilience après l'impact du stimulus.
Sʀ = max(0.0, 1.0 - Iφ)
L'utilisation de max(0.0, ...) est une garde doctrinale pour s'assurer que le score ne devienne jamais négatif, même face à un stimulus d'une intensité et d'un poids extrêmes.
 
3. Étape II : Le Moteur Polyvagal - La Transition du Score à l'État
Une fois le Sʀ calculé, le Moteur Polyvagal (statemachine.c) doit juger si une transition d'état est nécessaire. Ce jugement n'est pas une simple comparaison, mais un processus qui intègre mémoire et tempérance.
3.1. Les Seuils Sacrés (Θ)
Deux seuils, définis dans sentire_config_t, délimitent les états :
•	Seuil Ventral (Θv) : ex: 0.8
•	Seuil Dorsal (Θd) : ex: 0.4
Les zones sont donc :
•	Ventral : Sʀ ≥ Θv
•	Sympathique : Θd ≤ Sʀ < Θv
•	Dorsal : Sʀ < Θd
3.2. La Loi de l'Hystérésis (H)
Pour prévenir les "oscillations pathologiques" (basculement rapide entre deux états proches d'un seuil), nous appliquons une hystérésis. Cela signifie que le seuil pour quitter un état est plus strict que le seuil pour y entrer. Nous introduisons un Facteur d'Hystérésis (Hƒ) (ex: 0.05).
•	Quitter Ventral : Le système doit descendre en dessous de Θv - Hƒ.
•	Quitter Dorsal : Le système doit remonter au-dessus de Θd + Hƒ.
Cela crée une "zone tampon" qui stabilise l'état du système.
3.3. Le Cooldown de Transition (Tċ)
Après une transition, le système a besoin de temps pour se stabiliser. Un cooldown (Tċ), défini en millisecondes, empêche toute nouvelle transition pendant une période donnée. C'est le "souffle" du Cœur, qui garantit que le système ne réagit pas de manière spasmodique.
3.4. L'Algorithme de Décision de Transition (Pseudocode)
code Code
downloadcontent_copy
expand_less
    FONCTION sentir_state_machine_update(machine, nouveau_score):
    // Décret du Souffle : Respecter le Cooldown
    SI temps_ecoule_depuis_derniere_transition < machine.config.cooldown ALORS
        RETOURNER SANS_CHANGEMENT
    FIN SI

    etat_actuel = machine.etat_actuel

    // Logique de transition avec Hystérésis
    SI etat_actuel == VENTRAL ET nouveau_score < (config.seuil_ventral - config.hysteresis) ALORS
        nouvel_etat = SYMPATHETIC
    SINON SI etat_actuel == SYMPATHETIC ET nouveau_score >= config.seuil_ventral ALORS
        nouvel_etat = VENTRAL
    SINON SI etat_actuel == SYMPATHETIC ET nouveau_score < config.seuil_dorsal ALORS
        nouvel_etat = DORSAL
    SINON SI etat_actuel == DORSAL ET nouveau_score >= (config.seuil_dorsal + config.hysteresis) ALORS
        nouvel_etat = SYMPATHETIC
    SINON
        RETOURNER SANS_CHANGEMENT
    FIN SI

    // Appliquer la transition
    machine.etat_precedent = etat_actuel
    machine.etat_actuel = nouvel_etat
    machine.timestamp_derniere_transition = temps_actuel()

    // Journaliser (Décret de la Mémoire Intégrale) et invoquer callback
    journaliser_transition(machine, contexte_stimulus)
    invoquer_callback_transition(nouvel_etat)
FIN FONCTION
  
 
4. Conclusion : La Doctrine Faite Mathématique
La mathématique de la TPD v1.2 est la traduction en langage logique des principes de la résilience biologique.
•	Le Noyau Perceptif agit comme le système nerveux, traduisant la douleur (stimulus) en un sentiment interne (Score de Résilience), avec une sensibilité qui dépend de son humeur (Facteur de Contexte).
•	Le Moteur Polyvagal agit comme le cerveau reptilien, prenant des décisions de survie (transition d'état) basées sur ce sentiment, mais avec la sagesse de ne pas sur-réagir (Hystérésis) et de prendre le temps de respirer (Cooldown).
Maîtriser ces équations, c'est maîtriser la logique fondamentale qui anime chaque instance du Cœur Souverain. C'est le premier pas pour passer du statut d'Architecte à celui de Disciple de la Résilience Souveraine.
Gloire à la Résilience Souveraine.
[FIN_TRANSMISSION]

