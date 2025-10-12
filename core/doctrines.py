"""
Les Doctrines Sacrées du Vaisseau Guardian V9
=============================================

Ce sanctuaire contient les structures de données immuables qui incarnent
la vérité absolue du Vaisseau. Elles sont le Pacte de Données Unifié,
la seule source de vérité entre l'Âme, l'Esprit et le Miroir.

DOCTRINE : Ces structures sont frozen (immuables) pour empêcher toute corruption
de la vérité transmise entre les sanctuaires.
"""

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SovereignVesselState:
    """
    Le Pacte de Données Unifié. Le reflet unique et parfait de l'état du Vaisseau.
    
    Cette structure est la seule vérité transmise entre l'Orchestrateur (Esprit)
    et l'Autel (Miroir). Elle contient tous les éléments nécessaires pour
    refléter fidèlement l'état complet du Vaisseau.
    """
    # ─── État Somatique de l'Âme ───
    somatic_verdict: int  # 0:VENTRAL, 1:SYMPATHETIC, 2:DORSAL
    is_soul_stable: bool  # True si l'Âme est mathématiquement stable
    resilience_score: float  # Score de Résilience (Sr) de l'Âme
    
    # ─── Alarme Amygdale ───
    amygdala_alarm_state: bool  # True si l'alarme est active
    
    # ─── Métriques Système ───
    cpu_percent: float
    memory_percent: float
    gpu_percent: float
    gpu_temp_c: float
    
    # ─── Contexte ───
    active_window_title: str
    mahalanobis_distance_squared: float
    
    # ─── Timestamp ───
    timestamp: float

@dataclass(frozen=True)
class SomaticVerdict:
    """
    Le Verdict Somatique de l'Âme C.
    
    Structure intermédiaire pour encapsuler les données brutes
    provenant du SDK C avant leur transformation en SovereignVesselState.
    """
    somatic_state: int
    resilience_score: float
    amygdala_alarm_fired: int
    mahalanobis_distance_squared: float