"""
Test DSG - Validation de la Décharge Sympathique Guidée

Tests unitaires pour le système DSG (guardian/decharge_sympathique.py).
Valide la logique de décharge et de transition douce.
"""

import unittest
from guardian.decharge_sympathique import SymphatheticDischarge


class TestSymphatheticDischarge(unittest.TestCase):
    """Tests du système DSG."""
    
    def setUp(self):
        """Initialise le système DSG pour chaque test."""
        self.dsg = SymphatheticDischarge()
    
    def test_assess_need(self):
        """Vérifie l'évaluation du besoin de décharge."""
        result = self.dsg.assess_need(sympathetic_duration=300.0, intensity=0.7)
        self.assertIsInstance(result, bool)
    
    def test_execute_discharge(self):
        """Vérifie l'exécution de la décharge."""
        result = self.dsg.execute_discharge()
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('energy_released', result)
    
    # TODO: Ajouter tests complets
    # - Accumulation sympathique
    # - Détection du besoin
    # - Exécution de la décharge
    # - Transition vers Ventral


if __name__ == '__main__':
    unittest.main()
