# --- START OF FILE: guardian/sensors/log_file_sensor.py ---
"""
Le Premier Acolyte : Senseur de Surveillance des Logs.

Le "Pourquoi": Ce senseur surveille les fichiers de logs pour détecter des patterns
d'erreur ou d'anomalie. Il incarne la doctrine de la vigilance externe, permettant
au Vaisseau de percevoir les signaux de détresse du monde extérieur.
"""
import logging
from .base_sensor import BaseSensor
from typing import Dict, Any

_log = logging.getLogger(__name__)

class LogFileSensor(BaseSensor):
    """
    Senseur de surveillance des fichiers de logs.
    
    Doctrine :
    - Surveille un fichier de log spécifique
    - Détecte des mots-clés d'erreur prédéfinis
    - Retourne des métriques quantitatives sur l'état des logs
    - Respecte le Pacte de Célérité avec lecture limitée
    """
    
    def __init__(self, log_file_path: str, error_keywords: list[str]):
        """
        Initialise le senseur de logs.
        
        Args:
            log_file_path: Chemin vers le fichier de log à surveiller
            error_keywords: Liste des mots-clés à rechercher (insensible à la casse)
        """
        self.log_file_path = log_file_path
        self.error_keywords = [kw.lower() for kw in error_keywords]
        self._sensor_id = f"log_file_monitor_{log_file_path.replace('/', '_').replace('\\', '_')}"
    
    @property
    def sensor_id(self) -> str:
        """Identifiant unique du senseur."""
        return self._sensor_id
    
    def read(self) -> Dict[str, Any]:
        """
        Lit le fichier de log et analyse les dernières lignes pour détecter des erreurs.
        
        Doctrine du Pacte de Célérité :
        - Lit seulement les 100 dernières lignes pour éviter la lenteur
        - Gère gracieusement les erreurs de fichier
        - Retourne toujours un dictionnaire valide
        
        Returns:
            Dict[str, Any]: Métriques sur l'état des logs
        """
        try:
            # Pour la simplicité, nous lisons les N dernières lignes
            # Une implémentation plus robuste suivrait le fichier en temps réel
            with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[-100:]  # Lire les 100 dernières lignes
            
            error_count = 0
            warning_count = 0
            
            for line in lines:
                line_lower = line.lower()
                if any(kw in line_lower for kw in self.error_keywords):
                    error_count += 1
                elif 'warning' in line_lower or 'warn' in line_lower:
                    warning_count += 1
            
            return {
                "lines_scanned": len(lines),
                "error_count": error_count,
                "warning_count": warning_count,
                "error_rate": error_count / max(len(lines), 1),
                "status": "healthy" if error_count == 0 else "degraded" if error_count < 5 else "critical"
            }
            
        except FileNotFoundError:
            _log.warning(f"Senseur de log : fichier non trouvé à {self.log_file_path}")
            return {
                "error": "FileNotFound",
                "status": "unavailable",
                "lines_scanned": 0,
                "error_count": 0,
                "warning_count": 0
            }
        except PermissionError:
            _log.warning(f"Senseur de log : accès refusé à {self.log_file_path}")
            return {
                "error": "PermissionDenied",
                "status": "unavailable",
                "lines_scanned": 0,
                "error_count": 0,
                "warning_count": 0
            }
        except Exception as e:
            _log.error(f"Erreur dans le senseur de log : {e}")
            return {
                "error": str(e),
                "status": "error",
                "lines_scanned": 0,
                "error_count": 0,
                "warning_count": 0
            }
# --- END OF FILE: guardian/sensors/log_file_sensor.py ---
