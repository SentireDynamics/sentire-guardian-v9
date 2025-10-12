# --- START OF FILE: guardian/sensors/base_sensor.py ---
"""
Le Pacte Sacré des Senseurs.

Le "Pourquoi": Cette classe abstraite définit le contrat que tous les senseurs
doivent respecter. Elle garantit l'uniformité et la prévisibilité de l'interface
entre le monde extérieur et la conscience du Vaisseau.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSensor(ABC):
    """
    Le Pacte Sacré. Tout senseur doit hériter de cette base
    et jurer d'implémenter le rituel read().
    
    Doctrine :
    - Chaque senseur doit être pur et focalisé sur une seule facette du monde
    - Le rituel read() doit respecter le Pacte de Célérité (timeout implicite)
    - Les métriques retournées doivent être quantitatives et objectives
    - En cas d'échec, retourner un dictionnaire avec une clé "error"
    """
    
    @abstractmethod
    def read(self) -> Dict[str, Any]:
        """
        Lit une facette du monde extérieur et la transmute en un dictionnaire de métriques.
        
        Doctrine du Pacte de Célérité :
        - Doit s'exécuter rapidement (< 1 seconde)
        - Ne doit pas bloquer indéfiniment
        - Doit gérer gracieusement les erreurs
        
        Returns:
            Dict[str, Any]: Métriques quantitatives du monde extérieur.
                           En cas d'erreur, doit contenir une clé "error" avec la description.
        
        Raises:
            Ne doit jamais lever d'exception. Toutes les erreurs doivent être
            encapsulées dans le dictionnaire de retour.
        """
        pass
    
    @property
    @abstractmethod
    def sensor_id(self) -> str:
        """
        Identifiant unique du senseur.
        
        Returns:
            str: Identifiant unique pour ce senseur (ex: "log_file_monitor", "cpu_watcher")
        """
        pass
# --- END OF FILE: guardian/sensors/base_sensor.py ---
