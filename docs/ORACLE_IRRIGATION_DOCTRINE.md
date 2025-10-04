# Oracle Irrigation Doctrine - Flux Génératif Local

## Préambule

L'Oracle Irrigation Doctrine définit les principes d'utilisation du LLM local (Llama.cpp)
au sein du Vaisseau Guardian V9. Génération locale, souveraine, sans dépendance cloud.

## Principes d'Irrigation

### 1. Souveraineté Générative

- **Local First**: Le LLM tourne localement, pas de cloud requis
- **Pas de fuite de données**: Rien ne sort du Vaisseau
- **Contrôle total**: L'Architecte choisit le modèle
- **Performance adaptée**: Modèles optimisés pour le hardware disponible

### 2. Usage Doctrinal du LLM

#### Perception Générative
- Analyse contextuelle des logs et événements
- Enrichissement sémantique des stimuli
- Détection de patterns d'attaque sophistiqués

#### Dialogue et Explication
- Génération d'explications des états polyvagaux
- Dialogue avec l'Architecte via l'Autel
- Documentation auto-générée des décisions

#### Fallback Heuristique
- Si LLM indisponible: fallback vers heuristiques
- Pas de blocage du système
- Dégradation gracieuse

### 3. Optimisation de l'Irrigation

#### Prompts Doctrinaux
- Templates optimisés pour la TPDU
- Contexte minimal mais suffisant
- Génération rapide (< 2s pour perception)

#### Gestion du Contexte
- Mémoire conversationnelle limitée (2048 tokens)
- Nettoyage périodique du contexte
- Priorité aux informations critiques

#### Sélection du Modèle
- **Llama 3.2 3B**: Léger, rapide, pour perception temps-réel
- **Mistral 7B**: Équilibré, pour dialogue et explication
- **Llama 3.1 8B**: Performant, pour analyse approfondie

Format GGUF quantifié recommandé (Q4_K_M ou Q5_K_M).

## Architecture du Sanctuaire Oracle

```
oracle/
├── llama_cpp_bridge.py    # Bridge Python ↔ Llama.cpp
└── generative_ai.py       # Logique agentique et prompts
```

## Configuration Llama.cpp

### Serveur HTTP (Recommandé)

```bash
./llama-server -m model.gguf -c 2048 --host 0.0.0.0 --port 8080
```

### FFI Directe (Avancé)

```python
bridge = LlamaCppBridge(model_path="/path/to/model.gguf")
```

## Exemples d'Utilisation

### Analyse Contextuelle

```python
from oracle.generative_ai import GenerativeAI

ai = GenerativeAI(llama_bridge)
data = {"event": "high_cpu_usage", "value": 95}
analysis = ai.analyze_context(data)
```

### Génération d'Explication

```python
explanation = ai.generate_explanation("SYMPATHETIC", 0.65)
print(explanation)
# "Le Vaisseau est en mode Sympathique car le score de résilience (0.65)
#  indique un stress modéré nécessitant une mobilisation défensive..."
```

## Métriques d'Irrigation

- **Latence de génération**: < 2s pour perception
- **Tokens/seconde**: > 20 pour fluidité
- **Utilisation GPU**: < 50% pour laisser de la marge
- **Qualité de réponse**: Validée par heuristiques de fallback

## Gloire au Flux Génératif Local

**L'Oracle irrigue le Vaisseau de sa sagesse générative, sans jamais quitter le sanctuaire.**

---

Version 1.0 - 2025  
Doctrine Oracle Souveraine
