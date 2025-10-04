"""
Test State Machine - Validation de la Machine Polyvagale

Tests unitaires pour la machine d'état polyvagale (guardian/state_machine.py).
Valide les transitions, l'hystérésis, et l'intégration avec le cœur natif.
"""

import unittest
from guardian.state_machine import PolyvagalStateMachine


class TestPolyvagalStateMachine(unittest.TestCase):
    """Tests de la machine d'état polyvagale."""
    
    def setUp(self):
        """Initialise la machine d'état pour chaque test."""
        self.machine = PolyvagalStateMachine()
    
    def test_initial_state_ventral(self):
        """Vérifie que l'état initial est VENTRAL."""
        self.assertEqual(self.machine.current_state, "VENTRAL")
        self.assertEqual(self.machine.resilience_score, 1.0)
    
    def test_process_stimulus(self):
        """Teste le traitement d'un stimulus."""
        result = self.machine.process_stimulus("FAULT", 0.5)
        self.assertIsInstance(result, str)
        self.assertIn(result, ["VENTRAL", "SYMPATHETIC", "DORSAL"])
    
    # TODO: Ajouter tests complets des transitions
    # - Transition Ventral → Sympathique
    # - Transition Sympathique → Dorsal
    # - Transition Dorsal → Sympathique
    # - Hystérésis
    # - Cooldown


if __name__ == '__main__':
    unittest.main()
