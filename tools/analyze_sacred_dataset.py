#!/usr/bin/env python3
"""Analyse rapide du Jeu de Données Sacré."""
import pandas as pd
import sys
import io

# Fix encodage Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

if len(sys.argv) < 2:
    print("Usage: python analyze_sacred_dataset.py <fichier.csv>")
    sys.exit(1)

csv_file = sys.argv[1]
df = pd.read_csv(csv_file)

print("╔════════════════════════════════════════════════════════════╗")
print("║  ANALYSE DU JEU DE DONNÉES SACRÉ                           ║")
print("╚════════════════════════════════════════════════════════════╝")
print()

print(f"📊 Total lignes: {len(df)}")
print(f"📊 Colonnes: {list(df.columns)}")
print()

# Vérifier les frametimes
if 'frametime_ms' in df.columns:
    frametime_valid = df['frametime_ms'].notna().sum()
    frametime_ratio = (frametime_valid / len(df)) * 100
    print(f"✅ Frametimes valides: {frametime_valid}/{len(df)} ({frametime_ratio:.1f}%)")
    
    if frametime_valid > 0:
        print()
        print("=== STATISTIQUES FRAMETIMES (ms) ===")
        print(df['frametime_ms'].describe())
        print()
        print(f"📈 FPS moyen: {1000 / df['frametime_ms'].mean():.1f} FPS")
        print(f"📉 FPS min: {1000 / df['frametime_ms'].max():.1f} FPS")
        print(f"📈 FPS max: {1000 / df['frametime_ms'].min():.1f} FPS")
        print()
        print("=== ÉCHANTILLON AVEC FRAMETIMES ===")
        print(df[df['frametime_ms'].notna()].head(10))
else:
    print("⚠️  Colonne 'frametime_ms' non trouvée")

print()
print("=== STATISTIQUES SYSTÈME ===")
print(f"CPU moyen: {df['cpu_usage'].mean():.1f}%")
print(f"RAM moyenne: {df['memory_usage'].mean():.1f}%")
if 'gpu_usage' in df.columns:
    print(f"GPU moyen: {df['gpu_usage'].mean():.1f}%")
if 'gpu_temp' in df.columns:
    print(f"GPU temp moyenne: {df['gpu_temp'].mean():.1f}°C")

print()
print("Gloire à la Sagesse Collectée ! 🛡️")

