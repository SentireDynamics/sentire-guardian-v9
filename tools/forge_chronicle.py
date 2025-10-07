# --- START OF FILE: tools/forge_chronicle.py ---
"""
Le Chroniqueur de Forge - LA QUÊTE DU SAINT GRAAL.

Le "Pourquoi": Cet outil sacré collecte le Jeu de Données qui sera la base de toutes
les futures prophéties (Phase III - TimesFM) et détections d'anomalies (Phase II - ML).
Il synchronise les métriques système (CPU, GPU, Mémoire) avec la "vérité terrain" du
frametime obtenue via PresentMon, créant ainsi un corpus d'entraînement de qualité
divine pour les modèles futurs.

Ce n'est PAS une partie du Vaisseau - c'est un outil pour nous, les Architectes.
"""
import subprocess
import time
import psutil
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional
import logging
import sys
import io

# Configurer l'encodage UTF-8 pour Windows
# Le "Pourquoi": Windows utilise cp1252 par défaut, ce qui empêche l'affichage
# des caractères Unicode (bordures, émojis). On force UTF-8 pour la sortie.
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Tentative d'import pynvml pour GPU
try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False
    print("⚠️  GPU monitoring non disponible (pynvml manquant)")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
_log = logging.getLogger(__name__)


class ForgeChronicler:
    """
    Le Chroniqueur de Forge - Collecteur du Jeu de Données Sacré.
    """
    
    def __init__(self, output_dir: str = "data/chronicles"):
        """
        Initialise le Chroniqueur.
        
        Args:
            output_dir: Répertoire où sauvegarder les chroniques
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chronicle_data = []
        self.presentmon_process = None
        self.presentmon_csv_path = None
        
    def chronicle_benchmark(
        self, 
        app_path: str,
        duration_seconds: int = 60,
        sample_rate_hz: int = 5,
        presentmon_path: Optional[str] = None,
        app_args: Optional[list] = None
    ):
        """
        Lance un benchmark et collecte toutes les métriques.
        
        Le "Pourquoi": Ce rituel est le cœur du Chroniqueur. Il orchestre trois
        flux de données en parallèle :
        1. Lancement de l'application cible (ex: Superposition Benchmark)
        2. Collecte haute fréquence des métriques système (CPU/GPU/RAM)
        3. Collecte de la vérité terrain frametime via PresentMon
        
        La synchronisation temporelle de ces trois flux produit le Saint Graal :
        un dataset où chaque frametime est associé à son contexte système exact.
        
        Args:
            app_path: Chemin vers l'application à benchmarker
            duration_seconds: Durée du benchmark en secondes
            sample_rate_hz: Fréquence d'échantillonnage (samples par seconde)
            presentmon_path: Chemin vers PresentMon.exe (optionnel, cherche dans PATH)
            app_args: Arguments supplémentaires pour l'application (liste)
        """
        _log.info(f"🔥 Début de la Chronique de Forge")
        _log.info(f"📁 Application cible: {app_path}")
        _log.info(f"⏱️  Durée: {duration_seconds}s à {sample_rate_hz}Hz")
        
        # Préparer PresentMon si disponible
        if presentmon_path:
            self.presentmon_csv_path = self.output_dir / f"presentmon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            _log.info(f"📊 PresentMon sera utilisé: {presentmon_path}")
        else:
            _log.warning("⚠️  PresentMon non spécifié, frametime réel non disponible")
        
        # Lancer PresentMon AVANT l'application si disponible
        # Le "Pourquoi": PresentMon v2.x doit être lancé AVANT l'application cible
        # pour détecter le démarrage du processus et commencer la capture dès la première frame.
        if presentmon_path and self.presentmon_csv_path:
            try:
                # PresentMon v2.x : syntaxe purifiée et validée
                # Le "Pourquoi": PresentMon v2.x utilise une syntaxe simplifiée.
                # -process_name : nom du processus sans .exe (ex: "superposition")
                # -output_file : fichier CSV de sortie
                # PresentMon continuera automatiquement jusqu'à la fin du processus.
                process_name = Path(app_path).stem  # Extraire "superposition" de "superposition.exe"
                
                _log.info(f"📊 Lancement de PresentMon (en attente du processus '{process_name}')...")
                
                # Utiliser un chemin absolu pour le fichier de sortie
                # Le "Pourquoi": PresentMon peut ne pas comprendre les chemins relatifs
                presentmon_csv_abs = self.presentmon_csv_path.resolve()
                _log.debug(f"   Fichier de sortie: {presentmon_csv_abs}")
                
                self.presentmon_process = subprocess.Popen(
                    [
                        presentmon_path,
                        "-process_name", process_name,
                        "-output_file", str(presentmon_csv_abs),
                        "--stop_existing_session"  # Arrêter les sessions existantes
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                _log.info(f"✅ PresentMon lancé (PID: {self.presentmon_process.pid})")
                time.sleep(2)  # Laisser PresentMon s'initialiser complètement
            except Exception as e:
                _log.warning(f"⚠️  PresentMon non lancé: {e}")
                self.presentmon_process = None
        
        # Lancer l'application cible
        _log.info(f"🚀 Lancement de l'application cible...")
        
        # Extraire la Terre Natale : Le répertoire où réside l'application
        # Le "Pourquoi": Les applications (surtout les benchmarks) ont besoin d'être
        # lancées depuis leur propre répertoire pour trouver leurs ressources
        # (DLLs, assets, configurations). Sans cwd, elles cherchent dans le répertoire
        # du Chroniqueur et échouent.
        app_directory = str(Path(app_path).parent.resolve())
        _log.debug(f"📍 Terre Natale de l'application: {app_directory}")
        
        try:
            # CRUCIAL pour Windows : passer le chemin comme liste pour gérer les espaces
            # Le "Pourquoi": Sur Windows, subprocess.Popen avec une string simple peut mal
            # interpréter les espaces dans les chemins ("C:\Program Files\..."). En passant
            # le chemin comme liste [app_path], Python gère correctement les guillemets et
            # les espaces, évitant les crashs immédiats de l'application.
            
            # Préparer la commande avec arguments si fournis
            # Le "Pourquoi": Certaines applications (comme Superposition) nécessitent
            # des arguments en ligne de commande pour tourner en mode automatique/headless.
            # Sans arguments, elles se lancent puis se ferment immédiatement (exit code 0).
            command = [app_path]
            if app_args:
                command.extend(app_args)
                _log.info(f"📋 Arguments de l'application: {' '.join(app_args)}")
            
            # Capturer stderr pour diagnostic si l'app crash
            target_process = subprocess.Popen(
                command,  # ← Commande complète avec arguments
                cwd=app_directory,  # Sceau sacré : Lance l'app sur sa propre terre
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            _log.info(f"✅ Application lancée (PID: {target_process.pid})")
            
            # Vérifier immédiatement si l'app crash
            time.sleep(0.5)
            poll_result = target_process.poll()
            if poll_result is not None:
                # App a crashé immédiatement - récupérer stderr
                _, stderr = target_process.communicate(timeout=1)
                error_msg = stderr.decode('utf-8', errors='ignore') if stderr else "Aucun message d'erreur"
                _log.error(f"❌ Application crashée immédiatement (code: {poll_result})")
                _log.error(f"   Message d'erreur: {error_msg[:500]}")  # Limiter à 500 chars
                return None
        except Exception as e:
            _log.error(f"❌ Échec du lancement: {e}")
            return None
        
        # Attendre que l'app démarre complètement
        time.sleep(2)  # Réduit de 3s à 2s car on a déjà attendu 0.5s ci-dessus
        
        # Collecter les métriques en boucle
        _log.info(f"📈 Début de la collecte (durée: {duration_seconds}s)...")
        sample_interval = 1.0 / sample_rate_hz
        start_time = time.time()
        samples_collected = 0
        
        while time.time() - start_time < duration_seconds:
            try:
                # Vérifier que l'app tourne toujours
                if target_process.poll() is not None:
                    _log.warning("⚠️  Application cible terminée prématurément")
                    break
                
                # Collecter métriques système
                timestamp = time.time()
                metrics = self._collect_system_metrics(timestamp)
                
                if metrics:
                    self.chronicle_data.append(metrics)
                    samples_collected += 1
                    
                    # Log périodique
                    if samples_collected % (sample_rate_hz * 10) == 0:
                        _log.info(f"📊 Échantillons collectés: {samples_collected}")
                
                time.sleep(sample_interval)
                
            except KeyboardInterrupt:
                _log.info("⚠️  Interruption utilisateur")
                break
        
        # Terminer l'app cible si elle tourne encore
        if target_process.poll() is None:
            _log.info("🛑 Arrêt de l'application cible...")
            target_process.terminate()
            try:
                target_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                target_process.kill()
        
        # Attendre PresentMon si lancé
        if self.presentmon_process and self.presentmon_process.poll() is None:
            _log.info("⏳ Attente de la finalisation de PresentMon...")
            try:
                self.presentmon_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.presentmon_process.kill()
        
        # Vérifier si PresentMon a écrit des erreurs
        if self.presentmon_process:
            try:
                stdout, stderr = self.presentmon_process.communicate(timeout=1)
                if stderr:
                    stderr_text = stderr.decode('utf-8', errors='ignore').strip()
                    if stderr_text:
                        _log.warning(f"⚠️  PresentMon stderr: {stderr_text[:500]}")
            except:
                pass  # Ignorer les erreurs de lecture
        
        _log.info(f"✅ Collecte terminée: {samples_collected} échantillons")
        
        # Sauvegarder les données
        output_file = self._save_chronicle_data()
        
        # Fusionner avec PresentMon si disponible
        if self.presentmon_csv_path and self.presentmon_csv_path.exists():
            merged_file = self._merge_with_presentmon(output_file)
            _log.info(f"✅ Jeu de Données Sacré créé: {merged_file}")
            return merged_file
        else:
            _log.info(f"✅ Chronique sauvegardée: {output_file}")
            return output_file
    
    def _collect_system_metrics(self, timestamp: float) -> Optional[dict]:
        """
        Collecte les métriques système à un instant T.
        
        Returns:
            dict avec timestamp et toutes les métriques
        """
        try:
            metrics = {
                "timestamp": timestamp,
                "cpu_usage": psutil.cpu_percent(interval=0),
                "memory_usage": psutil.virtual_memory().percent,
            }
            
            # GPU si disponible
            if GPU_AVAILABLE:
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    metrics["gpu_usage"] = float(util.gpu)
                    metrics["gpu_temp"] = float(temp)
                except:
                    metrics["gpu_usage"] = None
                    metrics["gpu_temp"] = None
            else:
                metrics["gpu_usage"] = None
                metrics["gpu_temp"] = None
            
            return metrics
        except Exception as e:
            _log.debug(f"Échec collecte: {e}")
            return None
    
    def _save_chronicle_data(self) -> Path:
        """Sauvegarde les métriques collectées en CSV."""
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f"chronicle_system_{timestamp_str}.csv"
        
        if not self.chronicle_data:
            _log.warning("⚠️  Aucune donnée à sauvegarder")
            return output_file
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = self.chronicle_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.chronicle_data)
        
        _log.info(f"💾 Chronique système sauvegardée: {output_file}")
        return output_file
    
    def _merge_with_presentmon(self, system_file: Path) -> Path:
        """
        Fusionne les métriques système avec les données PresentMon.
        
        Le "Pourquoi": C'est le rituel le plus sacré. Il aligne temporellement
        les métriques système avec le frametime réel via une fusion temporelle précise.
        pandas.merge_asof effectue une interpolation temporelle pour associer chaque
        frametime au contexte système le plus proche dans le temps. C'est la vérité
        divine de la synchronisation temporelle.
        
        Returns:
            Path du fichier fusionné
        """
        if not self.presentmon_csv_path.exists():
            _log.warning(f"⚠️  Fichier PresentMon non trouvé: {self.presentmon_csv_path}")
            return system_file
        
        _log.info(f"🔗 Fusion temporelle des données PresentMon avec métriques système...")
        
        try:
            # Lire les données système avec pandas
            df_system = pd.read_csv(system_file)
            _log.info(f"📊 Données système chargées: {len(df_system)} échantillons")
            
            # Lire les données PresentMon avec pandas
            df_presentmon = pd.read_csv(self.presentmon_csv_path)
            _log.info(f"📊 Données PresentMon chargées: {len(df_presentmon)} échantillons")
            
            # Convertir les timestamps en datetime pour fusion temporelle précise
            # Les timestamps système sont en format Unix (float)
            df_system['timestamp_dt'] = pd.to_datetime(df_system['timestamp'], unit='s')
            
            # PresentMon v2.x utilise "TimeInMs" (millisecondes depuis le début de la capture)
            # Le "Pourquoi": PresentMon v2.x démarre son horloge à 0 et incrémente en ms.
            # On doit convertir ce temps relatif en timestamp absolu Unix pour le fusionner
            # avec les métriques système qui utilisent time.time() (timestamp Unix).
            if 'TimeInMs' in df_presentmon.columns:
                # Calculer le timestamp de départ (premier échantillon système)
                start_time = df_system['timestamp'].iloc[0]
                # Convertir TimeInMs (millisecondes) en secondes, puis en timestamp absolu
                df_presentmon['timestamp_dt'] = pd.to_datetime(
                    start_time + (df_presentmon['TimeInMs'] / 1000.0),  # ms → secondes
                    unit='s'
                )
            else:
                _log.error("❌ Colonne 'TimeInMs' non trouvée dans PresentMon v2.x")
                _log.info(f"   Colonnes disponibles: {list(df_presentmon.columns)}")
                return system_file
            
            # Extraire le frametime (MsBetweenPresents dans PresentMon v2.x)
            # Le "Pourquoi": C'est LA métrique sacrée - le temps entre deux frames.
            # Plus ce nombre est bas, plus le FPS est élevé (FPS = 1000 / MsBetweenPresents).
            if 'MsBetweenPresents' in df_presentmon.columns:
                df_presentmon_clean = df_presentmon[['timestamp_dt', 'MsBetweenPresents']].copy()
                df_presentmon_clean.rename(columns={'MsBetweenPresents': 'frametime_ms'}, inplace=True)
            else:
                _log.warning("⚠️  Colonne 'MsBetweenPresents' non trouvée, tentative alternatives...")
                # Chercher colonnes alternatives
                frametime_cols = [col for col in df_presentmon.columns if 'between' in col.lower() and 'ms' in col.lower()]
                if frametime_cols:
                    _log.info(f"📊 Utilisation de la colonne alternative: {frametime_cols[0]}")
                    df_presentmon_clean = df_presentmon[['timestamp_dt', frametime_cols[0]]].copy()
                    df_presentmon_clean.rename(columns={frametime_cols[0]: 'frametime_ms'}, inplace=True)
                else:
                    _log.error("❌ Aucune colonne frametime trouvée")
                    _log.info(f"   Colonnes disponibles: {list(df_presentmon.columns)}")
                    return system_file
            
            # Trier par timestamp pour merge_asof
            df_system = df_system.sort_values('timestamp_dt')
            df_presentmon_clean = df_presentmon_clean.sort_values('timestamp_dt')
            
            # LE RITUEL SACRÉ : Fusion temporelle inversée
            # Le "Pourquoi": On veut PRÉSERVER les 98k+ frametimes de PresentMon, pas les 299 échantillons système.
            # merge_asof avec PresentMon comme base associe chaque frametime au contexte système le plus proche.
            # direction='backward' = utiliser le dernier échantillon système disponible avant ce frametime.
            # Cela crée un dataset de 98k+ lignes, parfait pour le ML !
            _log.info("🔗 Exécution du rituel sacré : merge_asof inversé...")
            df_merged = pd.merge_asof(
                df_presentmon_clean,  # ← Base = PresentMon (haute fréquence)
                df_system,            # ← Associer les métriques système
                on='timestamp_dt',
                direction='backward',  # Utiliser le dernier échantillon système avant ce frame
                tolerance=pd.Timedelta(seconds=0.5)  # Tolérance réduite à 500ms
            )
            
            # Nettoyer : supprimer la colonne timestamp_dt temporaire
            df_merged = df_merged.drop(columns=['timestamp_dt'])
            
            # Créer fichier fusionné
            merged_file = self.output_dir / f"sacred_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Sauvegarder
            df_merged.to_csv(merged_file, index=False, encoding='utf-8')
            
            _log.info(f"✅ Jeu de Données Sacré fusionné: {merged_file}")
            _log.info(f"📊 Lignes totales: {len(df_merged)}")
            _log.info(f"📊 Colonnes: {list(df_merged.columns)}")
            
            # Statistiques de qualité
            frametime_valid = df_merged['frametime_ms'].notna().sum()
            frametime_ratio = (frametime_valid / len(df_merged)) * 100
            _log.info(f"✅ Frametimes valides: {frametime_valid}/{len(df_merged)} ({frametime_ratio:.1f}%)")
            
            return merged_file
            
        except Exception as e:
            _log.error(f"❌ Erreur lors de la fusion pandas: {e}", exc_info=True)
            return system_file


def main():
    """Point d'entrée du Chroniqueur de Forge."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Chroniqueur de Forge - Collecte du Jeu de Données Sacré"
    )
    parser.add_argument(
        "app_path",
        help="Chemin vers l'application à benchmarker (ex: Superposition.exe)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Durée du benchmark en secondes (défaut: 60)"
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=5,
        help="Fréquence d'échantillonnage en Hz (défaut: 5)"
    )
    parser.add_argument(
        "--presentmon",
        help="Chemin vers PresentMon.exe (optionnel)"
    )
    parser.add_argument(
        "--output-dir",
        default="data/chronicles",
        help="Répertoire de sortie (défaut: data/chronicles)"
    )
    parser.add_argument(
        "--app-args",
        type=str,
        help="Arguments supplémentaires pour l'application entre guillemets (ex: --app-args \"-video_app direct3d11 -sound_app null\")"
    )
    
    args = parser.parse_args()
    
    # Afficher bannière
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  CHRONIQUEUR DE FORGE - LA QUÊTE DU SAINT GRAAL            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Vérifier que l'app existe
    if not Path(args.app_path).exists():
        _log.error(f"❌ Application non trouvée: {args.app_path}")
        return 1
    
    # Créer le chroniqueur
    chronicler = ForgeChronicler(output_dir=args.output_dir)
    
    # Préparer les arguments de l'application
    app_args_list = None
    if args.app_args:
        # Convertir la string d'arguments en liste
        # Ex: "-video_app direct3d11 -sound_app null" -> ["-video_app", "direct3d11", "-sound_app", "null"]
        import shlex
        app_args_list = shlex.split(args.app_args)
    
    # Lancer la chronique
    try:
        output_file = chronicler.chronicle_benchmark(
            app_path=args.app_path,
            duration_seconds=args.duration,
            sample_rate_hz=args.sample_rate,
            presentmon_path=args.presentmon,
            app_args=app_args_list
        )
        
        if output_file:
            print()
            print("╔════════════════════════════════════════════════════════════╗")
            print("║  SUCCÈS - JEU DE DONNÉES SACRÉ CRÉÉ                        ║")
            print("╚════════════════════════════════════════════════════════════╝")
            print()
            print(f"📁 Fichier: {output_file}")
            print(f"📊 Échantillons: {len(chronicler.chronicle_data)}")
            print()
            print("Ce fichier peut être utilisé pour:")
            print("  - Entraîner l'IntuitionEngine (Phase II)")
            print("  - Fine-tuner TimesFM (Phase III)")
            print("  - Analyser les patterns système")
            print()
            print("Gloire à la Sagesse Collectée ! 🛡️")
            return 0
        else:
            _log.error("❌ Échec de la chronique")
            return 1
            
    except KeyboardInterrupt:
        _log.info("⚠️  Chronique interrompue par l'utilisateur")
        return 1
    except Exception as e:
        _log.error(f"❌ Erreur fatale: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
# --- END OF FILE: tools/forge_chronicle.py ---

