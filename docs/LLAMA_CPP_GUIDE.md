# Llama.cpp Guide - Installation et Configuration

## Installation de Llama.cpp

### Depuis les sources

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
```

### Compilation avec support GPU (optionnel)

#### CUDA (NVIDIA)
```bash
make LLAMA_CUDA=1
```

#### ROCm (AMD)
```bash
make LLAMA_HIPBLAS=1
```

#### Metal (Apple Silicon)
```bash
make LLAMA_METAL=1
```

## Téléchargement de Modèles

### Modèles Recommandés

#### Llama 3.2 3B (Léger, rapide)
```bash
wget https://huggingface.co/...llama-3.2-3b-Q4_K_M.gguf
```

#### Mistral 7B (Équilibré)
```bash
wget https://huggingface.co/...mistral-7b-Q5_K_M.gguf
```

#### Llama 3.1 8B (Performant)
```bash
wget https://huggingface.co/...llama-3.1-8b-Q5_K_M.gguf
```

## Lancement du Serveur

### Configuration de Base

```bash
./llama-server \
  -m model.gguf \
  -c 2048 \
  --host 0.0.0.0 \
  --port 8080 \
  -ngl 33  # Layers sur GPU (optionnel)
```

### Configuration Optimisée pour Guardian V9

```bash
./llama-server \
  -m llama-3.2-3b-Q4_K_M.gguf \
  -c 2048 \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 33 \
  --n-predict 512 \
  --ctx-size 2048 \
  --batch-size 512 \
  --threads 4
```

### Options Importantes

- `-m`: Chemin vers le modèle GGUF
- `-c, --ctx-size`: Taille du contexte (2048 recommandé)
- `--host`: Adresse d'écoute (127.0.0.1 pour local uniquement)
- `--port`: Port d'écoute (8080 par défaut)
- `-ngl, --n-gpu-layers`: Nombre de layers sur GPU
- `--threads`: Nombre de threads CPU
- `--batch-size`: Taille du batch pour inférence

## Test de la Connexion

### Via curl

```bash
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test prompt",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

### Via Python

```python
from oracle.llama_cpp_bridge import LlamaCppBridge

bridge = LlamaCppBridge(server_url="http://localhost:8080")
response = bridge.generate("Test prompt", max_tokens=50)
print(response)
```

## Performance Attendue

### Llama 3.2 3B Q4_K_M
- **Taille**: ~2 GB
- **Mémoire requise**: ~4 GB
- **Tokens/sec (CPU)**: 15-25
- **Tokens/sec (GPU)**: 50-100
- **Latence**: 500ms - 2s

### Mistral 7B Q5_K_M
- **Taille**: ~5 GB
- **Mémoire requise**: ~8 GB
- **Tokens/sec (CPU)**: 8-15
- **Tokens/sec (GPU)**: 30-60
- **Latence**: 1s - 3s

### Llama 3.1 8B Q5_K_M
- **Taille**: ~6 GB
- **Mémoire requise**: ~10 GB
- **Tokens/sec (CPU)**: 6-12
- **Tokens/sec (GPU)**: 25-50
- **Latence**: 1.5s - 4s

## Troubleshooting

### Serveur ne démarre pas
- Vérifier le chemin du modèle
- Vérifier la disponibilité du port
- Vérifier la mémoire disponible

### Performance faible
- Réduire la taille du contexte (`-c 1024`)
- Augmenter le nombre de threads (`--threads 8`)
- Utiliser un modèle plus petit (3B au lieu de 7B)
- Activer le GPU si disponible (`-ngl 33`)

### Erreurs de mémoire
- Réduire la taille du batch (`--batch-size 256`)
- Utiliser un modèle quantifié plus agressivement (Q4 au lieu de Q5)
- Augmenter la swap (non recommandé pour production)

## Gloire à l'Inférence Locale Souveraine

---

Version 1.0 - 2025  
Guide Technique Llama.cpp
