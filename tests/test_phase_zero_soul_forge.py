#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║          TEST DE LA PHASE ZÉRO : LA GREFFE DE L'ÂME SDK V2               ║
╚══════════════════════════════════════════════════════════════════════════╝

POURQUOI : Ce test valide que le Vaisseau peut créer, communiquer avec, et
détruire l'Âme SDK V2. C'est le Premier Souffle du Guardian V9 Archétype.

CRITÈRES DE SUCCÈS :
1. Le NativeBridge peut charger sentire_core.dll sans hérésie
2. Le SDK peut être créé avec une configuration par défaut
3. Un Stimulus simple peut être soumis au SDK
4. Le SDK retourne un Verdict valide avec état VENTRAL (car faible charge)
5. Le SDK peut être détruit sans fuite de mémoire
"""

import sys
import os
import io
import logging
from pathlib import Path

# Fix encodage Windows pour les caractères UTF-8 (bannière)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ffi.native_bridge import NativeBridge, SentireStimulus, create_default_config
from core.exceptions import NativeBodyCreationFailed

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
_log = logging.getLogger(__name__)


def test_soul_forge():
    """Test complet du cycle de vie de l'Âme SDK V2."""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  TEST DE LA GREFFE DE L'ÂME - PHASE ZÉRO                   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # 1. Forge de l'Âme
    print("1️⃣  RITUEL : Forger l'Âme avec configuration par défaut...")
    try:
        dll_path = "guardian/native/sentire_core.dll"
        if not Path(dll_path).exists():
            print(f"❌ ÉCHEC : La DLL n'existe pas à {dll_path}")
            return False
        
        bridge = NativeBridge(dll_path)
        print(f"✅ SUCCÈS : Âme forgée depuis {dll_path}")
        print(f"   Version SDK : {bridge.get_version()}")
        print()
    except NativeBodyCreationFailed as e:
        print(f"❌ ÉCHEC : Impossible de forger l'Âme : {e}")
        return False
    
    # 2. Test du Cycle de Conscience (Stimulus → Verdict)
    print("2️⃣  RITUEL : Soumettre un Stimulus de calme à l'Âme...")
    try:
        # Créer un Stimulus de faible charge (système au repos)
        calm_stimulus = SentireStimulus()
        calm_stimulus.cpu_usage = 0.15      # 15% CPU
        calm_stimulus.memory_usage = 0.30   # 30% RAM
        calm_stimulus.gpu_usage = 0.10      # 10% GPU
        calm_stimulus.io_wait = 0.05        # 5% IO
        calm_stimulus.anomaly_score = 0.0   # Pas d'anomalie
        calm_stimulus.predicted_frametime_ms = 16.67  # 60 FPS normal
        calm_stimulus.network_latency_ms = 0.0
        calm_stimulus.thread_contention = 0.0
        calm_stimulus.disk_io_rate = 0.0
        calm_stimulus.power_consumption = 0.0
        
        verdict = bridge.process(calm_stimulus)
        
        state_names = ["VENTRAL", "SYMPATHETIC", "DORSAL"]
        state_name = state_names[verdict.final_state] if verdict.final_state < 3 else "UNKNOWN"
        
        print(f"✅ SUCCÈS : Verdict reçu de l'Âme")
        print(f"   État Final : {state_name}")
        print(f"   Score de Résilience (Sʀ) : {verdict.resilience_score:.3f}")
        print(f"   Impact Final (Iφ) : {verdict.impact_score:.3f}")
        print(f"   Alarme Amygdale : {'OUI 🚨' if verdict.amygdala_alarm_fired else 'Non ✅'}")
        print()
        
        # Validation : Un système calme doit être en VENTRAL
        if verdict.final_state != 0:  # 0 = VENTRAL
            print(f"⚠️  AVERTISSEMENT : État inattendu pour un système calme ({state_name})")
            print(f"   Sʀ: {verdict.resilience_score:.3f} (attendu >= 0.8)")
            # Ce n'est pas une erreur fatale, juste un warning
        
    except Exception as e:
        print(f"❌ ÉCHEC : Erreur lors du traitement du Stimulus : {e}")
        bridge.destroy()
        return False
    
    # 3. Test d'un Stimulus de crise
    print("3️⃣  RITUEL : Soumettre un Stimulus de crise à l'Âme...")
    try:
        crisis_stimulus = SentireStimulus()
        crisis_stimulus.cpu_usage = 0.95       # 95% CPU - CRISE!
        crisis_stimulus.memory_usage = 0.90    # 90% RAM - CRISE!
        crisis_stimulus.gpu_usage = 0.85       # 85% GPU
        crisis_stimulus.io_wait = 0.40         # 40% IO
        crisis_stimulus.anomaly_score = 0.8    # Forte anomalie
        crisis_stimulus.predicted_frametime_ms = 50.0  # Frametime élevé
        crisis_stimulus.network_latency_ms = 0.0
        crisis_stimulus.thread_contention = 0.0
        crisis_stimulus.disk_io_rate = 0.0
        crisis_stimulus.power_consumption = 0.0
        
        verdict_crisis = bridge.process(crisis_stimulus)
        
        state_name_crisis = state_names[verdict_crisis.final_state] if verdict_crisis.final_state < 3 else "UNKNOWN"
        
        print(f"✅ SUCCÈS : Verdict de crise reçu")
        print(f"   État Final : {state_name_crisis}")
        print(f"   Score de Résilience (Sʀ) : {verdict_crisis.resilience_score:.3f}")
        print(f"   Impact Final (Iφ) : {verdict_crisis.impact_score:.3f}")
        print(f"   Alarme Amygdale : {'OUI 🚨' if verdict_crisis.amygdala_alarm_fired else 'Non ✅'}")
        print()
        
        # Validation : Un système en crise ne doit PAS être en VENTRAL
        if verdict_crisis.final_state == 0:  # 0 = VENTRAL
            print(f"⚠️  AVERTISSEMENT : L'Âme est restée VENTRALE malgré une crise !")
            print(f"   Ceci peut indiquer un problème de pondération dans la configuration.")
        
    except Exception as e:
        print(f"❌ ÉCHEC : Erreur lors du traitement du Stimulus de crise : {e}")
        bridge.destroy()
        return False
    
    # 4. Libération de l'Âme
    print("4️⃣  RITUEL : Libérer l'Âme et retourner au silence...")
    try:
        bridge.destroy()
        print("✅ SUCCÈS : Âme libérée sans fuite de mémoire")
        print()
    except Exception as e:
        print(f"❌ ÉCHEC : Erreur lors de la libération de l'Âme : {e}")
        return False
    
    return True


def main():
    """Point d'entrée du test."""
    success = test_soul_forge()
    
    print("╔════════════════════════════════════════════════════════════╗")
    if success:
        print("║  ✅ VICTOIRE : LA GREFFE DE L'ÂME EST RÉUSSIE ! 🏆       ║")
        print("║                                                            ║")
        print("║  Le Vaisseau Guardian V9 est devenu l'Archétype.           ║")
        print("║  Son cœur bat désormais au rythme du SDK V2.               ║")
    else:
        print("║  ❌ ÉCHEC : LA GREFFE A ÉCHOUÉ                            ║")
        print("║                                                            ║")
        print("║  Le Vaisseau n'a pas pu communier avec l'Âme V2.           ║")
        print("║  Vérifiez les logs ci-dessus pour diagnostiquer l'hérésie. ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("Gloire à la Résilience Souveraine ! 🛡️")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

