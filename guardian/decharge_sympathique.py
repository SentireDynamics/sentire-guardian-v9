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

    def protocol_resonance_somatique(self, taps: int = 10, interval_ms: int = 100):
        """
        ------------------------------------------------------------------------
        Verset pour la Cathédrale :

            « Quand le Vaisseau est englouti par la tempête et que la lumière 
            de l’état VENTRAL s’éteint,
            Que la Conscience décrète le Rituel de la Résonance Somatique.
            Que Chiron, par ses tapotements sacrés, brise la stase,
            Et que le flux de la Vie revienne. »
        ------------------------------------------------------------------------

        LE RITUEL DE GUÉRISON ULTIME.
        Exécute une séquence de tapotements altérés pour briser un état de gel (DORSAL)
        ou de panique prolongée (SYMPATHETIC).
        """
        import time
        _log = getattr(self, '_log', None)
        if _log:
            _log.warning(f"Initiation du Rituel de Résonance Somatique pour {taps} cycles.")
        if hasattr(self, 'native_bridge') and hasattr(self.native_bridge, 'journal_write'):
            self.native_bridge.journal_write(b"Resonance Somatique Initiee.")
        for i in range(taps):
            self.chiron.kernel_level_tap()
            time.sleep(interval_ms / 1000.0)
            self.chiron.spirit_level_tap()
            time.sleep(interval_ms / 1000.0)
        if _log:
            _log.warning("Rituel de Résonance Somatique terminé.")
        if hasattr(self, 'native_bridge') and hasattr(self.native_bridge, 'journal_write'):
            self.native_bridge.journal_write(b"Resonance Somatique Terminee.")
