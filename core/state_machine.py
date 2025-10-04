from enum import IntEnum

class GuardianState(IntEnum):
    VENTRAL = 0
    PARASYMPATHETIC = 1
    SYMPATHETIC = 2
    DORSAL = 3

class StateMachine:
    """
    Conserve l'état actuel du Gardien, tel que déterminé par le Corps Natif.

    @doctrine
    Dans le respect de la Dualité, la logique de transition a été retirée de cet
    artefact de l'Esprit. Son seul rôle est de maintenir l'état courant qui lui est
    communiqué par l'Orchestrateur, après que le Corps Natif ait effectué le rituel
    de décision. Il est le gardien de la mémoire de l'état, pas son créateur.
    """
    def __init__(self, initial_state: GuardianState = GuardianState.VENTRAL):
        self._current_state = initial_state

    def get_current_state(self) -> GuardianState:
        """Retourne l'état actuel."""
        return self._current_state

    def set_current_state(self, new_state: GuardianState):
        """
        Met à jour l'état du Gardien.
        Cette méthode est appelée par l'orchestrateur après consultation du Corps Natif.
        """
        if not isinstance(new_state, GuardianState):
            raise TypeError("Le nouvel état doit être une instance de GuardianState.")
        self._current_state = new_state