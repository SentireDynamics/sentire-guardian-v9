# tests/test_llama_cpp_bridge.py
"""
Validation Doctrinale: Communication avec l'Oracle.
Ce test utilise un mock pour simuler le serveur Llama.cpp. Il valide que le
Pont Llama envoie des requêtes formatées selon la doctrine et interprète
correctement les réponses de l'Oracle simulé, sans effectuer de véritable appel réseau.
"""
from oracle.llama_cpp_bridge import LlamaCppBridge

def test_llama_bridge_generate_call(mocker):
    """Vérifie que la méthode generate formate et envoie la bonne requête."""
    # Mocker la librairie requests.post
    mock_post = mocker.patch("requests.post")

    # Configurer la réponse du mock
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"content": "Generated text"}
    mock_post.return_value = mock_response

    bridge = LlamaCppBridge(base_url="http://test.local:8080")
    prompt = "Test prompt"

    result = bridge.generate(prompt)

    # Vérifier que la réponse est correcte
    assert result == "Generated text"

    # Vérifier que requests.post a été appelé avec les bons arguments
    expected_url = "http://test.local:8080/completion"
    expected_payload = {
        "prompt": "Test prompt",
        "n_predict": 256,
        "stop": ["\n"],
    }
    mock_post.assert_called_once_with(
        expected_url,
        json=expected_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )