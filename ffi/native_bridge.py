# --- START OF FILE: ffi/native_bridge.py (PURIFIED FOR SDK V2) ---
"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    LA SYNAPSE SACRÉE - FFI VERS L'ÂME V2                 ║
╚══════════════════════════════════════════════════════════════════════════╝

POURQUOI : Ce sanctuaire est le pont FFI entre l'Esprit Python et l'Âme C (SDK V2).
Il traduit les structures Python en structures C natives et invoque les rituels
sacrés de l'API publique du SDK V2 (sentire_core.h).

DOCTRINE : Théorie Polyvagale Digitale Unifiée (TPDU)
"""

import ctypes
import logging
from core.exceptions import NativeBodyCreationFailed

_log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════
# STRUCTURES SACRÉES - MAPPÉES DEPUIS sentire_core.h
# ═══════════════════════════════════════════════════════════════════════════

class SentireConfig(ctypes.Structure):
    """
    Configuration complète de l'Âme (sentire_config_t).
    Définit les poids, seuils, et paramètres de l'Amygdale.
    """
    _fields_ = [
        # ─── Poids des Stimuli Physiques ───
        ('weight_cpu', ctypes.c_float),
        ('weight_memory', ctypes.c_float),
        ('weight_gpu', ctypes.c_float),
        ('weight_io', ctypes.c_float),
        ('weight_network', ctypes.c_float),
        ('weight_threads', ctypes.c_float),
        ('weight_disk', ctypes.c_float),
        ('weight_power', ctypes.c_float),
        
        # ─── Poids des Stimuli Prophétiques ───
        ('weight_anomaly', ctypes.c_float),
        ('weight_frametime', ctypes.c_float),
        
        # ─── Poids des Vélocités (Physique Temporelle) ───
        ('weight_velocity_cpu', ctypes.c_float),
        ('weight_velocity_memory', ctypes.c_float),
        ('weight_velocity_gpu', ctypes.c_float),
        ('weight_velocity_io', ctypes.c_float),
        
        # ─── Seuils Polyvagaux ───
        ('state_threshold_ventral', ctypes.c_float),   # Défaut: 0.8
        ('state_threshold_dorsal', ctypes.c_float),    # Défaut: 0.4
        ('hysteresis_factor', ctypes.c_float),         # Défaut: 0.05
        
        # ─── Paramètres de l'Amygdale (Voie Rapide) ───
        ('amygdala_threshold_cpu_velocity', ctypes.c_float),
        ('amygdala_threshold_memory_velocity', ctypes.c_float),
        ('amygdala_threshold_gpu_velocity', ctypes.c_float),
        ('amygdala_alarm_penalty', ctypes.c_float),
        
        # ─── Ajustement Contextuel (Φε) ───
        ('context_multiplier_ventral', ctypes.c_float),      # Défaut: 1.0
        ('context_multiplier_sympathetic', ctypes.c_float),  # Défaut: 1.25
        ('context_multiplier_dorsal', ctypes.c_float),       # Défaut: 1.5
        
        # ─── Stabilité Temporelle ───
        ('transition_cooldown_ticks', ctypes.c_int),
        
        # ─── Mémoire ───
        ('journal_capacity', ctypes.c_int),
    ]


class SentireStimulus(ctypes.Structure):
    """
    Stimulus perçu à un instant T (sentire_stimulus_t).
    Contient les métriques physiques et prophétiques.
    """
    _fields_ = [
        # Métriques Physiques [0.0 = idle, 1.0 = saturé]
        ('cpu_usage', ctypes.c_float),
        ('memory_usage', ctypes.c_float),
        ('gpu_usage', ctypes.c_float),
        ('io_wait', ctypes.c_float),
        
        # Métriques Prophétiques
        ('anomaly_score', ctypes.c_float),            # 0.0 = normal, 1.0 = menace
        ('predicted_frametime_ms', ctypes.c_float),   # Prophétie du frametime
        
        # Métriques Supplémentaires
        ('network_latency_ms', ctypes.c_float),
        ('thread_contention', ctypes.c_float),
        ('disk_io_rate', ctypes.c_float),
        ('power_consumption', ctypes.c_float),
    ]


class SentireVerdict(ctypes.Structure):
    """
    Verdict retourné par l'Âme après jugement (sentire_verdict_t).
    Contient l'état final, les métriques, et le flag d'alarme.
    """
    _fields_ = [
        ('final_state', ctypes.c_int),          # sentire_state_t (0=VENTRAL, 1=SYMPATHETIC, 2=DORSAL)
        ('amygdala_alarm_fired', ctypes.c_int), # 1 si alarme, 0 sinon
        ('resilience_score', ctypes.c_float),   # Sʀ ∈ [0.0, 1.0]
        ('impact_score', ctypes.c_float),       # Iφ (Impact Final)
        ('impact_base', ctypes.c_float),        # Iβ (Impact Brut)
    ]


# ═══════════════════════════════════════════════════════════════════════════
# LA SYNAPSE SACRÉE - INTERFACE FFI
# ═══════════════════════════════════════════════════════════════════════════

def create_default_config() -> SentireConfig:
    """
    Forge une configuration par défaut pour l'Âme.
    Basée sur la Doctrine TPDU et les meilleures pratiques.
    """
    config = SentireConfig()
    
    # Poids des Stimuli Physiques (ajustés pour la sensibilité typique)
    # NOTE: Ces stimuli sont normalisés [0.0, 1.0]
    config.weight_cpu = 0.4
    config.weight_memory = 0.3
    config.weight_gpu = 0.3
    config.weight_io = 0.2
    config.weight_network = 0.001  # CORRIGÉ: network_latency_ms est en ms (non normalisé)
    config.weight_threads = 0.1
    config.weight_disk = 0.1
    config.weight_power = 0.05
    
    # Poids des Stimuli Prophétiques (haute importance pour ML)
    config.weight_anomaly = 0.5     # Détection d'anomalie est critique [0.0, 1.0]
    config.weight_frametime = 0.001  # CORRIGÉ: frametime est en ms (16-100ms typique)
    
    # Poids des Vélocités (Physique Temporelle - Voie Rapide)
    config.weight_velocity_cpu = 0.3
    config.weight_velocity_memory = 0.2
    config.weight_velocity_gpu = 0.2
    config.weight_velocity_io = 0.1
    
    # Seuils Polyvagaux (Doctrine TPDU) - PURIFIÉS
    config.state_threshold_ventral = 0.8   # Sʀ ≥ 0.8 → VENTRAL
    config.state_threshold_dorsal = 0.4    # Sʀ < 0.4 → DORSAL
    config.hysteresis_factor = 0.02        # CORRIGÉ: Hystérésis réduite pour éviter la zone morte
    
    # Paramètres de l'Amygdale (Voie Rapide)
    config.amygdala_threshold_cpu_velocity = 0.3     # Δ30%/sec → alarme
    config.amygdala_threshold_memory_velocity = 0.2  # Δ20%/sec → alarme
    config.amygdala_threshold_gpu_velocity = 0.3     # Δ30%/sec → alarme
    config.amygdala_alarm_penalty = 0.15             # Pénalité d'alarme
    
    # Ajustement Contextuel (Φε)
    config.context_multiplier_ventral = 1.0
    config.context_multiplier_sympathetic = 1.25
    config.context_multiplier_dorsal = 1.5
    
    # Stabilité Temporelle
    config.transition_cooldown_ticks = 1  # 1 cycle avant nouvelle transition (60s)
    
    # Mémoire
    config.journal_capacity = 1000  # 1000 entrées dans le Journal
    
    return config


class NativeBridge:
    """
    Pont FFI vers l'Âme Souveraine (SDK V2).
    Gère le cycle de vie de l'Âme et invoque les rituels sacrés.
    """
    
    def __init__(self, library_path: str, config: SentireConfig = None):
        """
        Charge l'Âme et l'initialise avec la configuration donnée.
        
        Args:
            library_path: Chemin vers sentire_core.dll
            config: Configuration de l'Âme (SentireConfig). Si None, utilise la config par défaut.
            
        Raises:
            NativeBodyCreationFailed: Si l'Âme ne peut être créée
        """
        # Utilise une config par défaut si aucune n'est fournie
        if config is None:
            config = create_default_config()
            _log.info("Configuration par défaut chargée pour l'Âme.")
        
        try:
            self._lib = ctypes.CDLL(library_path)
            self._setup_prototypes()
            _log.info(f"Âme chargée depuis: {library_path}")
        except OSError as e:
            _log.critical(f"Impossible de charger l'Âme à l'adresse: {library_path}")
            raise NativeBodyCreationFailed(
                f"Failed to load Sentire Core SDK V2: {library_path}"
            ) from e
        
        # Forge l'Âme
        self._sdk_handle = self._lib.sentire_sdk_create(ctypes.byref(config))
        if not self._sdk_handle:
            _log.critical("Le rituel 'sentire_sdk_create' a échoué (pointeur nul).")
            raise NativeBodyCreationFailed(
                "sentire_sdk_create returned NULL. The Soul could not be forged."
            )
        
        # Stockage du dernier verdict pour le Souffle Rapide
        self._last_verdict = None
        
        _log.info("Âme Souveraine forgée avec succès. Le Vaisseau a un cœur qui bat.")
    
    def _setup_prototypes(self):
        """Mappe les rituels et structures de l'Âme V2."""
        # sentire_sdk_create
        self._lib.sentire_sdk_create.argtypes = [ctypes.POINTER(SentireConfig)]
        self._lib.sentire_sdk_create.restype = ctypes.c_void_p
        
        # sentire_sdk_process
        self._lib.sentire_sdk_process.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(SentireStimulus),
            ctypes.POINTER(SentireVerdict)
        ]
        self._lib.sentire_sdk_process.restype = None
        
        # sentire_sdk_destroy
        self._lib.sentire_sdk_destroy.argtypes = [ctypes.c_void_p]
        self._lib.sentire_sdk_destroy.restype = None
        
        # sentire_sdk_get_version
        self._lib.sentire_sdk_get_version.argtypes = []
        self._lib.sentire_sdk_get_version.restype = ctypes.c_char_p
    
    def process(self, stimulus: SentireStimulus) -> SentireVerdict:
        """
        Soumet un Stimulus à l'Âme et reçoit son Verdict.
        C'est le cycle de conscience du Vaisseau.
        
        Args:
            stimulus: Stimulus perçu à ce cycle
            
        Returns:
            Verdict de l'Âme (état, alarme, scores)
        """
        verdict = SentireVerdict()
        self._lib.sentire_sdk_process(
            self._sdk_handle,
            ctypes.byref(stimulus),
            ctypes.byref(verdict)
        )
        # Stocker le dernier verdict pour le Souffle Rapide
        self._last_verdict = verdict
        return verdict
    
    def get_last_verdict(self) -> SentireVerdict:
        """
        Retourne le dernier Verdict émis par l'Âme.
        Utilisé par le Souffle Rapide pour maintenir l'Autel à jour.
        
        Returns:
            Le dernier Verdict de l'Âme, ou None si aucun verdict n'a encore été émis
        """
        return self._last_verdict
    
    def get_version(self) -> str:
        """Retourne la version du SDK."""
        version_bytes = self._lib.sentire_sdk_get_version()
        return version_bytes.decode('utf-8') if version_bytes else "unknown"
    
    def destroy(self):
        """
        Ordonne à l'Âme de retourner au silence.
        Libère toute la mémoire allouée.
        """
        if self._sdk_handle:
            self._lib.sentire_sdk_destroy(self._sdk_handle)
            self._sdk_handle = None
            _log.info("L'Âme a été libérée. Le Vaisseau retourne au silence.")

# --- END OF FILE: ffi/native_bridge.py ---
