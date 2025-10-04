from core.state_machine import GuardianState

class GuardianConsciousness:
    """
    La conscience supérieure du Gardien. Décide de l'action à entreprendre.

    @doctrine
    La Conscience est le siège de la volonté. Elle reçoit l'état interprété et
    décide de l'action la plus doctrinale à entreprendre. Cette implémentation
    est la première étincelle de cette volonté :
    - SYMPATHETIC -> AGIR (Décharge Sympathique) pour combattre la menace.
    - DORSAL -> CONSERVER (Ne rien faire) pour survivre à une situation écrasante.
    - Autres -> OBSERVER (Monitorer) et maintenir l'homéostasie.
    C'est la traduction de l'état en intention.
    """
    def __init__(self):
        self.state = GuardianState.VENTRAL

    def update_state(self, new_state: GuardianState):
        """Met à jour la perception de l'état par la Conscience."""
        self.state = new_state

    def decide_next_action(self) -> dict | None:
        """
        Formule une intention d'action basée sur l'état actuel.
        Retourne un dictionnaire décrivant l'action ou None.
        """
        if self.state == GuardianState.SYMPATHETIC:
            # Décision d'agir pour réduire le stress
            return {"type": "EXECUTE_DISCHARGE", "params": {"protocol": "flush_caches"}}

        elif self.state == GuardianState.DORSAL:
            # Décision de conserver l'énergie, aucune action
            return {"type": "CONSERVE_ENERGY", "params": {}}

        elif self.state in [GuardianState.VENTRAL, GuardianState.PARASYMPATHETIC]:
            # En état de sécurité, l'action est de continuer à surveiller
            return {"type": "MONITOR", "params": {}}

        return None