# tests/test_chroniqueur_souverain.py
"""
Tests pour le Chroniqueur Souverain.
Validation du rituel de transmission vers le Dojo Cloud.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from guardian.chroniqueur_souverain import ChroniqueurSouverain
from core.exceptions import HeresyException


def test_chroniqueur_init_success():
    """Vérifie que le Chroniqueur s'initialise correctement avec des crédentials valides."""
    with patch('guardian.chroniqueur_souverain.pubsub_v1.PublisherClient') as mock_publisher:
        mock_client = Mock()
        mock_client.topic_path.return_value = "projects/test-project/topics/test-topic"
        mock_publisher.return_value = mock_client
        
        chroniqueur = ChroniqueurSouverain(
            project_id="test-project",
            topic_name="test-topic",
            credentials_path="/path/to/credentials.json"
        )
        
        assert chroniqueur.project_id == "test-project"
        assert chroniqueur.topic_name == "test-topic"
        assert chroniqueur.credentials_path == "/path/to/credentials.json"
        assert chroniqueur.publisher is not None
        assert chroniqueur.topic_path == "projects/test-project/topics/test-topic"


def test_chroniqueur_init_failure():
    """Vérifie qu'une HeresyException est levée si l'initialisation échoue."""
    with patch('guardian.chroniqueur_souverain.pubsub_v1.PublisherClient') as mock_publisher:
        mock_publisher.side_effect = Exception("Invalid credentials")
        
        with pytest.raises(HeresyException) as exc_info:
            ChroniqueurSouverain(
                project_id="test-project",
                topic_name="test-topic",
                credentials_path="/invalid/path.json"
            )
        
        assert "Échec de l'initialisation du Chroniqueur Souverain" in str(exc_info.value)


def test_transmettre_chroniques_empty_list():
    """Vérifie que la transmission avec une liste vide ne fait rien."""
    with patch('guardian.chroniqueur_souverain.pubsub_v1.PublisherClient') as mock_publisher:
        mock_client = Mock()
        mock_client.topic_path.return_value = "projects/test/topics/test"
        mock_publisher.return_value = mock_client
        
        chroniqueur = ChroniqueurSouverain("test", "test", "/path/to/creds.json")
        
        # Ne devrait rien faire avec une liste vide
        chroniqueur.transmettre_chroniques([])
        
        # Aucune publication ne devrait avoir été faite
        mock_client.publish.assert_not_called()


def test_transmettre_chroniques_launches_thread():
    """Vérifie que la transmission lance un thread en arrière-plan."""
    with patch('guardian.chroniqueur_souverain.pubsub_v1.PublisherClient') as mock_publisher:
        mock_client = Mock()
        mock_client.topic_path.return_value = "projects/test/topics/test"
        mock_publisher.return_value = mock_client
        
        chroniqueur = ChroniqueurSouverain("test", "test", "/path/to/creds.json")
        
        with patch('guardian.chroniqueur_souverain.threading.Thread') as mock_thread:
            mock_thread_instance = Mock()
            mock_thread.return_value = mock_thread_instance
            
            entries = ["Entry 1", "Entry 2", "Entry 3"]
            chroniqueur.transmettre_chroniques(entries)
            
            # Vérifie qu'un thread a été créé
            mock_thread.assert_called_once()
            # Vérifie que le thread a été démarré
            mock_thread_instance.start.assert_called_once()


def test_transmettre_en_arriere_plan():
    """Vérifie que la transmission en arrière-plan publie correctement les messages."""
    with patch('guardian.chroniqueur_souverain.pubsub_v1.PublisherClient') as mock_publisher:
        mock_client = Mock()
        mock_client.topic_path.return_value = "projects/test/topics/test"
        
        # Mock pour le future retourné par publish
        mock_future = Mock()
        mock_future.result.return_value = "message-id-123"
        mock_client.publish.return_value = mock_future
        
        mock_publisher.return_value = mock_client
        
        chroniqueur = ChroniqueurSouverain("test", "test", "/path/to/creds.json")
        
        entries = ["Entry 1", "Entry 2", "Entry 3"]
        
        # Appeler directement la méthode privée pour tester
        chroniqueur._transmettre_en_arriere_plan(entries)
        
        # Vérifie que publish a été appelé 3 fois
        assert mock_client.publish.call_count == 3
        
        # Vérifie que les données sont encodées en UTF-8
        for i, entry in enumerate(entries):
            call_args = mock_client.publish.call_args_list[i]
            assert call_args[1]['data'] == entry.encode('utf-8')
