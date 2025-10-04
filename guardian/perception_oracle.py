import psutil
import random

class PerceptionOracle:
    """
    L'Oracle de la Perception, responsable de la collecte des stimuli du système.

    @doctrine
    Cet oracle est le premier maillon de la chaîne de conscience. Il doit fournir
    une lecture aussi fidèle que possible de la réalité du système. L'utilisation de
    `psutil` remplace la simulation par une mesure directe, ancrant les décisions du
    Gardien dans la vérité du matériel sur lequel il opère.
    """
    def get_system_metrics(self) -> dict:
        """
        Retourne les métriques système actuelles.
        """
        # Utilisation de psutil pour des données réelles
        cpu_load = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        # Simule l'io_wait qui n'est pas directement disponible partout
        # Une valeur aléatoire raisonnable est utilisée pour simuler la réalité.
        io_wait = random.uniform(0.0, 15.0) if cpu_load < 80 else random.uniform(10.0, 40.0)

        return {
            "cpu_load": cpu_load,
            "memory_usage": memory_info.percent,
            "io_wait": io_wait
        }