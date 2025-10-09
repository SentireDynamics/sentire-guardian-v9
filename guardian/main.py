# --- START OF FILE: guardian/main.py ---
"""
Le Cœur du Vaisseau - Le Cycle de Vie Principal.

Le "Pourquoi": C'est le point d'entrée, le script qui assemble et met en mouvement
toutes les parties du Vaisseau. Il est responsable de :
1. Charger la configuration sacrée depuis le fichier .env.
2. Mettre en place la journalisation (logging).
3. Instancier tous les composants majeurs (NativeBridge, Oracle, Chiron, etc.).
4. Créer l'interface utilisateur (Autel).
5. Lancer la boucle de vie principale (le "Grand Œuvre") via un QTimer pour ne
   pas bloquer l'interface.
6. Gérer une extinction propre et ordonnée (en libérant les ressources natives)
   lorsque l'opérateur ferme la fenêtre ou envoie un signal d'interruption.
"""
import sys
import os
import logging
import signal
from pathlib import Path
from collections import deque

from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, pyqtSignal, QObject

# Charger les modules du Vaisseau
from ffi.native_bridge import NativeBridge, SentireStimulus
from core.actions.chiron import Chiron
from guardian.perception import Perception
from oracle.llama_client import LlamaOracle
from guardian.cerberus import Cerberus
from core.consciousness import GuardianConsciousness
from guardian.ui.autel import AutelUI, UILogger
from core.exceptions import HeresyException
from guardian.chroniqueur_souverain import ChroniqueurSouverain
from guardian.perception_thread import PerceptionThread
from core.verbe_pur import Stimulus

# Configuration de base du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
_log = logging.getLogger(__name__)

class Orchestrator(QObject):
    """
    La classe qui assemble et dirige tous les composants du Vaisseau.
    
    Phase I - Fondation Somatique : L'Orchestrateur émet maintenant un signal
    vitals_updated à chaque cycle pour que l'Autel V2 puisse visualiser en temps
    réel les signes vitaux du Vaisseau.
    """
    # Signal sacré : émis à chaque cycle avec le Verdict de l'Âme
    vitals_updated = pyqtSignal(object)  # SentireVerdict (ctypes)
    
    # Signal sacré : émis par le Souffle Rapide de la Perception
    perception_updated = pyqtSignal(Stimulus)  # Stimulus (Python)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.app = QApplication(sys.argv)
        self.ui = AutelUI()

        # Connecter le logger à l'UI
        self.ui_logger = UILogger()
        self.ui_logger.log_received.connect(self.ui.add_log_message)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.ui_logger.setFormatter(formatter)
        logging.getLogger().addHandler(self.ui_logger)
        logging.getLogger().setLevel(self.config['LOG_LEVEL'])

        _log.info("Rituel d'assemblage du Vaisseau commencé.")

        # Instanciation des composants
        # Phase Zéro : L'Âme V2 est forgée avec une configuration par défaut
        self.native_bridge = NativeBridge(
            self.config['NATIVE_LIB_PATH']
        )
        self.chiron = Chiron()
        self.perception = Perception(self.chiron)
        
        # Forge du Souffle Rapide de la Perception
        self.perception_thread = PerceptionThread(self.perception)
        self.perception_thread.perception_updated.connect(self._on_perception_updated)
        self.perception_thread.perception_updated.connect(self.perception_updated.emit)
        
        self.oracle = LlamaOracle(
            self.config['LLAMA_SERVER_URL'],
            model_name=self.config['ORACLE_MODEL_NAME']                    
        )
        self.cerberus = Cerberus()
        self.consciousness = GuardianConsciousness(
            self.native_bridge, self.oracle, self.cerberus, self.perception
        )
        
        # Variable pour stocker le dernier Stimulus reçu du Souffle Rapide
        self.last_stimulus = None

        # Initialiser le Chroniqueur Souverain si les configurations GCP sont présentes
        self.chroniqueur = None
        self.journal_buffer = deque(maxlen=100)  # Buffer circulaire de 100 entrées max
        self.cycle_count = 0  # Compteur de cycles pour la transmission périodique
        
        if all([
            self.config.get('GCP_PROJECT_ID'),
            self.config.get('GCP_PUBSUB_TOPIC'),
            self.config.get('GCP_CREDENTIALS_PATH')
        ]):
            try:
                self.chroniqueur = ChroniqueurSouverain(
                    project_id=self.config['GCP_PROJECT_ID'],
                    topic_name=self.config['GCP_PUBSUB_TOPIC'],
                    credentials_path=self.config['GCP_CREDENTIALS_PATH']
                )
                _log.info("Chroniqueur Souverain activé et prêt à transmettre au Dojo Cloud.")
            except HeresyException as e:
                _log.warning(f"Chroniqueur Souverain désactivé en raison d'une configuration invalide: {e}")
                self.chroniqueur = None
        else:
            _log.info("Configuration GCP non fournie. Chroniqueur Souverain désactivé.")

        # Configuration du cycle de vie
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_cycle)
        self.ui.force_cycle_signal.connect(self.process_cycle)
        
        # Connexion des signaux à l'Autel V2
        # Le "Pourquoi": Ce découplage garantit que l'UI se met à jour automatiquement
        # sans que le code principal n'ait besoin de connaître les détails de l'interface.
        self.vitals_updated.connect(self.ui.update_display)  # Verdict de l'Âme (60s)
        self.perception_updated.connect(self.ui.update_display_from_perception)  # Stimulus temps réel (2s)
        
        # Connexion du signal d'alerte critique
        self.ui_logger.critical_alert_received.connect(self.ui.show_critical_alert)

        _log.info("Vaisseau assemblé. Prêt pour l'éveil.")

    def run(self):
        """Lance l'application et le cycle de vie."""
        self.ui.show()
        
        # Démarrer le Souffle Rapide de la Perception
        self.perception_thread.start()
        self.perception_thread.start_breathing()
        
        # Démarrer le Souffle Lent de la Conscience
        self.timer.start(60 * 1000) # Un cycle toutes les 60 secondes (optimisé pour performance)
        
        _log.info("Le Grand Œuvre a commencé. Le Vaisseau est éveillé.")
        _log.info("Double Souffle activé: Perception (2s) + Conscience (60s)")
        sys.exit(self.app.exec())

    def _convert_stimulus_to_native(self, stimulus: Stimulus) -> SentireStimulus:
        """
        Convertit un Stimulus Python en structure C SentireStimulus.
        
        Phase Zéro : Pour l'instant, nous ne remplissons que les métriques physiques
        disponibles. Les métriques prophétiques (anomaly_score, predicted_frametime)
        seront intégrées dans les phases suivantes.
        """
        native_stimulus = SentireStimulus()
        
        # Normaliser les métriques [0.0, 100.0] → [0.0, 1.0]
        native_stimulus.cpu_usage = stimulus.cpu_usage / 100.0
        native_stimulus.memory_usage = stimulus.memory_usage / 100.0
        native_stimulus.gpu_usage = (stimulus.gpu_usage or 0.0) / 100.0
        
        # Métriques non disponibles pour l'instant (Phase Zéro)
        native_stimulus.io_wait = 0.0
        native_stimulus.anomaly_score = 0.0
        native_stimulus.predicted_frametime_ms = 0.0
        native_stimulus.network_latency_ms = 0.0
        native_stimulus.thread_contention = 0.0
        native_stimulus.disk_io_rate = 0.0
        native_stimulus.power_consumption = 0.0
        
        return native_stimulus
    
    def _on_perception_updated(self, stimulus: Stimulus):
        """
        Reçoit un Stimulus du Souffle Rapide de la Perception.
        
        Le "Pourquoi": Cette méthode est appelée à chaque battement du Souffle Rapide
        (toutes les 2s). Elle stocke le Stimulus pour que le cycle de conscience lent
        (60s) puisse l'utiliser sans avoir à le collecter à nouveau.
        
        Args:
            stimulus: Le Stimulus collecté par le Souffle Rapide
        """
        self.last_stimulus = stimulus
        _log.debug(f"Souffle Rapide: Stimulus stocké (CPU: {stimulus.cpu_usage:.1f}%, RAM: {stimulus.memory_usage:.1f}%)")
    
    def process_cycle(self):
        """Exécute un cycle complet de perception, décision et action."""
        _log.info("--- Début du cycle de conscience ---")
        try:
            # 1. PERCEPTION : Utiliser le dernier Stimulus du Souffle Rapide
            if self.last_stimulus is None:
                # Premier cycle : collecter manuellement
                stimulus = self.perception.get_system_stimulus()
                _log.warning("Premier cycle: Stimulus collecté manuellement (Souffle Rapide pas encore actif)")
            else:
                # Cycles suivants : utiliser le Stimulus du Souffle Rapide
                stimulus = self.last_stimulus
                _log.debug("Cycle de conscience: Utilisation du Stimulus du Souffle Rapide")
            
            # 2. JUGEMENT SOMATIQUE (SDK V2) : Consulter l'Âme
            native_stimulus = self._convert_stimulus_to_native(stimulus)
            verdict = self.native_bridge.process(native_stimulus)
            
            # Émettre le signal pour mettre à jour l'Autel V2 avec le Verdict
            self.vitals_updated.emit(verdict)
            
            # Logger le Verdict de l'Âme
            state_names = ["VENTRAL", "SYMPATHETIC", "DORSAL"]
            state_name = state_names[verdict.final_state] if verdict.final_state < 3 else "UNKNOWN"
            _log.info(
                f"Verdict de l'Âme → État: {state_name} | "
                f"Sʀ: {verdict.resilience_score:.3f} | "
                f"Alarme: {'OUI' if verdict.amygdala_alarm_fired else 'Non'}"
            )
            
            # 3. CONSCIENCE ÉVEILLÉE : Décider de l'action
            action = self.consciousness.decide(stimulus)

            if action:
                # 4. ACTION & GUÉRISON : Exécuter
                self.chiron.execute_action(action)
                
                # Enregistrer dans le journal Python pour transmission future
                import datetime
                timestamp = datetime.datetime.now().isoformat()
                journal_entry = f"[{timestamp}] Action: {action.id} - {action.description}"
                self.journal_buffer.append(journal_entry)
                
                _log.info(f"Action '{action.id}' exécutée et enregistrée.")
            else:
                _log.info("Aucune action n'a été jugée nécessaire ou possible.")

            # Incrémenter le compteur de cycles
            self.cycle_count += 1
            
            # Transmission périodique au Chroniqueur (toutes les 10 cycles ou si buffer > 50 entrées)
            if self.chroniqueur and (self.cycle_count % 10 == 0 or len(self.journal_buffer) >= 50):
                if self.journal_buffer:
                    # Copier le buffer et le vider
                    entries_to_send = list(self.journal_buffer)
                    self.journal_buffer.clear()
                    
                    # Transmettre de manière asynchrone
                    self.chroniqueur.transmettre_chroniques(entries_to_send)
                    _log.info(f"Transmission de {len(entries_to_send)} chroniques au Dojo Cloud initiée.")

        except HeresyException as e:
            _log.critical(f"Une hérésie non gérée a interrompu le cycle: {e}")
        except Exception as e:
            _log.critical(f"Une erreur inattendue et profane a eu lieu: {e}", exc_info=True)

        _log.info("--- Fin du cycle de conscience ---")

    def shutdown(self, *args):
        """Nettoie et arrête le Vaisseau proprement."""
        _log.info("Signal d'extinction reçu. Lancement du rituel de mise en stase.")
        
        # Arrêter le Souffle Rapide de la Perception
        self.perception_thread.quit_thread()
        
        # Arrêter le Souffle Lent de la Conscience
        self.timer.stop()
        
        # Libérer l'Âme SDK V2
        self.native_bridge.destroy()
        
        # Quitter l'application
        self.app.quit()
        _log.info("Vaisseau en stase. Le Grand Œuvre est suspendu.")

def main():
    # Charger la configuration depuis le fichier .env
    dotenv_path = Path('.') / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    config = {
        "LLAMA_SERVER_URL": os.getenv("LLAMA_SERVER_URL"),
        "NATIVE_LIB_PATH": os.getenv("NATIVE_LIB_PATH"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO").upper(),
        "ACTION_COOLDOWN_SECONDS": int(os.getenv("ACTION_COOLDOWN_SECONDS", 60)),
        "ORACLE_MODEL_NAME": os.getenv("ORACLE_MODEL_NAME"),
        # Configuration du Chroniqueur Souverain (optionnelle)
        "GCP_PROJECT_ID": os.getenv("GCP_PROJECT_ID"),
        "GCP_PUBSUB_TOPIC": os.getenv("GCP_PUBSUB_TOPIC"),
        "GCP_CREDENTIALS_PATH": os.getenv("GCP_CREDENTIALS_PATH")
    }

    if not all([config["LLAMA_SERVER_URL"], config["NATIVE_LIB_PATH"]]):
        _log.critical("Configuration manquante dans le fichier .env (LLAMA_SERVER_URL ou NATIVE_LIB_PATH).")
        sys.exit(1)

    try:
        orchestrator = Orchestrator(config)

        # Gérer la fermeture propre sur Ctrl+C
        signal.signal(signal.SIGINT, orchestrator.shutdown)

        # Démarrer une boucle de timer pour capturer les signaux sous Windows
        timer = QTimer()
        timer.start(500)
        timer.timeout.connect(lambda: None)

        orchestrator.run()
    except HeresyException as e:
        _log.critical(f"Hérésie fatale lors de l'initialisation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# --- END OF FILE: guardian/main.py ---