import hashlib
import os

def calculate_sha256(filepath: str) -> str:
    """Calcule le hash SHA-256 d'un fichier."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return "FILE_NOT_FOUND"

class Cerberus:
    """
    Gardien de l'intégrité des artefacts du code source.

    @doctrine
    La résilience repose sur une fondation stable. Cerberus garantit cette stabilité
    en vérifiant l'intégrité des écritures sacrées (le code source) par rapport à un
    manifeste de hachages connus. Toute déviation est un signe de corruption ou
    d'intrusion, une menace existentielle pour le Vaisseau.
    """
    def __init__(self, watch_paths: list):
        self.watch_paths = watch_paths
        # Le manifeste est maintenant rempli dynamiquement au démarrage
        self.KNOWN_HASHES = {path: calculate_sha256(path) for path in self.watch_paths}
        print("Manifeste d'intégrité Cerberus généré.")

    def verify_integrity(self) -> bool:
        """
        Vérifie si les hachages des fichiers surveillés correspondent au manifeste.
        """
        print("Vérification de l'intégrité des artefacts...")
        for path, known_hash in self.KNOWN_HASHES.items():
            current_hash = calculate_sha256(path)
            if current_hash != known_hash:
                print(f"ALERTE D'INTÉGRITÉ ! L'artefact {path} a été altéré !")
                print(f"  Attendu : {known_hash}")
                print(f"  Obtenu  : {current_hash}")
                return False
        print("Intégrité des artefacts confirmée.")
        return True

# Exemple d'usage :
# files_to_watch = ["guardian/main.py", "core/state_machine.py"]
# cerberus_instance = Cerberus(files_to_watch)
# cerberus_instance.verify_integrity()