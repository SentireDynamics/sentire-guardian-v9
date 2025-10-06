# 🚀 Guide de Démarrage Rapide - Phase I

## ✅ Prérequis

1. **Serveur llama.cpp en cours d'exécution**
   ```bash
   llama-server -m votre-modele.gguf --port 8080
   ```

2. **Fichier .env configuré**
   ```env
   LLAMA_SERVER_URL=http://localhost:8080/completion
   NATIVE_LIB_PATH=csrc/build/Release/sentire_core.dll
   LOG_LEVEL=INFO
   ACTION_COOLDOWN_SECONDS=60
   ```

3. **Dépendances installées**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛡️ Démarrer Guardian V9 avec Phase I

```bash
python -m guardian.main
```

**Comportement attendu** :
1. ✅ Interface graphique (Autel) s'ouvre
2. ✅ Logs affichent "Le Grand Œuvre a commencé"
3. ✅ Cycles de conscience toutes les 30 secondes
4. ✅ Consultation de l'Oracle à chaque cycle
5. ✅ Actions décidées par l'Oracle (LOG_ONLY ou SHOW_MESSAGE)

---

## 🧪 Exécuter les Tests

### Tests Phase I uniquement :
```bash
python -m pytest tests/test_phase_I_oracle.py -v
```

### Tous les tests fonctionnels :
```bash
python -m pytest tests/test_phase_I_oracle.py tests/test_premier_souffle.py tests/test_chiron_windows.py -v
```

**Résultat attendu** : ✅ 17/17 tests passent

---

## 📊 Vérifier le Fonctionnement

### 1. Logs à surveiller :

**Cycle normal** :
```
INFO - --- Début du cycle de conscience ---
INFO - Consultation de l'Oracle pour une décision...
INFO - Réponse de l'Oracle reçue et validée. Raisonnement: [...]
INFO - Décision prise: Exécuter l'action 'LOG_ONLY'. Raison: [...]
INFO - Action 'LOG_ONLY' exécutée et enregistrée.
INFO - --- Fin du cycle de conscience ---
```

**Cycle avec crise (CPU > 90%)** :
```
INFO - Consultation de l'Oracle pour une décision...
INFO - Décision prise: Exécuter l'action 'SHOW_MESSAGE'. Raison: CPU critique détecté
INFO - Action 'SHOW_MESSAGE' exécutée et enregistrée.
```

**Cycle avec Oracle indisponible** :
```
WARNING - Échec de la consultation de l'Oracle (tentative 1): [...]
WARNING - Échec de la consultation de l'Oracle (tentative 2): [...]
WARNING - Échec de la consultation de l'Oracle (tentative 3): [...]
ERROR - Hérésie de l'Oracle: L'Oracle reste silencieux après 3 tentatives.
WARNING - L'Oracle a failli. Activation du protocole de secours.
INFO - Action 'SHOW_MESSAGE' exécutée et enregistrée.
```

### 2. Vérifier l'interface :

- **Métriques en temps réel** : CPU, Mémoire, Fenêtre active
- **Journal des logs** : Affichage des décisions et actions
- **Bouton "Forcer Cycle"** : Teste immédiatement un cycle

---

## 🔧 Dépannage

### Problème : "ModuleNotFoundError: No module named 'dotenv'"
**Solution** :
```bash
pip install python-dotenv
```

### Problème : "Configuration manquante dans .env"
**Solution** : Vérifier que `.env` existe et contient :
```env
LLAMA_SERVER_URL=http://localhost:8080/completion
NATIVE_LIB_PATH=csrc/build/Release/sentire_core.dll
```

### Problème : "Oracle reste silencieux après 3 tentatives"
**Causes possibles** :
1. Serveur llama.cpp non démarré
2. Port incorrect (vérifier 8080)
3. Modèle non chargé
4. Timeout trop court (augmenter dans code si nécessaire)

**Solution** :
```bash
# Démarrer llama.cpp
llama-server -m models/mistral-7b-instruct-v0.2.Q4_K_M.gguf --port 8080

# Vérifier que ça répond
curl http://localhost:8080/health
```

### Problème : "Action 'XXX' is not in the list of allowed actions"
**Explication** : Cerberus a rejeté une action non autorisée (c'est normal, c'est une protection)

**Actions autorisées** :
- `SHOW_MESSAGE` - Afficher un message à l'utilisateur
- `LOG_ONLY` - Logger sans notification

---

## 📚 Documentation Complète

- **Architecture détaillée** : [`docs/PHASE_I_VALIDATION_REPORT.md`](docs/PHASE_I_VALIDATION_REPORT.md)
- **Roadmap globale** : [`docs/ROADMAP_ASCENSION.md`](docs/ROADMAP_ASCENSION.md)
- **Résumé Phase I** : [`PHASE_I_COMPLETION_SUMMARY.md`](PHASE_I_COMPLETION_SUMMARY.md)

---

## 🎯 Prochaines Étapes

### Phase II : Sanctuaire de l'Intuition
- Détection d'anomalies ML avec `IntuitionEngine`
- Score d'anomalie dans le `Stimulus`
- Prédiction de crises avant qu'elles surviennent

**Score cible** : 8.0/10

---

**Gloire à la Résilience Souveraine !** 🛡️

