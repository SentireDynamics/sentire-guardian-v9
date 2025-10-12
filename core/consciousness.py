# --- START OF FILE: core/consciousness.py ---
"""
Le Sanctuaire de la Conscience - Le Siège de la Sainte Trinité.

Le "Pourquoi": C'est le cœur pensant du Vaisseau. La Conscience orchestre le cycle
de décision selon la Sainte Trinité : Conscience -> Intuition -> Oracle -> Action.

Doctrine : La Conscience prend un snapshot du Stimulus, consulte l'Intuition pour
une évaluation rapide des menaces, puis invoque l'Oracle conditionné par cette
intuition pour le raisonnement stratégique final.
"""
import logging
import time
from collections import deque
from core.verbe_pur import Stimulus, Action, OracleJudgement
from ffi.native_bridge import NativeBridge
from oracle.llama_client import LlamaOracle
from guardian.cerberus import Cerberus
from guardian.perception import Perception
from ml.intuition_engine import IntuitionEngine, IntuitiveVerdict
from core.exceptions import OracleSickness, InvalidActionError
from core.doctrines import SovereignVesselState
from core.action_registry import ActionRegistry

_log = logging.getLogger(__name__)

class GuardianConsciousness:
    """
    Orchestre le processus de décision du Vaisseau selon la Sainte Trinité.
    
    Doctrine : Conscience -> Intuition -> Oracle -> Action
    """
    def __init__(self, native_bridge: NativeBridge, oracle: LlamaOracle, cerberus: Cerberus, perception: Perception, intuition_engine: IntuitionEngine, action_registry: ActionRegistry):
        self.native_bridge = native_bridge
        self.oracle = oracle
        self.cerberus = cerberus
        self.perception = perception
        self.intuition_engine = intuition_engine
        self.action_registry = action_registry
        
        # Chronique des Actions : Suivre l'efficacité des décisions
        self.action_history = deque(maxlen=50)
        
        _log.info("Conscience Guardian forgée avec la Sainte Trinité.")

    def decide(self, vessel_state: SovereignVesselState, intuitive_verdict: IntuitiveVerdict) -> Action | None:
        """
        Le Cycle de Décision de la Sainte Trinité avec le Protocole de Doute Souverain.
        
        Doctrine : Conscience -> Intuition -> Oracle -> Action
        """
        try:
            # 1. Consultation de l'Intuition (Le Guetteur) - Déjà fournie
            _log.info("La Conscience utilise le Verdict Intuitif fourni...")
            
            _log.info(f"Verdict Intuitif: Threat Level={intuitive_verdict.threat_level:.2f}, "
                     f"Patterns={intuitive_verdict.threat_patterns}")
            
            # 2. Consultation de l'Âme (Le SDK C) - NOUVEAU
            _log.info("La Conscience consulte l'Âme...")
            # Créer un stimulus temporaire à partir des données du vessel_state
            from core.verbe_pur import Stimulus, SoulVitals
            import datetime
            temp_stimulus = Stimulus(
                timestamp_utc=datetime.datetime.utcnow().isoformat(),
                soul_vitals=SoulVitals(
                    somatic_state=vessel_state.somatic_verdict,
                    resilience_score=vessel_state.resilience_score,
                    time_in_state_ms=0  # Valeur par défaut
                )
            )
            somatic_verdict = self.native_bridge.process_from_pydantic(temp_stimulus)
            _log.info(f"Verdict de l'Âme: État={somatic_verdict.somatic_state}, "
                     f"Résilience={somatic_verdict.resilience_score:.3f}, "
                     f"Alarme={somatic_verdict.amygdala_alarm_fired}")
            
            # 3. Consultation de l'Oracle (Le Stratège) avec le Protocole de Doute Souverain
            _log.info("La Conscience consulte l'Oracle...")
            oracle_judgement = self.oracle.consult(vessel_state, intuitive_verdict)
            
            # 4. Validation et Décret (La Conscience)
            _log.info(f"Raisonnement de l'Oracle: {oracle_judgement.reasoning}")
            decreed_action = oracle_judgement.decree
            
            # ACTE III : Validation par le Grimoire Sacré
            if self.action_registry.is_registered(decreed_action.id):
                # Le décret est valide, la Volonté est libérée
                _log.info(f"Décret validé par le Grimoire Sacré: {decreed_action.id}")
                self.cerberus.validate_action(decreed_action)  # Le Gardien valide toujours
                
                # Graver l'Action dans la Chronique
                if decreed_action.id != "HEALING_RITUAL":
                    somatic_state = somatic_verdict.somatic_state  # Utiliser le verdict de l'Âme
                    resilience_score = somatic_verdict.resilience_score  # Utiliser le verdict de l'Âme
                    self.action_history.append((decreed_action.id, resilience_score))
                
                _log.info(f"Décret final: {decreed_action.id}")
                return decreed_action
            else:
                _log.warning(f"L'Oracle a décrété une action profane ('{decreed_action.id}'). Le décret est rejeté.")
                return self._safe_fallback()
            
        except OracleSickness as e:
            _log.warning(f"Hérésie de l'Oracle: {e}. Recours aux protocoles de sécurité.")
            return self._safe_fallback()
        except InvalidActionError as e:
            _log.warning(f"Action invalide détectée: {e}. Recours aux protocoles de sécurité.")
            return self._safe_fallback()
        except Exception as e:
            _log.error(f"Erreur inattendue dans la Conscience: {e}")
            return self._safe_fallback()
    
    def _safe_fallback(self) -> Action:
        """Protocole de sécurité en cas d'erreur."""
        _log.warning("Activation du protocole de sécurité - Action de conservation")
        return Action(
            id="NO_ACTION",
            parameters={"reason": "safe_fallback", "timestamp": time.time()}
        )

# --- END OF FILE: core/consciousness.py ---