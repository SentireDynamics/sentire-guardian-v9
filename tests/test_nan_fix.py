#!/usr/bin/env python3
"""
Test de validation des corrections NaN
"""
import subprocess
import time
import os

def main():
    print('TEST DE VALIDATION - Verification des Modifications C SDK')

    # Supprimer l'ancien fichier de log s'il existe
    if os.path.exists('soul_debug.log'):
        os.remove('soul_debug.log')

    # Démarrer l'application en arrière-plan
    process = subprocess.Popen(['python', '-m', 'guardian.main'], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             text=True)

    # Attendre 30 secondes pour voir plusieurs cycles
    time.sleep(30)

    # Tuer le processus
    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()

    # Lire la sortie
    stdout, stderr = process.communicate()

    print('=== RECHERCHE DES DIAGNOSTICS C SDK ===')
    if 'DEBUG - d_squared calculé:' in stdout:
        print('SUCCES: Les modifications C SDK sont actives !')
    else:
        print('ECHEC: Les modifications C SDK ne sont pas actives')

    if 'ALERTE MATH - d_squared negatif' in stdout:
        print('SUCCES: La protection contre les valeurs negatives est active !')
    else:
        print('ECHEC: La protection contre les valeurs negatives n\'est pas active')

    # Vérifier le fichier de log
    if os.path.exists('soul_debug.log'):
        with open('soul_debug.log', 'r') as f:
            log_content = f.read()
        
        if 'd²=-' in log_content:
            print('PROBLEME: Valeurs negatives encore presentes dans les logs')
            print('Extrait des logs:')
            lines = log_content.split('\n')
            for line in lines:
                if 'd²=-' in line:
                    print(f'  {line}')
        else:
            print('SUCCES: Aucune valeur negative dans les logs')
    else:
        print('ECHEC: AUCUN FICHIER DE LOG TROUVE')

    print('=== RÉSUMÉ ===')
    print(f'STDOUT contient {len(stdout)} caractères')
    print(f'STDERR contient {len(stderr)} caractères')
    
    # Vérifier s'il y a encore des erreurs NaN
    if 'cannot convert float NaN to integer' in stderr:
        print('ECHEC: Erreurs NaN encore presentes !')
    else:
        print('SUCCES: Aucune erreur NaN detectee !')

if __name__ == '__main__':
    main()
