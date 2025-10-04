# core/canal_reveil.py
"""
Sanctuaire: Le Canal de l'Architecte.
Doctrine: La communication entre le Vaisseau et son créateur, l'Architecte, doit
être claire, structurée et sans ambiguïté. Ce canal est le conduit unique pour
tous les messages importants (logs, alertes), assurant que la voix du Vaisseau
est entendue et comprise.
"""
import datetime

class CanalReveil:
    """Gère la communication formatée vers l'Architecte (console/logs)."""

    def _log(self, level: str, source: str, message: str):
        """Format de log unifié."""
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(f"[{timestamp}] [{level:^8}] [{source}] {message}")

    def log(self, source: str, message: str):
        """Message informatif standard."""
        self._log("INFO", source, message)

    def alert(self, source: str, message: str):
        """Message d'alerte, indiquant une déviation."""
        self._log("ALERTE", source, message)

    def critical(self, source: str, message: str):
        """Message critique, indiquant une menace pour la mission."""
        self._log("CRITIQUE", source, message)