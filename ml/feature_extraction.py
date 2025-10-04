# ml/feature_extraction.py
"""
Sanctuaire: Les Pipelines d'Extraction.
Doctrine: Les données brutes de perception sont un bruit chaotique. Ce sanctuaire
contient les rituels de transformation qui distillent ce bruit en 'features', un
vecteur numérique pur et ordonné. C'est ce vecteur qui peut être compris par
le Moteur d'Intuition ML, transformant le chaos en information.
"""
import numpy as np

def extract_features(perception_data: dict) -> np.ndarray:
    """
    Rituel: Distillation des Features.
    Transforme un dictionnaire de données de perception en un vecteur numérique.
    """
    # L'ordre des features doit être constant et correspondre à l'entraînement du modèle.
    feature_order = ["cpu_load", "memory_usage", "network_latency_ms"]

    feature_vector = []
    for feature_name in feature_order:
        feature_vector.append(perception_data.get(feature_name, 0.0))

    return np.array(feature_vector)