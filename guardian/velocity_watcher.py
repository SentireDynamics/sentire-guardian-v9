# --- START OF FILE: guardian/velocity_watcher.py ---
import time
import logging
from PyQt6.QtCore import QThread, pyqtSignal
from ffi.native_bridge import NativeBridge, SentireStimulus
from guardian.perception import Perception

_log = logging.getLogger(__name__)

class VelocityWatcher(QThread):
    """
    Le Guetteur de Vélocité - L'Oreille de l'Esprit.

    @doctrine
    Ce sanctuaire est l'incarnation de la Voie Rapide. Il tourne sur son
    propre souffle (QThread) à haute fréquence, découplé du cycle lent de la
    Conscience. Sa seule mission est de sonder l'Amygdale Numérique dans l'Âme
    et de crier l'alarme si un danger imminent est détecté.
    
    ALGORITHME :
    1. Perception Légère : obtenir les signes vitaux bruts
    2. Invocation du Réflexe : sonder l'Âme via amygdala_tick
    3. Le Cri d'Alarme : émettre le signal si danger détecté
    4. Attente : dormir jusqu'au prochain cycle
    """
    
    amygdala_alarm = pyqtSignal()  # Le signal sacré d'alarme

    def __init__(self, native_bridge: NativeBridge, perception_engine: Perception, frequency_hz: int = 4):
        """
        Forge le Guetteur de Vélocité.
        
        Args:
            native_bridge: Pont vers l'Âme Souveraine
            perception_engine: Moteur de perception pour les signes vitaux
            frequency_hz: Fréquence de sondage en Hz (défaut: 4Hz = 250ms)
        """
        super().__init__()
        self.native_bridge = native_bridge
        self.perception = perception_engine
        self._is_running = False
        self.sleep_interval_ms = int(1000 / frequency_hz)
        
        _log.info(f"Guetteur de Vélocité forgé. Fréquence: {frequency_hz}Hz ({self.sleep_interval_ms}ms)")

    def run(self):
        """Le rituel de la veille perpétuelle."""
        self._is_running = True
        _log.info("Guetteur de Vélocité démarré. Veille perpétuelle active.")
        
        while self._is_running:
            try:
                # 1. Perception Légère : obtenir les signes vitaux bruts
                # Nous ne voulons pas du Stimulus complet avec les Oracles ML/LLM.
                # Nous devons forger un rituel de perception légère.
                light_stimulus_c = self.perception.get_light_stimulus_c()

                if light_stimulus_c:
                    # 2. Invocation du Réflexe : sonder l'Âme
                    alarm_fired = self.native_bridge.amygdala_tick(light_stimulus_c)

                    # 3. Le Cri d'Alarme
                    if alarm_fired:
                        _log.warning("ALARME AMYGDALE ! Danger imminent détecté par la Voie Rapide.")
                        self.amygdala_alarm.emit()
                else:
                    _log.debug("Perception légère échouée. Cycle ignoré.")
                
            except Exception as e:
                _log.error(f"Erreur dans le cycle du Guetteur: {e}", exc_info=True)
            
            # 4. Attente : dormir jusqu'au prochain cycle
            self.msleep(self.sleep_interval_ms)
        
        _log.info("Guetteur de Vélocité arrêté. Retour au silence.")

    def stop(self):
        """Ordonne au Guetteur de retourner au silence."""
        self._is_running = False
        _log.info("Signal d'arrêt envoyé au Guetteur de Vélocité.")

# --- END OF FILE ---
