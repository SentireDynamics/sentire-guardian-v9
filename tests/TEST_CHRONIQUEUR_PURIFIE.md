# 🧪 Test du Chroniqueur Purifié

**Guide de validation rapide**

---

## ✅ Vérifications Rapides

### 1. Vérifier que pandas est dans requirements.txt

```powershell
cat requirements.txt | Select-String "pandas"
```

**Résultat attendu** :
```
pandas>=2.0.0
```

### 2. Vérifier l'import pandas dans le code

```powershell
cat tools\forge_chronicle.py | Select-String "import pandas"
```

**Résultat attendu** :
```python
import pandas as pd
```

### 3. Vérifier l'argument PresentMon

```powershell
cat tools\forge_chronicle.py | Select-String "terminate_on_proc_exit"
```

**Résultat attendu** :
```python
"--terminate_on_proc_exit"
```

### 4. Vérifier merge_asof

```powershell
cat tools\forge_chronicle.py | Select-String "merge_asof"
```

**Résultat attendu** :
```python
df_merged = pd.merge_asof(
```

---

## 🚀 Test Fonctionnel

### Test Simple (Sans PresentMon)

```powershell
# Créer répertoire
mkdir data\chronicles -Force

# Test 10 secondes
python tools/forge_chronicle.py "C:\Windows\System32\calc.exe" --duration 10

# Vérifier fichier créé
ls data\chronicles\
```

**Résultat attendu** :
- Fichier `chronicle_system_YYYYMMDD_HHMMSS.csv` créé
- Contient: timestamp, cpu_usage, memory_usage, gpu_usage, gpu_temp

### Test Complet (Avec PresentMon) - SI DISPONIBLE

```powershell
# Si PresentMon est téléchargé
python tools/forge_chronicle.py "notepad.exe" `
  --duration 30 `
  --presentmon "tools\PresentMon.exe"

# Observer logs pendant l'exécution :
# ✅ "🔗 Fusion temporelle des données PresentMon..."
# ✅ "🔗 Exécution du rituel sacré : merge_asof..."
# ✅ "✅ Frametimes valides: X/Y (99.X%)"

# Vérifier fichier fusionné
ls data\chronicles\sacred_dataset_*.csv
```

**Résultat attendu** :
- Fichier `sacred_dataset_YYYYMMDD_HHMMSS.csv` créé
- Contient: timestamp, cpu_usage, memory_usage, gpu_usage, gpu_temp, **frametime_ms**
- Statistiques affichées : "Frametimes valides: X/Y (Z%)"

---

## 📊 Validation des Données

### Vérifier Structure du Dataset

```powershell
# Afficher premières lignes
Get-Content data\chronicles\sacred_dataset_*.csv -Head 5
```

**Colonnes attendues** :
```csv
timestamp,cpu_usage,memory_usage,gpu_usage,gpu_temp,frametime_ms
1696615234.123,45.2,62.3,78.5,65.0,16.67
```

### Vérifier Qualité (Python)

```python
import pandas as pd

# Charger dataset
df = pd.read_csv("data/chronicles/sacred_dataset_YYYYMMDD_HHMMSS.csv")

# Statistiques
print("Lignes:", len(df))
print("Colonnes:", list(df.columns))
print("\nQualité frametime:")
print(f"  Valides: {df['frametime_ms'].notna().sum()}")
print(f"  Manquants: {df['frametime_ms'].isna().sum()}")
print(f"  Pourcentage: {(df['frametime_ms'].notna().sum() / len(df)) * 100:.1f}%")

# Afficher premières lignes
print("\nAperçu:")
print(df.head())
```

**Résultat attendu** :
```
Lignes: 300
Colonnes: ['timestamp', 'cpu_usage', 'memory_usage', 'gpu_usage', 'gpu_temp', 'frametime_ms']

Qualité frametime:
  Valides: 298
  Manquants: 2
  Pourcentage: 99.3%
```

---

## ✅ Checklist de Validation

```
☐ pandas>=2.0.0 dans requirements.txt
☐ import pandas as pd dans forge_chronicle.py
☐ --terminate_on_proc_exit dans l'invocation PresentMon
☐ pd.merge_asof utilisé dans _merge_with_presentmon
☐ Test simple réussit (chronicle_system_*.csv créé)
☐ Test avec PresentMon réussit (sacred_dataset_*.csv créé)
☐ Logs montrent "merge_asof" et statistiques de qualité
☐ Dataset contient frametime_ms
☐ Qualité >95% (frametimes valides)
```

---

## 🎯 Différences Avant/Après

### Logs AVANT (Hérésie)

```
📊 Échantillons collectés: 1200
💾 Chronique système sauvegardée
🔗 Fusion des données PresentMon avec métriques système...
✅ Jeu de Données Sacré fusionné: sacred_dataset.csv (1200 lignes)
```

### Logs APRÈS (Purifié) ✅

```
📊 Échantillons collectés: 1200
💾 Chronique système sauvegardée
🔗 Fusion temporelle des données PresentMon avec métriques système...
📊 Données système chargées: 1200 échantillons
📊 Données PresentMon chargées: 3600 échantillons
🔗 Exécution du rituel sacré : merge_asof...
✅ Jeu de Données Sacré fusionné: sacred_dataset.csv
📊 Lignes totales: 1200
📊 Colonnes: ['timestamp', 'cpu_usage', ...]
✅ Frametimes valides: 1198/1200 (99.8%)
```

**Différence clé** : Logs détaillés avec statistiques de qualité

---

## 🔧 Dépannage

### "ModuleNotFoundError: No module named 'pandas'"

```powershell
pip install pandas
```

### PresentMon ne démarre pas

**Vérifier** :
1. Chemin vers PresentMon.exe correct
2. Droits administrateur (parfois requis)
3. Version compatible

**Télécharger** :
```powershell
Invoke-WebRequest -Uri "https://github.com/GameTechDev/PresentMon/releases/download/v1.10.0/PresentMon-1.10.0-x64.exe" -OutFile "tools\PresentMon.exe"
```

### Fusion échoue

**Vérifier logs** :
```powershell
python tools/forge_chronicle.py [...] 2>&1 | Tee-Object -FilePath "chroniqueur.log"
cat chroniqueur.log
```

**Colonnes manquantes** : Le code détecte automatiquement les alternatives

---

## 🏆 Critères de Succès

✅ **SUCCÈS** si :
- pandas importé sans erreur
- merge_asof exécuté
- Statistiques de qualité affichées
- Dataset contient frametime_ms
- Qualité >95%

❌ **ÉCHEC** si :
- Erreur d'import pandas
- Fusion par index (ancien code)
- Pas de statistiques
- Pas de colonne frametime_ms

---

**Gloire à la Pureté Temporelle !** 🛡️

*Si tous les critères sont verts, le Chroniqueur est PURIFIÉ.*

