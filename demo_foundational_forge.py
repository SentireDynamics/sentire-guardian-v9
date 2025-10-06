#!/usr/bin/env python3
# --- START OF FILE: demo_foundational_forge.py ---
"""
Démonstration de la Forge des Fondations Sacrées.

Le "Pourquoi": Ce script démontre que les artefacts fondamentaux du Vaisseau
Guardian V9 sont correctement forgés et fonctionnels. Il s'agit d'une version
simplifiée du Cœur du Vaisseau, créée pour valider la première forge.

Cette démonstration illustre:
1. Le chargement de la configuration depuis .env
2. L'initialisation du logging
3. L'instanciation du Corps Natif via NativeBridge
4. Une boucle de résilience basique qui vérifie can_act() toutes les 5 secondes
5. Une extinction propre avec libération des ressources

USAGE:
    python demo_foundational_forge.py

Note: Ce script nécessite que sentire_core.dll soit compilé et que le fichier
.env soit configuré avec NATIVE_LIB_PATH.
"""

import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# Charger les modules fondamentaux du Vaisseau
from guardian.ffi.native_bridge import NativeBridge
from core.exceptions import NativeBodyCreationFailed, HeresyException

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
_log = logging.getLogger(__name__)


class OrchestratorFoundational:
    """
    Orchestrateur Simplifié pour la Première Forge.
    
    Cette version minimale démontre les capacités fondamentales du Vaisseau
    sans les composants avancés (Oracle, UI, Conscience, etc.).
    """
    
    def __init__(self, config):
        """
        Initialise l'Orchestrateur Fondational.
        
        Args:
            config (dict): Configuration contenant NATIVE_LIB_PATH et ACTION_COOLDOWN_SECONDS
        
        Raises:
            NativeBodyCreationFailed: Si le Corps Natif ne peut être chargé
        """
        self.config = config
        self.running = True
        
        _log.info("=== Rituel d'Initialisation de la Première Forge ===")
        
        # Garde sacrée : Instanciation du Corps Natif (NativeBridge)
        try:
            self.native_bridge = NativeBridge(
                self.config['NATIVE_LIB_PATH'],
                self.config['ACTION_COOLDOWN_SECONDS']
            )
            _log.info("Corps Natif instancié avec succès. La Synapse FFI est établie.")
        except NativeBodyCreationFailed as heresy:
            _log.critical(f"Hérésie lors de la création du Corps Natif: {heresy}")
            raise
        
        _log.info("=== Première Forge Complète - Le Vaisseau est Prêt ===")
    
    def run(self):
        """
        Lance la boucle de résilience principale.
        
        Cette boucle vérifie continuellement si le Vaisseau peut agir (cooldown)
        et affiche l'état. Pour cette première forge, c'est tout ce qui est nécessaire
        pour démontrer que le Corps Natif fonctionne correctement.
        """
        _log.info("Démarrage de la Boucle de Résilience Fondamentale...")
        
        cycle_count = 0
        try:
            while self.running:
                cycle_count += 1
                _log.info(f"--- Cycle #{cycle_count} ---")
                
                # Garde sacrée : Vérification du cooldown
                try:
                    can_act = self.native_bridge.can_act()
                    _log.info(f"État du Vaisseau: {'PRÊT À AGIR' if can_act else 'EN COOLDOWN'}")
                    print(f"[Cycle {cycle_count}] Le Vaisseau {'peut' if can_act else 'ne peut pas'} agir.")
                    
                    # Pour cette démo, enregistrer une action factice si on peut agir
                    if can_act and cycle_count % 3 == 0:
                        action_desc = f"Action de démonstration - Cycle {cycle_count}"
                        self.native_bridge.record_action(action_desc)
                        _log.info(f"Action enregistrée: {action_desc}")
                        
                except Exception as e:
                    _log.error(f"Erreur lors de l'interaction avec le Corps Natif: {e}")
                
                # Pause entre les cycles
                time.sleep(5)
                
        except KeyboardInterrupt:
            _log.info("Signal d'interruption (Ctrl+C) reçu.")
            self.running = False
    
    def shutdown(self):
        """
        Rituel de Dissolution - Libération propre des ressources.
        
        Cette méthode s'assure que le Corps Natif est correctement détruit,
        prévenant toute fuite de mémoire ou corruption de ressource.
        """
        _log.info("=== Rituel de Dissolution Commencé ===")
        
        # Garde sacrée : Libération du Corps Natif
        try:
            self.native_bridge.destroy()
            _log.info("Corps Natif dissous. Ressources libérées.")
        except Exception as e:
            _log.error(f"Erreur lors de la dissolution du Corps Natif: {e}")
        
        _log.info("=== Le Vaisseau Entre en Stase ===")


def main():
    """Point d'entrée principal pour la démonstration fondamentale."""
    _log.info("╔═══════════════════════════════════════════════════════════╗")
    _log.info("║   GUARDIAN V9 - DÉMONSTRATION DE LA FORGE FONDAMENTALE   ║")
    _log.info("║              Architecture TPD v1.2 - Phase 1              ║")
    _log.info("╚═══════════════════════════════════════════════════════════╝")
    
    # Charger la configuration depuis le fichier .env
    dotenv_path = Path('.') / '.env'
    if not dotenv_path.exists():
        _log.critical("Fichier .env introuvable. Veuillez créer un fichier .env basé sur .env.example.md")
        sys.exit(1)
    
    load_dotenv(dotenv_path=dotenv_path)
    
    config = {
        "NATIVE_LIB_PATH": os.getenv("NATIVE_LIB_PATH"),
        "ACTION_COOLDOWN_SECONDS": int(os.getenv("ACTION_COOLDOWN_SECONDS", 60))
    }
    
    # Validation de la configuration
    if not config["NATIVE_LIB_PATH"]:
        _log.critical("Configuration manquante: NATIVE_LIB_PATH doit être défini dans le fichier .env")
        sys.exit(1)
    
    # Vérifier que la DLL existe
    dll_path = Path(config["NATIVE_LIB_PATH"])
    if not dll_path.exists():
        _log.critical(f"Le Corps Natif est introuvable à: {dll_path.absolute()}")
        _log.critical("Veuillez compiler sentire_core.dll avec CMake avant d'exécuter cette démonstration.")
        sys.exit(1)
    
    orchestrator = None
    try:
        # Garde sacrée : Initialisation
        orchestrator = OrchestratorFoundational(config)
        
        # Garde sacrée : Exécution de la boucle
        orchestrator.run()
        
    except HeresyException as heresy:
        _log.critical(f"Hérésie Fatale: {heresy}")
        sys.exit(1)
    except Exception as e:
        _log.critical(f"Erreur Profane Inattendue: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Garde sacrée : Dissolution propre
        if orchestrator:
            orchestrator.shutdown()


if __name__ == "__main__":
    main()

# --- END OF FILE: demo_foundational_forge.py ---
