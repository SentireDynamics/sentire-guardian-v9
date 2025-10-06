"""
Test Seal of Purity - Validation de l'Audit Doctrinal Automatisé

Tests unitaires pour le Sceau de la Pureté (seal_of_purity.py).
Valide la détection des hérésies doctrinales selon la TPDU.
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path to import seal_of_purity
sys.path.insert(0, str(Path(__file__).parent.parent))

from seal_of_purity import (
    Heresie, 
    scan_python_duality, 
    scan_c_duality, 
    scan_python_trinite,
    scan_python_resilience,
    GRAVITE_CRITIQUE,
    GRAVITE_MAJEURE,
    GRAVITE_AVERTISSEMENT
)


class TestHeresie(unittest.TestCase):
    """Tests de la classe Heresie."""
    
    def test_heresie_creation(self):
        """Vérifie la création d'une hérésie."""
        h = Heresie(
            "Dualité", 
            "test.py", 
            42, 
            GRAVITE_MAJEURE,
            "Test hérésie",
            "II. L'ARCHITECTURE SACRÉE"
        )
        self.assertEqual(h.type, "Dualité")
        self.assertEqual(h.fichier, "test.py")
        self.assertEqual(h.ligne, 42)
        self.assertEqual(h.gravite, GRAVITE_MAJEURE)
        self.assertEqual(h.texte, "Test hérésie")
        self.assertEqual(h.verset, "II. L'ARCHITECTURE SACRÉE")
    
    def test_heresie_to_markdown(self):
        """Vérifie la conversion en markdown."""
        h = Heresie(
            "Dualité", 
            "test.py", 
            10, 
            GRAVITE_CRITIQUE,
            "Message test",
            "Verset test"
        )
        md = h.to_markdown()
        self.assertIn("**Type**: Dualité", md)
        self.assertIn("`test.py`", md)
        self.assertIn("ligne 10", md)
        self.assertIn("CRITIQUE", md)
        self.assertIn("Message test", md)
        self.assertIn("Verset test", md)


class TestScanPythonDuality(unittest.TestCase):
    """Tests du sceau de la Dualité pour Python."""
    
    def test_forbidden_symbol_detection(self):
        """Vérifie la détection des symboles mathématiques sacrés interdits."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# Test file\n")
            f.write("result = Sʀ * 2\n")
            f.write("value = Iφ + 1\n")
            fname = f.name
        
        try:
            heresies = scan_python_duality(fname)
            # Should detect usage of Sʀ and Iφ
            self.assertGreaterEqual(len(heresies), 2)
            self.assertTrue(any("Sʀ" in h.texte for h in heresies))
            self.assertTrue(any("Iφ" in h.texte for h in heresies))
        finally:
            os.unlink(fname)
    
    def test_duality_import_detection(self):
        """Vérifie la détection des imports directs du Corps Natif."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("import sentire_core\n")
            f.write("from ffi import native_bridge\n")
            fname = f.name
        
        try:
            heresies = scan_python_duality(fname)
            # Should detect imports from forbidden modules
            self.assertGreater(len(heresies), 0)
            self.assertTrue(any("sentire_core" in h.texte or "ffi" in h.texte for h in heresies))
        finally:
            os.unlink(fname)
    
    def test_clean_python_file(self):
        """Vérifie qu'un fichier Python pur ne génère pas d'hérésies de Dualité."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# Clean Python file\n")
            f.write("def hello():\n")
            f.write("    return 'Hello World'\n")
            fname = f.name
        
        try:
            heresies = scan_python_duality(fname)
            self.assertEqual(len(heresies), 0)
        finally:
            os.unlink(fname)


class TestScanCDuality(unittest.TestCase):
    """Tests du sceau de la Dualité pour C/C++."""
    
    def test_strategy_keyword_detection(self):
        """Vérifie la détection des mots-clés stratégiques dans le code C."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write("// Test C file\n")
            f.write("// This uses strategy as a concept\n")
            f.write("void execute() {\n")
            f.write("    int plan = 0;\n")
            f.write("}\n")
            fname = f.name
        
        try:
            heresies = scan_c_duality(fname)
            # Should detect 'strategy' and 'plan'
            self.assertGreaterEqual(len(heresies), 2)
            self.assertTrue(any("strategy" in h.texte for h in heresies))
            self.assertTrue(any("plan" in h.texte for h in heresies))
        finally:
            os.unlink(fname)
    
    def test_clean_c_file(self):
        """Vérifie qu'un fichier C pur ne génère pas d'hérésies de Dualité."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write("// Clean C file\n")
            f.write("int compute(int a, int b) {\n")
            f.write("    return a + b;\n")
            f.write("}\n")
            fname = f.name
        
        try:
            heresies = scan_c_duality(fname)
            self.assertEqual(len(heresies), 0)
        finally:
            os.unlink(fname)


class TestScanPythonTrinite(unittest.TestCase):
    """Tests du sceau de la Trinité Cognitive."""
    
    def test_ml_oracle_fusion_detection(self):
        """Vérifie la détection de la fusion SENTIR/PENSER."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("from ml import feature_extraction\n")
            f.write("from oracle import generative_ai\n")
            f.write("# Fusion profane\n")
            fname = f.name
        
        try:
            heresies = scan_python_trinite(fname)
            # Should detect fusion of ml and oracle
            self.assertGreater(len(heresies), 0)
            self.assertTrue(any("SENTIR" in h.texte and "PENSER" in h.texte for h in heresies))
        finally:
            os.unlink(fname)
    
    def test_chiron_ml_fusion_detection(self):
        """Vérifie la détection de la fusion AGIR/SENTIR."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("from core.actions.chiron import Chiron\n")
            f.write("from ml import model\n")
            fname = f.name
        
        try:
            heresies = scan_python_trinite(fname)
            # Should detect fusion of chiron and ml
            self.assertGreater(len(heresies), 0)
            self.assertTrue(any("AGIR" in h.texte and "SENTIR" in h.texte for h in heresies))
        finally:
            os.unlink(fname)


class TestScanPythonResilience(unittest.TestCase):
    """Tests du sceau de la Résilience."""
    
    def test_unguarded_open_detection(self):
        """Vérifie la détection des open() sans try/except."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def read_file():\n")
            f.write("    f = open('test.txt')\n")
            f.write("    return f.read()\n")
            fname = f.name
        
        try:
            heresies = scan_python_resilience(fname)
            # Should detect open without try/except
            self.assertGreater(len(heresies), 0)
            self.assertTrue(any("open" in h.texte for h in heresies))
            self.assertEqual(heresies[0].gravite, GRAVITE_CRITIQUE)
        finally:
            os.unlink(fname)
    
    def test_guarded_open_no_detection(self):
        """Vérifie qu'un open() avec try/except ne génère pas d'hérésie."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def read_file():\n")
            f.write("    try:\n")
            f.write("        f = open('test.txt')\n")
            f.write("        return f.read()\n")
            f.write("    except Exception as e:\n")
            f.write("        return None\n")
            fname = f.name
        
        try:
            heresies = scan_python_resilience(fname)
            # Should NOT detect open with try/except
            self.assertEqual(len(heresies), 0)
        finally:
            os.unlink(fname)
    
    def test_unguarded_socket_detection(self):
        """Vérifie la détection des opérations socket sans try/except."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("import socket\n")
            f.write("def connect():\n")
            f.write("    s = socket.socket()\n")
            f.write("    return s\n")
            fname = f.name
        
        try:
            heresies = scan_python_resilience(fname)
            # Should detect socket without try/except
            self.assertGreater(len(heresies), 0)
            self.assertTrue(any("socket" in h.texte for h in heresies))
        finally:
            os.unlink(fname)


if __name__ == '__main__':
    unittest.main()
