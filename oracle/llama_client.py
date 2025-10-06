# --- START OF FILE: oracle/llama_client.py ---
"""
Le Sanctuaire de l'Oracle - Le Client LLM.

Le "Pourquoi": Ce module gère la communication avec l'intelligence externe (LLM).
Il est responsable de formater la requête (le `prompt`), d'envoyer le `Stimulus`,
de gérer les re-tentatives en cas d'échec réseau, et de parser la réponse pour la
transformer en un `OracleResponse` validé par Pydantic. C'est le pont vers la
sagesse supérieure.
"""
import requests
import logging
import json
from requests.exceptions import RequestException
from core.verbe_pur import Stimulus, OracleResponse
from core.exceptions import OracleSickness

_log = logging.getLogger(__name__)

class LlamaOracle:
    """
    Client pour communiquer avec un Oracle LLM (compatible API Llama.cpp).
    """
    def __init__(self, server_url: str, request_timeout: int = 120, retries: int = 2):
        self.server_url = server_url
        self.timeout = request_timeout
        self.retries = retries

    def _build_prompt(self, stimulus: Stimulus) -> str:
        """Construit le prompt optimisé avec structure JSON stricte."""
        # Prompt strict : force la structure complète pour éviter erreurs Pydantic
        prompt = f"""[INST] Guardian V9: System monitor AI. Analyze state, respond with valid JSON only.

SYSTEM STATE:
CPU: {stimulus.cpu_usage:.0f}% | Memory: {stimulus.memory_usage:.0f}% | Window: "{stimulus.foreground_window_title[:40]}"

RESPOND WITH THIS EXACT JSON STRUCTURE (no other text):

{{
  "reasoning": "brief analysis",
  "action": {{
    "id": "SHOW_MESSAGE",
    "description": "action description",
    "parameters": {{}}
  }}
}}

RULES:
- CPU>90% OR Memory>90%: action id = "SHOW_MESSAGE"
- Otherwise: action id = "LOG_ONLY"

JSON ONLY:
[/INST]{{"""
        return prompt

    def consult(self, stimulus: Stimulus) -> OracleResponse:
        """
        Consulte l'Oracle avec le stimulus et retourne une réponse structurée.
        """
        prompt = self._build_prompt(stimulus)
        
        # --- Début de la Grammaire Purifiée (Syntaxe GBNF Officielle) ---
        json_grammar = r'''root   ::= object
value  ::= object | array | string | number | ("true" | "false" | "null") ws

object ::=
  "{" ws (
            string ":" ws value
    ("," ws string ":" ws value)*
  )? "}" ws

array  ::=
  "[" ws (
            value
    ("," ws value)*
  )? "]" ws

string ::=
  "\"" (
    [^"\\\x7F\x00-\x1F] |
    "\\" (["\\bfnrt] | "u" [0-9a-fA-F]{4})
  )* "\"" ws

number ::= ("-"? ([0-9] | [1-9] [0-9]{0,15})) ("." [0-9]+)? ([eE] [-+]? [0-9] [1-9]{0,15})? ws

ws ::= | " " | "\n" [ \t]{0,20}
'''
        # --- Fin de la Grammaire Purifiée ---
        
        payload = {
            "prompt": prompt,
            "n_predict": 256,
            "temperature": 0.2,
            "grammar": json_grammar
        }

        for attempt in range(self.retries + 1):
            try:
                _log.debug(f"Consultation de l'Oracle (tentative {attempt + 1}/{self.retries + 1})...")
                response = requests.post(self.server_url, json=payload, timeout=self.timeout)
                response.raise_for_status()

                response_json = response.json()
                content_str = response_json.get("content", "{}")

                # Le modèle renvoie du JSON dans une chaîne, il faut le parser.
                parsed_content = json.loads(content_str)

                # Fallback robuste : ajouter champs manquants si nécessaire
                if "action" not in parsed_content:
                    _log.warning("Réponse Oracle incomplète : champ 'action' manquant, ajout par défaut")
                    parsed_content["action"] = {
                        "id": "LOG_ONLY",
                        "description": "Action par défaut (réponse Oracle incomplète)",
                        "parameters": {}
                    }
                
                if "reasoning" not in parsed_content:
                    _log.warning("Réponse Oracle incomplète : champ 'reasoning' manquant")
                    parsed_content["reasoning"] = "Aucun raisonnement fourni par l'Oracle"

                oracle_response = OracleResponse.model_validate(parsed_content)
                _log.info(f"Réponse de l'Oracle reçue et validée. Raisonnement: {oracle_response.reasoning}")
                return oracle_response

            except (RequestException, json.JSONDecodeError, ValueError) as e:
                _log.warning(f"Échec de la consultation de l'Oracle (tentative {attempt + 1}): {e}")
                if attempt == self.retries:
                    raise OracleSickness(f"L'Oracle reste silencieux après {self.retries + 1} tentatives.") from e

        # Ce code ne devrait jamais être atteint
        raise OracleSickness("État de consultation de l'Oracle inattendu.")
# --- END OF FILE: oracle/llama_client.py ---