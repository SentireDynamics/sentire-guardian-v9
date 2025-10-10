#!/usr/bin/env python3
"""
Test de la Phase II - Conscience Éveillée
Épreuve réelle avec processus sacrifié et actions souveraines
"""
import time
import subprocess
import psutil
import pytest

from core.verbe_pur import Stimulus, Action, OracleResponse
from core.actions.chiron import Chiron
from guardian.perception import Perception
from oracle.llama_client import LlamaOracle


def test_phase_ii_real_trial():
    """
    ÉPREUVE RÉELLE (simplifiée):
    - Lance un processus inoffensif (sleep 30)
    - Crée un Stimulus de crise pointant vers ce PID
    - Simule une réponse Oracle recommandant ISOLATE_PROCESS
    - Exécute l'action via Chiron et vérifie l'effet
    """
    # 1. Démon sacrifié
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.Popen(
        ["python", "-c", "import time; time.sleep(30)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=flags
    )
    pid = proc.pid

    try:
        # 2. Stimulus ciblé
        stimulus = Stimulus(
            cpu_usage=95.0,
            memory_usage=10.0,
            foreground_window_title="Test",
            gpu_usage=0.0,
            gpu_temp=None,
            top_cpu_process_pid=pid,
            top_cpu_process_name="python",
            top_mem_process_pid=pid,
            top_mem_process_name="python",
        )

        # 3. Action souveraine directe (simulation Oracle)
        action = Action(
            id="ISOLATE_PROCESS", 
            description="Suspend culprit process", 
            parameters={"pid": pid}
        )

        # 4. Exécution via Chiron
        chiron = Chiron()
        chiron.execute_action(action)

        # 5. Contempler le résultat
        p = psutil.Process(pid)
        # Attendre brièvement que l'état change
        time.sleep(0.2)

        # Sur Windows, le status peut rester 'running' malgré suspend; on teste l'exception sur cpu_times()
        suspended_effect = False
        try:
            _ = p.cpu_times()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            suspended_effect = True

        assert suspended_effect or p.status() in {getattr(psutil, "STATUS_STOPPED", "stopped"), getattr(psutil, "STATUS_SUSPENDED", "suspended")}  # noqa: E501

    finally:
        # Purification finale : arrêter proprement le démon
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
                proc.wait(timeout=3)
            except Exception:
                pass


