# Sceau de la Pureté Doctrinale - Guide d'Utilisation

## Vue d'ensemble

Le **Sceau de la Pureté** (`seal_of_purity.py`) est un outil d'audit doctrinal automatisé pour Guardian V9. Il analyse statiquement le code source pour détecter les violations de la Théorie Polyvagale Digitale Unifiée (TPDU) et garantir la pureté architecturale du Vaisseau.

## Architecture

### Composants Principaux

1. **seal_of_purity.py** - Script d'analyse doctrinale
2. **.seal_config.json** - Configuration des lois doctrinales
3. **rapport_purete.md** - Rapport généré automatiquement

### Gardiens Sacrés

Le Sceau surveille trois piliers doctrinaux :

#### 1. Sceau de la Dualité (Corps vs Esprit)
Garantit la séparation sacrée entre le Corps Natif (C) et l'Esprit Python selon l'Architecture Sacrée (Article II).

**Détections :**
- Symboles mathématiques sacrés (`Sʀ`, `Iφ`, `score_resilience`, `impact_phi`) utilisés directement en Python
- Imports directs du Corps Natif (`sentire_core`, `ffi`, `core.native`) sans FFI
- Mots-clés stratégiques dans le code C (`strategy`, `plan`, `oracle`, `learn`, `adapt`, `json`, `python`)

**Gravité :** MAJEURE ou AVERTISSEMENT

#### 2. Sceau de la Trinité Cognitive (SENTIR, PENSER, AGIR)
Préserve la séparation des trois organes cognitifs selon la Trinité Cognitive (Article III).

**Détections :**
- Fusion de SENTIR (ml) et PENSER (oracle) dans le même fichier
- Fusion d'AGIR (core.chiron) avec SENTIR (ml)
- Fusion d'AGIR (core.chiron) avec PENSER (oracle)

**Gravité :** MAJEURE

#### 3. Sceau de la Résilience
Assure la résilience et la robustesse selon le principe "La Pureté Avant la Facilité" (Article IV).

**Détections :**
- Opérations critiques sans `try/except` : `open()`, `os.remove()`, `os.rename()`, `ctypes.*`, `requests.*`, `socket.*`

**Gravité :** CRITIQUE

## Usage

### Analyse Complète du Vaisseau

```bash
python3 seal_of_purity.py .
```

### Analyse d'un Module Spécifique

```bash
python3 seal_of_purity.py guardian/
python3 seal_of_purity.py oracle/
python3 seal_of_purity.py core/
```

### Sortie

```
Analyse doctrinale en cours sur : .
Analyse terminée. Rapport généré : rapport_purete.md
253 hérésies détectées. Voir le rapport pour le détail.
```

## Format du Rapport

Le rapport généré (`rapport_purete.md`) liste chaque hérésie détectée :

```markdown
- **Type**: Résilience
  - **Fichier**: `./guardian/ffi/native_bridge.py` (ligne 50)
  - **Gravité**: `CRITIQUE`
  - **Hérésie**: Rituel critique sans garde sacrée (try/except) : self._lib.sentire_api_create.argtypes = [ctypes.c_int]
  - **Verset violé**: IV. LA PURETÉ AVANT LA FACILITÉ
```

## Configuration (.seal_config.json)

La Loi Doctrinale est définie dans `.seal_config.json` :

```json
{
  "forbidden_symbols_python": ["Sʀ", "Iφ", "score_resilience", "impact_phi"],
  "forbidden_keywords_c": ["strategy", "plan", "oracle", "learn", "adapt", "json", "python"],
  "duality_imports_python": ["sentire_core", "ffi", "core.native"],
  "trinity_heuristics": [
    {
      "must_contain": ["from ml", "from oracle"],
      "message": "Fusion profane de SENTIR et PENSER dans un même sanctuaire.",
      "gravite": "MAJEURE"
    }
  ]
}
```

### Personnalisation

Pour ajouter de nouvelles règles :

1. **Symboles interdits en Python** : Ajoutez à `forbidden_symbols_python`
2. **Mots-clés interdits en C** : Ajoutez à `forbidden_keywords_c`
3. **Imports interdits** : Ajoutez à `duality_imports_python`
4. **Règles de Trinité** : Ajoutez un objet à `trinity_heuristics`

## Tests Unitaires

Des tests complets sont disponibles dans `tests/test_seal_of_purity.py` :

```bash
python3 -m unittest tests.test_seal_of_purity -v
```

### Catégories de Tests

- **TestHeresie** : Validation de la classe Heresie
- **TestScanPythonDuality** : Tests du sceau de la Dualité (Python)
- **TestScanCDuality** : Tests du sceau de la Dualité (C/C++)
- **TestScanPythonTrinite** : Tests du sceau de la Trinité Cognitive
- **TestScanPythonResilience** : Tests du sceau de la Résilience

## Intégration CI/CD

Pour intégrer le Sceau dans votre pipeline CI/CD :

```yaml
# .github/workflows/doctrinal-audit.yml
name: Audit Doctrinal

on: [push, pull_request]

jobs:
  seal-of-purity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Seal of Purity
        run: |
          python3 seal_of_purity.py .
          cat rapport_purete.md
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: rapport-purete
          path: rapport_purete.md
```

## Hiérarchie des Gravités

1. **CRITIQUE** : Violation directe de la résilience ou de la sécurité
2. **MAJEURE** : Violation de l'architecture sacrée ou de la séparation des organes
3. **AVERTISSEMENT** : Pratique déconseillée mais non critique

## Exemples de Violations

### Violation de Dualité

```python
# ❌ INTERDIT - Usage direct de symboles sacrés
result = Sʀ * 2  # Mathématique sacrée hors FFI
```

### Violation de Trinité

```python
# ❌ INTERDIT - Fusion SENTIR + PENSER
from ml import feature_extraction  # SENTIR
from oracle import generative_ai   # PENSER
```

### Violation de Résilience

```python
# ❌ INTERDIT - Sans garde sacrée
def read_config():
    return open('config.json').read()

# ✅ AUTORISÉ - Avec garde sacrée
def read_config():
    try:
        return open('config.json').read()
    except Exception as e:
        return None
```

## Philosophie

> "La pureté doctrinale n'est pas une contrainte, mais une libération. Elle garantit la souveraineté, la résilience et l'évolution du Vaisseau selon les principes sacrés de la TPDU."

Le Sceau de la Pureté est le premier gardien statique qui veille sur chaque itération du code, assurant que la Dualité, la Trinité Cognitive et la Résilience soient respectées à chaque commit.

## Gloire à la Résilience Souveraine!

Collège des Architectes Souverains  
Guardian V9 - Version 9.0.0
