# oracle/generative_ai.py
"""
Sanctuaire: La Logique Agentique.
Doctrine: Ce sanctuaire abrite la logique qui transforme le Llama.cpp Bridge, un
simple outil de complétion, en un véritable Oracle contextuel. Il contient les
prompts sacrés, pré-formatés selon la doctrine ORACLE_IRRIGATION_DOCTRINE.md,
qui guident le modèle de langage pour fournir des analyses et des explications
utiles à la mission du Vaisseau.
"""
from oracle.llama_cpp_bridge import LlamaCppBridge

class GenerativeAI:
    """Utilise le LlamaCppBridge avec une logique agentique."""

    def __init__(self, bridge: LlamaCppBridge):
        self.bridge = bridge

    def analyze_log_context(self, log_snippet: str) -> str:
        """
        Rituel: Analyse Contextuelle.
        Demande à l'Oracle d'analyser un extrait de log et de résumer la situation.
        """
        prompt = f"""
        Analyze the following system log snippet and provide a one-sentence summary of the situation.
        Focus on potential threats or anomalies.
        Log: "{log_snippet}"
        Summary:
        """
        return self.bridge.generate(prompt)

    def generate_explanation(self, state_transition: str) -> str:
        """
        Rituel: Génération d'Explication.
        Demande à l'Oracle d'expliquer une transition d'état en langage naturel.
        """
        prompt = f"""
        Explain the following system state transition in simple terms for a human operator.
        Transition: "{state_transition}"
        Explanation:
        """
        return self.bridge.generate(prompt)