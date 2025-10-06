import os
import gc
import time
import logging
import ctypes
import psutil
from typing import Optional

class Chiron:
    def kernel_level_tap(self):
        """
        Tapotement sur la Nuque : Interagit avec le noyau (sync disque, flush DNS...).
        """
        try:
            if os.name == "nt":
                # Windows: flush DNS (placeholder, usually needs admin)
                os.system("ipconfig /flushdns")
            else:
                os.sync()
        except Exception as e:
            logging.warning(f"kernel_level_tap échoué : {e}")

    def spirit_level_tap(self):
        """
        Tapotement sur le Front : Forcer la GC, pause, nettoyage cache python.
        """
        try:
            gc.collect()
            time.sleep(0.05)
        except Exception as e:
            logging.warning(f"spirit_level_tap échoué : {e}")

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

    def execute_action(self, action):
        """
        Rituel Principal : Exécute une Action en fonction de son identifiant sacré.
        
        Le "Pourquoi" : Chiron est le centaure-exécuteur, celui qui transforme l'intention
        (Action) en réalité (appel système). Ce rituel est le cœur de la volonté du Vaisseau.
        """
        action_map = {
            "SHOW_MESSAGE": self._execute_show_message,
            "LOG_ONLY": self._execute_log_only,
            "FLUSH_CACHE": self.flush_memory_cache,
            "REDUCE_PRIORITY": self.reduce_cpu_priority,
            "TERMINATE_PROCESS": self._execute_terminate_process,
        }
        
        handler = action_map.get(action.id)
        if handler:
            try:
                # Les méthodes existantes ne prennent pas de params
                if action.id in ["FLUSH_CACHE", "REDUCE_PRIORITY"]:
                    handler()
                else:
                    handler(action.parameters)
                logging.info(f"Action '{action.id}' exécutée avec succès.")
            except Exception as e:
                logging.error(f"Échec de l'exécution de l'action '{action.id}': {e}")
        else:
            logging.warning(f"Action inconnue: {action.id}. Aucune exécution.")

    def _execute_show_message(self, params: dict):
        """
        Affiche un message souverain à l'utilisateur.
        
        Le "Pourquoi" : Permet au Vaisseau de communiquer directement avec l'opérateur.
        """
        title = params.get("title", "Guardian V9")
        message = params.get("message", "Le Vaisseau vous salue.")
        self.show_sovereign_message(title, message)

    def _execute_log_only(self, params: dict):
        """
        Enregistre un message dans le journal.
        
        Le "Pourquoi" : Action minimale de logging sans effet secondaire système.
        """
        message = params.get("message", "Action de journalisation.")
        self.log_to_journal(message)

    def _execute_terminate_process(self, params: dict):
        """
        Termine un processus par sa signature.
        
        Le "Pourquoi" : Neutralise une menace identifiée en état Sympathique.
        """
        signature = params.get("signature")
        if signature:
            self.terminate_process_by_signature(signature)
        else:
            logging.warning("Signature de processus manquante pour l'action TERMINATE_PROCESS.")

    def get_foreground_window_title(self) -> str:
        """
        Rituel de Perception : Obtient le titre de la fenêtre actuellement active.
        
        Le "Pourquoi" : Permet au Vaisseau de percevoir le contexte de l'utilisateur
        en identifiant l'application active. C'est une forme de "conscience du contexte".
        """
        try:
            if os.name == "nt":  # Windows
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd) + 1
                buffer = ctypes.create_unicode_buffer(length)
                ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length)
                return buffer.value
            else:  # Linux/MacOS - placeholder
                logging.warning("get_foreground_window_title non implémenté pour cet OS.")
                return "Unknown (Non-Windows)"
        except Exception as e:
            logging.warning(f"get_foreground_window_title échoué : {e}")
            return "Error"

    def show_sovereign_message(self, title: str, message: str):
        """
        Rituel de Communication : Affiche un message modal à l'utilisateur.
        
        Le "Pourquoi" : Permet au Vaisseau de communiquer directement avec l'opérateur
        humain en cas d'urgence ou d'information critique. C'est la voix du Gardien.
        """
        try:
            if os.name == "nt":  # Windows
                # MB_ICONINFORMATION (0x40) | MB_OK (0x0)
                ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x0)
            else:
                # Fallback pour Linux/MacOS : print dans la console
                logging.info(f"[MESSAGE SOUVERAIN] {title}: {message}")
                print(f"\n{'='*60}\n{title}\n{'-'*60}\n{message}\n{'='*60}\n")
        except Exception as e:
            logging.warning(f"show_sovereign_message échoué : {e}")

    def terminate_process_by_signature(self, signature: str):
        """
        Rituel de Purge : Termine un processus identifié par une signature (nom ou motif).
        
        Le "Pourquoi" : En cas de menace détectée (état Sympathique), le Vaisseau doit
        pouvoir neutraliser un processus suspect. C'est l'instinct de survie numérique.
        """
        try:
            terminated = False
            for proc in psutil.process_iter(['pid', 'name']):
                if signature.lower() in proc.info['name'].lower():
                    logging.warning(f"Terminaison du processus suspecté : {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    terminated = True
            
            if not terminated:
                logging.info(f"Aucun processus correspondant à '{signature}' n'a été trouvé.")
        except Exception as e:
            logging.error(f"terminate_process_by_signature échoué : {e}")