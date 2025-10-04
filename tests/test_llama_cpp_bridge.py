"""
Test Llama.cpp Bridge - Validation du Bridge LLM

Tests unitaires pour le bridge Llama.cpp (oracle/llama_cpp_bridge.py).
Valide l'interface avec le LLM local.
"""

import unittest
from oracle.llama_cpp_bridge import LlamaCppBridge


class TestLlamaCppBridge(unittest.TestCase):
    """Tests du bridge Llama.cpp."""
    
    def setUp(self):
        """Initialise le bridge Llama.cpp pour chaque test."""
        # Note: Ces tests peuvent être skippés si Llama.cpp n'est pas disponible
        self.bridge = LlamaCppBridge(server_url="http://localhost:8080")
    
    def test_initialization(self):
        """Vérifie l'initialisation du bridge."""
        self.assertIsNotNone(self.bridge)
    
    def test_generate_returns_string(self):
        """Vérifie que generate() retourne une string."""
        result = self.bridge.generate("Test prompt")
        self.assertIsInstance(result, str)
    
    def test_embed_returns_list(self):
        """Vérifie que embed() retourne une liste."""
        result = self.bridge.embed("Test text")
        self.assertIsInstance(result, list)
    
    # TODO: Ajouter tests complets
    # - Génération de texte
    # - Génération d'embeddings
    # - Gestion du contexte
    # - Fallback si serveur indisponible


if __name__ == '__main__':
    unittest.main()
