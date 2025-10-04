"""
Feature Extraction - Pipelines d'Intuition

Épigraphe Doctrinale:
L'extraction de features transforme les stimuli bruts en vecteurs d'intuition
exploitables par les modèles ML. Pipelines doctrinaux pour chaque type de stimulus,
extraction multi-échelle, et enrichissement contextuel.

Rôle dans la Résilience Souveraine:
- Extraction de features depuis stimuli bruts
- Pipelines spécialisés par type de stimulus
- Features temporelles (tendances, vélocité)
- Features contextuelles (état, historique)
- Normalisation et standardisation
- Réduction de dimensionnalité si nécessaire
"""

from typing import Dict, List, Any
import math


class FeatureExtractor:
    """
    Extracteur de features pour l'intuition ML.
    """
    
    def __init__(self):
        """Initialise l'extracteur de features."""
        self.history = []
    
    def extract(self, stimulus: Dict, context: Dict) -> Dict[str, float]:
        """
        Extrait les features d'un stimulus.
        
        Args:
            stimulus: Stimulus brut
            context: Contexte opérationnel
        
        Returns:
            Features extraites
        """
        features = {}
        
        # Features basiques
        features['intensity'] = stimulus.get('intensity', 0.0)
        features['type_fault'] = 1.0 if stimulus.get('type') == 'FAULT' else 0.0
        features['type_drift'] = 1.0 if stimulus.get('type') == 'DRIFT' else 0.0
        features['type_attack'] = 1.0 if stimulus.get('type') == 'ATTACK' else 0.0
        
        # Features temporelles
        features.update(self._extract_temporal_features())
        
        # Features contextuelles
        features.update(self._extract_contextual_features(context))
        
        # Ajouter à l'historique
        self.history.append(stimulus)
        
        return features
    
    def _extract_temporal_features(self) -> Dict[str, float]:
        """Extrait les features temporelles."""
        if len(self.history) < 2:
            return {'velocity': 0.0, 'trend': 0.0}
        
        # Vélocité: taux de changement
        recent = self.history[-5:] if len(self.history) >= 5 else self.history
        intensities = [s.get('intensity', 0.0) for s in recent]
        velocity = (intensities[-1] - intensities[0]) / len(intensities) if len(intensities) > 1 else 0.0
        
        # Tendance: moyenne des derniers stimuli
        trend = sum(intensities) / len(intensities) if intensities else 0.0
        
        return {'velocity': velocity, 'trend': trend}
    
    def _extract_contextual_features(self, context: Dict) -> Dict[str, float]:
        """Extrait les features contextuelles."""
        features = {}
        
        # État polyvagal
        state = context.get('state', 'VENTRAL')
        features['state_ventral'] = 1.0 if state == 'VENTRAL' else 0.0
        features['state_sympathetic'] = 1.0 if state == 'SYMPATHETIC' else 0.0
        features['state_dorsal'] = 1.0 if state == 'DORSAL' else 0.0
        
        # Score de résilience
        features['resilience_score'] = context.get('resilience_score', 1.0)
        
        return features
