# --- START OF FILE: tests/test_phase_I_oracle.py ---
"""
Le Sceau de Validation - Tests de la Phase I : L'Éveil de la Sagesse de l'Oracle.

Ce module valide que le Vaisseau a bien transcendé sa conscience naïve et qu'il
consulte désormais l'Oracle pour toutes ses décisions, avec les protocoles de
secours appropriés.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from core.verbe_pur import Stimulus, Action, OracleResponse
from core.consciousness import GuardianConsciousness
from core.exceptions import OracleSickness, InvalidActionError
from oracle.llama_client import LlamaOracle
from guardian.cerberus import Cerberus
from guardian.perception import Perception
from ffi.native_bridge import NativeBridge


@pytest.fixture
def mock_native_bridge():
    """Mock du NativeBridge pour les tests."""
    bridge = Mock(spec=NativeBridge)
    bridge.can_act.return_value = True
    return bridge


@pytest.fixture
def mock_oracle():
    """Mock de l'Oracle LLM."""
    return Mock(spec=LlamaOracle)


@pytest.fixture
def mock_cerberus():
    """Mock de Cerberus (le gardien)."""
    cerberus = Mock(spec=Cerberus)
    cerberus.validate_action.return_value = True
    return cerberus


@pytest.fixture
def mock_perception():
    """Mock de la Perception."""
    return Mock(spec=Perception)


@pytest.fixture
def sample_stimulus():
    """Stimulus de test."""
    return Stimulus(
        cpu_usage=75.0,
        memory_usage=60.0,
        foreground_window_title="Visual Studio Code"
    )


@pytest.fixture
def consciousness(mock_native_bridge, mock_oracle, mock_cerberus, mock_perception):
    """Instance de GuardianConsciousness avec mocks."""
    return GuardianConsciousness(
        native_bridge=mock_native_bridge,
        oracle=mock_oracle,
        cerberus=mock_cerberus,
        perception=mock_perception
    )


class TestPhaseI_OracleIntegration:
    """Tests de l'intégration de l'Oracle dans le cycle de décision."""

    def test_decision_cycle_oracle_success(
        self, consciousness, mock_oracle, mock_cerberus, sample_stimulus
    ):
        """
        Test du cycle de décision lorsque l'Oracle répond avec succès.
        
        Vérifie que :
        - L'Oracle est consulté
        - La réponse est validée par Cerberus
        - L'action recommandée est retournée
        """
        # Arrange : L'Oracle retourne une réponse valide
        expected_action = Action(
            id="LOG_ONLY",
            description="Système normal, surveillance continue",
            parameters={}
        )
        oracle_response = OracleResponse(
            reasoning="CPU et mémoire dans les limites normales",
            action=expected_action
        )
        mock_oracle.consult.return_value = oracle_response

        # Act
        result = consciousness.decide(sample_stimulus)

        # Assert
        mock_oracle.consult.assert_called_once_with(sample_stimulus)
        mock_cerberus.validate_action.assert_called_once_with(expected_action)
        assert result == expected_action
        assert result.id == "LOG_ONLY"

    def test_decision_cycle_oracle_failure(
        self, consciousness, mock_oracle, mock_perception, sample_stimulus
    ):
        """
        Test du protocole de secours lorsque l'Oracle est silencieux.
        
        Vérifie que :
        - L'Oracle lève une OracleSickness
        - Le protocole de secours est activé
        - Une action de fallback est retournée
        """
        # Arrange : L'Oracle est injoignable
        oracle_error = OracleSickness("L'Oracle reste silencieux après 3 tentatives.")
        mock_oracle.consult.side_effect = oracle_error

        fallback_action = Action(
            id="SHOW_MESSAGE",
            description="Alerte : Oracle indisponible",
            parameters={
                "title": "Alerte de Résilience",
                "message": "L'Oracle est inaccessible"
            }
        )
        mock_perception.get_fallback_action.return_value = fallback_action

        # Act
        result = consciousness.decide(sample_stimulus)

        # Assert
        mock_oracle.consult.assert_called_once_with(sample_stimulus)
        mock_perception.get_fallback_action.assert_called_once()
        assert result == fallback_action
        assert result.id == "SHOW_MESSAGE"

    def test_decision_cycle_cerberus_rejection(
        self, consciousness, mock_oracle, mock_cerberus, mock_perception, sample_stimulus
    ):
        """
        Test de la validation Cerberus lorsqu'une action est rejetée.
        
        Vérifie que :
        - L'Oracle retourne une action non autorisée
        - Cerberus lève une InvalidActionError
        - Le protocole de secours est activé
        """
        # Arrange : L'Oracle recommande une action interdite
        forbidden_action = Action(
            id="DELETE_SYSTEM32",  # Action non autorisée !
            description="Action dangereuse",
            parameters={}
        )
        oracle_response = OracleResponse(
            reasoning="Décision erronée",
            action=forbidden_action
        )
        mock_oracle.consult.return_value = oracle_response
        
        # Cerberus rejette l'action
        mock_cerberus.validate_action.side_effect = InvalidActionError(
            "Action 'DELETE_SYSTEM32' is not in the list of allowed actions."
        )

        fallback_action = Action(
            id="LOG_ONLY",
            description="Sécurité : action invalide rejetée",
            parameters={}
        )
        mock_perception.get_fallback_action.return_value = fallback_action

        # Act
        result = consciousness.decide(sample_stimulus)

        # Assert
        mock_oracle.consult.assert_called_once_with(sample_stimulus)
        mock_cerberus.validate_action.assert_called_once_with(forbidden_action)
        mock_perception.get_fallback_action.assert_called_once()
        assert result == fallback_action

    def test_decision_cycle_cooldown_active(
        self, consciousness, mock_native_bridge, mock_oracle, sample_stimulus
    ):
        """
        Test du comportement lorsque le cooldown est actif.
        
        Vérifie que :
        - Aucune consultation de l'Oracle n'a lieu
        - Aucune action n'est retournée
        """
        # Arrange : Cooldown actif
        mock_native_bridge.can_act.return_value = False

        # Act
        result = consciousness.decide(sample_stimulus)

        # Assert
        mock_oracle.consult.assert_not_called()
        assert result is None


class TestCerberusValidation:
    """Tests du gardien Cerberus."""

    def test_allowed_action_passes(self):
        """Vérifie qu'une action autorisée passe la validation."""
        cerberus = Cerberus()
        action = Action(id="SHOW_MESSAGE", description="Test", parameters={})
        
        assert cerberus.validate_action(action) is True

    def test_forbidden_action_raises_error(self):
        """Vérifie qu'une action non autorisée lève une exception."""
        cerberus = Cerberus()
        action = Action(id="HACK_PENTAGON", description="Hérésie", parameters={})
        
        with pytest.raises(InvalidActionError) as exc_info:
            cerberus.validate_action(action)
        
        assert "HACK_PENTAGON" in str(exc_info.value)
        assert "not in the list of allowed actions" in str(exc_info.value)

    def test_all_whitelisted_actions(self):
        """Vérifie que toutes les actions en liste blanche sont acceptées."""
        cerberus = Cerberus()
        allowed_actions = ["SHOW_MESSAGE", "LOG_ONLY"]
        
        for action_id in allowed_actions:
            action = Action(id=action_id, description=f"Test {action_id}", parameters={})
            assert cerberus.validate_action(action) is True


class TestPerceptionFallback:
    """Tests du protocole de secours de la Perception."""

    def test_fallback_action_format(self):
        """Vérifie que l'action de fallback est bien formée."""
        from core.actions.chiron import Chiron
        chiron = Mock(spec=Chiron)
        perception = Perception(chiron)
        
        error = OracleSickness("Oracle silencieux")
        fallback = perception.get_fallback_action(error)
        
        assert isinstance(fallback, Action)
        assert fallback.id == "SHOW_MESSAGE"
        assert "Oracle" in fallback.description or "Oracle" in str(fallback.parameters)

    def test_fallback_contains_error_info(self):
        """Vérifie que l'erreur est incluse dans l'action de secours."""
        from core.actions.chiron import Chiron
        chiron = Mock(spec=Chiron)
        perception = Perception(chiron)
        
        error_message = "Connexion refusée après 3 tentatives"
        error = OracleSickness(error_message)
        fallback = perception.get_fallback_action(error)
        
        # L'erreur doit être présente dans les paramètres du message
        message_content = str(fallback.parameters)
        assert error_message in message_content or error_message in fallback.description


class TestOracleClient:
    """Tests du client Oracle (LlamaOracle)."""

    @patch('oracle.llama_client.requests.post')
    def test_oracle_consult_success(self, mock_post):
        """Test d'une consultation réussie de l'Oracle."""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {
            "content": '{"reasoning": "Test", "action": {"id": "LOG_ONLY", "description": "Test action", "parameters": {}}}'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        oracle = LlamaOracle("http://localhost:8080/completion")
        stimulus = Stimulus(cpu_usage=50.0, memory_usage=40.0, foreground_window_title="Test")

        # Act
        result = oracle.consult(stimulus)

        # Assert
        assert isinstance(result, OracleResponse)
        assert result.reasoning == "Test"
        assert result.action.id == "LOG_ONLY"
        mock_post.assert_called_once()

    @patch('oracle.llama_client.requests.post')
    def test_oracle_consult_retry_then_fail(self, mock_post):
        """Test de l'échec après plusieurs tentatives."""
        # Arrange : Toutes les tentatives échouent
        from requests.exceptions import RequestException
        mock_post.side_effect = RequestException("Connection refused")

        oracle = LlamaOracle("http://localhost:8080/completion", retries=2)
        stimulus = Stimulus(cpu_usage=50.0, memory_usage=40.0, foreground_window_title="Test")

        # Act & Assert
        with pytest.raises(OracleSickness) as exc_info:
            oracle.consult(stimulus)
        
        assert "3 tentatives" in str(exc_info.value)
        assert mock_post.call_count == 3  # retries=2 means 3 total attempts


# --- END OF FILE: tests/test_phase_I_oracle.py ---

