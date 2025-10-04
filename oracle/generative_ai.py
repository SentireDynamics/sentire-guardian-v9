"""
Generative AI - Logique Agentique et Dialogue

Épigraphe Doctrinale:
Le moteur d'IA générative orchestre les interactions avec le LLM local.
Prompts doctrinaux, dialogue contextuel, raisonnement agentique, et fallback
en cas d'indisponibilité du LLM.

Rôle dans la Résilience Souveraine:
- Orchestration des prompts doctrinaux
- Dialogue contextuel avec le LLM
- Raisonnement agentique (chain-of-thought)
- Analyse sémantique des logs et événements
- Fallback vers heuristiques si LLM indisponible
- Génération de contexte pour les décisions
"""

from typing import Optional, Dict, List


class GenerativeAI:
    """
    Moteur d'IA générative du Vaisseau.
    """
    
    def __init__(self, llama_bridge=None):
        """
        Initialise le moteur d'IA générative.
        
        Args:
            llama_bridge: Instance de LlamaCppBridge
        """
        self.llama_bridge = llama_bridge
        self.conversation_history = []
    
    def analyze_context(self, data: Dict) -> Dict:
        """
        Analyse le contexte via le LLM.
        
        Args:
            data: Données à analyser
        
        Returns:
            Analyse contextuelle
        """
        if self.llama_bridge:
            prompt = self._build_analysis_prompt(data)
            response = self.llama_bridge.generate(prompt)
            return self._parse_analysis(response)
        else:
            # Fallback heuristique
            return self._heuristic_analysis(data)
    
    def _build_analysis_prompt(self, data: Dict) -> str:
        """Construit un prompt d'analyse doctrinal."""
        return f"Analyze the following system data: {data}"
    
    def _parse_analysis(self, response: str) -> Dict:
        """Parse la réponse du LLM."""
        return {"analysis": response}
    
    def _heuristic_analysis(self, data: Dict) -> Dict:
        """Analyse heuristique de fallback."""
        return {"analysis": "heuristic_fallback", "confidence": 0.5}
    
    def generate_explanation(self, state: str, score: float) -> str:
        """
        Génère une explication de l'état actuel.
        
        Args:
            state: État polyvagal
            score: Score de résilience
        
        Returns:
            Explication textuelle
        """
        if self.llama_bridge:
            prompt = f"Explain why the system is in {state} state with resilience score {score}"
            return self.llama_bridge.generate(prompt, max_tokens=256)
        return f"État {state}, score {score:.2f}"
