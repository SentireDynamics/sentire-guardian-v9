# guardian/perception_llama.py
"""
Sanctuaire: La Perception Générative.
Doctrine: Au-delà du matériel, il y a le contexte. Ce sanctuaire utilise l'Oracle
local (Llama.cpp) pour transformer les logs bruts en une compréhension narrative
de la situation. Il donne un sens, une intentionnalité perçue, aux événements.
"""
from oracle.llama_cpp_bridge import LlamaCppBridge
from oracle.generative_ai import GenerativeAI

class PerceptionLlama:
    """Utilise l'Oracle local pour une analyse contextuelle."""

    def __init__(self):
        self.bridge = LlamaCppBridge()
        self.agent = GenerativeAI(self.bridge)

    def sense_context(self, raw_log_data: str) -> str:
        """
        Rituel: Divination Contextuelle.
        Interroge l'Oracle pour obtenir une analyse des logs.
        """
        if not self.bridge.is_healthy():
            return "Oracle local non disponible."

        # // TODO: Gérer les erreurs de manière plus résiliente
        context = self.agent.analyze_log_context(raw_log_data)
        return context