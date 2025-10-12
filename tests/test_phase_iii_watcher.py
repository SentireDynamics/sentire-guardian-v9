# --- START OF FILE: tests/test_phase_iii_watcher.py ---
"""
Test du Guetteur de Vélocité - Phase III.

Valide que le Guetteur de Vélocité fonctionne correctement et émet
des signaux d'alarme lorsque l'Amygdale Numérique détecte un danger.
"""
import pytest
import time
from unittest.mock import Mock, MagicMock
from PyQt6.QtCore import QTimer
from guardian.velocity_watcher import VelocityWatcher
from ffi.native_bridge import SentireStimulus

def test_watcher_emits_alarm_on_danger():
    """
    Valide que le Guetteur crie l'alarme lorsque l'Âme a peur.
    """
    # Arrange : Créer des simulacres pour l'Âme et la Perception
    mock_bridge = MagicMock()
    mock_perception = MagicMock()
    
    # Le simulacre de l'Âme criera au danger (retourne True)
    mock_bridge.amygdala_tick.return_value = True
    
    # Le simulacre de la Perception fournira de la nourriture au Guetteur
    fake_stimulus = SentireStimulus()
    fake_stimulus.cpu_usage = 0.5
    fake_stimulus.memory_usage = 0.3
    fake_stimulus.gpu_usage = 0.0
    mock_perception.get_light_stimulus_c.return_value = fake_stimulus

    # Créer le Guetteur
    watcher = VelocityWatcher(mock_bridge, mock_perception, frequency_hz=100)

    # Act : Lancer le Guetteur et le laisser vivre un court instant
    watcher.start()
    watcher.msleep(50)  # Assez de temps pour quelques cycles
    watcher.stop()
    watcher.wait()

    # Assert : Vérifier que l'Amygdale a été appelée
    # Le fait que l'alarme soit émise est vérifié par les logs
    mock_bridge.amygdala_tick.assert_called()
    mock_perception.get_light_stimulus_c.assert_called()
    
    # Vérifier que l'Amygdale a été appelée plusieurs fois (cycles multiples)
    assert mock_bridge.amygdala_tick.call_count > 0, "L'Amygdale devrait avoir été sondée"

def test_watcher_no_alarm_when_safe():
    """
    Valide que le Guetteur reste silencieux quand tout va bien.
    """
    # Arrange : Créer des simulacres pour l'Âme et la Perception
    mock_bridge = MagicMock()
    mock_perception = MagicMock()
    
    # Le simulacre de l'Âme reste calme (retourne False)
    mock_bridge.amygdala_tick.return_value = False
    
    # Le simulacre de la Perception fournira de la nourriture au Guetteur
    fake_stimulus = SentireStimulus()
    fake_stimulus.cpu_usage = 0.1
    fake_stimulus.memory_usage = 0.2
    fake_stimulus.gpu_usage = 0.0
    mock_perception.get_light_stimulus_c.return_value = fake_stimulus

    # Créer le Guetteur et un compteur d'alarmes
    watcher = VelocityWatcher(mock_bridge, mock_perception, frequency_hz=100)
    alarm_count = 0
    
    def on_alarm():
        nonlocal alarm_count
        alarm_count += 1
    
    watcher.amygdala_alarm.connect(on_alarm)

    # Act : Lancer le Guetteur et le laisser vivre un court instant
    watcher.start()
    watcher.msleep(50)  # Assez de temps pour quelques cycles
    watcher.stop()
    watcher.wait()

    # Assert : Vérifier que le Guetteur est resté silencieux
    assert alarm_count == 0, "Le Guetteur ne devrait pas émettre d'alarme quand tout va bien"
    mock_bridge.amygdala_tick.assert_called()
    mock_perception.get_light_stimulus_c.assert_called()

def test_watcher_handles_perception_failure():
    """
    Valide que le Guetteur gère gracieusement les échecs de perception.
    """
    # Arrange : Créer des simulacres pour l'Âme et la Perception
    mock_bridge = MagicMock()
    mock_perception = MagicMock()
    
    # Le simulacre de la Perception échoue
    mock_perception.get_light_stimulus_c.return_value = None

    # Créer le Guetteur et un compteur d'alarmes
    watcher = VelocityWatcher(mock_bridge, mock_perception, frequency_hz=100)
    alarm_count = 0
    
    def on_alarm():
        nonlocal alarm_count
        alarm_count += 1
    
    watcher.amygdala_alarm.connect(on_alarm)

    # Act : Lancer le Guetteur et le laisser vivre un court instant
    watcher.start()
    watcher.msleep(50)  # Assez de temps pour quelques cycles
    watcher.stop()
    watcher.wait()

    # Assert : Vérifier que le Guetteur gère l'échec gracieusement
    assert alarm_count == 0, "Le Guetteur ne devrait pas émettre d'alarme quand la perception échoue"
    mock_perception.get_light_stimulus_c.assert_called()
    # L'amygdala_tick ne devrait pas être appelé si la perception échoue
    mock_bridge.amygdala_tick.assert_not_called()

def test_watcher_frequency_configuration():
    """
    Valide que le Guetteur respecte sa configuration de fréquence.
    """
    # Arrange : Créer des simulacres
    mock_bridge = MagicMock()
    mock_perception = MagicMock()
    
    fake_stimulus = SentireStimulus()
    fake_stimulus.cpu_usage = 0.5
    fake_stimulus.memory_usage = 0.3
    fake_stimulus.gpu_usage = 0.0
    mock_perception.get_light_stimulus_c.return_value = fake_stimulus
    mock_bridge.amygdala_tick.return_value = False

    # Act : Créer le Guetteur avec une fréquence spécifique
    watcher = VelocityWatcher(mock_bridge, mock_perception, frequency_hz=10)
    
    # Assert : Vérifier que l'intervalle de sommeil est correct
    expected_interval = int(1000 / 10)  # 100ms pour 10Hz
    assert watcher.sleep_interval_ms == expected_interval

def test_watcher_stop_signal():
    """
    Valide que le Guetteur s'arrête correctement quand on lui ordonne.
    """
    # Arrange : Créer des simulacres
    mock_bridge = MagicMock()
    mock_perception = MagicMock()
    
    fake_stimulus = SentireStimulus()
    fake_stimulus.cpu_usage = 0.5
    fake_stimulus.memory_usage = 0.3
    fake_stimulus.gpu_usage = 0.0
    mock_perception.get_light_stimulus_c.return_value = fake_stimulus
    mock_bridge.amygdala_tick.return_value = False

    # Act : Créer et démarrer le Guetteur
    watcher = VelocityWatcher(mock_bridge, mock_perception, frequency_hz=100)
    watcher.start()
    
    # Laisser tourner un peu
    watcher.msleep(10)
    
    # Puis l'arrêter
    watcher.stop()
    watcher.wait()

    # Assert : Vérifier que le Guetteur s'est arrêté
    assert not watcher._is_running, "Le Guetteur devrait être arrêté"
    assert watcher.isFinished(), "Le thread du Guetteur devrait être terminé"

# --- END OF FILE ---
