# --- START OF FILE: tests/test_chiron_windows.py ---
"""
Validation de Chiron - Le bras du Vaisseau sur Windows.

Le "Pourquoi": Ces tests valident que Chiron formule correctement ses appels à l'API
Windows. En utilisant des "mocks", nous simulons les fonctions de l'API Win32 pour
vérifier que Chiron les appelle avec les bons arguments, sans réellement affecter
le système hôte. C'est un test de pureté de l'intention d'action.
"""
import pytest
import ctypes
from core.actions.chiron import Chiron

def test_chiron_show_sovereign_message(mocker):
    """
    Vérifie que Chiron appelle bien MessageBoxW avec les bons paramètres.
    """
    # Arrange: Simuler la fonction de l'API Windows
    mock_messagebox = mocker.patch('ctypes.windll.user32.MessageBoxW')
    chiron = Chiron()
    title = "Test Titre"
    message = "Test Message"

    # Act: Appeler la méthode de Chiron
    chiron.show_sovereign_message(title, message)

    # Assert: Vérifier que la fonction simulée a été appelée correctement
    mock_messagebox.assert_called_once()
    args, _ = mock_messagebox.call_args
    assert args[1] == message  # LPCWSTR (message)
    assert args[2] == title    # LPCWSTR (title)

def test_chiron_get_foreground_window_title(mocker):
    """
    Vérifie que Chiron interroge correctement la fenêtre de premier plan.
    """
    # Arrange: Simuler les fonctions GetForegroundWindow et GetWindowTextW
    mock_get_hwnd = mocker.patch('ctypes.windll.user32.GetForegroundWindow', return_value=12345)
    mock_get_text_len = mocker.patch('ctypes.windll.user32.GetWindowTextLengthW', return_value=11)

    # Simuler le remplissage du buffer par GetWindowTextW
    def fill_buffer(*args):
        buffer = args[1]
        buffer.value = "Test Window"
        return 11
    mock_get_text = mocker.patch('ctypes.windll.user32.GetWindowTextW', side_effect=fill_buffer)

    chiron = Chiron()

    # Act
    title = chiron.get_foreground_window_title()

    # Assert
    assert title == "Test Window"
    mock_get_hwnd.assert_called_once()
    mock_get_text_len.assert_called_once_with(12345)
    mock_get_text.assert_called_once()
# --- END OF FILE: tests/test_chiron_windows.py ---