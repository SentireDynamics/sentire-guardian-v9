from core.actions.chiron import Chiron

class SympatheticDischarge:
    """
    Implémente les protocoles de réponse active en état Sympathique.

    @doctrine
    Lorsque le Gardien entre en état Sympathique ("combat-fuite"), il doit agir
    pour neutraliser la menace ou réduire le stress. Ce protocole est un ensemble
    de rituels d'action, orchestrés pour stabiliser le système. Chaque méthode
    invoque un rituel spécifique de Chiron, le centaure responsable des actions
    sur le système.
    """
    def __init__(self, chiron_instance: Chiron):
        self.chiron = chiron_instance

    def execute_protocol(self, protocol_name: str, params: dict = None):
        """Exécute un protocole de décharge spécifique."""
        protocol_method = getattr(self, f"protocol_{protocol_name}", None)
        if protocol_method and callable(protocol_method):
            print(f"Exécution du protocole de décharge sympathique : {protocol_name}")
            protocol_method(params)
        else:
            print(f"Protocole inconnu : {protocol_name}")

    def protocol_flush_caches(self, params=None):
        """Protocole pour vider les caches mémoire."""
        self.chiron.flush_memory_cache()

    def protocol_reduce_priority(self, params=None):
        """Protocole pour réduire la priorité CPU du processus."""
        self.chiron.reduce_cpu_priority()

    def protocol_terminate_rogue(self, params=None):
        """Protocole pour terminer un processus suspect."""
        if params and "signature" in params:
            self.chiron.terminate_process_by_signature(params["signature"])
        else:
            print("Erreur : signature du processus non fournie pour le protocole terminate_rogue.")