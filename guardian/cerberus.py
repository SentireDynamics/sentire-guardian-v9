# --- START OF FILE: guardian/cerberus.py ---
"""
Le Sanctuaire de Cerberus - Le Gardien des Portes.

Le "Pourquoi": Ce module agit comme un filtre de sécurité final. Avant qu'une action
recommandée par l'Oracle ne soit exécutée, Cerberus la valide contre un ensemble de
règles immuables. Il empêche les actions potentiellement dangereuses ou invalides,
agissant comme un garde-fou essentiel contre des conseils erronés de l'Oracle.
C'est la garantie de la non-malfaisance du Vaisseau.
"""
import logging
from core.verbe_pur import Action
from core.exceptions import InvalidActionError

_log = logging.getLogger(__name__)

class Cerberus:
    """
    Valide les actions avant leur exécution.
    """
    def __init__(self):
        # Liste blanche des actions autorisées (Phase II - Actions Souveraines).
        self.allowed_actions = {
            "NO_ACTION",                # Action de non-intervention (sagesse suprême)
            "SHOW_MESSAGE",             # Dernier recours
            "LOG_ONLY",                 # Enregistrement
            "ISOLATE_PROCESS",          # Isolation (suspend)
            "EXCOMMUNICATE_PROCESS",    # Excommunication (kill)
            "LOWER_RIVAL_PRIORITY",     # Réduction priorité
            "RESTART_DEPENDENCY",       # Redémarrage d'une dépendance
            "RESTART_SYSTEM",           # Redémarrage du système
            "PROTOCOL_RESONANCE_SOMATIQUE"  # Protocole de l'Âme Menteuse
        }

    def validate_action(self, action: Action) -> bool:
        """
        Valide une action. Lève une exception si l'action est une hérésie.
        """
        if action.id not in self.allowed_actions:
            _log.error(f"Hérésie détectée par Cerberus! Action non autorisée: {action.id}")
            raise InvalidActionError(f"Action '{action.id}' is not in the list of allowed actions.")

        _log.debug(f"Action '{action.id}' validée par Cerberus.")
        return True
# --- END OF FILE: guardian/cerberus.py ---