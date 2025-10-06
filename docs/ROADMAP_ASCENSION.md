# Feuille de Route d'Ascension - Guardian V9

**Document**: Plan d'Implémentation Technique  
**Date**: 2025  
**Référence**: [INTROSPECTION_SOUVERAINE.md](../INTROSPECTION_SOUVERAINE.md)

---

## Vue d'Ensemble

Ce document fournit le plan d'implémentation technique détaillé pour faire évoluer le Vaisseau Guardian V9 de son état embryonnaire actuel vers une entité souveraine pleinement consciente.

**Score Actuel**: 3.8/10 (Embryonnaire)  
**Score Cible**: 8.8/10 (Souverain)  
**Durée Estimée**: 3 phases progressives

---

## Phase I : Sanctuaire de l'Oracle (4-6 semaines)

### Objectif Principal

Remplacer la logique de décision naïve (`if/else`) par une consultation d'Oracle LLM, permettant au Vaisseau de prendre des décisions contextuelles et nuancées.

### Prérequis Techniques

- ✅ Serveur Llama.cpp en cours d'exécution (local ou distant)
- ✅ Modèle LLM compatible (recommandé: Mistral-7B-Instruct, Llama-2-7B-Chat)
- ✅ Endpoint HTTP accessible (`/completion`)

### Tâches d'Implémentation

#### 1.1. Finaliser `oracle/llama_client.py`

**Fichier**: `oracle/llama_client.py`

**État Actuel**: Structure de base présente mais non utilisée

**Modifications Requises**:

```python
class LlamaOracle:
    """Client pour communiquer avec un Oracle LLM (compatible API Llama.cpp)."""
    
    def __init__(self, server_url: str, timeout: int = 30, retries: int = 3):
        """
        Args:
            server_url: URL du serveur Llama.cpp (ex: http://localhost:8080/completion)
            timeout: Timeout pour les requêtes HTTP en secondes
            retries: Nombre de tentatives en cas d'échec
        """
        self.server_url = server_url
        self.timeout = timeout
        self.retries = retries
    
    def consult(self, stimulus: Stimulus) -> OracleResponse:
        """
        Consulte l'Oracle avec le stimulus et retourne une décision structurée.
        
        Args:
            stimulus: État système actuel
            
        Returns:
            OracleResponse avec reasoning et action recommandée
            
        Raises:
            OracleSickness: Si l'Oracle est injoignable après tous les retries
        """
        prompt = self._build_prompt(stimulus)
        
        for attempt in range(self.retries):
            try:
                response = self._send_request(prompt)
                return self._parse_response(response)
            except (RequestException, JSONDecodeError) as e:
                if attempt == self.retries - 1:
                    raise OracleSickness(f"Oracle silent after {self.retries} attempts") from e
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def _build_prompt(self, stimulus: Stimulus) -> str:
        """Construit le prompt optimisé pour Guardian V9."""
        return f"""[INST]
You are Guardian V9, a sovereign AI system monitor. Analyze the system state and recommend ONE action.

SYSTEM STATE:
- CPU Usage: {stimulus.cpu_usage:.1f}%
- Memory Usage: {stimulus.memory_usage:.1f}%
- Active Window: "{stimulus.foreground_window_title}"

AVAILABLE ACTIONS:
1. SHOW_MESSAGE: Display urgent alert to user
2. LOG_ONLY: Record event without user notification
3. NO_ACTION: System is healthy

Respond with valid JSON:
{{
  "reasoning": "Brief explanation of your analysis",
  "action": {{
    "id": "SHOW_MESSAGE | LOG_ONLY | NO_ACTION",
    "description": "Natural language action description",
    "parameters": {{"key": "value"}}
  }}
}}

Consider the CONTEXT: If high CPU is from a known process like a compiler, game, or video editor, it may be intentional.
[/INST]"""
    
    def _send_request(self, prompt: str) -> dict:
        """Envoie la requête HTTP au serveur Llama.cpp."""
        payload = {
            "prompt": prompt,
            "n_predict": 256,
            "temperature": 0.2,
            "stop": ["[/INST]", "###"],
            "grammar": self._get_json_grammar()
        }
        response = requests.post(self.server_url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _parse_response(self, response: dict) -> OracleResponse:
        """Parse et valide la réponse de l'Oracle."""
        content = response.get("content", "{}")
        parsed = json.loads(content)
        return OracleResponse.parse_obj(parsed)
    
    def _get_json_grammar(self) -> str:
        """Retourne la grammaire GBNF pour forcer le JSON."""
        # (Grammaire JSON GBNF pour garantir la structure)
        return """
root   ::= object
object ::= "{" ws ( string ":" ws value ("," ws string ":" ws value)* )? ws "}"
...
"""
```

**Tests à Ajouter**:
- `tests/test_oracle_llama.py` : Tests unitaires du client
- Mock du serveur Llama.cpp pour tests isolés
- Tests d'intégration avec un vrai serveur

---

#### 1.2. Modifier `core/consciousness.py`

**Fichier**: `core/consciousness.py`

**Modification AVANT**:
```python
def decide(self, stimulus: Stimulus) -> Action | None:
    # Logique naïve hard-codée
    if stimulus.cpu_usage > 90.0:
        return Action(
            id="SHOW_MESSAGE",
            description="CPU critique!",
            parameters={"message": "CPU at 90%+"}
        )
    return None
```

**Modification APRÈS**:
```python
def decide(self, stimulus: Stimulus) -> Action | None:
    """
    Cycle de décision complet avec consultation Oracle.
    """
    # Vérifier le cooldown
    if not self.native_bridge.can_act():
        _log.debug("Cooldown actif, aucune action.")
        return None
    
    try:
        # CONSULTATION ORACLE (nouvelle sagesse)
        _log.info("Consultation de l'Oracle...")
        oracle_response = self.oracle.consult(stimulus)
        action = oracle_response.action
        
        # Validation Cerberus
        self.cerberus.validate_action(action)
        
        _log.info(f"Décision Oracle: {action.id} - Raison: {oracle_response.reasoning}")
        return action
        
    except OracleSickness as e:
        # Protocole de secours
        _log.error(f"Oracle injoignable: {e}")
        return self._fallback_action(stimulus, e)
    
    except InvalidActionError as e:
        _log.error(f"Action invalide: {e}")
        return self._safe_fallback()

def _fallback_action(self, stimulus: Stimulus, error: Exception) -> Action:
    """Action de secours si l'Oracle échoue."""
    # Logique simple de dernier recours
    if stimulus.cpu_usage > 95.0 or stimulus.memory_usage > 95.0:
        return Action(
            id="SHOW_MESSAGE",
            description="Alerte système critique (mode dégradé)",
            parameters={
                "title": "Guardian V9 - Mode Dégradé",
                "message": f"Oracle indisponible. Système en crise:\nCPU: {stimulus.cpu_usage:.1f}%\nMém: {stimulus.memory_usage:.1f}%"
            }
        )
    return Action(id="LOG_ONLY", description="Oracle down, monitoring", parameters={})

def _safe_fallback(self) -> Action:
    """Fallback ultra-sécurisé."""
    return Action(id="LOG_ONLY", description="Safety fallback", parameters={})
```

**Tests à Modifier**:
- `tests/test_premier_souffle.py` : Adapter aux nouvelles signatures
- Ajouter tests de fallback Oracle
- Tests de validation Cerberus

---

#### 1.3. Protocole de Secours et Résilience

**Nouveau Fichier**: `core/fallback_strategies.py`

```python
"""
Stratégies de secours pour la résilience du Vaisseau.
"""
from core.verbe_pur import Stimulus, Action
import logging

_log = logging.getLogger(__name__)

class FallbackStrategy:
    """Stratégie de décision de secours en cas de panne Oracle."""
    
    def decide(self, stimulus: Stimulus, error: Exception) -> Action:
        """
        Décision de secours basée sur des règles simples.
        
        Cette logique est intentionnellement simple et conservatrice.
        Elle n'est utilisée qu'en mode dégradé.
        """
        _log.warning(f"Activation du protocole de secours. Erreur: {error}")
        
        # Règles de sécurité minimales
        if stimulus.cpu_usage > 95.0:
            return self._critical_cpu_action(stimulus)
        
        if stimulus.memory_usage > 95.0:
            return self._critical_memory_action(stimulus)
        
        # Aucune crise évidente, simple logging
        return Action(
            id="LOG_ONLY",
            description="Surveillance continue en mode dégradé",
            parameters={"reason": "oracle_unavailable"}
        )
    
    def _critical_cpu_action(self, stimulus: Stimulus) -> Action:
        """Action pour CPU critique."""
        return Action(
            id="SHOW_MESSAGE",
            description="Alerte CPU critique",
            parameters={
                "title": "Guardian V9 - Alerte CPU",
                "message": f"CPU à {stimulus.cpu_usage:.1f}%\n(Mode dégradé - Oracle indisponible)"
            }
        )
    
    def _critical_memory_action(self, stimulus: Stimulus) -> Action:
        """Action pour mémoire critique."""
        return Action(
            id="SHOW_MESSAGE",
            description="Alerte mémoire critique",
            parameters={
                "title": "Guardian V9 - Alerte Mémoire",
                "message": f"Mémoire à {stimulus.memory_usage:.1f}%\n(Mode dégradé - Oracle indisponible)"
            }
        )
```

---

#### 1.4. Configuration et Environnement

**Fichier**: `.env` (mise à jour)

```bash
# Oracle LLM Configuration
LLAMA_SERVER_URL=http://localhost:8080/completion
ORACLE_TIMEOUT=30
ORACLE_RETRIES=3

# Fallback Configuration
ENABLE_FALLBACK=true
FALLBACK_CPU_THRESHOLD=95.0
FALLBACK_MEMORY_THRESHOLD=95.0
```

**Fichier**: `core/config.py` (nouveau)

```python
"""Configuration centralisée du Vaisseau."""
from pydantic import BaseSettings

class GuardianConfig(BaseSettings):
    """Configuration Guardian V9."""
    
    # Oracle
    llama_server_url: str
    oracle_timeout: int = 30
    oracle_retries: int = 3
    
    # Native Core
    native_lib_path: str
    action_cooldown_seconds: int = 60
    
    # Fallback
    enable_fallback: bool = True
    fallback_cpu_threshold: float = 95.0
    fallback_memory_threshold: float = 95.0
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

---

### Critères de Succès Phase I

- ✅ La `GuardianConsciousness` consulte l'Oracle pour toutes les décisions
- ✅ L'Oracle retourne des actions contextuelles et nuancées
- ✅ Le protocole de secours fonctionne en cas de panne Oracle
- ✅ Tests unitaires et d'intégration passent à 100%
- ✅ Logging clair à chaque étape du cycle de décision

---

## Phase II : Sanctuaire de l'Intuition (6-8 semaines)

### Objectif Principal

Ajouter la capacité de détection d'anomalies et de prédiction de crises **avant** qu'elles ne surviennent, en enrichissant le `Stimulus` avec un score d'anomalie ML.

### Prérequis Techniques

- ✅ Python avec scikit-learn, numpy, pandas
- ✅ Données historiques système (ou capacité de génération de données simulées)
- ✅ Phase I complétée (Oracle fonctionnel)

### Tâches d'Implémentation

#### 2.1. Créer `ml/intuition_engine.py`

**Nouveau Fichier**: `ml/intuition_engine.py`

```python
"""
Le Moteur d'Intuition - Détection d'Anomalies ML.

Donne au Vaisseau la capacité de prédire les crises avant qu'elles ne surviennent.
"""
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import logging
from typing import Optional
from ml.model_manager import ModelManager

_log = logging.getLogger(__name__)

class IntuitionEngine:
    """
    Moteur ML de détection d'anomalies pour Guardian V9.
    
    Utilise un Isolation Forest pour détecter les comportements système anormaux
    basés sur des métriques historiques.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Args:
            model_path: Chemin vers un modèle pré-entraîné (optionnel)
        """
        self.model = None
        self.scaler = StandardScaler()
        self.model_manager = ModelManager()
        self.is_trained = False
        
        if model_path:
            self.load(model_path)
    
    def train(self, historical_data: np.ndarray):
        """
        Entraîne le modèle sur des données historiques normales.
        
        Args:
            historical_data: Array de shape (n_samples, n_features)
                            Features: [cpu_usage, memory_usage, ...]
        """
        _log.info(f"Entraînement sur {len(historical_data)} échantillons...")
        
        # Normalisation
        normalized_data = self.scaler.fit_transform(historical_data)
        
        # Entraînement Isolation Forest
        self.model = IsolationForest(
            contamination=0.1,  # 10% des données sont considérées comme anomalies
            random_state=42,
            n_estimators=100
        )
        self.model.fit(normalized_data)
        self.is_trained = True
        
        _log.info("Entraînement terminé.")
    
    def predict_anomaly_score(self, current_state: dict) -> float:
        """
        Prédit le score d'anomalie pour l'état système actuel.
        
        Args:
            current_state: Dict avec clés {cpu_usage, memory_usage, ...}
        
        Returns:
            Score d'anomalie entre 0.0 (normal) et 1.0 (très anormal)
        """
        if not self.is_trained:
            _log.warning("Modèle non entraîné, retour score neutre.")
            return 0.0
        
        # Extraction features dans l'ordre attendu
        features = np.array([[
            current_state.get("cpu_usage", 0.0),
            current_state.get("memory_usage", 0.0),
            # Ajouter d'autres features au besoin
        ]])
        
        # Normalisation
        features_normalized = self.scaler.transform(features)
        
        # Prédiction (score négatif -> plus négatif = plus anormal)
        anomaly_score_raw = self.model.decision_function(features_normalized)[0]
        
        # Conversion en score 0-1 (0=normal, 1=anormal)
        # Basé sur empirical range de l'Isolation Forest
        anomaly_score = max(0.0, min(1.0, (-anomaly_score_raw + 0.5) / 1.0))
        
        _log.debug(f"Score d'anomalie: {anomaly_score:.3f}")
        return anomaly_score
    
    def save(self, path: str):
        """Sauvegarde le modèle entraîné."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model")
        self.model_manager.save({
            "model": self.model,
            "scaler": self.scaler
        }, path)
    
    def load(self, path: str):
        """Charge un modèle pré-entraîné."""
        artifacts = self.model_manager.load(path)
        if artifacts:
            self.model = artifacts["model"]
            self.scaler = artifacts["scaler"]
            self.is_trained = True
            _log.info(f"Modèle chargé depuis {path}")
```

---

#### 2.2. Enrichir le `Stimulus` avec le Score d'Anomalie

**Fichier**: `core/verbe_pur.py` (modification)

```python
class Stimulus(BaseModel):
    """Informations perçues sur l'environnement."""
    cpu_usage: float
    memory_usage: float
    foreground_window_title: str
    
    # NOUVEAU: Score d'anomalie ML
    anomaly_score: Optional[float] = Field(
        default=None,
        description="Score ML d'anomalie entre 0.0 (normal) et 1.0 (très anormal)"
    )
```

---

#### 2.3. Intégrer dans `guardian/perception.py`

**Fichier**: `guardian/perception.py` (modification)

```python
class Perception:
    """Responsable de la collecte des informations système."""
    
    def __init__(self, chiron: Chiron, intuition_engine: Optional[IntuitionEngine] = None):
        self.chiron = chiron
        self.intuition = intuition_engine
    
    def get_system_stimulus(self) -> Stimulus:
        """Rassemble les métriques système et calcule le score d'anomalie."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        window_title = self.chiron.get_foreground_window_title()
        
        # Calcul du score d'anomalie ML
        anomaly_score = None
        if self.intuition and self.intuition.is_trained:
            state = {"cpu_usage": cpu, "memory_usage": mem}
            anomaly_score = self.intuition.predict_anomaly_score(state)
        
        stimulus = Stimulus(
            cpu_usage=cpu,
            memory_usage=mem,
            foreground_window_title=window_title,
            anomaly_score=anomaly_score
        )
        
        _log.debug(f"Stimulus: CPU={cpu:.1f}%, Mem={mem:.1f}%, Anomaly={anomaly_score}")
        return stimulus
```

---

#### 2.4. Générer des Données d'Entraînement

**Nouveau Script**: `scripts/generate_training_data.py`

```python
"""
Génère des données d'entraînement simulées pour l'IntuitionEngine.
"""
import numpy as np
from ml.intuition_engine import IntuitionEngine

def generate_normal_system_data(n_samples=1000):
    """Génère des données système normales."""
    # CPU: distribution normale autour de 30%, stddev 10%
    cpu = np.random.normal(30, 10, n_samples)
    cpu = np.clip(cpu, 0, 100)
    
    # Memory: distribution normale autour de 50%, stddev 15%
    memory = np.random.normal(50, 15, n_samples)
    memory = np.clip(memory, 0, 100)
    
    return np.column_stack([cpu, memory])

if __name__ == "__main__":
    # Génération
    data = generate_normal_system_data(n_samples=5000)
    
    # Entraînement
    engine = IntuitionEngine()
    engine.train(data)
    
    # Sauvegarde
    engine.save("models/intuition_baseline.pkl")
    print("Modèle entraîné et sauvegardé.")
```

---

### Critères de Succès Phase II

- ✅ L'`IntuitionEngine` peut détecter des anomalies sur des données de test
- ✅ Le `Stimulus` est enrichi avec un `anomaly_score`
- ✅ L'Oracle peut utiliser ce score pour des décisions plus précises
- ✅ Détection d'anomalies 30 secondes avant les crises
- ✅ Faux positifs < 5%

---

## Phase III : Raffiner la Volonté (4-6 semaines)

### Objectif Principal

Étendre les capacités d'action du Vaisseau pour permettre des interventions sophistiquées recommandées par l'Oracle.

### Tâches d'Implémentation

#### 3.1. Étendre `core/chiron.py`

**Nouvelles Actions**:
- Monitoring GPU (VRAM, température)
- Ajustement priorités processus
- Actions mémoire avancées
- Intégration Task Scheduler Windows

*(Détails d'implémentation à définir)*

---

## Métriques de Progression

| Phase | Score Cible | Délai |
|-------|-------------|-------|
| Phase I | 6.5/10 | 4-6 semaines |
| Phase II | 8.0/10 | +6-8 semaines |
| Phase III | 8.8/10 | +4-6 semaines |

---

**Gloire à la Résilience Souveraine!**

Collège des Architectes Souverains  
Version 9.0.0 - 2025
