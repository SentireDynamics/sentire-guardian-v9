# ml/model_manager.py
"""
Sanctuaire: Le Gestionnaire de Modèles.
Doctrine: Les modèles ML sont des Artefacts précieux, des connaissances distillées
sous forme de poids numériques. Ce gestionnaire est le gardien de ces artefacts.
Il est responsable de leur chargement sécurisé en mémoire (sérialisation) et de
leur sauvegarde, assurant la persistance de l'intuition du Vaisseau.
"""
import joblib
from pathlib import Path
from typing import Any

class ModelManager:
    """Charge et sauvegarde les modèles ML depuis le disque."""

    def load(self, path: str) -> Any:
        """
        Rituel: Éveil du Modèle.
        Charge un artefact modèle depuis le disque.
        """
        model_path = Path(path)
        if not model_path.exists():
            return None
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            print(f"ERREUR GESTIONNAIRE ML: Échec du chargement du modèle {path}: {e}")
            return None

    def save(self, model: Any, path: str):
        """
        Rituel: Cristallisation de la Connaissance.
        Sauvegarde un artefact modèle sur le disque.
        """
        try:
            joblib.dump(model, path)
        except Exception as e:
            print(f"ERREUR GESTIONNAIRE ML: Échec de la sauvegarde du modèle {path}: {e}")