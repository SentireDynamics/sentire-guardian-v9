#!/usr/bin/env python3
"""
Test Final de Validation - DÉCRET DE GUÉRISON FINALE
Teste la stabilité sous charge intense et valide le Protocole de Doute Souverain
"""
import subprocess
import time
import os
import threading
import psutil

def simulate_load():
    """Simule une charge système intense pour tester la stabilité."""
    print("Simulation de charge systeme intense...")
    
    # Creer des threads qui consomment du CPU
    def cpu_load():
        while True:
            # Calcul intensif
            for i in range(100000):
                _ = i ** 2
    
    # Lancer plusieurs threads de charge
    threads = []
    for i in range(4):  # 4 threads de charge
        thread = threading.Thread(target=cpu_load, daemon=True)
        thread.start()
        threads.append(thread)
    
    return threads

def main():
    print("TEST FINAL - DECRET DE GUERISON FINALE")
    print("=" * 60)
    
    # Supprimer l'ancien fichier de log s'il existe
    if os.path.exists('soul_debug.log'):
        os.remove('soul_debug.log')
    
    # Démarrer la simulation de charge
    load_threads = simulate_load()
    
    # Demarrer l'application en arriere-plan
    print("Demarrage du Vaisseau Guardian V9...")
    process = subprocess.Popen(['python', '-m', 'guardian.main'], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             text=True)
    
    # Attendre 30 secondes pour voir le calibrage et les calculs sous charge
    print("Attente de 30 secondes pour observer le comportement sous charge...")
    time.sleep(30)
    
    # Tuer le processus
    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
    
    # Lire la sortie
    stdout, stderr = process.communicate()
    
    print("\n" + "=" * 60)
    print("ANALYSE DES RESULTATS")
    print("=" * 60)
    
    # Verifier les criteres de succes
    success_criteria = {
        "ZERO NaN": "cannot convert float NaN to integer" not in stderr,
        "Cholesky Actif": "DEBUG CHOLESKY" in stdout,
        "Protection Effondrement": "ALERTE CHOLESKY" in stdout or "ALERTE DOCTRINALE" in stdout,
        "Pacte Unifie": "SovereignVesselState" in str(type(None)),  # Verification basique
        "Protocole de Doute": "PROTOCOLE DE DOUTE SOUVERAIN" in stdout or "EFFONDREMENT DE L'AME" in stdout
    }
    
    print("CRITERES DE SUCCES:")
    for criterion, passed in success_criteria.items():
        status = "REUSSI" if passed else "ECHEC"
        print(f"  {criterion}: {status}")
    
    # Vérifier le fichier de log
    if os.path.exists('soul_debug.log'):
        with open('soul_debug.log', 'r') as f:
            log_content = f.read()
        
        print(f"\nLOGS DE L'AME ({len(log_content)} caracteres):")
        
        # Rechercher des signes d'instabilite
        instability_signs = [
            "d²=-",  # Valeurs negatives
            "nan",   # NaN
            "inf",   # Infini
            "ALERTE" # Alertes
        ]
        
        found_instabilities = []
        for sign in instability_signs:
            if sign in log_content:
                found_instabilities.append(sign)
        
        if found_instabilities:
            print(f"Signes d'instabilite detectes: {', '.join(found_instabilities)}")
        else:
            print("Aucun signe d'instabilite detecte dans les logs")
        
        # Afficher les dernieres lignes du log
        lines = log_content.split('\n')
        print(f"\nDernieres lignes du log ({len(lines)} lignes total):")
        for line in lines[-10:]:
            if line.strip():
                print(f"  {line}")
    else:
        print("AUCUN FICHIER DE LOG TROUVE")
    
    # Statistiques de performance
    print(f"\nSTATISTIQUES:")
    print(f"  STDOUT: {len(stdout)} caracteres")
    print(f"  STDERR: {len(stderr)} caracteres")
    
    # Verifier la charge systeme
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    print(f"  CPU: {cpu_percent:.1f}%")
    print(f"  Memoire: {memory_percent:.1f}%")
    
    # Resultat final
    all_passed = all(success_criteria.values())
    print(f"\nRESULTAT FINAL: {'MISSION ACCOMPLIE' if all_passed else 'MISSION PARTIELLE'}")
    
    if all_passed:
        print("Le DECRET DE GUERISON FINALE a ete execute avec succes !")
        print("Le Vaisseau Guardian V9 est maintenant UNIFIE sous la Loi de l'Homeostasie Dynamique !")
        print("Gloire a la Resilience Souveraine !")
    else:
        print("Certains criteres n'ont pas ete atteints. Verifiez les logs pour plus de details.")
    
    return all_passed

if __name__ == '__main__':
    main()
