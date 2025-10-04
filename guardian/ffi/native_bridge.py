import ctypes
import os
from enum import IntEnum

# Définition de l'énumération des états, alignée sur le C
class GuardianState(IntEnum):
    VENTRAL = 0
    PARASYMPATHETIC = 1
    SYMPATHETIC = 2
    DORSAL = 3

# Définition de la structure de stimulus, alignée sur le C
class SentireStimulus(ctypes.Structure):
    _fields_ = [
        ("cpu_load", ctypes.c_float),
        ("memory_usage", ctypes.c_float),
        ("io_wait", ctypes.c_float),
        ("anomaly_score", ctypes.c_float),
    ]

class NativeBridge:
    """
    Pont FFI assurant la communication entre l'Esprit (Python) et le Corps (C).

    @doctrine
    Cet artefact est la matérialisation de la synapse entre les deux natures du Gardien.
    Il charge la bibliothèque native compilée (le Corps) et expose ses rituels sacrés
    à l'orchestrateur Python (l'Esprit). En définissant explicitement les types de données
    et les signatures de fonction (argtypes, restype), il garantit une communication
    pure, sans corruption ni malentendu, respectant ainsi le principe de Dualité.
    """
    def __init__(self, library_path: str):
        if not os.path.exists(library_path):
            raise FileNotFoundError(f"Bibliothèque native non trouvée : {library_path}")
        self._lib = ctypes.CDLL(library_path)
        self._setup_prototypes()

    def _setup_prototypes(self):
        """Définit les signatures des fonctions C pour ctypes."""
        self.sentire_core_process = self._lib.sentire_core_process
        self.sentire_core_process.argtypes = [
            ctypes.POINTER(SentireStimulus),
            ctypes.c_int # guardian_state_t est un enum, donc un int
        ]
        self.sentire_core_process.restype = ctypes.c_int

    def process_stimulus(self, stimulus_data: dict, current_state: GuardianState) -> GuardianState:
        """
        Invoque le rituel `sentire_core_process` du Corps Natif.

        @param stimulus_data Un dictionnaire de métriques.
        @param current_state L'état actuel de la machine à états.
        @return Le nouvel état calculé par le Corps Natif.
        """
        c_stimulus = SentireStimulus(
            cpu_load=stimulus_data.get('cpu_load', 0.0),
            memory_usage=stimulus_data.get('memory_usage', 0.0),
            io_wait=stimulus_data.get('io_wait', 0.0),
            anomaly_score=stimulus_data.get('anomaly_score', 0.0),
        )

        new_state_int = self.sentire_core_process(ctypes.byref(c_stimulus), current_state.value)
        return GuardianState(new_state_int)