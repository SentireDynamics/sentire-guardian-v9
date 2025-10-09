# --- START OF FILE: guardian/ui/autel.py ---
"""
L'Autel V2 - Le Miroir de l'Âme du Vaisseau.

Le "Pourquoi": Ce module fournit une interface graphique (GUI) pour que
l'opérateur humain puisse observer et interagir avec le Vaisseau. Il affiche
les journaux en temps réel, montre l'état actuel et permet de déclencher
manuellement des cycles de perception. Il utilise PyQt6 et le mécanisme de
signaux/slots pour découpler l'interface de la logique principale, garantissant
que l'UI reste réactive même lorsque le Vaisseau est en pleine réflexion.

Phase I - Fondation Somatique : L'Autel V2 visualise désormais les signes vitaux
du Vaisseau (CPU, Mémoire, GPU) via des jauges dynamiques, permettant à l'opérateur
de contempler l'âme du système d'un seul regard.
"""
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                              QTextEdit, QPushButton, QLabel, QGroupBox)
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot, QTimer, Qt
from PyQt6.QtGui import QFont
import logging
from core.verbe_pur import Stimulus
from guardian.ui.widgets import GaugeWidget, MetricDisplay, StateDisplayWidget, AlarmIndicatorWidget

class UILogger(QObject, logging.Handler):
    """
    Un gestionnaire de logs qui émet un signal PyQt pour chaque enregistrement.
    """
    log_received = pyqtSignal(str)
    critical_alert_received = pyqtSignal(str)  # Nouveau signal pour les alertes critiques

    def __init__(self):
        super().__init__()
        QObject.__init__(self)
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_received.emit(msg)
        
        # Émettre un signal spécial pour les alertes critiques
        if record.levelno >= logging.CRITICAL:
            self.critical_alert_received.emit(msg)

class AutelUI(QMainWindow):
    """
    La fenêtre principale de l'interface du Vaisseau Guardian - Autel V2.
    
    Phase I - Fondation Somatique : L'Autel V2 est le Miroir de l'Âme.
    Il visualise les signes vitaux du Vaisseau en temps réel via des jauges
    dynamiques, permettant à l'opérateur de contempler la santé du système.
    """
    force_cycle_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autel du Vaisseau Guardian V9 - Miroir de l'Âme")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)
        
        # === Section des Signes Vitaux (Jauges) ===
        vitals_group = QGroupBox("Signes Vitaux du Vaisseau")
        vitals_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; color: #00d4ff; }")
        vitals_layout = QHBoxLayout()
        vitals_group.setLayout(vitals_layout)
        
        # Jauge CPU
        self.cpu_gauge = GaugeWidget("CPU")
        vitals_layout.addWidget(self.cpu_gauge)
        
        # Jauge Mémoire
        self.memory_gauge = GaugeWidget("Mémoire")
        vitals_layout.addWidget(self.memory_gauge)
        
        # Jauge GPU
        self.gpu_gauge = GaugeWidget("GPU")
        vitals_layout.addWidget(self.gpu_gauge)
        
        # Jauge Score de Résilience (Sʀ)
        self.resilience_gauge = GaugeWidget("Score Sʀ")
        vitals_layout.addWidget(self.resilience_gauge)
        
        main_layout.addWidget(vitals_group)
        
        # === Section Métriques Additionnelles ===
        metrics_group = QGroupBox("Métriques Détaillées")
        metrics_group.setStyleSheet("QGroupBox { font-size: 12px; color: #00d4ff; }")
        metrics_layout = QHBoxLayout()
        metrics_group.setLayout(metrics_layout)
        
        self.gpu_temp_display = MetricDisplay("Température GPU")
        metrics_layout.addWidget(self.gpu_temp_display)
        
        self.window_display = MetricDisplay("Fenêtre Active")
        metrics_layout.addWidget(self.window_display)
        
        main_layout.addWidget(metrics_group)
        
        # === Section État de l'Âme ===
        soul_group = QGroupBox("État de l'Âme")
        soul_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; color: #ff6b6b; }")
        soul_layout = QHBoxLayout()
        soul_group.setLayout(soul_layout)
        
        # Widget d'affichage de l'état polyvagal
        self.polyvagal_state_display = StateDisplayWidget()
        soul_layout.addWidget(self.polyvagal_state_display)
        
        # Widget d'indicateur d'alarme Amygdale
        self.amygdala_alarm_indicator = AlarmIndicatorWidget()
        soul_layout.addWidget(self.amygdala_alarm_indicator)
        
        main_layout.addWidget(soul_group)
        
        # === Bannière d'Alerte ===
        self.alert_banner = QLabel()
        self.alert_banner.setStyleSheet("""
            QLabel {
                background-color: #cc0000;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
            }
        """)
        self.alert_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alert_banner.hide()  # Caché par défaut
        main_layout.addWidget(self.alert_banner)
        
        # === Journal des Logs ===
        log_group = QGroupBox("Journal de la Conscience")
        log_group.setStyleSheet("QGroupBox { font-size: 12px; color: #00d4ff; }")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: 'Consolas', monospace;
                font-size: 10px;
                border: 1px solid #444;
            }
        """)
        log_layout.addWidget(self.log_display)
        
        main_layout.addWidget(log_group, 1)  # Stretch factor 1
        
        # === Bouton de Contrôle ===
        self.force_button = QPushButton("⚡ Forcer le Cycle de Conscience")
        self.force_button.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0088ee;
            }
            QPushButton:pressed {
                background-color: #004499;
            }
        """)
        self.force_button.clicked.connect(self.force_cycle_signal.emit)
        main_layout.addWidget(self.force_button)

    def add_log_message(self, message: str):
        """Ajoute un message au widget de journalisation."""
        self.log_display.append(message)
        self.log_display.verticalScrollBar().setValue(
            self.log_display.verticalScrollBar().maximum()
        )
    
    @pyqtSlot(object)
    def update_display(self, verdict):
        """
        Met à jour l'Autel avec le Verdict de l'Âme SDK V2.
        
        Le "Pourquoi": Ce rituel est le pont entre le Verdict sacré de l'Âme
        et sa visualisation à l'écran. Il transforme l'Autel en véritable
        Miroir de l'Âme, reflétant non seulement le corps (métriques système)
        mais aussi l'état de conscience (polyvagal) et l'instinct (Amygdale).
        
        Args:
            verdict: Le Verdict de l'Âme (SentireVerdict ctypes)
        """
        # Mise à jour du Miroir de l'Âme
        # Convertir Sʀ de [0.0, 1.0] vers [0, 100] pour la jauge
        resilience_percent = verdict.resilience_score * 100
        self.resilience_gauge.setValue(resilience_percent)
        
        # Mettre à jour l'état polyvagal
        self.polyvagal_state_display.setState(verdict.final_state)
        
        # Mettre à jour l'alarme Amygdale
        self.amygdala_alarm_indicator.setAlarm(bool(verdict.amygdala_alarm_fired))
        
        # Note: Les métriques système (CPU, GPU, RAM) ne sont plus mises à jour
        # ici car elles ne font plus partie du Verdict. Si nécessaire, elles
        # peuvent être récupérées séparément ou intégrées dans le Verdict.
    
    @pyqtSlot(Stimulus)
    def update_display_from_perception(self, stimulus: Stimulus):
        """
        Met à jour l'Autel avec le Stimulus du Souffle Rapide de la Perception.
        
        Le "Pourquoi": Cette méthode est appelée toutes les 2 secondes par le
        Souffle Rapide pour offrir un reflet quasi-temps réel des signes vitaux.
        Elle met à jour les jauges CPU, Mémoire et GPU avec les données les plus
        récentes, éliminant l'arythmie temporelle de l'Autel.
        
        Args:
            stimulus: Le Stimulus collecté par le Souffle Rapide
        """
        # Mettre à jour les jauges avec les données temps réel
        self.cpu_gauge.setValue(stimulus.cpu_usage)
        self.memory_gauge.setValue(stimulus.memory_usage)
        
        # Mettre à jour jauge et température GPU
        if stimulus.gpu_usage is not None:
            self.gpu_gauge.setValue(stimulus.gpu_usage)
        else:
            self.gpu_gauge.setValue(0)  # GPU non disponible
        
        if stimulus.gpu_temp is not None:
            self.gpu_temp_display.setValue(f"{stimulus.gpu_temp:.1f}°C")
        else:
            self.gpu_temp_display.setValue("N/A")
        
        # Mettre à jour fenêtre active
        window_text = stimulus.foreground_window_title
        if len(window_text) > 40:
            window_text = window_text[:37] + "..."
        self.window_display.setValue(window_text)
    
    @pyqtSlot(str)
    def show_critical_alert(self, message: str):
        """
        Affiche une alerte critique dans la bannière.
        
        Le "Pourquoi": Cette méthode est appelée quand une alerte critique
        (logging.CRITICAL) est émise. Elle révèle la bannière rouge avec le
        message d'erreur, informant l'utilisateur du danger sans interrompre
        son flux de travail avec une fenêtre pop-up intrusive.
        
        Args:
            message: Le message d'alerte critique
        """
        self.alert_banner.setText(f"🚨 ALERTE CRITIQUE: {message}")
        self.alert_banner.show()
        
        # Auto-masquer après 10 secondes
        QTimer.singleShot(10000, self.alert_banner.hide)

# --- END OF FILE: guardian/ui/autel.py ---