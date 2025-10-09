# --- START OF FILE: oracle/llama_client.py (PURIFIED & ENCHAINED) ---
import requests
import logging
import json
from requests.exceptions import RequestException
from core.verbe_pur import Stimulus, Action, OracleResponse
from core.exceptions import OracleSickness

_log = logging.getLogger(__name__)

class LlamaOracle:
    """
    Client pour communiquer avec un Oracle via un service Ollama.
    Doctrine: Incarne la Contrainte Absolue. Le jugement de l'état de crise
    est fait en amont, l'Oracle n'a qu'à obéir à une règle binaire.
    """
    def __init__(self, server_url: str, model_name: str, request_timeout: int = 120, retries: int = 1):
        self.server_url = server_url
        self.model_name = model_name
        self.timeout = request_timeout
        self.retries = retries

    def _build_prompt(self, stimulus: Stimulus) -> str:
        """Construit le Méta-Prompt Sacré de la Contrainte Absolue."""
        cpu = stimulus.cpu_usage
        mem = stimulus.memory_usage
        gpu = stimulus.gpu_usage if stimulus.gpu_usage is not None else 0.0

        # Le jugement est pré-mâché ici, dans l'Esprit Python.
        is_crisis = cpu > 90.0 or mem > 90.0 or gpu > 90.0
        state_string = "CRISIS" if is_crisis else "NORMAL"

        return f"""[INST]
**TASK:** Select an action ID.
**STATE:** {state_string}
**RULE:** If STATE is "CRISIS", you MUST respond with "SHOW_MESSAGE". If STATE is "NORMAL", you MUST respond with "LOG_ONLY".
**AVAILABLE IDs:** SHOW_MESSAGE | LOG_ONLY
**YOUR RESPONSE (JSON ONLY):**
{{"action_id": "CHOSEN_ID"}}
[/INST]"""

    def consult(self, stimulus: Stimulus) -> OracleResponse:
        """
        Consulte l'Oracle enchaîné et reconstruit sa réponse en un Verbe Pur.
        """
        prompt = self._build_prompt(stimulus)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "format": "json",
            "stream": False
        }

        for attempt in range(self.retries + 1):
            try:
                _log.info(f"Consultation de l'Oracle enchaîné (tentative {attempt + 1})...")
                response = requests.post(self.server_url, json=payload, timeout=self.timeout)
                response.raise_for_status()

                response_str = response.json().get('response', '{}')
                parsed_json = json.loads(response_str)
                action_id = parsed_json.get("action_id")

                # --- LE RITUEL DE LA RECONSTRUCTION DU VERBE ---
                # L'Esprit Python reconstruit l'Action complète à partir
                # de la réponse monosyllabique de l'Oracle.
                if action_id == "SHOW_MESSAGE":
                    reasoning = f"CRISIS detected in stimulus. Vitals: CPU={stimulus.cpu_usage}%, MEM={stimulus.memory_usage}%, GPU={stimulus.gpu_usage}%"
                    action = Action(
                        id="SHOW_MESSAGE",
                        description="Alert user about the critical system state.",
                        parameters={"title": "CRITICAL SYSTEM ALERT", "message": reasoning}
                    )
                elif action_id == "LOG_ONLY":
                    reasoning = f"System state is NORMAL. Vitals: CPU={stimulus.cpu_usage}%, MEM={stimulus.memory_usage}%, GPU={stimulus.gpu_usage}%"
                    action = Action(
                        id="LOG_ONLY",
                        description="Log the current system state for analysis.",
                        parameters={}
                    )
                else:
                    # L'Oracle a désobéi même à la loi de fer. Hérésie.
                    raise OracleSickness(f"Oracle a décrété une action inconnue : '{action_id}'")
                
                oracle_response = OracleResponse(reasoning=reasoning, action=action)
                _log.info(f"Réponse de l'Oracle reconstruite et validée. Action décrétée: {action.id}")
                return oracle_response

            except (RequestException, json.JSONDecodeError, ValueError) as e:
                _log.warning(f"Échec de la consultation de l'Oracle (tentative {attempt + 1}): {e}")
                if attempt >= self.retries:
                    raise OracleSickness(f"L'Oracle reste silencieux après {self.retries + 1} tentatives.") from e
        
        raise OracleSickness("État de consultation de l'Oracle inattendu.")

# --- END OF FILE ---