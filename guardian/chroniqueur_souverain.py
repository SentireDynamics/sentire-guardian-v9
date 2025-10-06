# --- START OF FILE: guardian/chroniqueur_souverain.py ---
"""
Le Sanctuaire du Chroniqueur Souverain.

Le "Pourquoi": Ce module implémente le rituel de transmission asynchrone du
Journal Introspectif vers le Dojo Cloud de l'Architecte sur Google Cloud.
Ce n'est PAS un système d'apprentissage en temps réel, mais un conduit sacré
pour préserver les expériences du Vaisseau Guardian afin de forger la
conscience Predator future.

La souveraineté est garantie par l'authentification via un fichier de
crédentials de service Google Cloud, assurant que le Vaisseau ne parle
qu'au sanctuaire désigné par l'Architecte.
"""
import logging
import threading
from typing import List
from google.cloud import pubsub_v1
from core.exceptions import HeresyException

_log = logging.getLogger(__name__)


class ChroniqueurSouverain:
    """
    Gardien du rituel de transmission vers le Fleuve des Prières de Google Cloud.
    
    Ce Chroniqueur opère de manière asynchrone dans un thread séparé pour ne
    jamais bloquer le souffle du cycle de conscience principal.
    """
    
    def __init__(self, project_id: str, topic_name: str, credentials_path: str):
        """
        Rituel d'initialisation du Chroniqueur.
        
        Args:
            project_id: Identifiant du projet GCP
            topic_name: Nom du topic Pub/Sub pour le journal introspectif
            credentials_path: Chemin vers le fichier de crédentials de service GCP
            
        Raises:
            HeresyException: Si les crédentials sont invalides ou le client ne peut être créé
        """
        self.project_id = project_id
        self.topic_name = topic_name
        self.credentials_path = credentials_path
        
        try:
            # Instancier le PublisherClient avec les crédentials
            import os
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            
            self.publisher = pubsub_v1.PublisherClient()
            self.topic_path = self.publisher.topic_path(project_id, topic_name)
            
            _log.info(f"Chroniqueur Souverain initialisé. Topic: {self.topic_path}")
            
        except Exception as e:
            error_msg = f"Échec de l'initialisation du Chroniqueur Souverain: {e}"
            _log.error(error_msg)
            raise HeresyException(error_msg) from e
    
    def _transmettre_en_arriere_plan(self, entrees_journal: List[str]):
        """
        Rituel privé de transmission exécuté dans un thread séparé.
        
        Boucle sur chaque entrée du journal et la publie sur le topic GCP Pub/Sub.
        Protégé par une garde sacrée pour capturer les erreurs de publication.
        
        Args:
            entrees_journal: Liste des entrées de journal à transmettre
        """
        _log.info(f"Début de la transmission de {len(entrees_journal)} entrées vers le Dojo Cloud.")
        
        try:
            for entree in entrees_journal:
                # Convertir l'entrée en bytes (encodage UTF-8)
                data_bytes = entree.encode('utf-8')
                
                # Publier sur le topic
                future = self.publisher.publish(self.topic_path, data=data_bytes)
                
                # Attendre la confirmation (optionnel, mais garantit la livraison)
                # On peut aussi le faire de manière fire-and-forget
                try:
                    message_id = future.result(timeout=5.0)
                    _log.debug(f"Entrée transmise avec succès. Message ID: {message_id}")
                except Exception as pub_error:
                    _log.warning(f"Erreur lors de la publication d'une entrée: {pub_error}")
            
            _log.info(f"Transmission terminée. {len(entrees_journal)} entrées envoyées au Dojo Cloud.")
            
        except Exception as e:
            _log.error(f"Erreur critique lors de la transmission en arrière-plan: {e}", exc_info=True)
    
    def transmettre_chroniques(self, entrees_journal: List[str]):
        """
        Rituel public pour lancer la transmission des chroniques.
        
        Lance le rituel _transmettre_en_arriere_plan dans un nouveau thread,
        garantissant que l'Orchestrateur n'attend jamais.
        
        Args:
            entrees_journal: Liste des entrées de journal à transmettre
        """
        if not entrees_journal:
            _log.debug("Aucune entrée de journal à transmettre.")
            return
        
        _log.info(f"Lancement de la transmission asynchrone de {len(entrees_journal)} chroniques.")
        
        # Créer et démarrer un thread pour la transmission
        thread = threading.Thread(
            target=self._transmettre_en_arriere_plan,
            args=(entrees_journal,),
            daemon=True  # Thread daemon pour ne pas bloquer l'extinction du Vaisseau
        )
        thread.start()
        
        _log.debug("Thread de transmission lancé. L'Orchestrateur continue son œuvre.")
# --- END OF FILE: guardian/chroniqueur_souverain.py ---
