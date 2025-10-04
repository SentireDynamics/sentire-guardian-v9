# Oracle - Sanctuaire Génératif Local

## Épigraphe Doctrinale

Le sanctuaire Oracle abrite le LLM local Llama.cpp, source de perception générative
et d'intuition linguistique du Vaisseau Guardian V9. Inférence souveraine, locale,
sans dépendance cloud.

## Architecture

- **llama_cpp_bridge.py**: Bridge Python ↔ Llama.cpp (HTTP/FFI)
- **generative_ai.py**: Logique agentique, prompts, dialogue, fallback

## Usage

### Initialisation

```python
from oracle.llama_cpp_bridge import LlamaCppBridge
from oracle.generative_ai import GenerativeAI

# Via serveur HTTP Llama.cpp
bridge = LlamaCppBridge(server_url="http://localhost:8080")

# Ou via FFI directe (à implémenter)
# bridge = LlamaCppBridge(model_path="/path/to/model.gguf")

# Initialiser l'IA générative
ai = GenerativeAI(llama_bridge=bridge)
```

### Analyse Contextuelle

```python
data = {"event": "high_cpu_usage", "value": 95}
analysis = ai.analyze_context(data)
print(analysis)
```

### Génération d'Explication

```python
explanation = ai.generate_explanation("SYMPATHETIC", 0.65)
print(explanation)
```

## Configuration Llama.cpp

Le serveur Llama.cpp peut être lancé via:

```bash
./llama-server -m model.gguf -c 2048 --host 0.0.0.0 --port 8080
```

## Modèles Recommandés

- **Llama 3.2 3B** (léger, rapide)
- **Mistral 7B** (équilibré)
- **Llama 3.1 8B** (performant)

Format GGUF quantifié (Q4_K_M ou Q5_K_M) recommandé.

---

**Gloire à la Souveraineté Générative Locale**
