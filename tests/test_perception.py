# tests/test_perception.py
"""
Validation Doctrinale: Fusion Sensorielle.
Ce test valide le rituel de fusion du Moteur de Perception. En fournissant
des perceptions simulées (mockées) des oracles matériel et génératif, nous
nous assurons qu'ils sont correctement agrégés en un artefact Stimulus pur.
"""
from guardian.perception import PerceptionEngine
from unittest.mock import MagicMock

def test_perception_engine_aggregation():
    """Vérifie que le moteur agrège correctement les données."""
    engine = PerceptionEngine()

    # Mocker les sous-moteurs
    engine.oracle = MagicMock()
    engine.llama = MagicMock()

    engine.oracle.sense_material_world.return_value = {"cpu_load": 50.0}
    engine.llama.sense_context.return_value = "Anomaly detected in auth logs."

    stimulus = engine.gather_stimuli()

    assert stimulus.material_perception["cpu_load"] == 50.0
    assert stimulus.contextual_perception == "Anomaly detected in auth logs."
    engine.oracle.sense_material_world.assert_called_once()
    engine.llama.sense_context.assert_called_once()