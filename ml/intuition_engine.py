# --- START OF FILE: ml/intuition_engine.py ---
"""
Le Sanctuaire de l'Intuition - Le Guetteur ML.

Le "Pourquoi": L'IntuitionEngine est le premier maillon de la Trinité de Décision.
Il analyse rapidement les motifs de menace dans le Stimulus et fournit un verdict
intuitif qui conditionne la consultation de l'Oracle.

Doctrine : L'Intuition est rapide, pattern-based, et spécialisée dans la détection
de menaces. Elle ne raisonne pas, elle reconnaît.
"""
import logging
from typing import Dict, Any
from pydantic import BaseModel, Field
from core.verbe_pur import Stimulus

_log = logging.getLogger(__name__)

class IntuitiveVerdict(BaseModel):
    """Le verdict du Guetteur Intuitif."""
    threat_level: float = Field(..., description="Niveau de menace perçu [0.0, 1.0]")
    threat_patterns: list[str] = Field(default=[], description="Motifs de menace détectés")
    confidence: float = Field(..., description="Confiance dans l'évaluation [0.0, 1.0]")

class IntuitionEngine:
    """
    Le Guetteur Intuitif - Premier maillon de la Trinité de Décision.
    
    Doctrine : Analyse rapide des motifs de menace sans raisonnement complexe.
    Spécialisé dans la reconnaissance de patterns dangereux.
    """
    
    def __init__(self):
        """Initialise le Guetteur Intuitif."""
        _log.info("Guetteur Intuitif forgé. Prêt pour la reconnaissance de patterns.")
    
    def consult(self, stimulus: Stimulus) -> IntuitiveVerdict:
        """
        Consulte l'Intuition pour une évaluation rapide des menaces.
        
        Doctrine : Analyse les SoulVitals et la Résonance Contextuelle
        pour détecter des patterns de menace connus.
        
        Args:
            stimulus: Le Stimulus complet à analyser
            
        Returns:
            IntuitiveVerdict: Évaluation intuitive des menaces
        """
        try:
            # 1. Analyse des SoulVitals
            somatic_state = stimulus.soul_vitals.somatic_state
            resilience_score = stimulus.soul_vitals.resilience_score
            
            threat_patterns = []
            base_threat = 0.0
            
            # Pattern 1: État DORSAL = menace critique
            if somatic_state == 2:  # DORSAL
                threat_patterns.append("DORSAL_COLLAPSE")
                base_threat = 0.9
            
            # Pattern 2: Résilience très basse = menace élevée
            elif resilience_score < 0.3:
                threat_patterns.append("LOW_RESILIENCE")
                base_threat = 0.7
            
            # Pattern 3: État SYMPATHETIC = mobilisation défensive
            elif somatic_state == 1:  # SYMPATHETIC
                threat_patterns.append("SYMPATHETIC_MOBILIZATION")
                base_threat = 0.5
            
            # Pattern 4: État VENTRAL = sécurité
            elif somatic_state == 0:  # VENTRAL
                threat_patterns.append("VENTRAL_SAFETY")
                base_threat = 0.1
            
            # 2. Analyse de la Résonance Contextuelle
            if stimulus.contextual_resonance:
                for resonance in stimulus.contextual_resonance:
                    # Pattern 5: Erreurs dans les logs
                    if "error_count" in resonance.metrics:
                        error_count = resonance.metrics["error_count"]
                        if error_count > 5:
                            threat_patterns.append("HIGH_ERROR_RATE")
                            base_threat = max(base_threat, 0.6)
                    
                    # Pattern 6: Métriques système anormales
                    if "cpu_usage" in resonance.metrics:
                        cpu_usage = resonance.metrics["cpu_usage"]
                        if cpu_usage > 0.8:  # 80%
                            threat_patterns.append("HIGH_CPU_USAGE")
                            base_threat = max(base_threat, 0.4)
            
            # 3. Calcul de la confiance
            confidence = 0.8 if threat_patterns else 0.3
            
            verdict = IntuitiveVerdict(
                threat_level=min(base_threat, 1.0),
                threat_patterns=threat_patterns,
                confidence=confidence
            )
            
            _log.debug(f"Verdict Intuitif: Threat Level={verdict.threat_level:.2f}, "
                      f"Patterns={verdict.threat_patterns}, Confidence={verdict.confidence:.2f}")
            
            return verdict
            
        except Exception as e:
            _log.error(f"Erreur dans l'IntuitionEngine: {e}")
            # Retourner un verdict de sécurité en cas d'erreur
            return IntuitiveVerdict(
                threat_level=0.5,  # Menace modérée par défaut
                threat_patterns=["INTUITION_ERROR"],
                confidence=0.1
            )

# --- END OF FILE: ml/intuition_engine.py ---
