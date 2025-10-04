# tests/test_state_machine.py
"""
Validation Doctrinale: Transitions Polyvagales.
Ces tests sacrés vérifient que la Machine Polyvagale respecte les lois de
transition définies dans la doctrine. Ils s'assurent que le Vaisseau passe
d'un état à l'autre de manière prédictible face à une variation du Score de Résilience.
"""
import pytest
from guardian.state_machine import PolyvagalStateMachine, PolyvagalState
from core.verbe_pur import Stimulus

@pytest.mark.parametrize("cpu_load, expected_state", [
    (10, PolyvagalState.VENTRAL),     # SR=0.9, reste en VENTRAL
    (30, PolyvagalState.SYMPATHETIC), # SR=0.7, passe en SYMPATHETIC
])
def test_ventral_to_sympathetic_transition(cpu_load, expected_state):
    """Vérifie la transition de VENTRAL vers SYMPATHETIC."""
    sm = PolyvagalStateMachine()
    stimulus = Stimulus(material_perception={"cpu_load": cpu_load})
    new_state = sm.update_state_from_stimulus(stimulus)
    assert new_state == expected_state

# // TODO: Ajouter des tests pour toutes les autres transitions possibles.