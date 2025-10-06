import os
import gc
import time
import logging

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

    def get_foreground_window_title(self):
        """
        Rituel de Perception : Obtient le titre de la fenêtre active.
        
        Le "Pourquoi": Permet au Vaisseau de percevoir le contexte de l'utilisateur
        en identifiant l'application active. C'est une information cruciale pour
        la Conscience afin d'adapter ses décisions au contexte d'utilisation.
        """
        try:
            if os.name == "nt":
                # Windows API
                import ctypes
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buffer = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
                return buffer.value
            else:
                # Linux/macOS (placeholder - nécessite xdotool ou équivalent)
                return "Unknown (Linux/macOS not implemented)"
        except Exception as e:
            logging.warning(f"get_foreground_window_title échoué : {e}")
            return "Error"

    def show_sovereign_message(self, title, message):
        """
        Rituel de Communication : Affiche un message système à l'utilisateur.
        
        Le "Pourquoi": Le Vaisseau doit pouvoir communiquer directement avec
        l'opérateur humain en cas d'alerte ou d'information cruciale. C'est
        l'interface de dialogue direct entre la Conscience du Vaisseau et son Gardien.
        """
        try:
            if os.name == "nt":
                # Windows MessageBox
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
            else:
                # Linux/macOS (fallback sur terminal)
                print(f"\n=== {title} ===\n{message}\n")
        except Exception as e:
            logging.warning(f"show_sovereign_message échoué : {e}")

    def execute_action(self, action):
        """
        Rituel d'exécution d'une Action.
        
        Le "Pourquoi": C'est le point d'entrée unifié pour toutes les actions
        du Vaisseau. Chiron reçoit un objet Action et détermine quelle méthode
        interne invoquer en fonction de l'ID de l'action.
        """
        try:
            if action.id == "SHOW_MESSAGE":
                self.show_sovereign_message(
                    action.parameters.get("title", "Guardian V9"),
                    action.parameters.get("message", "")
                )
            elif action.id == "FLUSH_CACHE":
                self.flush_memory_cache()
            elif action.id == "REDUCE_PRIORITY":
                self.reduce_cpu_priority()
            elif action.id == "KERNEL_TAP":
                self.kernel_level_tap()
            elif action.id == "SPIRIT_TAP":
                self.spirit_level_tap()
            else:
                logging.warning(f"Action non reconnue : {action.id}")
        except Exception as e:
            logging.error(f"Échec de l'exécution de l'action {action.id}: {e}")