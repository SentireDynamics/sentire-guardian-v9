import os
import subprocess
import sys
import psutil

class Chiron:
    """
    Le bras armé du Gardien, responsable de l'exécution des actions sur le système.

    @doctrine
    Chiron est la matérialisation de la volonté du Gardien. Chaque méthode est un rituel
    d'action, une intervention directe sur le système d'exploitation. L'implémentation
    doit être puissante mais prudente, capable d'affecter le changement nécessaire
    tout en préservant l'intégrité du Vaisseau. L'utilisation de `subprocess` et `psutil`
    permet des interactions réelles et contrôlées avec l'environnement.
    """
    def flush_memory_cache(self):
        """
        Rituel pour forcer le noyau à vider les caches de page, dentries et inodes.
        Action puissante réservée aux situations de stress mémoire intense.
        NOTE : Nécessite des privilèges élevés (root).
        """
        if sys.platform != "linux":
            print("AVERTISSEMENT : Le rituel flush_memory_cache n'est implémenté que pour Linux.")
            return

        print("Rituel Chiron : Vidage des caches mémoire système...")
        try:
            # Synchronise les données sur disque avant de vider.
            subprocess.run(["sync"], check=True)
            # Écrit '3' dans drop_caches pour vider tous les caches.
            with open('/proc/sys/vm/drop_caches', 'w') as f:
                f.write('3\n')
            print("Rituel accompli. Les caches mémoire ont été purgés.")
        except PermissionError:
            print("ERREUR : Privilèges insuffisants pour exécuter le rituel flush_memory_cache.")
        except Exception as e:
            print(f"ERREUR lors de l'exécution du rituel flush_memory_cache : {e}")

    def reduce_cpu_priority(self, increment: int = 10):
        """
        Rituel pour réduire la priorité CPU du processus Gardien lui-même.
        Permet de céder des ressources en cas de contention.
        """
        print(f"Rituel Chiron : Réduction de la priorité CPU (nice +{increment})...")
        try:
            current_nice = os.nice(0)
            os.nice(increment)
            new_nice = os.nice(0)
            print(f"Rituel accompli. Priorité 'nice' passée de {current_nice} à {new_nice}.")
        except Exception as e:
            print(f"ERREUR lors de l'exécution du rituel reduce_cpu_priority : {e}")

    def terminate_process_by_signature(self, signature: str):
        """
        Rituel pour trouver et terminer un processus basé sur une signature
        (ex: une partie de son nom ou de sa ligne de commande).
        """
        print(f"Rituel Chiron : Recherche et terminaison des processus avec la signature '{signature}'...")
        terminated_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # La signature peut être dans le nom ou la ligne de commande
                if signature in proc.info['name'] or (proc.info['cmdline'] and signature in ' '.join(proc.info['cmdline'])):
                    if proc.pid == os.getpid(): # Ne pas se terminer soi-même
                        continue

                    print(f"  Processus correspondant trouvé : PID={proc.pid}, Nom='{proc.info['name']}'. Terminaison...")
                    p = psutil.Process(proc.pid)
                    p.terminate() # Envoie SIGTERM pour une terminaison propre
                    terminated_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if terminated_count > 0:
            print(f"Rituel accompli. {terminated_count} processus terminés.")
        else:
            print(f"Aucun processus correspondant à la signature '{signature}' n'a été trouvé.")