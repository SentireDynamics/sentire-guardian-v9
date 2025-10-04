"""
Verbe Pur - Schémas de Messages Purs (Rituel II)

Épigraphe Doctrinale:
Le Verbe Pur définit les schémas de communication sacrés entre tous les
modules du Vaisseau. Messages typés, validés, et purs selon le Rituel II.
Utilise Pydantic pour la validation et la sérialisation.

Rôle dans la Résilience Souveraine:
- Schémas de messages entre modules
- Validation stricte des données (Pydantic)
- Sérialisation/désérialisation sûre
- Contrat de communication inter-modules
- Garantie d'intégrité des échanges
"""

from typing import Literal, Optional
from enum import Enum


class StimulusType(str, Enum):
    """Types de stimuli doctrinaux."""
    FAULT = "FAULT"      # Défaillance technique
    DRIFT = "DRIFT"      # Dérive comportementale
    ATTACK = "ATTACK"    # Attaque hostile


class PolyvagalState(str, Enum):
    """États polyvagaux fondamentaux."""
    VENTRAL = "VENTRAL"          # Sécurité sociale
    SYMPATHETIC = "SYMPATHETIC"  # Mobilisation
    DORSAL = "DORSAL"            # Immobilisation


# TODO: Ajouter schémas Pydantic complets quand pydantic est installé
class StimulusMessage:
    """Schéma d'un message de stimulus."""
    
    def __init__(self, stimulus_type: str, intensity: float, context: dict = None):
        self.type = stimulus_type
        self.intensity = intensity
        self.context = context or {}


class StateMessage:
    """Schéma d'un message d'état."""
    
    def __init__(self, state: str, resilience_score: float, timestamp: float):
        self.state = state
        self.resilience_score = resilience_score
        self.timestamp = timestamp
