# --- START OF FILE: guardian/perception.py ---
"""
Le Sanctuaire de la Perception - Poly-rythmique.

Le "Pourquoi": Ce module orchestre la perception graduée du Vaisseau, séparant
le sentiment interne (SoulVitals) de la réalité externe (ContextualResonance).
Il implémente la doctrine poly-rythmique avec deux souffles distincts :
- Le Souffle Rapide : Perception de l'Âme (haute fréquence)
- Le Souffle Lent : Perception du monde extérieur (basse fréquence)

Doctrine de la Perception Graduée :
- SoulVitals : État interne de l'Âme (SDK C) - Synchrone, rapide
- ContextualResonance : Réalité externe (senseurs) - Asynchrone, lent
- Stimulus : Fusion harmonieuse des deux perceptions
"""
import time
import asyncio
import logging
import psutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from ffi.native_bridge import NativeBridge
from core.verbe_pur import SoulVitals, ContextualResonance, Stimulus
from guardian.sensors.base_sensor import BaseSensor
from guardian.sensors.log_file_sensor import LogFileSensor
from guardian.sacred_target_sensor import SacredTargetSensor, TargetVitals

_log = logging.getLogger(__name__)

class Perception:
    """
    Le Grand Prêtre de la Perception Poly-rythmique.
    
    Doctrine :
    - Orchestre les deux souffles de perception
    - Gère dynamiquement les senseurs externes
    - Fournit une interface unifiée pour la conscience
    """
    
    def __init__(self, native_bridge: NativeBridge, sensor_configs: List[Dict[str, Any]]):
        """
        Initialise la Perception avec l'Âme et les senseurs.
        
        Args:
            native_bridge: Pont vers l'Âme (SDK C)
            sensor_configs: Configuration des senseurs externes
        """
        self.native_bridge = native_bridge
        self.sensors: List[BaseSensor] = self._init_sensors(sensor_configs)
        self.sacred_target_sensor: Optional[SacredTargetSensor] = None
        self._last_contextual_resonance: Optional[List[ContextualResonance]] = None
        self._last_contextual_update: float = 0.0
        
        _log.info(f"Perception poly-rythmique initialisée avec {len(self.sensors)} senseurs")
    
    def set_sacred_target(self, target_name: str):
        """Définit la Cible Sacrée pour la surveillance."""
        self.sacred_target_sensor = SacredTargetSensor(target_name)
        _log.info(f"Cible Sacrée définie dans la Perception: {target_name}")
    
    def _init_sensors(self, configs: List[Dict[str, Any]]) -> List[BaseSensor]:
        """
        Initialise dynamiquement les senseurs à partir de la configuration.
        
        Args:
            configs: Liste des configurations de senseurs
            
        Returns:
            Liste des senseurs instanciés
        """
        sensors = []
        
        for config in configs:
            sensor_type = config.get('type')
            
            if sensor_type == 'log_file':
                log_path = config.get('log_file_path')
                error_keywords = config.get('error_keywords', ['error', 'exception', 'fail'])
                
                if log_path:
                    sensor = LogFileSensor(log_path, error_keywords)
                    sensors.append(sensor)
                    _log.info(f"Senseur de log ajouté : {log_path}")
                else:
                    _log.warning("Configuration de senseur de log incomplète")
            
            # TODO: Ajouter d'autres types de senseurs ici
            # elif sensor_type == 'cpu_watcher':
            #     ...
            # elif sensor_type == 'network_monitor':
            #     ...
        
        return sensors
    
    def get_soul_vitals(self) -> SoulVitals:
        """
        LE SOUFFLE RAPIDE (Synchrone).
        
        Interroge l'Âme pour son état interne immédiat.
        Cette méthode doit être rapide et ne pas bloquer.
        
        Returns:
            SoulVitals: État actuel de l'Âme
        """
        try:
            # Récupérer le verdict de l'Âme
            verdict = self.native_bridge.get_last_verdict()
            
            if verdict:
                # Calculer le temps passé dans l'état actuel
                # Pour l'instant, on utilise une approximation
                # Dans une implémentation complète, on suivrait les transitions d'état
                time_in_state_ms = 1000  # Valeur par défaut
                
                return SoulVitals(
                    somatic_state=verdict.somatic_state,
                    resilience_score=verdict.resilience_score,
                    time_in_state_ms=time_in_state_ms
                )
            else:
                # État par défaut si pas de verdict
                return SoulVitals(
                    somatic_state=0,  # VENTRAL
                    resilience_score=1.0,
                    time_in_state_ms=0
                )
                
        except Exception as e:
            _log.error(f"Erreur lors de la récupération des SoulVitals : {e}")
            # Retourner un état de sécurité
            return SoulVitals(
                somatic_state=2,  # DORSAL (état de sécurité)
                resilience_score=0.5,
                time_in_state_ms=0
            )
    
    async def get_contextual_resonance(self) -> List[ContextualResonance]:
        """
        LE SOUFFLE LENT (Asynchrone).
        
        Interroge le monde extérieur via tous les senseurs.
        Cette méthode peut prendre du temps et doit être appelée moins fréquemment.
        
        Returns:
            Liste des observations contextuelles de tous les senseurs
        """
        try:
            # Exécuter tous les senseurs en parallèle
            tasks = [asyncio.to_thread(sensor.read) for sensor in self.sensors]
            sensor_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            resonance_list = []
            
            # Ajouter les vitaux de la Cible Sacrée si elle est définie
            if self.sacred_target_sensor:
                try:
                    target_vitals = self.sacred_target_sensor.measure_health()
                    target_resonance = ContextualResonance(
                        sensor_id="sacred_target",
                        metrics={
                            "is_running": target_vitals.is_running,
                            "status": target_vitals.status,
                            "cpu_percent": target_vitals.cpu_percent,
                            "memory_mb": target_vitals.memory_mb,
                            "pid": target_vitals.pid,
                            "name": target_vitals.name
                        }
                    )
                    resonance_list.append(target_resonance)
                except Exception as e:
                    _log.error(f"Erreur dans le senseur de Cible Sacrée: {e}")
                    target_resonance = ContextualResonance(
                        sensor_id="sacred_target",
                        metrics={"error": str(e), "status": "error"}
                    )
                    resonance_list.append(target_resonance)
            
            for i, result in enumerate(sensor_results):
                sensor = self.sensors[i]
                
                if isinstance(result, Exception):
                    _log.error(f"Erreur dans le senseur {sensor.sensor_id}: {result}")
                    # Créer une résonance d'erreur
                    resonance = ContextualResonance(
                        sensor_id=sensor.sensor_id,
                        metrics={"error": str(result), "status": "error"}
                    )
                else:
                    # Créer une résonance normale
                    resonance = ContextualResonance(
                        sensor_id=sensor.sensor_id,
                        metrics=result
                    )
                
                resonance_list.append(resonance)
            
            # Mettre à jour le cache
            self._last_contextual_resonance = resonance_list
            self._last_contextual_update = time.time()
            
            return resonance_list
            
        except Exception as e:
            _log.error(f"Erreur lors de la récupération de la résonance contextuelle : {e}")
            return []
    
    def get_top_contenders(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Retourne les processus les plus gourmands en ressources pour la sélection de Cible Sacrée.
        Compatible avec l'interface existante de l'Autel.
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    pinfo = proc.info
                    if pinfo['pid'] == 0:  # Skip kernel process
                        continue
                    
                    # Calculer la mémoire en MB
                    mem_mb = pinfo['memory_info'].rss / 1024 / 1024 if pinfo['memory_info'] else 0
                    
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'] or 'Unknown',
                        'cpu': pinfo['cpu_percent'] or 0.0,
                        'mem_mb': mem_mb
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Trier par CPU + mémoire combinés et retourner les top
            processes.sort(key=lambda x: x['cpu'] + (x['mem_mb'] / 100), reverse=True)
            return processes[:count]
            
        except Exception as e:
            _log.error(f"Erreur lors de la collecte des processus: {e}")
            return []
    
    def get_light_stimulus_c(self) -> Optional[Any]:
        """
        Génère un stimulus léger pour le VelocityWatcher.
        Compatible avec l'ancienne interface SentireStimulus.
        """
        try:
            # Créer un stimulus léger avec les métriques système de base
            import psutil
            
            # Obtenir les métriques système
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Créer un stimulus compatible avec l'ancienne interface
            from ffi.native_bridge import SentireStimulus
            
            stimulus = SentireStimulus(
                cpu_usage=cpu_percent / 100.0,  # Normaliser en [0.0, 1.0]
                memory_usage=memory_percent / 100.0,  # Normaliser en [0.0, 1.0]
                gpu_usage=0.0,  # Pas de GPU pour l'instant
                sacred_target=None,  # Pas de cible sacrée pour le stimulus léger
                rival_process=None
            )
            
            return stimulus
            
        except Exception as e:
            _log.error(f"Erreur lors de la génération du stimulus léger: {e}")
            return None
    
    def get_cached_contextual_resonance(self) -> Optional[List[ContextualResonance]]:
        """
        Récupère la dernière résonance contextuelle mise en cache.
        
        Returns:
            Dernière résonance contextuelle ou None si pas encore disponible
        """
        return self._last_contextual_resonance
    
    def get_stimulus(self, use_cached_context: bool = True) -> Stimulus:
        """
        Construit un Stimulus complet en fusionnant les deux perceptions.
        
        Args:
            use_cached_context: Si True, utilise la résonance contextuelle mise en cache
            
        Returns:
            Stimulus complet avec SoulVitals et ContextualResonance
        """
        # Toujours récupérer les SoulVitals (rapide)
        soul_vitals = self.get_soul_vitals()
        
        # Récupérer la résonance contextuelle
        if use_cached_context and self._last_contextual_resonance is not None:
            contextual_resonance = self.get_cached_contextual_resonance()
        else:
            # Mode synchrone - force la mise à jour
            contextual_resonance = asyncio.run(self.get_contextual_resonance())
            self._last_contextual_resonance = contextual_resonance
        
        # Construire le Stimulus
        timestamp_utc = datetime.utcnow().isoformat()
        
        return Stimulus(
            timestamp_utc=timestamp_utc,
            soul_vitals=soul_vitals,
            contextual_resonance=contextual_resonance
        )
    
    def add_sensor(self, sensor: BaseSensor):
        """
        Ajoute un nouveau senseur à la perception.
        
        Args:
            sensor: Senseur à ajouter
        """
        self.sensors.append(sensor)
        _log.info(f"Senseur ajouté : {sensor.sensor_id}")
    
    def remove_sensor(self, sensor_id: str) -> bool:
        """
        Supprime un senseur de la perception.
        
        Args:
            sensor_id: Identifiant du senseur à supprimer
            
        Returns:
            True si le senseur a été trouvé et supprimé
        """
        for i, sensor in enumerate(self.sensors):
            if sensor.sensor_id == sensor_id:
                del self.sensors[i]
                _log.info(f"Senseur supprimé : {sensor_id}")
                return True
        
        _log.warning(f"Senseur non trouvé : {sensor_id}")
        return False
    
    def get_sensor_count(self) -> int:
        """
        Retourne le nombre de senseurs actifs.
        
        Returns:
            Nombre de senseurs actifs
        """
        return len(self.sensors)
    
    def get_sensor_ids(self) -> List[str]:
        """
        Retourne la liste des identifiants des senseurs actifs.
        
        Returns:
            Liste des identifiants des senseurs
        """
        return [sensor.sensor_id for sensor in self.sensors]

# --- NOTE DOCTRINALE POUR L'ORCHESTRATEUR (guardian/main.py) ---
# L'Orchestrateur devra être reforgé pour utiliser cette nouvelle perception
# avec deux timers/tâches distincts :
# 1. Un timer rapide (ex: 1s) qui appelle `perception.get_soul_vitals()` et
#    construit la base du Stimulus.
# 2. Un timer plus lent (ex: 10s) qui `await perception.get_contextual_resonance()`
#    et met à jour la partie contextuelle du Stimulus.
# --- END OF FILE: guardian/perception.py ---