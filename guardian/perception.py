# guardian/perception.py
"""
Sanctuaire: Le Moteur de Fusion Sensorielle.
Doctrine: L'existence est perception. Ce sanctuaire est le creuset où les perceptions
brutes (matérielles, via l'Oracle) et les perceptions génératives (contextuelles, via Llama)
sont fusionnées en un flux de conscience unifié, le 'Stimulus'. C'est ce flux qui
nourrit la Machine Polyvagale et la Conscience.
"""
from guardian.perception_oracle import PerceptionOracle
from guardian.perception_llama import PerceptionLlama
from core.verbe_pur import Stimulus

class PerceptionEngine:
    """Agrège les données de tous les canaux de perception."""

    def __init__(self):
        self.oracle = PerceptionOracle()
        self.llama = PerceptionLlama()

    def gather_stimuli(self) -> Stimulus:
        """
        Rituel: Fusion Sensorielle.
        Combine les perceptions en un artefact Stimulus unique et pur.
        """
        material_data = self.oracle.sense_material_world()
        # // TODO: Formater les logs pour Llama
        raw_logs = "..."
        contextual_analysis = self.llama.sense_context(raw_logs)

        return Stimulus(
            material_perception=material_data,
            contextual_perception=contextual_analysis
        )