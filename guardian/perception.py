# --- START OF FILE: guardian/perception.py ---
"""
Le Sanctuaire de la Perception.

Le "Pourquoi": Ce module est les sens du Vaisseau. Il utilise des outils comme
`psutil` et `Chiron` pour collecter des données sur l'état du système (CPU,
mémoire, contexte utilisateur). Il transforme ces données brutes en un `Stimulus`
structuré, un objet `VerbePur` que la Conscience peut comprendre et analyser.
Il fournit également les actions de dernier recours en cas de défaillance de l'Oracle.

Phase I - Fondation Somatique : Le Vaisseau apprend à sentir le feu du GPU.
"""
import psutil
import logging
from typing import Optional
from core.verbe_pur import Stimulus, Action
from core.actions.chiron import Chiron

# Sanctification de la Perception GPU : Initialisation résiliente de pynvml
try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
    _log = logging.getLogger(__name__)
    _log.info("Perception GPU activée via pynvml.")
except Exception as e:
    GPU_AVAILABLE = False
    _log = logging.getLogger(__name__)
    _log.warning(f"Perception GPU non disponible : {e}. Le Vaisseau continuera sans vision du GPU.")

class Perception:
    """
    Responsable de la collecte des informations système.
    """
    def __init__(self, chiron: Chiron):
        self.chiron = chiron

    def _get_top_processes(self) -> Optional[dict]:
        """
        Rituel de Perception Fine : identifie les processus les plus gourmands.
        
        Returns:
            dict avec les infos top CPU/mémoire ou None en cas d'échec
        """
        try:
            top_cpu_pid = None
            top_cpu_name = None
            top_cpu_value = -1.0

            top_mem_pid = None
            top_mem_name = None
            top_mem_value = -1

            for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
                info = proc.info
                # cpu_percent peut être 0 au premier appel; accepter la meilleure valeur vue
                cpu_p = float(info.get("cpu_percent") or 0.0)
                if cpu_p > top_cpu_value:
                    top_cpu_value = cpu_p
                    top_cpu_pid = info.get("pid")
                    top_cpu_name = info.get("name")

                mem_info = info.get("memory_info")
                if mem_info:
                    rss = getattr(mem_info, "rss", 0)
                    if rss > top_mem_value:
                        top_mem_value = rss
                        top_mem_pid = info.get("pid")
                        top_mem_name = info.get("name")

            return {
                "top_cpu_process_pid": top_cpu_pid,
                "top_cpu_process_name": top_cpu_name,
                "top_mem_process_pid": top_mem_pid,
                "top_mem_process_name": top_mem_name,
            }
        except Exception as e:
            _log.debug(f"Perception fine des processus échouée: {e}")
            return None

    def _get_gpu_metrics(self) -> Optional[dict]:
        """
        Rituel sacré pour percevoir le feu du GPU.
        
        Le "Pourquoi": Le GPU est le cœur ardent du Vaisseau pour les tâches lourdes.
        Connaître son utilisation et sa température permet de détecter les surcharges
        et de prévenir les crises thermiques. Ce rituel est encapsulé dans une garde
        sacrée pour garantir la résilience : si le GPU n'est pas accessible, le 
        Vaisseau continue sans cette perception.
        
        Returns:
            dict avec 'gpu_usage' et 'gpu_temp', ou None si GPU non accessible
        """
        if not GPU_AVAILABLE:
            return None
        
        try:
            # Obtenir handle du premier GPU (index 0)
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            
            # Extraire utilization GPU (pourcentage)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_usage = float(util.gpu)
            
            # Extraire température GPU (degrés Celsius)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            gpu_temp = float(temp)
            
            return {
                "gpu_usage": gpu_usage,
                "gpu_temp": gpu_temp
            }
        except Exception as e:
            _log.debug(f"Échec de la perception GPU : {e}")
            return None

    def get_system_stimulus(self) -> Stimulus:
        """
        Rassemble les métriques système et le contexte pour former un Stimulus.
        
        Phase I - Fondation Somatique : Inclut maintenant la perception du GPU.
        """
        try:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            window_title = self.chiron.get_foreground_window_title()
            
            # Percevoir le GPU si disponible
            gpu_metrics = self._get_gpu_metrics()
            gpu_usage = gpu_metrics["gpu_usage"] if gpu_metrics else None
            gpu_temp = gpu_metrics["gpu_temp"] if gpu_metrics else None

            # Perception fine des processus
            top_procs = self._get_top_processes() or {}

            stimulus = Stimulus(
                cpu_usage=cpu,
                memory_usage=mem,
                foreground_window_title=window_title,
                gpu_usage=gpu_usage,
                gpu_temp=gpu_temp,
                **top_procs
            )
            _log.debug(f"Stimulus perçu: CPU={cpu:.1f}%, MEM={mem:.1f}%, GPU={gpu_usage}, Temp={gpu_temp}°C")
            return stimulus
        except psutil.Error as e:
            _log.error(f"Erreur de perception avec psutil: {e}")
            # Retourne un stimulus par défaut en cas d'erreur
            return Stimulus(cpu_usage=0.0, memory_usage=0.0, foreground_window_title="Error")

    def get_fallback_action(self, error: Exception) -> Action:
        """
        Génère une action de secours lorsque l'Oracle est indisponible.

        Le "Pourquoi": La résilience souveraine impose que le Vaisseau ne soit
        jamais paralysé. Si l'Oracle est silencieux, le Vaisseau doit pouvoir
        prendre une initiative simple et sûre, comme alerter l'utilisateur,
        plutôt que de ne rien faire.
        """
        _log.warning(f"L'Oracle a failli. Activation du protocole de secours. Erreur: {error}")
        return Action(
            id="SHOW_MESSAGE",
            description="Alerte l'utilisateur que l'Oracle est injoignable et que le Vaisseau opère en mode dégradé.",
            parameters={
                "title": "Alerte de Résilience",
                "message": f"L'Oracle est inaccessible. Le Vaisseau continue sa surveillance en autonomie limitée.\nErreur: {str(error)[:100]}"
            }
        )
# --- END OF FILE: guardian/perception.py ---