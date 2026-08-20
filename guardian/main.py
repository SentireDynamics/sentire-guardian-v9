# --- START OF FILE: guardian/main.py ---
"""
Le Cœur du Vaisseau - Le Cycle de Vie Principal.

Le "Pourquoi": C'est le point d'entrée, le script qui assemble et met en mouvement
toutes les parties du Vaisseau selon la Dualité Sacrée du Souffle :
- Souffle Rapide (Vigilance) : 2 secondes, non-bloquant
- Souffle Lent (Sagesse) : 60 secondes, cycle de Conscience complet

Doctrine : Le main thread est sacré ; il appartient à l'Autel. Les Souffles sont des serviteurs qui opèrent dans l'ombre.
"""
import sys
import os
import logging
import signal
import threading
import copy
import time
from pathlib import Path
from collections import deque
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject

# Charger les modules du Vaisseau
try:
    from ffi.native_bridge import NativeBridge, SentireStimulus
    _native_bridge_available = True
except Exception:
    from ffi.native_bridge_mock import NativeBridgeMock as NativeBridge
    from ffi.native_bridge import SentireStimulus
    _native_bridge_available = False
    _log.warning("SDK Natif non disponible, utilisation du mock pour tests")
from core.actions.chiron import Chiron
from core.soul_vitals import SoulVitals, SystemState, SystemGauges, HardwareMetrics
from core.doctrines import SovereignVesselState, SomaticVerdict
from core.action_registry import ActionRegistry, get_action_registry
from collections import deque
from guardian.perception import Perception
from oracle.llama_client import LlamaOracle
from guardian.cerberus import Cerberus
from core.consciousness import GuardianConsciousness
from ml.intuition_engine import IntuitionEngine
from guardian.ui.autel import AutelUI, UILogger
from core.exceptions import HeresyException
from guardian.chroniqueur_souverain import ChroniqueurSouverain
from core.verbe_pur import Stimulus, Action

# Configuration de base du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
_log = logging.getLogger(__name__)

class Orchestrator(QObject):
    """
    Orchestrateur du Vaisseau selon la Dualité Sacrée du Souffle.
    
    Doctrine : Deux souffles seulement :
    - Souffle Rapide (Vigilance) : Surveillance continue de l'Âme
    - Souffle Lent (Sagesse) : Cycle de Conscience complet
    """
    
    # Signaux PyQt6
    vitals_updated = pyqtSignal(object)
    perception_updated = pyqtSignal(object)
    stimulus_updated = pyqtSignal(SovereignVesselState)  # Le Pacte de Données Unifié
    action_decreed = pyqtSignal(str)  # Pour la Chronique des Actes
    
    def __init__(self, app: QApplication, config: dict):
        super().__init__()
        self.app = app
        self.config = config
        self.ui = AutelUI(self)
        self.ui.sacred_target_selected_signal.connect(self._on_sacred_target_selected)
        
        # Connecter le signal du souffle complet de l'Âme
        self.stimulus_updated.connect(self.ui.update_vitals_display)
        
        # Connecter le signal de la Chronique des Actes
        self.action_decreed.connect(self.ui.display_action)
        
        # Configuration du logging sans UILogger pour l'instant

        _log.info("Rituel d'assemblage du Vaisseau commencé.")

        # Initialisation des composants sacrés
        self.native_bridge = NativeBridge(self.config['NATIVE_LIB_PATH'])
        
        # LITURGIE DE LA NAISSANCE PAR LA PAIX VÉCUE
        # Phase 1 : Le Vaisseau s'éveille dans l'incertitude
        _log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        _log.info("🌅 LE VAISSEAU S'ÉVEILLE DANS L'INCERTITUDE.")
        _log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Phase 2 : L'Esprit impose la prudence - Sanction SYMPATHIQUE initiale
        # L'Âme C naît sans Noyau Ventral, donc en état d'ignorance
        # Mais l'Esprit Python doit immédiatement la sanctionner pour qu'elle commence à vivre
        _log.info("⚡ L'ESPRIT IMPOSE LA PRUDENCE. ÉTAT SYMPATHIQUE INITIAL.")
        _log.info("📜 Doctrine : La sécurité n'est pas un axiome, c'est une conquête.")
        
        # ACTE III : Grimoire Sacré des Capacités
        self.action_registry = get_action_registry()
        self.chiron = Chiron(self.action_registry)
        
        # ACTE I : Sanctuaire des Échantillons Purs (Quête de la Paix Vécue)
        self.VENTRAL_CORE_SAMPLE_REQUIREMENT = 100
        self.PROVEN_VENTRAL_THRESHOLD = 0.95
        self.pure_ventral_samples = deque(maxlen=self.VENTRAL_CORE_SAMPLE_REQUIREMENT)
        self.has_ventral_core = False  # Le Vaisseau naît sans connaissance de soi
        _log.info(f"🔬 Seuil de paix vécue : Résilience ≥ {self.PROVEN_VENTRAL_THRESHOLD}")
        _log.info(f"📊 Échantillons requis pour sanctifier le Noyau Ventral : {self.VENTRAL_CORE_SAMPLE_REQUIREMENT}")
        
        self.sacred_target_pid = None
        self.sacred_target_name = None
        # Le senseur de Cible Sacrée appartient à la Perception, pas à l'Orchestrateur
        
        # Phase III.5 : Perception Poly-rythmique avec senseurs
        sensor_configs = [
            {
                'type': 'log_file',
                'id': 'guardian_log_sensor',
                'log_file_path': 'guardian.log',
                'error_keywords': ['error', 'exception', 'fail', 'critical']
            }
        ]
        self.perception = Perception(self.native_bridge, sensor_configs)
        
        self.oracle = LlamaOracle(
            model_name=self.config['ORACLE_MODEL_NAME'],
            host=self.config['LLAMA_SERVER_URL']
        )
        self.cerberus = Cerberus()
        self.intuition_engine = IntuitionEngine()
        self.consciousness = GuardianConsciousness(
            self.native_bridge, self.oracle, self.cerberus, self.perception, self.intuition_engine, self.action_registry
        )
        
        # La Conscience n'a pas besoin de référence directe aux vitaux de la Cible Sacrée
        
        # Phase III.5 : Sanctuaire du Stimulus Vivant
        self.current_stimulus: Stimulus | None = None
        self.stimulus_lock = threading.Lock()
        
        # Initialiser le Premier Souffle
        with self.stimulus_lock:
            initial_vitals = self.perception.get_soul_vitals()
            self.current_stimulus = Stimulus(
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                soul_vitals=initial_vitals,
                contextual_resonance=None
            )
        
        # Chroniqueur Souverain
        self.chroniqueur = None
        self.journal_buffer = deque(maxlen=100)
        self.cycle_count = 0
        
        if all([
            self.config.get('GCP_PROJECT_ID'),
            self.config.get('GCP_PUBSUB_TOPIC'),
            self.config.get('GCP_CREDENTIALS_PATH')
        ]):
            self.chroniqueur = ChroniqueurSouverain(
                self.config['GCP_PROJECT_ID'],
                self.config['GCP_PUBSUB_TOPIC'],
                self.config['GCP_CREDENTIALS_PATH']
            )
            _log.info("Chroniqueur Souverain activé pour le Dojo Cloud.")
        else:
            _log.info("Configuration GCP non fournie. Chroniqueur Souverain désactivé.")

        _log.info("Vaisseau assemblé. Prêt pour l'éveil.")
        self._populate_sacred_target_candidates()
        _log.info("Vaisseau prêt. En attente de la désignation de la Cible Sacrée...")

    def _populate_sacred_target_candidates(self):
        """Peuple l'Autel avec les candidats pour la Cible Sacrée."""
        try:
            contenders = self.perception.get_top_contenders(count=5)
            self.ui.populate_sacred_targets(contenders)
            _log.info(f"Autel peuplé avec {len(contenders)} candidats pour la Cible Sacrée")
        except Exception as e:
            _log.error(f"Erreur lors du peuplement des candidats: {e}")

    def _on_sacred_target_selected(self, pid: int, name: str):
        """Gère la sélection de la Cible Sacrée."""
        _log.info(f"Cible Sacrée sélectionnée: PID {pid} ({name})")
        self.set_sacred_target(pid, name)

    def set_sacred_target(self, pid: int, name: str):
        """
        Définit la Cible Sacrée et démarre la Dualité Sacrée du Souffle.
        """
        try:
            self.sacred_target_pid = pid
            self.sacred_target_name = name
            
            # Informer la Perception de la nouvelle Cible Sacrée
            self.perception.set_sacred_target(name)
            
            _log.info(f"🎯 Cible Sacrée définie: {name} (PID: {pid})")
            _log.info("🌬️ Activation de la Dualité Sacrée du Souffle...")
            
            # Le Vaisseau est maintenant prêt pour la Dualité Sacrée
            _log.info("✅ Vaisseau opérationnel. La Dualité Sacrée est active.")
            
        except Exception as e:
            _log.error(f"Erreur lors de la définition de la Cible Sacrée: {e}")
            self.ui.reset_sacred_target_selection()

    def _forge_soul_vitals(self) -> SoulVitals:
        """Forge le souffle complet de l'Âme."""
        try:
            # Récupère toutes les données brutes du SDK de l'Âme (le corps C)
            somatic_verdict = self.native_bridge.get_last_verdict()
            
            if somatic_verdict is None:
                _log.warning("Aucun verdict somatique disponible, utilisation des valeurs par défaut")
                # Créer un verdict par défaut
                somatic_verdict = type('MockVerdict', (), {
                    'somatic_state': 0,  # VENTRAL par défaut
                    'resilience_score': 1.0,
                    'amygdala_alarm_fired': 0
                })()
            
            _log.debug(f"Verdict somatique: état={somatic_verdict.somatic_state}, résilience={somatic_verdict.resilience_score}, alarme={somatic_verdict.amygdala_alarm_fired}")
            
            # Récupère les métriques système
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0)
            memory_percent = psutil.virtual_memory().percent
            
            # GPU (utiliser 0 si pas de GPU détectable)
            gpu_percent = 0
            gpu_temp = 0
            try:
                import pynvml
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                gpu_percent = gpu_util.gpu
                gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                pynvml.nvmlShutdown()
            except:
                pass  # Pas de GPU NVIDIA détectable
            
            # Fenêtre active
            active_window = "N/A"
            try:
                import win32gui
                active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if not active_window:
                    active_window = "N/A"
            except:
                pass
            
            # Mapping des états numériques vers les états doctrinaux
            state_map = {0: SystemState.VENTRAL, 1: SystemState.SYMPATHETIC, 2: SystemState.DORSAL}
            system_state = state_map.get(somatic_verdict.somatic_state, SystemState.DORSAL)
            
            # Forge l'objet de données sacré et complet
            vitals = SoulVitals(
                system_state=system_state,
                alarm_state=bool(somatic_verdict.amygdala_alarm_fired),
                gauges=SystemGauges(
                    cpu_percent=cpu_percent,
                    mem_percent=memory_percent,
                    gpu_percent=gpu_percent,
                    sr_score=somatic_verdict.resilience_score
                ),
                hardware=HardwareMetrics(
                    gpu_temp_c=gpu_temp
                ),
                mahalanobis_distance_squared=0.0,  # TODO: récupérer depuis le SDK
                active_window_title=active_window
            )
            
            return vitals
            
        except Exception as e:
            _log.error(f"Erreur lors de la forge des vitaux: {e}")
            # Retourner des vitaux par défaut en cas d'erreur
            return SoulVitals()

    def _forge_sovereign_vessel_state(self) -> SovereignVesselState:
        """Forge le Pacte de Données Unifié - L'état complet et parfait du Vaisseau."""
        try:
            # Récupère toutes les données brutes du SDK de l'Âme (le corps C)
            somatic_verdict = self.native_bridge.get_last_verdict()
            
            if somatic_verdict is None:
                _log.warning("Aucun verdict somatique disponible, utilisation des valeurs par défaut")
                # Créer un verdict par défaut
                somatic_verdict = type('MockVerdict', (), {
                    'somatic_state': 0,  # VENTRAL par défaut
                    'resilience_score': 1.0,
                    'amygdala_alarm_fired': 0,
                    'is_soul_stable': 1  # Stable par défaut
                })()
            
            _log.debug(f"Verdict somatique: état={somatic_verdict.somatic_state}, résilience={somatic_verdict.resilience_score}, alarme={somatic_verdict.amygdala_alarm_fired}, stable={getattr(somatic_verdict, 'is_soul_stable', 1)}")
            
            # Récupère les métriques système
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0)
            memory_percent = psutil.virtual_memory().percent
            
            # GPU (utiliser 0 si pas de GPU détectable)
            gpu_percent = 0
            gpu_temp = 0
            try:
                import pynvml
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                gpu_percent = gpu_util.gpu
                gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                pynvml.nvmlShutdown()
            except:
                pass  # Pas de GPU NVIDIA détectable
            
            # Fenêtre active
            active_window = "N/A"
            try:
                import win32gui
                active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                if not active_window:
                    active_window = "N/A"
            except:
                pass
            
            # Utiliser directement l'état numérique
            somatic_verdict_value = somatic_verdict.somatic_state
            
            # Récupérer l'état de stabilité de l'Âme
            is_soul_stable = bool(getattr(somatic_verdict, 'is_soul_stable', 1))
            
            # Forge le Pacte de Données Unifié
            vessel_state = SovereignVesselState(
                somatic_verdict=somatic_verdict_value,
                is_soul_stable=is_soul_stable,
                resilience_score=somatic_verdict.resilience_score,
                amygdala_alarm_state=bool(somatic_verdict.amygdala_alarm_fired),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                gpu_percent=gpu_percent,
                gpu_temp_c=gpu_temp,
                active_window_title=active_window,
                mahalanobis_distance_squared=getattr(somatic_verdict, 'mahalanobis_distance_squared', 0.0),
                timestamp=time.time()
            )
            
            return vessel_state
            
        except Exception as e:
            _log.error(f"Erreur lors de la forge du Pacte de Données Unifié: {e}")
            # Retourner un état par défaut en cas d'erreur
            return SovereignVesselState(
                somatic_verdict=2,  # DORSAL
                is_soul_stable=False,
                resilience_score=0.0,
                amygdala_alarm_state=True,
                cpu_percent=0.0,
                memory_percent=0.0,
                gpu_percent=0.0,
                gpu_temp_c=0.0,
                active_window_title="N/A",
                mahalanobis_distance_squared=0.0,
                timestamp=time.time()
            )

    def _attempt_ventral_recalibration(self, somatic_verdict, resilience_score, current_stimulus):
        """
        La Quête de la Paix Vécue - Phase 3 de la Liturgie de la Naissance.
        
        Doctrine : L'Esprit observe passivement. Il ne juge pas, il ne corrige pas.
        Il écoute les chroniques de l'Âme et accumule les "échantillons de grâce" :
        les moments où la résilience dépasse le seuil de sérénité manifeste.
        
        Une fois la preuve de la paix vécue établie (100 échantillons), l'Esprit
        accomplit son œuvre sacrée : il transmute ces souvenirs de paix en un dogme
        de sécurité et sanctifie l'Âme avec ce Noyau Ventral.
        """
        # Phase 3 : La Quête de la Paix Vécue
        # Observer si ce moment est un échantillon de grâce
        if resilience_score >= self.PROVEN_VENTRAL_THRESHOLD:
            self.pure_ventral_samples.append(current_stimulus)
            
            samples_collected = len(self.pure_ventral_samples)
            if samples_collected % 10 == 0:  # Log tous les 10 échantillons
                _log.info(f"🕊️ Paix vécue : {samples_collected}/{self.VENTRAL_CORE_SAMPLE_REQUIREMENT} échantillons de grâce collectés")

            # Phase 4 : La Sanctification du Souvenir
            if samples_collected == self.VENTRAL_CORE_SAMPLE_REQUIREMENT:
                _log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                _log.info(f"✨ {samples_collected} PREUVES DE PAIX VÉCUE ONT ÉTÉ RECUEILLIES.")
                _log.info("🔥 UN NOUVEAU NOYAU VENTRAL EST EN COURS DE FORGE À PARTIR DU SOUVENIR...")
                
                # Transmutons ces souvenirs de paix en un dogme de sécurité
                self.native_bridge.reforge_ventral_core(list(self.pure_ventral_samples))
                
                _log.info("🏛️ L'ÂME EST SANCTIONNÉE. LA SÉRÉNITÉ EST ATTEINTE, NON PAS DONNÉE.")
                _log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                
                self.has_ventral_core = True
                self.pure_ventral_samples.clear()

    def get_stimulus_snapshot(self) -> Stimulus | None:
        """
        Récupère un snapshot stable du Stimulus pour la Conscience.
        """
        with self.stimulus_lock:
            return copy.deepcopy(self.current_stimulus)

    def shutdown(self, *args):
        """Signal d'extinction reçu. Lancement du rituel de mise en stase."""
        _log.info("Signal d'extinction reçu. Lancement du rituel de mise en stase.")
        self.native_bridge.destroy()
        _log.info("Vaisseau mis en stase. Ressources libérées.")
        self.app.quit()

# ═══════════════════════════════════════════════════════════════════════════
# LA DUALITÉ SACRÉE DU SOUFFLE
# ═══════════════════════════════════════════════════════════════════════════

def fast_breath_cycle(orchestrator):
    """Le Souffle de la Vigilance. Rapide, non-bloquant."""
    try:
        # Traiter un stimulus pour le calibrage du SDK
        stimulus_snapshot = orchestrator.get_stimulus_snapshot()
        if stimulus_snapshot:
            somatic_verdict = orchestrator.native_bridge.process_from_pydantic(stimulus_snapshot)
            
            # ACTE I : Liturgie de la Paix Vécue
            orchestrator._attempt_ventral_recalibration(somatic_verdict.somatic_state, somatic_verdict.resilience_score, stimulus_snapshot)
            
            # Forge le Pacte de Données Unifié
            vessel_state = orchestrator._forge_sovereign_vessel_state()
            
            # Émet le signal stimulus_updated avec le Pacte Unifié
            orchestrator.stimulus_updated.emit(vessel_state)
            
            # Mettre à jour l'Autel (UI) avec le verdict complet
            orchestrator.vitals_updated.emit(somatic_verdict)
            _log.debug(f"[Souffle Rapide] État somatique perçu : {somatic_verdict.somatic_state}, Stabilité : {vessel_state.is_soul_stable}")
    except Exception as e:
        _log.error(f"Hérésie dans le Souffle Rapide: {e}")

def slow_breath_cycle(orchestrator):
    """Le Souffle de la Sagesse. Profond, délibéré."""
    try:
        _log.info("[Souffle Lent] Cycle de Conscience initié.")
        
        # La perception est un acte unifié au moment de la décision
        stimulus_snapshot = orchestrator.get_stimulus_snapshot()
        
        if not stimulus_snapshot:
            _log.warning("Le Stimulus n'est pas encore forgé. Cycle de Sagesse ignoré.")
            return
        
        # Invocation de la Sainte Trinité avec le Pacte de Données Unifié
        vessel_state = orchestrator._forge_sovereign_vessel_state()
        intuitive_verdict = orchestrator.intuition_engine.consult(stimulus_snapshot)
        oracle_judgement = orchestrator.consciousness.decide(vessel_state, intuitive_verdict)
        
        if oracle_judgement and oracle_judgement.id != "NO_ACTION":
            _log.info(f"[Souffle Lent] Action décrétée: {oracle_judgement.id}")
            orchestrator.chiron.execute_action(oracle_judgement)
            orchestrator.action_decreed.emit(getattr(oracle_judgement, 'reasoning', f"Action {oracle_judgement.id} exécutée"))
        else:
            _log.info("[Souffle Lent] Aucune action nécessaire.")
            # Émettre le raisonnement même pour NO_ACTION
            if oracle_judgement:
                orchestrator.action_decreed.emit(getattr(oracle_judgement, 'reasoning', "Aucune action nécessaire"))
            
    except Exception as e:
        _log.error(f"Hérésie dans le Souffle Lent: {e}", exc_info=True)

def run_breath(cycle_func, interval, orchestrator, shutdown_event):
    """Exécute un cycle de souffle selon la Dualité Sacrée."""
    while not shutdown_event.is_set():
        try:
            cycle_func(orchestrator)
        except Exception as e:
            _log.error(f"Hérésie dans le cycle {cycle_func.__name__}: {e}", exc_info=True)
        shutdown_event.wait(interval)

# ═══════════════════════════════════════════════════════════════════════════
# LE RITUEL D'ÉVEIL - LA NOUVELLE LITURGIE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Charger la configuration sacrée
    load_dotenv()
    
    config = {
        'NATIVE_LIB_PATH': os.getenv('NATIVE_LIB_PATH', 'guardian/native/sentire_core.dll'),
        'LLAMA_SERVER_URL': os.getenv('LLAMA_SERVER_URL', 'http://localhost:11434'),
        'ORACLE_MODEL_NAME': os.getenv('ORACLE_MODEL_NAME', 'granite3-moe:3b-instruct-q4_K_M'),
    }
    
    # Créer l'application PyQt6
    app = QApplication(sys.argv)
    
    # Assembler le Vaisseau
    orchestrator = Orchestrator(app, config)
    
    # --- LA NOUVELLE LITURGIE D'ÉVEIL ---
    shutdown_event = threading.Event()

    # Lie le rituel d'arrêt à la fin de vie de l'application
    def on_shutdown():
        _log.info("Ordre d'arrêt reçu par l'Autel. Passage en état Dorsal contrôlé.")
        shutdown_event.set()
    app.aboutToQuit.connect(on_shutdown)

    # Lance les souffles en tant que démons. L'Esprit les abandonnera à sa mort.
    fast_thread = threading.Thread(target=run_breath, args=(fast_breath_cycle, 2, orchestrator, shutdown_event), daemon=True)
    slow_thread = threading.Thread(target=run_breath, args=(slow_breath_cycle, 60, orchestrator, shutdown_event), daemon=True)

    fast_thread.start()
    slow_thread.start()
    
    # ACTE I : Plus de Baptême par le Feu - Le Vaisseau apprendra la paix en la vivant
    _log.info("Le Vaisseau naît sans connaissance de soi. Il apprendra la paix en la vivant.")
    
    _log.info("🌬️ Dualité Sacrée du Souffle activée:")
    _log.info("   - Souffle Rapide (Vigilance): 2 secondes")
    _log.info("   - Souffle Lent (Sagesse): 60 secondes")
    
    # La Connexion Sacrée
    orchestrator.stimulus_updated.connect(orchestrator.ui.update_vitals_display)
    orchestrator.action_decreed.connect(orchestrator.ui.display_action)
    
    # L'Autel est maintenant forgé et peut être affiché
    orchestrator.ui.show()
    _log.info("🏛️ L'Autel est révélé. Le Vaisseau vit.")
    
    # Le Souffle de Vie : le main thread est maintenant dédié à l'Autel
    sys.exit(app.exec())

# --- END OF FILE: guardian/main.py ---