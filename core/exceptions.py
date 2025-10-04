# --- START OF FILE: core/exceptions.py ---
"""
Le Sanctuaire des Hérésies.

Le "Pourquoi": Ce module définit les exceptions personnalisées du Vaisseau.
Utiliser des exceptions spécifiques permet une gestion des erreurs plus fine et
plus explicite, distinguant les erreurs de logique interne (Hérésies) des
erreurs systèmes ou réseau. C'est la base d'un code robuste.
"""

class HeresyException(Exception):
    """Hérésie fondamentale, la base de toutes les erreurs doctrinales du Vaisseau."""
    pass

class NativeBodyCreationFailed(HeresyException):
    """
    Hérésie levée lorsque le Corps Natif (la DLL C) ne peut être instancié.
    Cela indique un problème fatal au démarrage, souvent lié à une DLL manquante,
    corrompue, ou une incompatibilité d'architecture (32/64 bits).
    """
    pass

class OracleSickness(HeresyException):
    """
    Hérésie levée lorsque l'Oracle (le LLM) est injoignable ou renvoie une réponse
    invalide après plusieurs tentatives. Le Vaisseau doit pouvoir continuer à
    fonctionner en mode dégradé même si son intelligence supérieure est coupée.
    """
    pass

class InvalidActionError(HeresyException):
    """
    Hérésie levée lorsqu'une action proposée par l'Oracle est jugée invalide ou
    dangereuse par les protocoles de sécurité internes (Cerberus).
    """
    pass
# --- END OF FILE: core/exceptions.py ---
