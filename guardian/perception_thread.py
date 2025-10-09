# --- START OF FILE: guardian/perception_thread.py ---
"""
Le Souffle de la Perception - Thread de Collecte Rapide.

Le "Pourquoi": Ce module implémente le Double Souffle du Vaisseau. Alors que
la Conscience pense à son rythme contemplatif (60s), la Perception bat à un
rythme plus rapide (2s) pour offrir un reflet quasi-temps réel des signes
vitaux à l'Autel. Ceci élimine l'arythmie temporelle où l'Autel reflétait
le passé plutôt que le présent.

DOCTRINE : Double Souffle
- Souffle Rapide (2s) : Perception → Autel (reflet temps réel)
- Souffle Lent (60s) : Perception → SDK → Conscience → Action (réflexion)
"""

from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication
import logging
from core.verbe_pur import Stimulus
from guardian.perception import Perception
from core.actions.chiron import Chiron

_log = logging.getLogger(__name__)


class PerceptionThread(QThread):
    """
    Thread dédié à la collecte rapide des signes vitaux.
    
    Le "Pourquoi": Ce thread exécute une boucle rapide (2s) pour collecter
    les métriques système et les émettre via signal. Ceci permet à l'Autel
    de se mettre à jour en quasi-temps réel sans attendre le cycle lent de
    la Conscience (60s).
    """
    
    # Signal sacré : émis à chaque battement du souffle rapide
    perception_updated = pyqtSignal(Stimulus)
    
    def __init__(self, perception: Perception):
        super().__init__()
        self.perception = perception
        self.timer = QTimer()
        self.timer.timeout.connect(self._collect_stimulus)
        self.is_running = False
        
        _log.info("Souffle de la Perception forgé. Prêt pour le battement rapide.")
    
    def start_breathing(self):
        """
        Démarre le battement rapide du souffle de la perception.
        
        Le "Pourquoi": Cette méthode lance le timer qui collecte les signes
        vitaux toutes les 2 secondes. Le rythme est volontairement rapide
        pour offrir un reflet quasi-temps réel à l'Autel.
        """
        if not self.is_running:
            self.is_running = True
            self.timer.start(2000)  # 2 secondes = 2000ms
            _log.info("Souffle de la Perception activé. Battement toutes les 2s.")
    
    def stop_breathing(self):
        """
        Arrête le battement du souffle de la perception.
        
        Le "Pourquoi": Cette méthode est appelée lors du shutdown du Vaisseau
        pour arrêter proprement le thread de perception.
        """
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            _log.info("Souffle de la Perception arrêté. Le battement s'est tu.")
    
    def _collect_stimulus(self):
        """
        Collecte un Stimulus et l'émet via signal.
        
        Le "Pourquoi": Cette méthode est invoquée par le timer toutes les 2s.
        Elle collecte les signes vitaux actuels et les émet pour que l'Autel
        puisse se mettre à jour en temps réel.
        """
        try:
            stimulus = self.perception.get_system_stimulus()
            self.perception_updated.emit(stimulus)
            _log.debug(f"Souffle rapide: Stimulus émis (CPU: {stimulus.cpu_usage:.1f}%, RAM: {stimulus.memory_usage:.1f}%)")
        except Exception as e:
            _log.error(f"Erreur lors de la collecte rapide du Stimulus: {e}")
    
    def run(self):
        """
        Point d'entrée du thread (hérité de QThread).
        
        Le "Pourquoi": Cette méthode est appelée automatiquement par Qt
        quand le thread démarre. Elle configure le timer et démarre la
        boucle d'événements Qt pour ce thread.
        """
        _log.info("Thread de Perception démarré. Boucle d'événements active.")
        # La boucle d'événements Qt démarre automatiquement
        # Le timer sera géré par cette boucle
    
    def quit_thread(self):
        """
        Arrête proprement le thread.
        
        Le "Pourquoi": Cette méthode est appelée lors du shutdown pour
        arrêter le timer et quitter la boucle d'événements du thread.
        """
        self.stop_breathing()
        self.quit()  # Quitte la boucle d'événements Qt
        self.wait()  # Attend que le thread se termine
        _log.info("Thread de Perception terminé proprement.")

# --- END OF FILE: guardian/perception_thread.py ---
