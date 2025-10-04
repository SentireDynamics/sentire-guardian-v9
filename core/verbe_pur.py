# core/verbe_pur.py
"""
Sanctuaire: Les Schémas de Messages Purs.
Doctrine: La communication interne de l'Esprit doit être immuable et sans effet
de bord. Ce sanctuaire utilise des dataclasses pour définir des 'Verbes Purs',
des structures de données pures qui transportent l'information entre les
sanctuaires sans risque de corruption. Ils sont les mots du langage interne du Vaisseau.
"""
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass(frozen=True)
class Stimulus:
    """
    Un artefact représentant un 'moment' de perception,
    la somme de toutes les sensations du Vaisseau à un instant t.
    """
    material_perception: Dict[str, Any] = field(default_factory=dict)
    contextual_perception: str = ""

@dataclass(frozen=True)
class StateTransition:
    """
    Un artefact qui encapsule le passage d'un état polyvagal à un autre,
    la cause de cette transition et le score de résilience associé.
    """
    from_state: Any # PolyvagalState
    to_state: Any   # PolyvagalState
    resilience_score: float
    triggering_stimulus: Stimulus