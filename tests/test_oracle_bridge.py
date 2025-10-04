"""
Test Oracle Bridge - Validation du Bridge Oracle

Tests unitaires pour le bridge Oracle (guardian/perception_oracle.py).
Valide l'interface FFI avec Oracle_Unification_Souveraine.dll.
"""

import unittest
from guardian.perception_oracle import OraclePerception


class TestOraclePerception(unittest.TestCase):
    """Tests du bridge Oracle."""
    
    def setUp(self):
        """Initialise le bridge Oracle pour chaque test."""
        self.oracle = OraclePerception()
    
    def test_read_sensors(self):
        """Vérifie la lecture des capteurs."""
        result = self.oracle.read_sensors()
        self.assertIsInstance(result, dict)
    
    # TODO: Ajouter tests complets
    # - Chargement DLL
    # - Lecture métriques système
    # - Gestion des erreurs


if __name__ == '__main__':
    unittest.main()
