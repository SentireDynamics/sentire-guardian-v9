# --- START OF FILE: core/consciousness.py ---
"""
Le Sanctuaire de la Conscience.

Le "Pourquoi": C'est le cœur pensant du Vaisseau. La Conscience orchestre le cycle
de décision. Elle reçoit un `Stimulus` de la Perception, consulte le `NativeBridge`
pour savoir si une action est possible (cooldown), interroge l' `Oracle` pour obtenir
une stratégie, fait valider cette stratégie par `Cerberus`, et finalement renvoie
l' `Action` à exécuter. C'est ici que l'information devient décision.
"""
import logging
from core.verbe_pur import Stimulus, Action
from ffi.native_bridge import NativeBridge
from oracle.llama_client import LlamaOracle
from guardian.cerberus import Cerberus
from guardian.perception import Perception
from core.exceptions import OracleSickness, InvalidActionError

_log = logging.getLogger(__name__)

class GuardianConsciousness:
    """
    Orchestre le processus de décision du Vaisseau.
    """
    def __init__(self, native_bridge: NativeBridge, oracle: LlamaOracle, cerberus: Cerberus, perception: Perception):
        self.native_bridge = native_bridge
        self.oracle = oracle
        self.cerberus = cerberus
        self.perception = perception

    def decide(self, stimulus: Stimulus) -> Action | None:
        """
        Le cycle de décision complet : peut-on agir, que faire, est-ce sûr ?
        """
        if not self.native_bridge.can_act():
            _log.debug("Décision: Cooldown actif. Aucune action ne sera entreprise.")
            return None

        try:
            _log.info("Consultation de l'Oracle pour une décision...")
            oracle_response = self.oracle.consult(stimulus)
            action = oracle_response.action

            self.cerberus.validate_action(action)
            _log.info(f"Décision prise: Exécuter l'action '{action.id}'. Raison: {oracle_response.reasoning}")
            return action

        except OracleSickness as e:
            _log.error(f"Hérésie de l'Oracle: {e}. Activation du protocole de secours.")
            return self.perception.get_fallback_action(e)

        except InvalidActionError as e:
            _log.error(f"Hérésie d'Action: {e}. Activation du protocole de sécurité.")
            # Utilise aussi le fallback pour notifier l'utilisateur du problème
            return self.perception.get_fallback_action(e)
# --- END OF FILE: core/consciousness.py ---