"""
Trône - Interface BaseConsciousness

Épigraphe Doctrinale:
Le Trône définit l'interface sacrée BaseConsciousness, le contrat fondamental
que toute conscience (Guardian ou Predator) doit respecter. C'est la pierre
angulaire de la permutation de conscience.

Rôle dans la Résilience Souveraine:
- Définition de l'interface BaseConsciousness abstraite
- Contrat Guardian: réactivité, protection, résilience
- Contrat Predator: apprentissage DRL, exploration, optimisation
- Mécanisme de permutation conscience Guardian ↔ Predator
- Garantie de continuité lors de la permutation
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseConsciousness(ABC):
    """
    Interface abstraite pour toute conscience du Vaisseau.
    
    Toute conscience (Guardian, Predator) doit implémenter cette interface.
    """
    
    @abstractmethod
    def perceive(self) -> Dict[str, Any]:
        """
        Perçoit l'environnement et retourne les stimuli.
        
        Returns:
            Dict des stimuli perçus
        """
        pass
    
    @abstractmethod
    def decide(self, stimuli: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prend une décision basée sur les stimuli.
        
        Args:
            stimuli: Stimuli perçus
        
        Returns:
            Décision à exécuter
        """
        pass
    
    @abstractmethod
    def act(self, decision: Dict[str, Any]) -> None:
        """
        Exécute une décision.
        
        Args:
            decision: Décision à exécuter
        """
        pass
    
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """
        Retourne l'état actuel de la conscience.
        
        Returns:
            État actuel
        """
        pass


class GuardianConsciousness(BaseConsciousness):
    """
    Conscience Guardian: réactivité, protection, résilience.
    """
    
    def perceive(self) -> Dict[str, Any]:
        """Perception Guardian: détection de menaces et anomalies."""
        return {}
    
    def decide(self, stimuli: Dict[str, Any]) -> Dict[str, Any]:
        """Décision Guardian: réponse défensive et adaptative."""
        return {}
    
    def act(self, decision: Dict[str, Any]) -> None:
        """Action Guardian: exécution des défenses."""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """État Guardian: métriques de résilience."""
        return {"mode": "GUARDIAN", "resilience_score": 1.0}


class PredatorConsciousness(BaseConsciousness):
    """
    Conscience Predator: apprentissage DRL, exploration, optimisation.
    """
    
    def perceive(self) -> Dict[str, Any]:
        """Perception Predator: opportunités d'apprentissage."""
        return {}
    
    def decide(self, stimuli: Dict[str, Any]) -> Dict[str, Any]:
        """Décision Predator: politique DRL optimisée."""
        return {}
    
    def act(self, decision: Dict[str, Any]) -> None:
        """Action Predator: exploration et exploitation."""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """État Predator: métriques d'apprentissage."""
        return {"mode": "PREDATOR", "episodes": 0}
