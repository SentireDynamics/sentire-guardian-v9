import joblib
import numpy as np
import os
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "anomaly_model.joblib"

class AnomalyDetector:
    """
    Le module d'Intuition, utilisant un modèle ML pour détecter des anomalies.

    @doctrine
    L'intuition complète la perception brute par une reconnaissance de formes subtiles.
    Ce modèle, bien que simple, incarne le principe d'apprentissage. Il a été entraîné
    à reconnaître des combinaisons "anormales" de métriques et fournit un score
    quantifiant cette intuition. Ce score est un stimulus à part entière pour le
    calcul de la résilience.
    """
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            print(f"Modèle non trouvé à {MODEL_PATH}. Création d'un modèle factice.")
            self._create_dummy_model()
        self.model = joblib.load(MODEL_PATH)

    def _create_dummy_model(self):
        """Crée, entraîne et sauvegarde un modèle factice."""
        X = np.random.rand(100, 2) * 100 # cpu_load, memory_usage
        # Anomalies = haute charge CPU ET haute mémoire
        y = ((X[:, 0] > 80) & (X[:, 1] > 80)).astype(int)

        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump(model, MODEL_PATH)

    def predict_anomaly(self, metrics: dict) -> float:
        """
        Prédit un score d'anomalie basé sur les métriques système.
        Retourne la probabilité d'être dans la classe "anomalie" (1).
        """
        cpu = metrics.get('cpu_load', 50.0)
        mem = metrics.get('memory_usage', 50.0)

        # Le modèle attend un array 2D
        features = np.array([[cpu, mem]])

        # predict_proba retourne les probabilités pour [classe_0, classe_1]
        anomaly_prob = self.model.predict_proba(features)[0][1]

        return anomaly_prob