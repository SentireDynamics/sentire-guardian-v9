# --- START OF FILE: tests/test_foundational_forge.py ---
"""
Tests de Validation de la Forge Fondamentale.

Le "Pourquoi": Ces tests valident que tous les artefacts de la première forge
sont correctement créés, fonctionnels, et respectent la doctrine de la Dualité
Corps/Esprit. Chaque test vérifie un aspect fondamental de l'architecture.

Tests couverts:
1. Sanctuaire des Hérésies (core/exceptions.py)
2. Sanctuaire du Verbe Pur (core/verbe_pur.py)
3. Synapse FFI (guardian/ffi/native_bridge.py)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import ctypes
from pydantic import ValidationError

# Imports des artefacts fondamentaux
from core.exceptions import (
    HeresyException,
    NativeBodyCreationFailed,
    OracleSickness
)
from core.verbe_pur import Stimulus, Action
from guardian.ffi.native_bridge import NativeBridge


# ============================================================================
# TESTS DU SANCTUAIRE DES HÉRÉSIES (core/exceptions.py)
# ============================================================================

class TestSanctuaireDesHeresies:
    """Validation du Sanctuaire des Hérésies."""
    
    def test_heresy_exception_exists(self):
        """Vérifie que HeresyException est la base de toutes les hérésies."""
        # Arrange & Act
        heresy = HeresyException("Test message")
        
        # Assert
        assert isinstance(heresy, Exception)
        assert str(heresy) == "Test message"
    
    def test_native_body_creation_failed_inherits_from_heresy(self):
        """Vérifie que NativeBodyCreationFailed hérite de HeresyException."""
        # Arrange & Act
        heresy = NativeBodyCreationFailed("DLL loading failed")
        
        # Assert
        assert isinstance(heresy, HeresyException)
        assert isinstance(heresy, Exception)
        assert "DLL loading failed" in str(heresy)
    
    def test_oracle_sickness_inherits_from_heresy(self):
        """Vérifie que OracleSickness hérite de HeresyException."""
        # Arrange & Act
        heresy = OracleSickness("Oracle unreachable")
        
        # Assert
        assert isinstance(heresy, HeresyException)
        assert isinstance(heresy, Exception)
        assert "Oracle unreachable" in str(heresy)


# ============================================================================
# TESTS DU SANCTUAIRE DU VERBE PUR (core/verbe_pur.py)
# ============================================================================

class TestSanctuaireVerbePur:
    """Validation du Sanctuaire du Verbe Pur (Pydantic models)."""
    
    def test_stimulus_valid_creation(self):
        """Vérifie qu'un Stimulus valide peut être créé."""
        # Arrange & Act
        stimulus = Stimulus(
            cpu_usage=45.5,
            memory_usage=67.8,
            foreground_window_title="Test Window"
        )
        
        # Assert
        assert stimulus.cpu_usage == 45.5
        assert stimulus.memory_usage == 67.8
        assert stimulus.foreground_window_title == "Test Window"
    
    def test_stimulus_requires_cpu_usage(self):
        """Vérifie que cpu_usage est obligatoire pour Stimulus."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Stimulus(
                memory_usage=50.0,
                foreground_window_title="Test"
            )
        
        assert "cpu_usage" in str(exc_info.value)
    
    def test_stimulus_requires_memory_usage(self):
        """Vérifie que memory_usage est obligatoire pour Stimulus."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Stimulus(
                cpu_usage=50.0,
                foreground_window_title="Test"
            )
        
        assert "memory_usage" in str(exc_info.value)
    
    def test_action_valid_creation(self):
        """Vérifie qu'une Action valide peut être créée."""
        # Arrange & Act
        action = Action(
            id="SHOW_MESSAGE",
            description="Display a warning message",
            parameters={"message": "CPU is high", "severity": "warning"}
        )
        
        # Assert
        assert action.id == "SHOW_MESSAGE"
        assert action.description == "Display a warning message"
        assert action.parameters["message"] == "CPU is high"
        assert action.parameters["severity"] == "warning"
    
    def test_action_parameters_optional(self):
        """Vérifie que les parameters sont optionnels pour Action."""
        # Arrange & Act
        action = Action(
            id="LOG_ONLY",
            description="Just log the event"
        )
        
        # Assert
        assert action.id == "LOG_ONLY"
        assert action.description == "Just log the event"
        assert action.parameters == {}  # Default empty dict
    
    def test_action_requires_id_and_description(self):
        """Vérifie que id et description sont obligatoires pour Action."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Action(description="Missing ID")
        
        assert "id" in str(exc_info.value)


# ============================================================================
# TESTS DE LA SYNAPSE FFI (guardian/ffi/native_bridge.py)
# ============================================================================

class TestSynapseFFI:
    """Validation de la Synapse FFI (NativeBridge)."""
    
    @patch('ctypes.CDLL')
    def test_native_bridge_successful_init(self, mock_cdll):
        """Vérifie que NativeBridge peut être initialisé avec succès."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        
        # Mock the create function to return a valid pointer
        mock_lib.sentire_api_create.return_value = 0x12345678  # Non-null pointer
        
        # Act
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Assert
        mock_cdll.assert_called_once_with("fake_path.dll")
        mock_lib.sentire_api_create.assert_called_once_with(60)
        assert bridge._state_ptr == 0x12345678
    
    @patch('ctypes.CDLL')
    def test_native_bridge_raises_on_dll_load_failure(self, mock_cdll):
        """Vérifie que NativeBodyCreationFailed est levée si la DLL ne charge pas."""
        # Arrange
        mock_cdll.side_effect = OSError("DLL not found")
        
        # Act & Assert
        with pytest.raises(NativeBodyCreationFailed) as exc_info:
            NativeBridge("nonexistent.dll", cooldown_seconds=60)
        
        assert "Failed to load native library" in str(exc_info.value)
    
    @patch('ctypes.CDLL')
    def test_native_bridge_raises_on_null_pointer(self, mock_cdll):
        """Vérifie que NativeBodyCreationFailed est levée si create retourne NULL."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0  # NULL pointer
        
        # Act & Assert
        with pytest.raises(NativeBodyCreationFailed) as exc_info:
            NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        assert "NULL pointer" in str(exc_info.value)
    
    @patch('ctypes.CDLL')
    def test_native_bridge_can_act(self, mock_cdll):
        """Vérifie que can_act() appelle correctement l'API native."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0x12345678
        mock_lib.sentire_api_can_act.return_value = 1  # Can act
        
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Act
        result = bridge.can_act()
        
        # Assert
        assert result is True
        mock_lib.sentire_api_can_act.assert_called_once_with(0x12345678)
    
    @patch('ctypes.CDLL')
    def test_native_bridge_record_action(self, mock_cdll):
        """Vérifie que record_action() appelle correctement l'API native."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0x12345678
        
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Act
        bridge.record_action("Test action performed")
        
        # Assert
        mock_lib.sentire_api_record_action.assert_called_once()
        call_args = mock_lib.sentire_api_record_action.call_args
        assert call_args[0][0] == 0x12345678  # State pointer
        assert call_args[0][1] == b"Test action performed"  # Encoded string
    
    @patch('ctypes.CDLL')
    def test_native_bridge_destroy(self, mock_cdll):
        """Vérifie que destroy() libère correctement les ressources natives."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0x12345678
        
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Act
        bridge.destroy()
        
        # Assert
        mock_lib.sentire_api_destroy.assert_called_once_with(0x12345678)
        assert bridge._state_ptr is None  # Pointer set to None after destroy
    
    @patch('ctypes.CDLL')
    def test_native_bridge_destroy_idempotent(self, mock_cdll):
        """Vérifie que destroy() peut être appelé plusieurs fois sans erreur."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0x12345678
        
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Act
        bridge.destroy()
        bridge.destroy()  # Second call should be safe
        
        # Assert
        mock_lib.sentire_api_destroy.assert_called_once()  # Only called once
    
    @patch('ctypes.CDLL')
    def test_native_bridge_sets_function_prototypes(self, mock_cdll):
        """Vérifie que _setup_function_prototypes configure correctement les signatures."""
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0x12345678
        
        # Act
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Assert - Verify all function signatures were set
        assert mock_lib.sentire_api_create.argtypes == [ctypes.c_int]
        assert mock_lib.sentire_api_create.restype == ctypes.c_void_p
        
        assert mock_lib.sentire_api_destroy.argtypes == [ctypes.c_void_p]
        assert mock_lib.sentire_api_destroy.restype is None
        
        assert mock_lib.sentire_api_can_act.argtypes == [ctypes.c_void_p]
        assert mock_lib.sentire_api_can_act.restype == ctypes.c_int
        
        assert mock_lib.sentire_api_record_action.argtypes == [ctypes.c_void_p, ctypes.c_char_p]
        assert mock_lib.sentire_api_record_action.restype is None


# ============================================================================
# TESTS D'INTÉGRATION FONDAMENTALE
# ============================================================================

class TestIntegrationFoundationnelle:
    """Tests d'intégration pour valider l'interaction entre les artefacts."""
    
    @patch('ctypes.CDLL')
    def test_complete_foundational_cycle(self, mock_cdll):
        """
        Test d'intégration complet simulant un cycle fondamental.
        Vérifie que tous les artefacts peuvent travailler ensemble.
        """
        # Arrange
        mock_lib = MagicMock()
        mock_cdll.return_value = mock_lib
        mock_lib.sentire_api_create.return_value = 0x12345678
        mock_lib.sentire_api_can_act.return_value = 1  # Can act
        
        # Act - Simulate a basic cycle
        bridge = NativeBridge("fake_path.dll", cooldown_seconds=60)
        
        # Create a stimulus (would come from Perception in real system)
        stimulus = Stimulus(
            cpu_usage=85.0,
            memory_usage=70.0,
            foreground_window_title="Heavy Process"
        )
        
        # Check if we can act
        can_act = bridge.can_act()
        
        # If we can act, create and record an action
        if can_act:
            action = Action(
                id="LOG_WARNING",
                description="CPU usage is high",
                parameters={"cpu": stimulus.cpu_usage}
            )
            bridge.record_action(action.description)
        
        # Cleanup
        bridge.destroy()
        
        # Assert
        assert can_act is True
        mock_lib.sentire_api_can_act.assert_called()
        mock_lib.sentire_api_record_action.assert_called()
        mock_lib.sentire_api_destroy.assert_called()

# --- END OF FILE: tests/test_foundational_forge.py ---
