# --- START OF FILE: core/verbe_pur.py ---
"""
Le Sanctuaire du Verbe Pur.

Le "Pourquoi": Ce module définit les structures de données fondamentales du Vaisseau
en utilisant Pydantic. Il agit comme un contrat, garantissant que les données qui
circulent entre les différents composants (Perception, Conscience, Oracle) sont
toujours valides, structurées et explicites. C'est le langage commun du Grand Œuvre.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class Stimulus(BaseModel):
    """
    Représente les informations brutes perçues par le Vaisseau sur son environnement.
    C'est l'étincelle qui initie le cycle de réflexion.
    """
    cpu_usage: float = Field(..., description="Utilisation actuelle du CPU en pourcentage.")
    memory_usage: float = Field(..., description="Utilisation actuelle de la mémoire en pourcentage.")
    foreground_window_title: str = Field(..., description="Titre de la fenêtre actuellement au premier plan.")
    
    # Fondation Somatique : Perception du GPU
    gpu_usage: Optional[float] = Field(None, description="Utilisation du GPU en pourcentage.")
    gpu_temp: Optional[float] = Field(None, description="Température du GPU en degrés Celsius.")

    # Phase II : Perception fine des processus gourmands
    top_cpu_process_pid: Optional[int] = Field(None, description="PID du processus le plus consommateur de CPU.")
    top_cpu_process_name: Optional[str] = Field(None, description="Nom du processus le plus consommateur de CPU.")
    top_mem_process_pid: Optional[int] = Field(None, description="PID du processus consommant le plus de mémoire.")
    top_mem_process_name: Optional[str] = Field(None, description="Nom du processus consommant le plus de mémoire.")

class Action(BaseModel):
    """
    Représente une action unique et atomique que le Vaisseau peut entreprendre.
    C'est la matérialisation de la volonté.
    """
    id: str = Field(..., description="Un identifiant unique pour l'action, ex: 'LOG_WARNING', 'SHOW_MESSAGE'.")
    description: str = Field(..., description="Description en langage naturel de ce que fait l'action.")
    parameters: Optional[dict] = Field(default_factory=dict, description="Paramètres nécessaires à l'exécution de l'action.")

class OracleResponse(BaseModel):
    """
    Représente la réponse structurée de l'Oracle à une sollicitation.
    C'est le conseil divin, la stratégie à adopter.
    """
    reasoning: str = Field(..., description="Explication de l'Oracle sur le choix de l'action.")
    action: Action = Field(..., description="L'action recommandée à entreprendre.")
# --- END OF FILE: core/verbe_pur.py ---
