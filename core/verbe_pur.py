# --- START OF FILE: core/verbe_pur.py ---
"""
Le Sanctuaire du Verbe Pur - Perception Graduée.

Le "Pourquoi": Ce module définit les structures de données fondamentales du Vaisseau
en utilisant Pydantic. Il agit comme un contrat, garantissant que les données qui
circulent entre les différents composants (Perception, Conscience, Oracle) sont
toujours valides, structurées et explicites. C'est le langage commun du Grand Œuvre.

Doctrine de la Perception Graduée : 
- SoulVitals : Le sentiment interne de l'Âme (SDK C)
- ContextualResonance : La réalité externe perçue par les senseurs
- Stimulus : La fusion harmonieuse du sentiment et de la réalité
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# --- Structures pour l'Action et le Jugement ---

class Action(BaseModel):
    """L'acte de la Volonté."""
    id: str = Field(..., description="The single, precise action to take. E.g., 'RESTART_SELF', 'NO_ACTION'.")
    parameters: Dict[str, Any] = Field({}, description="Parameters for the action.")

class OracleJudgement(BaseModel):
    """La Sagesse de l'Oracle : la pensée puis l'acte."""
    reasoning: str = Field(..., description="A step-by-step analysis of the situation, confronting Soul Vitals with Contextual Resonance through the lens of TPDU.")
    decree: Action = Field(..., description="The final, justified action decreed by the analysis.")

# --- Structures pour la Perception Graduée ---

class SoulVitals(BaseModel):
    """L'état interne de l'Âme (le SDK C). Le sentiment pur."""
    somatic_state: int = Field(..., description="Le Verdict Somatique de l'Âme: 0:VENTRAL, 1:SYMPATHETIC, 2:DORSAL")
    resilience_score: float = Field(..., description="Score de Résilience [0.0, 1.0]")
    time_in_state_ms: int = Field(..., description="Temps passé dans l'état actuel")

class ContextualResonance(BaseModel):
    """La réalité externe telle que perçue par un senseur. Le contexte objectif."""
    sensor_id: str = Field(..., description="Identifier of the sensor providing the context")
    metrics: Dict[str, float | int | str] = Field(..., description="Quantitative metrics from the external world")

class Stimulus(BaseModel):
    """Le tableau de situation complet. La fusion du sentiment et de la réalité."""
    timestamp_utc: str
    soul_vitals: SoulVitals
    contextual_resonance: Optional[List[ContextualResonance]] = Field(None, description="A list of observations from all active sensors for this cycle.")
# --- END OF FILE: core/verbe_pur.py ---