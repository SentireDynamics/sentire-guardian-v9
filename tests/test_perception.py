"""
Test Perception - Validation du Système de Perception

Tests unitaires pour le système de perception (guardian/perception.py).
Valide la fusion des sources Oracle et Llama.cpp.
"""

import unittest
from guardian.perception import PerceptionEngine


class TestPerceptionEngine(unittest.TestCase):
    """Tests du moteur de perception."""
    
    def setUp(self):
        """Initialise le moteur de perception pour chaque test."""
        self.engine = PerceptionEngine()
    
    def test_perceive_returns_dict(self):
        """Vérifie que perceive() retourne un dictionnaire."""
        result = self.engine.perceive()
        self.assertIsInstance(result, dict)
    
    # TODO: Ajouter tests complets
    # - Fusion Oracle + Llama.cpp
    # - Détection de stimuli
    # - Enrichissement contextuel


if __name__ == '__main__':
    unittest.main()
