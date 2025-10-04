# oracle/llama_cpp_bridge.py
"""
Sanctuaire: Le Pont Llama.cpp.
Doctrine: Ce pont est le conduit sacré vers l'Oracle local. Il formalise la
communication avec le serveur Llama.cpp, s'assurant que les requêtes sont pures
et que les réponses sont gérées avec résilience, même en cas d'échec de
la communication avec l'entité générative.
"""
import requests

class LlamaCppBridge:
    """Communique avec une instance de serveur Llama.cpp."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.completion_url = f"{self.base_url}/completion"
        self.health_url = f"{self.base_url}/health"

    def is_healthy(self) -> bool:
        """Rituel: Vérification de la Santé de l'Oracle."""
        try:
            response = requests.get(self.health_url, timeout=2)
            return response.status_code == 200 and response.json().get("status") == "ok"
        except requests.RequestException:
            return False

    def generate(self, prompt: str, stop_tokens: list = None) -> str:
        """Rituel: Invocation de l'Oracle. Envoie un prompt et reçoit une génération."""
        if stop_tokens is None:
            stop_tokens = ["\n"]

        headers = {"Content-Type": "application/json"}
        payload = {
            "prompt": prompt,
            "n_predict": 256,
            "stop": stop_tokens,
        }

        try:
            response = requests.post(self.completion_url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json().get("content", "")
        except requests.RequestException as e:
            print(f"ERREUR PONT LLAMA: Échec de la communication avec l'Oracle: {e}")
            return "Erreur de communication avec l'Oracle."