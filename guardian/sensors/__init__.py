# --- START OF FILE: guardian/sensors/__init__.py ---
"""
Le Sanctuaire des Senseurs.

Le "Pourquoi": Ce module contient tous les senseurs qui permettent au Vaisseau
de percevoir le monde extérieur. Chaque senseur respecte le Pacte Sacré défini
dans base_sensor.py et fournit des métriques quantitatives sur l'environnement.
"""
from .base_sensor import BaseSensor
from .log_file_sensor import LogFileSensor

__all__ = ['BaseSensor', 'LogFileSensor']
# --- END OF FILE: guardian/sensors/__init__.py ---
