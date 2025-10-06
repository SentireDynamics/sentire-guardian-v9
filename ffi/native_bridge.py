# --- START OF FILE: ffi/native_bridge.py ---
"""
La Synapse FFI - Le Pont entre l'Esprit et le Corps.

Le "Pourquoi": Ce module est le traducteur sacré entre le monde Python de haut niveau
(l'Esprit) et le monde C de bas niveau (le Corps Natif). Il utilise `ctypes` pour
charger la DLL `sentire_core.dll` et exposer ses fonctions de manière sécurisée et
pythonique. Il garantit que les types de données sont corrects et gère le cycle
de vie (création/destruction) des ressources natives, prévenant ainsi les fuites
de mémoire et les crashs.
"""
import ctypes
import logging
from core.exceptions import NativeBodyCreationFailed

_log = logging.getLogger(__name__)

class NativeBridge:
    """
    Interface pythonique pour interagir avec la librairie native `sentire_core`.
    """
    def __init__(self, library_path: str, cooldown_seconds: int):
        """
        Charge la librairie native et initialise l'état du Guardian.

        Args:
            library_path (str): Chemin vers le fichier `sentire_core.dll`.
            cooldown_seconds (int): Temps de recharge entre les actions.

        Raises:
            NativeBodyCreationFailed: Si la librairie ne peut être chargée ou si
                                      l'initialisation de l'état échoue.
        """
        try:
            self._lib = ctypes.CDLL(library_path)
            self._setup_function_prototypes()
            _log.info("Corps Natif (sentire_core.dll) chargé avec succès.")
        except OSError as e:
            _log.critical(f"Impossible de charger le Corps Natif à l'adresse : {library_path}. Erreur: {e}")
            raise NativeBodyCreationFailed(f"Failed to load native library: {library_path}") from e

        self._state_ptr = self._lib.sentire_api_create(cooldown_seconds)
        if not self._state_ptr:
            _log.critical("Le rituel de création du Corps Natif a échoué (pointeur nul retourné).")
            raise NativeBodyCreationFailed("sentire_api_create returned a NULL pointer.")
        _log.info("État du Corps Natif initialisé avec succès.")

    def _setup_function_prototypes(self):
        """Définit les types d'arguments et de retour pour les fonctions C."""
        self._lib.sentire_api_create.argtypes = [ctypes.c_int]
        self._lib.sentire_api_create.restype = ctypes.c_void_p

        self._lib.sentire_api_destroy.argtypes = [ctypes.c_void_p]
        self._lib.sentire_api_destroy.restype = None

        self._lib.sentire_api_can_act.argtypes = [ctypes.c_void_p]
        self._lib.sentire_api_can_act.restype = ctypes.c_int

        self._lib.sentire_api_record_action.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self._lib.sentire_api_record_action.restype = None

    def can_act(self) -> bool:
        """
        Vérifie si le Vaisseau est autorisé à agir (respect du cooldown).
        """
        return bool(self._lib.sentire_api_can_act(self._state_ptr))

    def record_action(self, description: str):
        """
        Enregistre une action dans le journal natif et réinitialise le cooldown.
        """
        self._lib.sentire_api_record_action(self._state_ptr, description.encode('utf-8'))
        _log.debug(f"Action enregistrée dans le journal natif: '{description}'")

    def destroy(self):
        """
        Libère les ressources du Corps Natif. Essentiel à appeler à la fin.
        """
        if self._state_ptr:
            self._lib.sentire_api_destroy(self._state_ptr)
            self._state_ptr = None
            _log.info("Les ressources du Corps Natif ont été libérées.")
# --- END OF FILE: ffi/native_bridge.py ---