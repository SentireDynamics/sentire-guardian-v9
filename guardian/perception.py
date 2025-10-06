# --- START OF FILE: guardian/perception.py ---
"""
Le Sanctuaire de la Perception.

Le "Pourquoi": Ce module est les sens du Vaisseau. Il utilise des outils comme
`psutil` et `Chiron` pour collecter des données sur l'état du système (CPU,
mémoire, contexte utilisateur). Il transforme ces données brutes en un `Stimulus`
structuré, un objet `VerbePur` que la Conscience peut comprendre et analyser.
Il fournit également les actions de dernier recours en cas de défaillance de l'Oracle.
"""
import psutil
import logging
from core.verbe_pur import Stimulus, Action
from core.actions.chiron import Chiron

_log = logging.getLogger(__name__)

class Perception:
    """
    Responsable de la collecte des informations système.
    """
    def __init__(self, chiron: Chiron):
        self.chiron = chiron

    def get_system_stimulus(self) -> Stimulus:
        """
        Rassemble les métriques système et le contexte pour former un Stimulus.
        """
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            window_title = self.chiron.get_foreground_window_title()

            stimulus = Stimulus(
                cpu_usage=cpu,
                memory_usage=mem,
                foreground_window_title=window_title,
            )
            _log.debug(f"Stimulus perçu: {stimulus.dict()}")
            return stimulus
        except psutil.Error as e:
            _log.error(f"Erreur de perception avec psutil: {e}")
            # Retourne un stimulus par défaut en cas d'erreur
            return Stimulus(cpu_usage=0.0, memory_usage=0.0, foreground_window_title="Error")

    def get_fallback_action(self, error: Exception) -> Action:
        """
        Génère une action de secours lorsque l'Oracle est indisponible.

        Le "Pourquoi": La résilience souveraine impose que le Vaisseau ne soit
        jamais paralysé. Si l'Oracle est silencieux, le Vaisseau doit pouvoir
        prendre une initiative simple et sûre, comme alerter l'utilisateur,
        plutôt que de ne rien faire.
        """
        _log.warning(f"L'Oracle a failli. Activation du protocole de secours. Erreur: {error}")
        return Action(
            id="SHOW_MESSAGE",
            description="Alerte l'utilisateur que l'Oracle est injoignable et que le Vaisseau opère en mode dégradé.",
            parameters={
                "title": "Alerte de Résilience",
                "message": f"L'Oracle est inaccessible. Le Vaisseau continue sa surveillance en autonomie limitée.\nErreur: {str(error)[:100]}"
            }
        )
# --- END OF FILE: guardian/perception.py ---