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
    def __init__(self, server_url: str, request_timeout: int = 60, retries: int = 2):
        self.server_url = server_url
        self.timeout = request_timeout
        self.retries = retries

    def _build_prompt(self, stimulus: Stimulus) -> str:
        """Construit le prompt pour le LLM basé sur le stimulus."""
        prompt = f"""[INST]
You are Guardian V9, a sovereign AI assistant for Windows. Your role is to analyze system state and recommend a single, precise action.
Your response MUST be a single JSON object matching this Pydantic schema:
{{
  "reasoning": "A brief explanation of why you chose this action.",
  "action": {{
    "id": "A unique action ID from the list: [SHOW_MESSAGE, LOG_ONLY]",
    "description": "A natural language description of the action.",
    "parameters": {{ "key": "value" }}
  }}
}}

Current system stimulus:
- CPU Usage: {stimulus.cpu_usage:.1f}%
- Memory Usage: {stimulus.memory_usage:.1f}%
- Active Window: "{stimulus.foreground_window_title}"

Analyze the stimulus and provide the single best JSON action.
If CPU or Memory is over 90%, it's a crisis. Recommend SHOW_MESSAGE to alert the user.
Otherwise, recommend LOG_ONLY.
[/INST]
"""
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

                oracle_response = OracleResponse.parse_obj(parsed_content)
                _log.info(f"Réponse de l'Oracle reçue et validée. Raisonnement: {oracle_response.reasoning}")
                return oracle_response

            except (RequestException, json.JSONDecodeError, ValueError) as e:
                _log.warning(f"Échec de la consultation de l'Oracle (tentative {attempt + 1}): {e}")
                if attempt == self.retries:
                    raise OracleSickness(f"L'Oracle reste silencieux après {self.retries + 1} tentatives.") from e

        # Ce code ne devrait jamais être atteint
        raise OracleSickness("État de consultation de l'Oracle inattendu.")
# --- END OF FILE: oracle/llama_client.py ---