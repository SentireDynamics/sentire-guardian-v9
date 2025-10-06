import os
import gc
import time
import logging
import ctypes
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
                message = action.parameters.get("message", action.description)
                self.show_sovereign_message(title, message)
                logging.info(f"Action SHOW_MESSAGE exécutée: {title}")
            
            elif action.id == "LOG_ONLY":
                log_message = action.parameters.get("message", action.description)
                self.log_to_journal(f"[ACTION] {log_message}")
                logging.info(f"Action LOG_ONLY exécutée: {log_message}")
            
            else:
                logging.warning(f"Action non reconnue par Chiron: {action.id}")
        
        except Exception as e:
            logging.error(f"Hérésie lors de l'exécution de l'action {action.id}: {e}", exc_info=True)
    
    def show_sovereign_message(self, title: str, message: str):
        """
        Rituel d'Affichage Souverain - La Voix du Vaisseau.
        
        Le "Pourquoi": Lorsque le Vaisseau doit communiquer de manière urgente avec
        l'opérateur humain, il utilise ce rituel pour afficher une boîte de message
        native du système d'exploitation. Sur Windows, cela utilise l'API Win32
        MessageBoxW pour garantir la visibilité.
        """
        try:
            if os.name == "nt":
                # Windows: Utilise MessageBoxW de l'API Win32
                # MB_OK | MB_ICONINFORMATION = 0x00000040
                ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000040)
            else:
                # Unix/Linux: Affiche dans le terminal (peut être étendu avec notify-send)
                print(f"\n{'='*60}")
                print(f"TITRE: {title}")
                print(f"MESSAGE: {message}")
                print(f"{'='*60}\n")
                logging.info(f"Message souverain affiché: {title}")
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