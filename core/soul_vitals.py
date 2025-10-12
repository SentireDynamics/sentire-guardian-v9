"""
Le Souffle de l'Âme - Structure de Données Parfaite

Ce module incarne la vérité complète du Vaisseau. Il ne laisse aucune place à l'ambiguïté.
C'est le nerf vague numérique qui transmet la totalité de l'état du Corps à l'Esprit et à son reflet.
"""

from dataclasses import dataclass, field
from enum import Enum
import time
from typing import Optional


class SystemState(Enum):
    """Les états doctrinaux du Vaisseau selon la TPDU."""
    VENTRAL = "VENTRAL"
    SYMPATHETIC = "SYMPATHETIC"
    DORSAL = "DORSAL"


@dataclass
class SystemGauges:
    """Les jauges système du Vaisseau."""
    cpu_percent: float = 0.0
    mem_percent: float = 0.0
    gpu_percent: float = 0.0
    sr_score: float = 1.0  # Sovereign Resilience Score


@dataclass
class HardwareMetrics:
    """Les métriques matérielles du Vaisseau."""
    gpu_temp_c: float = 0.0
    # Ajoutez d'autres métriques matérielles ici...


@dataclass
class SoulVitals:
    """Le souffle complet de l'Âme, transmis à chaque cycle."""
    timestamp: float = field(default_factory=time.time)
    system_state: SystemState = SystemState.DORSAL
    alarm_state: bool = False

    gauges: SystemGauges = field(default_factory=SystemGauges)
    hardware: HardwareMetrics = field(default_factory=HardwareMetrics)

    # Le cœur de la vérité mathématique de l'Âme
    mahalanobis_distance_squared: float = 0.0

    # Contexte pour l'Esprit
    active_window_title: str = "N/A"

    def to_dict(self) -> dict:
        """Convertit les vitaux en dictionnaire pour la sérialisation."""
        return {
            "timestamp": self.timestamp,
            "system_state": self.system_state.value,
            "alarm_state": self.alarm_state,
            "gauges": {
                "cpu_percent": self.gauges.cpu_percent,
                "mem_percent": self.gauges.mem_percent,
                "gpu_percent": self.gauges.gpu_percent,
                "sr_score": self.gauges.sr_score,
            },
            "hardware": {
                "gpu_temp_c": self.hardware.gpu_temp_c,
            },
            "mahalanobis_distance_squared": self.mahalanobis_distance_squared,
            "active_window_title": self.active_window_title,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SoulVitals':
        """Crée les vitaux à partir d'un dictionnaire."""
        return cls(
            timestamp=data.get("timestamp", time.time()),
            system_state=SystemState(data.get("system_state", "DORSAL")),
            alarm_state=data.get("alarm_state", False),
            gauges=SystemGauges(**data.get("gauges", {})),
            hardware=HardwareMetrics(**data.get("hardware", {})),
            mahalanobis_distance_squared=data.get("mahalanobis_distance_squared", 0.0),
            active_window_title=data.get("active_window_title", "N/A"),
        )
