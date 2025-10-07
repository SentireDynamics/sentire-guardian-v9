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
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot
from PyQt6.QtGui import QFont
import logging
from core.verbe_pur import Stimulus
from guardian.ui.widgets import GaugeWidget, MetricDisplay

class UILogger(QObject, logging.Handler):
    """
    Un gestionnaire de logs qui émet un signal PyQt pour chaque enregistrement.
    """
    log_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        QObject.__init__(self)
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_received.emit(msg)

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
    
    @pyqtSlot(Stimulus)
    def update_display(self, stimulus: Stimulus):
        """
        Met à jour toutes les jauges et affichages avec le Stimulus actuel.
        
        Le "Pourquoi": Ce rituel est le pont entre les données brutes du Stimulus
        et leur visualisation à l'écran. Il est déclenché par un signal émis par
        l'Orchestrateur à chaque cycle, garantissant que l'Autel reflète toujours
        l'état le plus récent du Vaisseau en temps réel.
        
        Args:
            stimulus: Le Stimulus actuel contenant toutes les métriques
        """
        # Mettre à jour les jauges
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

# --- END OF FILE: guardian/ui/autel.py ---