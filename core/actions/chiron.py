import os
import gc
import time
import logging
import ctypes
import sys
import sched
from typing import Optional

from core.action_registry import ActionRegistry

_log = logging.getLogger(__name__)

# Configuration spécifique à la plateforme
if sys.platform == "win32":
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

class Chiron:
    def __init__(self, action_registry: ActionRegistry):
        """
        Initialise Chiron avec le Grimoire Sacré des Capacités.
        
        Args:
            action_registry: Le registre des actions déclarées
        """
        self.registry = action_registry
        self._register_my_capacities()
        _log.info("Chiron forgé avec le Grimoire Sacré des Capacités.")
    
    def _register_my_capacities(self):
        """
        Le rituel de déclaration des pouvoirs de Chiron.
        
        Chiron déclare ici toutes ses capacités au Grimoire Sacré,
        permettant à la Conscience de savoir ce qui est possible.
        """
        # Actions de base
        self.registry.register("SHOW_MESSAGE", self.show_sovereign_message)
        self.registry.register("LOG_ONLY", self.log_to_journal)
        
        # Actions de gestion de processus
        self.registry.register("ISOLATE_PROCESS", self.isolate_process)
        self.registry.register("EXCOMMUNICATE_PROCESS", self.excommunicate_process)
        self.registry.register("LOWER_RIVAL_PRIORITY", self.lower_rival_process_priority)
        self.registry.register("TERMINATE_BY_SIGNATURE", self.terminate_process_by_signature)
        
        # Actions de guérison
        self.registry.register("FLUSH_MEMORY_CACHE", self.flush_memory_cache)
        self.registry.register("REDUCE_CPU_PRIORITY", self.reduce_cpu_priority)
        self.registry.register("PROTOCOL_RESONANCE_SOMATIQUE", self.protocol_resonance_somatique)
        
        _log.info(f"Chiron a déclaré {self.registry.get_action_count()} capacités au Grimoire Sacré.")
    def kernel_level_tap(self):
        """
        Tapotement sur la Nuque : Le tapotement doit être une "respiration" du noyau.
        
        Doctrine : Céder son temps de parole au thread suivant pour permettre
        une respiration naturelle du système et éviter la contention.
        """
        try:
            if sys.platform == "win32":
                # Rituel Windows : Céder son temps de parole au thread suivant.
                kernel32.SwitchToThread()
            else:
                # Rituel POSIX : Céder son quantum de temps à l'OS.
                os.sched_yield()
            _log.debug("Chiron: Tapotement Noyau (céder le temps).")
        except Exception as e:
            _log.warning(f"Hérésie mineure durant le tapotement noyau: {e}")

    def spirit_level_tap(self):
        """
        Tapotement sur le Front : Le tapotement doit être une introspection de l'Esprit.
        
        Doctrine : Forcer une passe de nettoyage mineure pour permettre
        une introspection et un nettoyage léger de l'espace mémoire.
        """
        try:
            # Rituel de l'auto-inspection : forcer une passe de nettoyage mineure.
            gc.collect(generation=0)
            _log.debug("Chiron: Tapotement Esprit (nettoyage mineur).")
        except Exception as e:
            _log.warning(f"Hérésie mineure durant le tapotement esprit: {e}")

    def flush_memory_cache(self):
        """
        Action de purification : Nettoie les caches mémoire applicatifs.
        """
        try:
            # Adapter selon la nature du cache applicatif réel
            gc.collect()
        except Exception as e:
            logging.warning(f"flush_memory_cache échoué : {e}")

    def reduce_cpu_priority(self):
        """
        Action de régénération : Réduit la priorité CPU du processus.
        """
        try:
            os.nice(10)
        except Exception as e:
            logging.warning(f"reduce_cpu_priority échoué : {e}")

    def log_to_journal(self, message):
        """
        Interface sacrée de journalisation.
        """
        try:
            logging.info(message)
        except Exception as e:
            print(f"[Erreur] log_to_journal: {e}")

    # =====================
    # Phase II - Rituels V2
    # =====================
    def isolate_process(self, pid: int) -> bool:
        """
        Isole un processus (suspend) pour stopper immédiatement sa consommation CPU.
        """
        try:
            import psutil
            proc = psutil.Process(pid)
            proc.suspend()
            logging.info(f"Processus isolé (suspendu): PID={pid}")
            return True
        except Exception as e:
            logging.error(f"isolate_process échoué (PID={pid}): {e}")
            return False

    def excommunicate_process(self, pid: int) -> bool:
        """
        Excommunie (kill) un processus identifié comme source de crise.
        """
        try:
            import psutil
            proc = psutil.Process(pid)
            proc.kill()
            logging.info(f"Processus excommunié (tué): PID={pid}")
            return True
        except Exception as e:
            logging.error(f"excommunicate_process échoué (PID={pid}): {e}")
            return False

    def lower_rival_process_priority(self, pid: int) -> bool:
        """
        Abaisse la priorité d'un processus rival pour réduire son impact.
        """
        try:
            import psutil
            proc = psutil.Process(pid)
            if os.name == "nt":
                # Windows: BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
                BELOW_NORMAL = 0x00004000
                ctypes.windll.kernel32.SetPriorityClass(int(proc.pid), BELOW_NORMAL)
            else:
                proc.nice(10)
            logging.info(f"Priorité abaissée pour PID={pid}")
            return True
        except Exception as e:
            logging.error(f"lower_rival_process_priority échoué (PID={pid}): {e}")
            return False
    
    def execute_action(self, action):
        """
        Rituel d'Exécution d'Action - Le Bras du Vaisseau.
        
        Le "Pourquoi": C'est le point de matérialisation de la Volonté de la Conscience.
        Après que l'Oracle ait décidé et que Cerberus ait validé, Chiron exécute l'action
        concrète sur le système. Ce rituel traduit les Actions abstraites (VerbePur) en
        effets tangibles dans le monde physique du système d'exploitation.
        
        Actions supportées:
        - SHOW_MESSAGE: Affiche un message souverain à l'opérateur
        - LOG_ONLY: Enregistre l'événement dans le journal sans intervention visible
        """
        from core.verbe_pur import Action
        
        if not isinstance(action, Action):
            logging.error(f"execute_action reçu un objet invalide: {type(action)}")
            return
        
        try:
            if action.id == "SHOW_MESSAGE":
                title = action.parameters.get("title", "Message du Vaisseau Guardian")
                message = action.parameters.get("message", action.parameters.get('description', 'Action sans description'))
                self.show_sovereign_message(title, message)
                logging.info(f"Action SHOW_MESSAGE exécutée: {title}")
            
            elif action.id == "LOG_ONLY":
                log_message = action.parameters.get("message", action.parameters.get('description', 'Action sans description'))
                self.log_to_journal(f"[ACTION] {log_message}")
                logging.info(f"Action LOG_ONLY exécutée: {log_message}")
            
            elif action.id == "ISOLATE_PROCESS":
                pid = int(action.parameters.get("pid"))
                self.isolate_process(pid)
            
            elif action.id == "EXCOMMUNICATE_PROCESS":
                pid = int(action.parameters.get("pid"))
                self.excommunicate_process(pid)

            elif action.id == "LOWER_RIVAL_PRIORITY":
                pid = int(action.parameters.get("pid"))
                self.lower_rival_process_priority(pid)
            
            else:
                logging.warning(f"Action non reconnue par Chiron: {action.id}")
        
        except Exception as e:
            logging.error(f"Hérésie lors de l'exécution de l'action {action.id}: {e}", exc_info=True)
    
    def show_sovereign_message(self, title: str, message: str):
        """
        Rituel d'Affichage Souverain - La Voix Sage du Vaisseau.
        
        Le "Pourquoi": Au lieu d'utiliser MessageBoxW (hérésie intrusive), le Vaisseau
        utilise maintenant le système de logging pour émettre une alerte critique. Cette
        alerte sera capturée par l'UILogger et affichée dans la bannière d'alerte de
        l'Autel, respectant la souveraineté de l'utilisateur sans interrompre son flux.
        """
        try:
            # Émettre une alerte critique via le système de logging
            logging.critical(f"VOIX SOUVERAINE - {title}: {message}")
        except Exception as e:
            logging.error(f"show_sovereign_message échoué: {e}")
    
    def get_foreground_window_title(self) -> str:
        """
        Rituel de Perception de Contexte - L'Œil du Vaisseau.
        
        Le "Pourquoi": Pour comprendre l'état mental et l'activité de l'opérateur,
        le Vaisseau doit savoir quelle fenêtre est actuellement au premier plan.
        Ce rituel interroge le système d'exploitation pour obtenir le titre de
        la fenêtre active, qui sera ensuite utilisé comme contexte pour les décisions
        de la Conscience.
        """
        try:
            if os.name == "nt":
                # Windows: Utilise l'API Win32
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                if hwnd == 0:
                    return "No window"
                
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                if length == 0:
                    return "No title"
                
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                return buff.value
            else:
                # Unix/Linux: Utilise xdotool si disponible
                import subprocess
                try:
                    result = subprocess.check_output(
                        ['xdotool', 'getactivewindow', 'getwindowname'],
                        stderr=subprocess.DEVNULL,
                        timeout=1
                    )
                    return result.decode('utf-8').strip()
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    return "Unknown (xdotool not available)"
        except Exception as e:
            logging.warning(f"get_foreground_window_title échoué: {e}")
            return "Error"
    
    def terminate_process_by_signature(self, signature: str):
        """
        Rituel de Terminaison de Processus - L'Épée du Vaisseau.
        
        Le "Pourquoi": En état Sympathique, si un processus est identifié comme
        une menace (consommation excessive de ressources, comportement suspect),
        le Vaisseau doit pouvoir l'arrêter de manière propre. Ce rituel recherche
        et termine les processus correspondant à la signature donnée.
        
        ATTENTION: Ce rituel est puissant et potentiellement dangereux. Il ne doit
        être invoqué que par les protocoles de Décharge Sympathique validés.
        """
        try:
            import psutil
            terminated_count = 0
            
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    # Vérifier si le nom ou le chemin contient la signature
                    if (signature.lower() in proc.info['name'].lower() or
                        (proc.info['exe'] and signature.lower() in proc.info['exe'].lower())):
                        
                        logging.warning(f"Tentative de terminaison du processus: {proc.info['name']} (PID: {proc.info['pid']})")
                        proc.terminate()
                        terminated_count += 1
                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if terminated_count > 0:
                logging.info(f"Terminé {terminated_count} processus correspondant à '{signature}'")
            else:
                logging.info(f"Aucun processus trouvé correspondant à '{signature}'")
        
        except Exception as e:
            logging.error(f"terminate_process_by_signature échoué: {e}")

    def protocol_resonance_somatique(self, initial_state, native_bridge) -> bool:
        """
        Le rituel de guérison vivant, basé sur le rythme adaptatif et le biofeedback.
        
        Doctrine : Ce rituel incarne la sagesse de l'auto-guérison somatique.
        Il utilise des tapotements subtils pour créer une résonance thérapeutique
        avec l'Âme, permettant un retour graduel à l'état VENTRAL.
        
        Args:
            initial_state: État initial de l'Âme (enum C mappé)
            native_bridge: Pont vers l'Âme pour le biofeedback
            
        Returns:
            True si la guérison a réussi, False sinon
        """
        _log.warning("Initiation du Rituel de Résonance Somatique...")
        
        cadence = self._generate_cadence(initial_state)
        start_time = time.time()
        
        # Le Biofeedback de l'Âme
        while native_bridge.get_resilience_score() < 0.8:  # Tant que nous ne sommes pas en VENTRAL
            if time.time() - start_time > 60:  # Garde-fou de 60 secondes
                _log.error("Hérésie: Le rituel de guérison a échoué par timeout.")
                return False

            # Exécute un cycle de tapotements
            for delay in cadence:
                self.kernel_level_tap()
                time.sleep(delay / 2)
                self.spirit_level_tap()
                time.sleep(delay / 2)
                
                # Vérification après chaque tapotement pour une réactivité maximale
                if native_bridge.get_resilience_score() >= 0.8:
                    break
            
            # Évolution du rituel : ralentir progressivement
            cadence = [d * 1.1 for d in cadence]
        
        _log.info("Retour à l'état VENTRAL réussi. Guérison accomplie.")
        return True

    def _generate_cadence(self, initial_state_enum) -> list[float]:
        """
        Génère la séquence de délais pour les tapotements.
        
        Doctrine : Chaque état nécessite une cadence thérapeutique spécifique.
        - SYMPATHETIC : Cadence accélérée pour calmer l'excitation
        - DORSAL : Cadence lente pour réveiller progressivement
        """
        # Note: Il faudra mapper l'enum C à un enum Python
        if initial_state_enum == 1:  # SYMPATHETIC
            return [0.05 * (1.25**i) for i in range(9)]
        elif initial_state_enum == 2:  # DORSAL
            return [2.0, 1.5, 1.0, 0.7, 0.5, 0.6, 0.8, 1.0]
        return [1.0]  # VENTRAL ou état inconnu