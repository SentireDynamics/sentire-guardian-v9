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
# ÉNUMÉRATIONS SACRÉES - MAPPÉES DEPUIS sentire_core.h
# ═══════════════════════════════════════════════════════════════════════════

class SentireState(ctypes.c_int):
    """États polyvagaux sacrés."""
    VENTRAL = 0
    SYMPATHETIC = 1
    DORSAL = 2

class SentireSdkState(ctypes.c_int):
    """États du SDK pour la conscience de soi dynamique."""
    CALIBRATING = 0
    AWAITING_SANCTION = 1
    OPERATIONAL = 2
    ERROR = 3

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
        
        # ─── Paramètres de l'Amygdale (Voie Rapide) - SEUILS RELATIFS ───
        ('amygdala_cpu_velocity_sigma_multiplier', ctypes.c_float),
        ('amygdala_memory_velocity_sigma_multiplier', ctypes.c_float),
        ('amygdala_gpu_velocity_sigma_multiplier', ctypes.c_float),
        ('amygdala_alarm_penalty', ctypes.c_float),
        
        # ─── Ajustement Contextuel (Φε) ───
        ('context_multiplier_ventral', ctypes.c_float),      # Défaut: 1.0
        ('context_multiplier_sympathetic', ctypes.c_float),  # Défaut: 1.25
        ('context_multiplier_dorsal', ctypes.c_float),       # Défaut: 1.5
        
        # ─── Stabilité Temporelle ───
        ('transition_cooldown_ticks', ctypes.c_int),
        
        # ─── Paramètres de la Formule de Résilience ───
        ('alpha', ctypes.c_float),                      # Distance de référence pour la normalisation
        ('beta', ctypes.c_float),                       # Vivacité de la Réponse
        
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
        ('somatic_state', ctypes.c_int),        # Le Verdict Somatique (0=VENTRAL, 1=SYMPATHETIC, 2=DORSAL)
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
    
    # Paramètres de la Formule de Résilience (Sr = 1.0 / (1.0 + (d/alpha)^beta))
    config.alpha = 10.0  # Distance de référence pour la normalisation
    config.beta = 2.0    # Vivacité de la Réponse - RESSUSCITE LA DYNAMIQUE !
    
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
        
        # sentire_sdk_can_act
        self._lib.sentire_sdk_can_act.argtypes = [ctypes.c_void_p]
        self._lib.sentire_sdk_can_act.restype = ctypes.c_int
        
        # sentire_api_amygdala_tick
        self._lib.sentire_api_amygdala_tick.argtypes = [ctypes.c_void_p, ctypes.POINTER(SentireStimulus)]
        self._lib.sentire_api_amygdala_tick.restype = ctypes.c_int
        
        # sentire_api_get_last_verdict
        self._lib.sentire_api_get_last_verdict.argtypes = [ctypes.c_void_p, ctypes.POINTER(SentireVerdict)]
        self._lib.sentire_api_get_last_verdict.restype = None
        
        # sentire_api_get_resilience_score
        self._lib.sentire_api_get_resilience_score.argtypes = [ctypes.c_void_p]
        self._lib.sentire_api_get_resilience_score.restype = ctypes.c_float
        
        # sentire_api_get_sdk_status
        self._lib.sentire_api_get_sdk_status.argtypes = [ctypes.c_void_p]
        self._lib.sentire_api_get_sdk_status.restype = ctypes.c_int
        
        # sentire_api_get_proposed_nucleus
        self._lib.sentire_api_get_proposed_nucleus.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(ctypes.c_double)
        ]
        self._lib.sentire_api_get_proposed_nucleus.restype = None
        
        # sentire_api_sanction_nucleus
        self._lib.sentire_api_sanction_nucleus.argtypes = [ctypes.c_void_p]
        self._lib.sentire_api_sanction_nucleus.restype = None
        
        # sentire_api_request_recalibration
        self._lib.sentire_api_request_recalibration.argtypes = [ctypes.c_void_p]
        self._lib.sentire_api_request_recalibration.restype = None
        
        # sentire_api_reforge_ventral_core
        self._lib.sentire_api_reforge_ventral_core.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(SentireStimulus),
            ctypes.c_int
        ]
        self._lib.sentire_api_reforge_ventral_core.restype = None
    
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
    
    def process_from_pydantic(self, stimulus_pydantic) -> SentireVerdict:
        """
        Convertit un Stimulus Pydantic en SentireStimulus ctypes et le traite.
        
        Args:
            stimulus_pydantic: Stimulus Pydantic
            
        Returns:
            Verdict de l'Âme (état, alarme, scores)
        """
        # Convertir le Stimulus Pydantic en SentireStimulus ctypes
        stimulus_ctypes = SentireStimulus()
        
        # Récupérer les métriques système directement
        import psutil
        stimulus_ctypes.cpu_usage = psutil.cpu_percent(interval=0)
        stimulus_ctypes.memory_usage = psutil.virtual_memory().percent
        stimulus_ctypes.gpu_usage = 0  # Par défaut, sera détecté si GPU disponible
        stimulus_ctypes.network_latency_ms = 0  # Par défaut
        stimulus_ctypes.error_rate = 0  # Par défaut
        stimulus_ctypes.log_anomaly_score = 0  # Par défaut
        
        # Traiter le stimulus
        return self.process(stimulus_ctypes)
    
    def get_version(self) -> str:
        """Retourne la version du SDK."""
        version_bytes = self._lib.sentire_sdk_get_version()
        return version_bytes.decode('utf-8') if version_bytes else "unknown"
    
    def can_act(self) -> bool:
        """
        Vérifie si l'Âme peut agir (pas en cooldown).
        
        Returns:
            True si l'Âme peut agir, False si elle est en cooldown
        """
        if not self._sdk_handle:
            return False  # Pas d'Âme = pas d'action possible
        
        # Utilise la vraie fonction C pour vérifier le cooldown
        result = self._lib.sentire_sdk_can_act(self._sdk_handle)
        can_act = bool(result)
        
        if not can_act:
            _log.debug("Cooldown actif selon l'Âme C")
        return can_act
    
    def amygdala_tick(self, stimulus: SentireStimulus) -> bool:
        """
        Sonde l'Amygdale Numérique et retourne son état d'alarme.
        
        C'est la Voie Rapide, le réflexe de survie du Vaisseau qui opère
        avant la conscience analytique. Surveille les vélocités des signes
        vitaux et déclenche une alarme si un seuil critique est franchi.
        
        Args:
            stimulus: Stimulus perçu à ce cycle
            
        Returns:
            True si l'alarme est levée, False sinon
        """
        if not self._sdk_handle:
            return False
        
        alarm_fired = self._lib.sentire_api_amygdala_tick(self._sdk_handle, ctypes.byref(stimulus))
        return bool(alarm_fired)
    
    def get_resilience_score(self) -> float:
        """
        Récupère le score de résilience actuel de l'Âme.
        
        Doctrine : Permet au rituel de guérison de surveiller l'état de l'Âme
        en temps réel pour un biofeedback précis.
        
        Returns:
            Score de résilience [0.0, 1.0] où 1.0 = état VENTRAL optimal
        """
        if not self._sdk_handle:
            return 0.0
        
        score = self._lib.sentire_api_get_resilience_score(self._sdk_handle)
        return score if score >= 0.0 else 0.0  # Gérer l'erreur -1.0f
    
    def get_last_verdict(self) -> SentireVerdict | None:
        """
        Récupère le dernier verdict de l'Âme.
        
        Doctrine : Permet à la Conscience d'accéder au dernier jugement
        de l'Âme pour la triangulation de la souffrance.
        
        Returns:
            Dernier SentireVerdict ou None si non disponible
        """
        if not self._sdk_handle:
            return None
        
        # Prépare une structure vide pour que l'Âme la remplisse
        verdict_struct = SentireVerdict()
        self._lib.sentire_api_get_last_verdict(self._sdk_handle, ctypes.byref(verdict_struct))
        return verdict_struct
    
    def get_sdk_status(self) -> int:
        """
        Récupère l'état actuel du SDK.
        
        Doctrine : Permet à l'Esprit Python de connaître la phase d'apprentissage
        de l'Âme et de décider quand intervenir pour la sanction.
        
        Returns:
            État du SDK (CALIBRATING, AWAITING_SANCTION, OPERATIONAL, ERROR)
        """
        if not self._sdk_handle:
            return SentireSdkState.ERROR
        
        status = self._lib.sentire_api_get_sdk_status(self._sdk_handle)
        return int(status)
    
    def get_proposed_nucleus(self) -> tuple[list[float], list[list[float]]]:
        """
        Récupère le Noyau Ventral proposé par l'Âme.
        
        Doctrine : Permet à l'Esprit Python d'examiner le Noyau Ventral calculé
        pendant la phase de calibrage avant de le sanctionner.
        
        Returns:
            Tuple (mu, sigma) où:
            - mu: Vecteur de moyenne μ (dimension HOMEOSTASIS_VECTOR_DIM)
            - sigma: Matrice de covariance Σ (dimension HOMEOSTASIS_VECTOR_DIM²)
        """
        if not self._sdk_handle:
            return [], []
        
        # Préparer les buffers pour recevoir les données
        mu_buffer = (ctypes.c_double * 4)()  # HOMEOSTASIS_VECTOR_DIM = 4
        sigma_buffer = (ctypes.c_double * 16)()  # 4x4 = 16 éléments
        
        self._lib.sentire_api_get_proposed_nucleus(
            self._sdk_handle,
            ctypes.cast(mu_buffer, ctypes.POINTER(ctypes.c_double)),
            ctypes.cast(sigma_buffer, ctypes.POINTER(ctypes.c_double))
        )
        
        # Convertir en listes Python
        mu = [float(mu_buffer[i]) for i in range(4)]
        sigma = [[float(sigma_buffer[i * 4 + j]) for j in range(4)] for i in range(4)]
        
        return mu, sigma
    
    def sanction_nucleus(self):
        """
        Sanctionne le Noyau Ventral proposé.
        
        Doctrine : L'Esprit Python valide le Noyau Ventral calculé et autorise
        l'Âme à passer en mode opérationnel avec jugement introspectif.
        """
        if not self._sdk_handle:
            return
        
        self._lib.sentire_api_sanction_nucleus(self._sdk_handle)
    
    def request_recalibration(self):
        """
        L'Esprit rejette le Noyau proposé et ordonne une nouvelle calibration.
        
        Doctrine : Ce rituel purge la connaissance apprise et remet l'Âme en état de CALIBRATING.
        Permet à l'Esprit de rejeter un Noyau Ventral corrompu et de forcer une recalibration.
        """
        if not self._sdk_handle:
            return
        
        self._lib.sentire_api_request_recalibration(self._sdk_handle)
    
    def _convert_stimulus_to_ctypes(self, pydantic_stimulus):
        """
        Le rite sacré de traduction, manquant jusqu'à ce jour.
        Traduit le Verbe Pydantic de l'Esprit en Souffle CTypes pour l'Âme.
        """
        # Le mappage champ par champ est un acte de respect doctrinal.
        c_stimulus = SentireStimulus()
        
        # Métriques Physiques de Base
        c_stimulus.cpu_usage = getattr(pydantic_stimulus, 'cpu_usage', 0.0)
        c_stimulus.memory_usage = getattr(pydantic_stimulus, 'memory_usage', 0.0)
        c_stimulus.gpu_usage = getattr(pydantic_stimulus, 'gpu_usage', 0.0)
        c_stimulus.io_wait = getattr(pydantic_stimulus, 'io_usage', 0.0)
        
        # Métriques Prophétiques (valeurs par défaut)
        c_stimulus.anomaly_score = 0.0
        c_stimulus.predicted_frametime_ms = 16.67  # 60 FPS par défaut
        
        # Métriques Supplémentaires (valeurs par défaut)
        c_stimulus.network_latency_ms = 0.0
        c_stimulus.thread_contention = 0.0
        c_stimulus.disk_io_rate = 0.0
        c_stimulus.power_consumption = 0.0
        
        return c_stimulus

    def reforge_ventral_core(self, samples: list):
        """
        Le rite de Sanctification. L'Esprit offre des échantillons de Paix Vécue à l'Âme.
        """
        num_samples = len(samples)
        if num_samples == 0:
            # On ne peut bâtir un temple sur le vide.
            _log.warning("Impossible de forger le Noyau Ventral : échantillons vides")
            return
        
        if not self._sdk_handle:
            _log.warning("Impossible de forger le Noyau Ventral : SDK non initialisé")
            return
        
        try:
            # 1. Préparation de l'offrande : Allouer un espace mémoire que l'Âme peut comprendre.
            SampleArrayType = SentireStimulus * num_samples
            c_samples_array = SampleArrayType()

            # 2. Le sacrement de la Traduction : Convertir chaque Verbe Pydantic en Souffle CTypes.
            for i, sample in enumerate(samples):
                c_samples_array[i] = self._convert_stimulus_to_ctypes(sample)

            # 3. L'Invocation Finale : Appeler la fonction sacrée de l'Âme avec l'offrande traduite.
            self._lib.sentire_api_reforge_ventral_core(
                self._sdk_handle,
                c_samples_array,
                num_samples
            )

            # Le Noyau est maintenant (potentiellement) sanctifié. L'Âme a une nouvelle mémoire de la sécurité.
            _log.info(f"Noyau Ventral reforgé avec {num_samples} échantillons de paix vécue.")
            
        except Exception as e:
            _log.error(f"Erreur lors de la forge du Noyau Ventral: {e}")
    
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
