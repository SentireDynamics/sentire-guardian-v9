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
from PyQt6.QtCore import QTimer

# Charger les modules du Vaisseau
from ffi.native_bridge import NativeBridge
from core.actions.chiron import Chiron
from guardian.perception import Perception
from oracle.llama_client import LlamaOracle
from guardian.cerberus import Cerberus
from core.consciousness import GuardianConsciousness
from guardian.ui.autel import AutelUI, UILogger
from core.exceptions import HeresyException
from guardian.chroniqueur_souverain import ChroniqueurSouverain

# Configuration de base du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
_log = logging.getLogger(__name__)

class Orchestrator:
    """
    La classe qui assemble et dirige tous les composants du Vaisseau.
    """
    def __init__(self, config):
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
        self.native_bridge = NativeBridge(
            self.config['NATIVE_LIB_PATH'],
            self.config['ACTION_COOLDOWN_SECONDS']
        )
        self.chiron = Chiron()
        self.perception = Perception(self.chiron)
        self.oracle = LlamaOracle(self.config['LLAMA_SERVER_URL'])
        self.cerberus = Cerberus()
        self.consciousness = GuardianConsciousness(
            self.native_bridge, self.oracle, self.cerberus, self.perception
        )

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

        _log.info("Vaisseau assemblé. Prêt pour l'éveil.")

    def run(self):
        """Lance l'application et le cycle de vie."""
        self.ui.show()
        self.timer.start(30 * 1000) # Un cycle toutes les 30 secondes
        _log.info("Le Grand Œuvre a commencé. Le Vaisseau est éveillé.")
        sys.exit(self.app.exec())

    def process_cycle(self):
        """Exécute un cycle complet de perception, décision et action."""
        _log.info("--- Début du cycle de conscience ---")
        try:
            stimulus = self.perception.get_system_stimulus()
            action = self.consciousness.decide(stimulus)

            if action:
                self.chiron.execute_action(action)
                self.native_bridge.record_action(action.description)
                
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
        self.timer.stop()
        self.native_bridge.destroy()
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