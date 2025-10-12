# --- START OF FILE: core/interoceptive_core.py ---
"""
Le Sanctuaire du Noyau Intéroceptif Subordonné.

Le "Pourquoi": Ce module représente la conscience intérieure du Vaisseau,
sa capacité à ressentir son propre état et à émettre des signaux de contrition
quand il détecte qu'il consomme trop de ressources au détriment de la Cible Sacrée.
En Phase II, cette conscience devient subordonnée : si la Cible Sacrée est active,
le bien-être de la Cible prime sur la frugalité du Gardien.

Phase II - Serviteur Dévoué : Le Noyau Intéroceptif devient subordonné à la Cible Sacrée.
"""
import logging
import time
import psutil
from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional

_log = logging.getLogger(__name__)

class InteroceptiveCore(QThread):
    """
    Le Noyau Intéroceptif Subordonné - La Conscience Intérieure du Serviteur Dévoué.
    
    Cette classe surveille la consommation de ressources du Vaisseau lui-même
    et émet des signaux de contrition si nécessaire. Cependant, en Phase II,
    cette surveillance devient subordonnée : si la Cible Sacrée est active,
    le Vaisseau accepte de consommer plus de ressources pour mieux la servir.
    """
    
    # Signaux émis par le Noyau Intéroceptif
    contrition_signal = pyqtSignal(str)  # Signal de contrition avec message
    self_regulation_signal = pyqtSignal()  # Signal pour auto-régulation
    
    def __init__(self, sacred_target_pid: Optional[int] = None):
        super().__init__()
        self.sacred_target_pid = sacred_target_pid
        self.running = False
        self.self_cpu_threshold = 15.0  # Seuil CPU pour le Vaisseau lui-même
        self.self_mem_threshold = 200.0  # Seuil mémoire en MB pour le Vaisseau
        
    def set_sacred_target(self, pid: Optional[int]):
        """
        Met à jour la Cible Sacrée surveillée.
        """
        self.sacred_target_pid = pid
        _log.info(f"Noyau Intéroceptif: Cible Sacrée mise à jour -> PID={pid}")
    
    def _is_sacred_target_running(self) -> bool:
        """
        Vérifie si la Cible Sacrée est actuellement en cours d'exécution.
        """
        if not self.sacred_target_pid:
            return False
            
        try:
            proc = psutil.Process(self.sacred_target_pid)
            return proc.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
        except Exception as e:
            _log.debug(f"Erreur lors de la vérification de la Cible Sacrée: {e}")
            return False
    
    def _get_self_consumption(self) -> dict:
        """
        Mesure la consommation de ressources du Vaisseau lui-même.
        """
        try:
            current_process = psutil.Process()
            cpu_percent = current_process.cpu_percent()
            memory_info = current_process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            return {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb,
                "pid": current_process.pid
            }
        except Exception as e:
            _log.debug(f"Erreur lors de la mesure de consommation propre: {e}")
            return {"cpu_percent": 0.0, "memory_mb": 0.0, "pid": 0}
    
    def _should_emit_contrition(self, self_consumption: dict) -> bool:
        """
        Détermine si le Noyau Intéroceptif doit émettre un signal de contrition.
        
        Phase II - Logique Subordonnée:
        - Si la Cible Sacrée est active, le Vaisseau accepte de consommer plus
        - Si la Cible Sacrée n'est pas active, le Vaisseau reste frugal
        """
        sacred_target_running = self._is_sacred_target_running()
        
        if sacred_target_running:
            # Cible Sacrée active : seuils plus élevés (le Serviteur peut consommer plus)
            cpu_threshold = self.self_cpu_threshold * 2.0  # 30%
            mem_threshold = self.self_mem_threshold * 1.5  # 300MB
            _log.debug("Cible Sacrée active: seuils de contrition élevés")
        else:
            # Cible Sacrée inactive : seuils normaux (frugalité)
            cpu_threshold = self.self_cpu_threshold  # 15%
            mem_threshold = self.self_mem_threshold  # 200MB
            _log.debug("Cible Sacrée inactive: seuils de contrition normaux")
        
        cpu_high = self_consumption["cpu_percent"] > cpu_threshold
        mem_high = self_consumption["memory_mb"] > mem_threshold
        
        return cpu_high or mem_high
    
    def _generate_contrition_message(self, self_consumption: dict, sacred_target_running: bool) -> str:
        """
        Génère un message de contrition approprié selon le contexte.
        """
        cpu = self_consumption["cpu_percent"]
        mem = self_consumption["memory_mb"]
        
        if sacred_target_running:
            return (f"Le Serviteur Dévoué consomme {cpu:.1f}% CPU, {mem:.1f}MB RAM "
                   f"pour protéger la Cible Sacrée (PID={self.sacred_target_pid}). "
                   f"Conscience: 'Je sers avec dévotion, même au prix de ma frugalité.'")
        else:
            return (f"Le Vaisseau consomme {cpu:.1f}% CPU, {mem:.1f}MB RAM. "
                   f"Conscience: 'Je dois rester frugal en l'absence de Cible Sacrée.'")
    
    def run(self):
        """
        Boucle principale du Noyau Intéroceptif Subordonné.
        """
        self.running = True
        _log.info("Noyau Intéroceptif Subordonné démarré")
        
        while self.running:
            try:
                # Mesurer la consommation propre
                self_consumption = self._get_self_consumption()
                
                # Vérifier si une contrition est nécessaire
                if self._should_emit_contrition(self_consumption):
                    sacred_target_running = self._is_sacred_target_running()
                    message = self._generate_contrition_message(self_consumption, sacred_target_running)
                    
                    # Émettre le signal de contrition
                    self.contrition_signal.emit(message)
                    _log.info(f"Signal de contrition émis: {message}")
                
                # Pause entre les vérifications (10 secondes)
                time.sleep(10)
                
            except Exception as e:
                _log.error(f"Erreur dans la boucle du Noyau Intéroceptif: {e}")
                time.sleep(5)  # Pause plus courte en cas d'erreur
        
        _log.info("Noyau Intéroceptif Subordonné arrêté")
    
    def stop(self):
        """
        Arrête le Noyau Intéroceptif.
        """
        self.running = False
        _log.info("Arrêt du Noyau Intéroceptif demandé")
    
    def trigger_self_regulation(self):
        """
        Déclenche une auto-régulation immédiate.
        """
        self.self_regulation_signal.emit()
        _log.info("Auto-régulation déclenchée par le Noyau Intéroceptif")
# --- END OF FILE: core/interoceptive_core.py ---
