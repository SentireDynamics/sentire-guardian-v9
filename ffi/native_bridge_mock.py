# --- MOCK DU SDK NATIF POUR TESTS ---
"""
Mock temporaire du SDK Natif pour tester la communication.
Ce mock simule le comportement du SDK natif sans nécessiter de compilation C.
"""
import logging
import random
import math
from ffi.native_bridge import SentireConfig, SentireStimulus, SentireVerdict, create_default_config

_log = logging.getLogger(__name__)


class NativeBridgeMock:
    """
    Mock du NativeBridge qui simule le comportement du SDK natif.
    """
    
    def __init__(self, library_path: str = None, config: SentireConfig = None):
        """Initialise le mock avec une configuration par défaut."""
        if config is None:
            self.config = create_default_config()
            _log.info("Mock: Configuration par défaut chargée pour l'Âme.")
        else:
            self.config = config
        
        # État interne simulé
        self._current_state = 2  # DORSAL au départ
        self._last_verdict = None
        self._cycle_count = 0
        self._last_stimulus = None
        
        _log.info(f"Mock: Âme simulée créée (chemin ignoré: {library_path})")
    
    def process(self, stimulus: SentireStimulus) -> SentireVerdict:
        """
        Simule le traitement d'un stimulus et retourne un verdict.
        """
        self._cycle_count += 1
        self._last_stimulus = stimulus
        
        # Calculer un score de résilience basé sur les métriques
        cpu = float(stimulus.cpu_usage)
        memory = float(stimulus.memory_usage)
        gpu = float(stimulus.gpu_usage)
        
        # Impact brut simulé (formule simplifiée)
        impact_base = (
            cpu * self.config.weight_cpu +
            memory * self.config.weight_memory +
            gpu * self.config.weight_gpu
        )
        
        # Score de résilience
        resilience_score = max(0.0, min(1.0, 1.0 - impact_base))
        
        # Ajouter un peu de bruit pour rendre réaliste
        resilience_score += random.uniform(-0.05, 0.05)
        resilience_score = max(0.0, min(1.0, resilience_score))
        
        # Déterminer l'état polyvagal
        if resilience_score >= self.config.state_threshold_ventral:
            new_state = 0  # VENTRAL
        elif resilience_score >= self.config.state_threshold_dorsal:
            new_state = 1  # SYMPATHETIC
        else:
            new_state = 2  # DORSAL
        
        # Transition progressive vers le nouvel état (hystérésis simulée)
        if new_state != self._current_state:
            # 30% de chance de transition
            if random.random() < 0.3:
                self._current_state = new_state
        
        # Alarme amygdale simulée (10% de chance si CPU ou mémoire > 80%)
        alarm_fired = 0
        if cpu > 0.8 or memory > 0.8:
            if random.random() < 0.1:
                alarm_fired = 1
        
        # Créer le verdict
        verdict = SentireVerdict()
        verdict.final_state = self._current_state
        verdict.amygdala_alarm_fired = alarm_fired
        verdict.resilience_score = resilience_score
        verdict.impact_score = impact_base
        verdict.impact_base = impact_base
        
        # Stocker pour get_last_verdict
        self._last_verdict = verdict
        
        state_names = ["VENTRAL", "SYMPATHETIC", "DORSAL"]
        _log.debug(
            f"Mock: Verdict généré → État={state_names[self._current_state]} "
            f"Sr={resilience_score:.3f} Alarme={'OUI' if alarm_fired else 'NON'}"
        )
        
        return verdict
    
    def get_last_verdict(self) -> SentireVerdict:
        """Retourne le dernier verdict émis."""
        return self._last_verdict
    
    def get_version(self) -> str:
        """Retourne la version du mock."""
        return "MOCK-2.0.0"
    
    def destroy(self):
        """Libère les ressources (rien à faire pour le mock)."""
        _log.info("Mock: Âme simulée libérée.")
