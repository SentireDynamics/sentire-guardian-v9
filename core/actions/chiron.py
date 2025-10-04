# --- START OF FILE: core/chiron.py ---
"""
Le Sanctuaire de Chiron - Le Centaure Exécuteur.

Le "Pourquoi": Ce module est le bras armé du Vaisseau. Il encapsule toutes les
interactions directes avec le système d'exploitation Windows via l'API Win32,
en utilisant `ctypes`. En centralisant ces appels de bas niveau, on isole le reste
de l'application des complexités de la plateforme, et on crée un point de contrôle
unique pour l'exécution des actions souveraines.
"""
import ctypes
import logging
from ctypes import wintypes

_log = logging.getLogger(__name__)

# Définition des prototypes de fonctions de l'API Windows
user32 = ctypes.windll.user32
MessageBoxW = user32.MessageBoxW
MessageBoxW.argtypes = (wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT)
MessageBoxW.restype = ctypes.c_int

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = wintypes.HWND

GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = (wintypes.HWND, wintypes.LPWSTR, ctypes.c_int)
GetWindowTextW.restype = ctypes.c_int

class Chiron:
    """
    La classe Chiron fournit des méthodes pour interagir avec l'OS Windows.
    """
    def get_foreground_window_title(self) -> str:
        """
        Récupère le titre de la fenêtre actuellement au premier plan.

        Le "Pourquoi": Connaître le contexte de l'utilisateur est un stimulus
        essentiel pour que l'Oracle puisse prendre des décisions pertinentes.
        """
        hwnd = GetForegroundWindow()
        if not hwnd:
            return "No Active Window"

        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return "Unnamed Window"

        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowTextW(hwnd, buff, length + 1)
        return buff.value

    def show_sovereign_message(self, title: str, message: str):
        """
        Affiche une boîte de message native Windows.

        Le "Pourquoi": C'est un moyen direct et non-intrusif de communiquer une
        information importante ou une alerte à l'utilisateur, en utilisant une
        interface familière et intégrée au système.
        """
        _log.info(f"Affichage du message souverain: '{title}' - '{message}'")
        MB_OK = 0x00000000
        MB_ICONINFORMATION = 0x00000040
        MessageBoxW(None, message, title, MB_OK | MB_ICONINFORMATION)

    def execute_action(self, action):
        """
        Exécute une action en fonction de son ID.
        C'est le dispatcher principal pour les commandes de Chiron.
        """
        _log.info(f"Chiron exécute l'action: {action.id} avec les paramètres {action.parameters}")
        if action.id == "SHOW_MESSAGE":
            title = action.parameters.get("title", "Message du Vaisseau Guardian")
            message = action.parameters.get("message", "Une action a été effectuée.")
            self.show_sovereign_message(title, message)
        elif action.id == "LOG_ONLY":
            _log.info(f"Action de journalisation seule: {action.description}")
        else:
            _log.warning(f"Action inconnue ou non implémentée demandée à Chiron: {action.id}")
# --- END OF FILE: core/chiron.py ---