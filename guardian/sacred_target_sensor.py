"""
Le Senseur de la Cible Sacrée - L'Ancre de l'Esprit

Ce senseur est un nouvel organe de perception pour l'Esprit, entièrement dédié à sa mission.
Il transforme le Gardien d'un observateur de soi-même en un protecteur actif.
"""

import psutil
from dataclasses import dataclass
from typing import Optional
import logging

_log = logging.getLogger(__name__)


@dataclass
class TargetVitals:
    """Les signes vitaux de la Cible Sacrée."""
    is_running: bool = False
    status: str = "stopped"
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    pid: Optional[int] = None
    name: str = ""


class SacredTargetSensor:
    """Le senseur dédié à la surveillance de la Cible Sacrée."""
    
    def __init__(self, target_process_name: str):
        self._target_name = target_process_name.lower()
        self._target_proc = None
        _log.info(f"Senseur de Cible Sacrée initialisé pour: {target_process_name}")

    def find_target(self) -> Optional[psutil.Process]:
        """Trouve l'instance du processus de la Cible Sacrée."""
        # Vérifier si le processus précédent est toujours valide
        if (self._target_proc and 
            self._target_proc.is_running() and 
            self._target_proc.name().lower() == self._target_name):
            return self._target_proc

        # Rechercher dans tous les processus
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == self._target_name:
                    self._target_proc = proc
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
        self._target_proc = None
        return None

    def measure_health(self) -> TargetVitals:
        """Mesure la santé de la Cible Sacrée."""
        target_proc = self.find_target()

        if not target_proc:
            # État DORSAL pour la cible : elle n'existe pas.
            return TargetVitals(is_running=False, name=self._target_name)

        try:
            with target_proc.oneshot():
                return TargetVitals(
                    is_running=True,
                    status=target_proc.status(),
                    cpu_percent=target_proc.cpu_percent(),
                    memory_mb=target_proc.memory_info().rss / (1024 * 1024),
                    pid=target_proc.pid,
                    name=target_proc.name()
                )
        except psutil.NoSuchProcess:
            # La cible a disparu entre la découverte et la mesure.
            return TargetVitals(is_running=False, status="terminated", name=self._target_name)
        except (psutil.AccessDenied, psutil.ZombieProcess) as e:
            _log.warning(f"Accès refusé au processus {self._target_name}: {e}")
            return TargetVitals(is_running=False, status="access_denied", name=self._target_name)

    def update_target(self, new_target_name: str):
        """Met à jour le nom de la Cible Sacrée."""
        self._target_name = new_target_name.lower()
        self._target_proc = None  # Réinitialiser la référence
        _log.info(f"Cible Sacrée mise à jour: {new_target_name}")

    def get_target_info(self) -> dict:
        """Retourne les informations sur la cible actuelle."""
        return {
            "target_name": self._target_name,
            "is_monitoring": self._target_proc is not None,
            "current_pid": self._target_proc.pid if self._target_proc else None
        }
