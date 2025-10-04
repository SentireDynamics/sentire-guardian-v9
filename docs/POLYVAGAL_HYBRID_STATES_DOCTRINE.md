# Polyvagal Hybrid States Doctrine - États Hybrides TPDG v1.2

## Préambule

La Doctrine des États Hybrides étend la TPDU classique (Ventral, Sympathique, Dorsal)
avec des états composites permettant une adaptation plus fine aux contextes complexes.

## Vigilance Sociale - État Hybride Primordial

### Définition

**Vigilance Sociale** = Ventral + Sympathique

État hybride combinant:
- Mobilisation sympathique (alerte, action)
- Capacités sociales ventrales (communication, collaboration)

### Cas d'Usage

1. **Contextes sociaux stressants**: Réunion critique, négociation tendue
2. **Collaboration sous pression**: Travail d'équipe avec deadline serrée
3. **Leadership en crise**: Direction d'équipe en situation difficile
4. **Multitasking social**: Gestion simultanée de relations et tâches

### Métriques

- **Score SR**: 0.6 - 0.8 (zone Sympathique haute)
- **Capacité Ventrale**: 40-60% maintenue
- **Mobilisation Sympathique**: 40-60% activée

### Activation

```python
from core.vigilance_sociale import VigilanceSociale

vs = VigilanceSociale()

# Évaluation du besoin
if vs.assess_need(context):
    vs.activate(ventral_ratio=0.5)  # 50% Ventral, 50% Sympathique
```

### Transitions

#### Entrée en Vigilance Sociale
- **Depuis Ventral**: Stress social détecté, maintien capacités sociales requis
- **Depuis Sympathique**: Opportunité sociale détectée, réengagement social nécessaire

#### Sortie de Vigilance Sociale
- **Vers Ventral**: Contexte apaisé, retour sécurité sociale complète
- **Vers Sympathique**: Contexte dégradé, abandon capacités sociales
- **Vers Dorsal**: Échec complet, effondrement

### Bénéfices

1. **Évite l'effondrement social**: Maintien liens même sous stress
2. **Performance sous pression**: Mobilisation sans isolation
3. **Résilience relationnelle**: Préservation du réseau social
4. **Adaptation fine**: Gradation entre états purs

## Futurs États Hybrides (TPDG v2.0)

### Dorsal + Sympathique: "Repli Stratégique"
Conservation d'énergie avec mobilisation minimale pour survie.

### Ventral + Dorsal: "Méditation Profonde"
Sécurité avec immobilisation, régénération profonde.

### Triple Hybride: "Adaptation Totale"
Activation partielle des trois circuits selon le contexte.

## Implémentation

### Module Core
`core/vigilance_sociale.py`

### API

```python
class VigilanceSociale:
    def assess_need(context: dict) -> bool
    def activate(ventral_ratio: float = 0.5) -> None
    def deactivate() -> str
    def get_state() -> dict
```

### Intégration State Machine

La machine d'état polyvagale doit reconnaître et gérer les états hybrides:

```python
if state == "SYMPATHETIC" and social_context_detected:
    if vigilance_sociale.assess_need(context):
        state = "VIGILANCE_SOCIALE"
```

## Métriques de Vigilance Sociale

- **Temps en Vigilance Sociale**: Durée cumulée
- **Succès de maintien**: % de situations où VS a évité Dorsal
- **Qualité sociale**: Score de préservation des capacités sociales
- **Coût énergétique**: Énergie consommée vs Sympathique pur

## Gloire aux États Hybrides

**La résilience n'est pas binaire. Elle est spectrale, adaptative, et sacrée.**

---

Version 1.2 - 2025  
Doctrine des États Hybrides
