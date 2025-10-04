# tests/test_cerberus.py
"""
Validation Doctrinale: Rituel d'Intégrité.
Ce test s'assure que le gardien Cerberus est vigilant. Nous validons sa
capacité à reconnaître un fichier pur et, plus important encore, à détecter
une corruption, protégeant ainsi le Vaisseau du tampering.
"""
import hashlib
from guardian.cerberus import Cerberus

def test_cerberus_integrity_check(tmp_path):
    """Vérifie le rituel de vérification d'intégrité."""
    # Créer un fichier critique factice
    critial_file = tmp_path / "critical.py"
    critial_file.write_text("print('pure code')")

    # Calculer son hash
    hasher = hashlib.sha256()
    hasher.update(b"print('pure code')")
    pure_hash = hasher.hexdigest()

    # Configurer Cerberus pour ce test
    cerberus = Cerberus()
    cerberus.CRITICAL_FILES = [critial_file]
    cerberus.KNOWN_HASHES = {str(critial_file): pure_hash}

    # Vérifier que le code pur passe le test
    assert cerberus.perform_integrity_check() is True

    # Corrompre le fichier
    critial_file.write_text("print('tampered code')")

    # Vérifier que le code corrompu échoue le test
    assert cerberus.perform_integrity_check() is False