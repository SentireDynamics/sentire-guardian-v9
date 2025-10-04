import time
from core.consciousness import GuardianConsciousness
from core.state_machine import StateMachine, GuardianState
from guardian.perception_oracle import PerceptionOracle
from guardian.intuition import AnomalyDetector
from guardian.ffi.native_bridge import NativeBridge

def resilience_loop():
    """
    La boucle de conscience principale du Gardien.
    Elle perçoit, analyse, décide et agit en un cycle continu.
    """
    # Initialisation des composants
    state_machine = StateMachine(initial_state=GuardianState.VENTRAL)
    consciousness = GuardianConsciousness()
    perception_oracle = PerceptionOracle()
    anomaly_detector = AnomalyDetector()

    # Établissement de la connexion synaptique avec le Corps Natif
    try:
        # Le chemin peut nécessiter un ajustement en fonction du système de build
        native_bridge = NativeBridge("./build/libsentire_core.so")
    except FileNotFoundError as e:
        print(f"ERREUR CRITIQUE: Impossible d'établir le lien avec le Corps Natif. {e}")
        return

    print("Gardien V9 initialisé. Entrée dans la boucle de résilience...")

    while True:
        # 1. PERCEPTION : Collecte des stimuli
        metrics = perception_oracle.get_system_metrics()
        anomaly_score = anomaly_detector.predict_anomaly(metrics)

        stimulus = {**metrics, "anomaly_score": anomaly_score}

        # 2. ANALYSE : Invocation du Corps Natif via le pont FFI
        current_state = state_machine.get_current_state()
        new_state = native_bridge.process_stimulus(stimulus, current_state)

        # 3. MISE À JOUR : L'Esprit accepte le nouvel état déterminé par le Corps
        if new_state != current_state:
            print(f"Transition d'état: {current_state.name} -> {new_state.name}")
            state_machine.set_current_state(new_state)

        # 4. DÉCISION & ACTION : La Conscience détermine la prochaine étape
        consciousness.update_state(state_machine.get_current_state())
        action = consciousness.decide_next_action()
        if action:
            print(f"Action décidée : {action['type']} avec les paramètres {action.get('params')}")
            # L'implémentation de l'exécution de l'action serait ici.
            # action_executor.execute(action)

        time.sleep(5)

if __name__ == "__main__":
    resilience_loop()