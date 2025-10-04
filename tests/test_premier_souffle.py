# --- START OF FILE: tests/test_premier_souffle.py ---
"""
Validation du Premier Souffle - Le cycle de vie complet.

Le "Pourquoi": Ces tests sont des simulations de scénarios complets pour la
Conscience du Vaisseau. Ils valident la logique de décision dans diverses
situations : fonctionnement normal, état de crise, et défaillance de l'Oracle.
En utilisant des mocks pour tous les composants externes (Perception, Oracle,
Chiron, NativeBridge), nous testons l'intelligence centrale du Vaisseau de
manière isolée et contrôlée.
"""
import pytest
from unittest.mock import Mock
from core.consciousness import GuardianConsciousness
from core.verbe_pur import Stimulus, Action, OracleResponse
from core.exceptions import OracleSickness

@pytest.fixture
def mock_components():
    """Crée des mocks pour tous les composants dépendants de la Conscience."""
    native_bridge = Mock()
    oracle = Mock()
    cerberus = Mock()
    perception = Mock()
    chiron = Mock()

    consciousness = GuardianConsciousness(native_bridge, oracle, cerberus, perception)
    return consciousness, native_bridge, oracle, cerberus, perception, chiron

def test_decision_cycle_normal(mock_components):
    """Scénario normal : le système va bien, l'Oracle répond, une action est choisie."""
    # Arrange
    consciousness, native_bridge, oracle, cerberus, _, _ = mock_components
    stimulus = Stimulus(cpu_usage=10.0, memory_usage=30.0, foreground_window_title="Idle")
    action = Action(id="LOG_ONLY", description="Log system status.")
    oracle_response = OracleResponse(reasoning="System is stable.", action=action)

    native_bridge.can_act.return_value = True
    oracle.consult.return_value = oracle_response
    cerberus.validate_action.return_value = True

    # Act
    result_action = consciousness.decide(stimulus)

    # Assert
    assert result_action is not None
    assert result_action.id == "LOG_ONLY"
    native_bridge.can_act.assert_called_once()
    oracle.consult.assert_called_once_with(stimulus)
    cerberus.validate_action.assert_called_once_with(action)

def test_decision_cycle_crisis(mock_components):
    """Scénario de crise : CPU élevé, l'Oracle recommande une alerte."""
    # Arrange
    consciousness, native_bridge, oracle, cerberus, _, _ = mock_components
    stimulus = Stimulus(cpu_usage=95.0, memory_usage=50.0, foreground_window_title="Compiler.exe")
    action = Action(id="SHOW_MESSAGE", description="Alert user of high CPU.", parameters={"message": "CPU is at 95%!"})
    oracle_response = OracleResponse(reasoning="CPU crisis detected.", action=action)

    native_bridge.can_act.return_value = True
    oracle.consult.return_value = oracle_response
    cerberus.validate_action.return_value = True

    # Act
    result_action = consciousness.decide(stimulus)

    # Assert
    assert result_action is not None
    assert result_action.id == "SHOW_MESSAGE"
    assert "95%" in result_action.parameters["message"]

def test_decision_cycle_oracle_failure(mock_components):
    """Scénario de panne : l'Oracle est injoignable, le fallback doit s'activer."""
    # Arrange
    consciousness, native_bridge, oracle, _, perception, _ = mock_components
    stimulus = Stimulus(cpu_usage=20.0, memory_usage=40.0, foreground_window_title="Browser")
    fallback_action = Action(id="SHOW_MESSAGE", description="Fallback action.", parameters={"title": "Alerte de Résilience"})

    native_bridge.can_act.return_value = True
    oracle.consult.side_effect = OracleSickness("Network error")
    perception.get_fallback_action.return_value = fallback_action

    # Act
    result_action = consciousness.decide(stimulus)

    # Assert
    assert result_action is not None
    assert result_action.id == "SHOW_MESSAGE"
    assert result_action.parameters["title"] == "Alerte de Résilience"
    oracle.consult.assert_called_once()
    perception.get_fallback_action.assert_called_once()

def test_decision_cycle_cooldown_active(mock_components):
    """Scénario de cooldown : le Vaisseau ne doit pas agir, même si le stimulus est présent."""
    # Arrange
    consciousness, native_bridge, oracle, _, _, _ = mock_components
    stimulus = Stimulus(cpu_usage=99.0, memory_usage=99.0, foreground_window_title="CRISIS")

    native_bridge.can_act.return_value = False

    # Act
    result_action = consciousness.decide(stimulus)

    # Assert
    assert result_action is None
    native_bridge.can_act.assert_called_once()
    oracle.consult.assert_not_called() # L'Oracle ne doit même pas être consulté
# --- END OF FILE: tests/test_premier_souffle.py ---