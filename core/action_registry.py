"""
Le Grimoire Sacré des Capacités de Chiron
=========================================

Ce sanctuaire contient le registre des actions que Chiron peut exécuter.
C'est la déclaration officielle des capacités de la Volonté, consultée
par la Conscience avant de décréter toute action.

DOCTRINE : La Conscience ne peut commander que ce que la Volonté a déclaré.
"""

import logging
from typing import Dict, Callable, Any, Optional

_log = logging.getLogger(__name__)

class ActionRegistry:
    """
    Le Grimoire des Capacités. Un Singleton Sacré qui contient tous les Actes possibles du Vaisseau.
    Il est forgé une seule fois à l'aube des temps et sa parole est loi.
    """
    _instance: Optional['ActionRegistry'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActionRegistry, cls).__new__(cls)
            # Initialisation du Grimoire au premier appel.
            cls._instance._actions: Dict[str, Callable] = {}
            _log.info("Le Grimoire Sacré est ouvert.")
        return cls._instance
    
    def __init__(self):
        # Éviter la réinitialisation multiple dans le singleton
        if not hasattr(self, '_actions'):
            self._actions: Dict[str, Callable] = {}
            _log.info("Grimoire Sacré des Capacités initialisé.")
    
    def register_action(self, name: str, function: Callable):
        """Inscrire un nouveau Décret dans le Grimoire."""
        if name in self._actions:
            _log.warning(f"WILL: La capacité '{name}' est déjà enregistrée. Remplacement.")
        self._actions[name] = function
        _log.info(f"WILL: Enregistrement de la capacité '{name}'.")
    
    def register(self, action_name: str, function_handler: Callable) -> None:
        """
        Chiron déclare une capacité à sa naissance.
        
        Args:
            action_name: Nom de l'action (ex: "RESTART_DEPENDENCY")
            function_handler: Fonction qui exécute l'action
        """
        self.register_action(action_name, function_handler)
    
    def is_profane(self, action_name: str) -> bool:
        """Vérifie si un Décret est hérétique (inconnu)."""
        return action_name not in self._actions
    
    def is_registered(self, action_name: str) -> bool:
        """
        La Conscience demande si une action est possible.
        
        Args:
            action_name: Nom de l'action à vérifier
            
        Returns:
            True si l'action est déclarée, False sinon
        """
        return action_name in self._actions
    
    def get_action(self, name: str) -> Optional[Callable]:
        """Récupère le rituel associé à un Décret."""
        return self._actions.get(name)
    
    def execute(self, action_name: str, **kwargs: Any) -> None:
        """
        La Conscience commande l'exécution d'une action validée.
        
        Args:
            action_name: Nom de l'action à exécuter
            **kwargs: Paramètres à passer à la fonction
        """
        if self.is_registered(action_name):
            _log.info(f"WILL: Exécution de '{action_name}' avec paramètres: {kwargs}")
            try:
                # La Volonté agit
                self._actions[action_name](**kwargs)
                _log.info(f"WILL: Action '{action_name}' exécutée avec succès.")
            except Exception as e:
                _log.error(f"WILL: Erreur lors de l'exécution de '{action_name}': {e}")
                raise
        else:
            # Cette branche ne devrait jamais être atteinte si la Conscience
            # respecte la doctrine. C'est un dernier rempart.
            _log.error(f"WILL: Tentative d'exécution d'une action non déclarée '{action_name}'.")
            raise ValueError(f"Action '{action_name}' non déclarée dans le Grimoire Sacré.")
    
    def list_actions(self) -> list[str]:
        """
        Retourne la liste de toutes les actions déclarées.
        
        Returns:
            Liste des noms d'actions disponibles
        """
        return list(self._actions.keys())
    
    def get_action_count(self) -> int:
        """
        Retourne le nombre d'actions déclarées.
        
        Returns:
            Nombre d'actions dans le registre
        """
        return len(self._actions)

# --- Liturgie de l'Unification ---

def no_action_function(**kwargs):
    """NO_ACTION est le premier souffle, le silence sacré."""
    _log.info("WILL: NO_ACTION - Le silence sacré de la sagesse.")

def recalibrate_function(**kwargs):
    """RECALIBRATE_SR - Recalibration du Score de Résilience."""
    _log.info("WILL: RECALIBRATE_SR - Recalibration du Score de Résilience.")

# Instance globale du Grimoire Sacré
_action_registry = None

def get_action_registry() -> ActionRegistry:
    """
    Retourne l'instance globale du Grimoire Sacré.
    
    Returns:
        Instance unique du registre d'actions
    """
    global _action_registry
    if _action_registry is None:
        _action_registry = ActionRegistry()
        # Les Actes Fondamentaux sont inscrits. NO_ACTION est le premier souffle, le silence sacré.
        _action_registry.register_action("NO_ACTION", no_action_function)
        _action_registry.register_action("RECALIBRATE_SR", recalibrate_function)
        _log.info("Grimoire Sacré initialisé avec les Actes Fondamentaux.")
    return _action_registry
