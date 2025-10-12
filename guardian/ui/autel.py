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
                              QTextEdit, QPushButton, QLabel, QGroupBox, QComboBox)
from PyQt6.QtCore import pyqtSignal, QObject, pyqtSlot, QTimer, Qt
from PyQt6.QtGui import QFont
import logging
import math
import time

from core.doctrines import SovereignVesselState
from datetime import datetime
import psutil
from core.verbe_pur import Stimulus
from guardian.ui.widgets import GaugeWidget, MetricDisplay, StateDisplayWidget, AlarmIndicatorWidget, GraphWidget, ActionLogWidget

def safe_float_to_int(value, default=0, name="value"):
    """
    Convertit une valeur flottante en entier de manière sécurisée.
    Protège contre NaN, infini et valeurs invalides.
    """
    try:
        if math.isnan(value) or math.isinf(value):
            logging.warning(f"{name} reçu comme NaN/Infini ({value}), utilisation de {default}")
            return default
        if not isinstance(value, (int, float)):
            logging.warning(f"{name} n'est pas numérique ({type(value)}), utilisation de {default}")
            return default
        return int(value)
    except Exception as e:
        logging.error(f"Erreur lors de la conversion de {name}: {e}")
        return default

def safe_float_to_str(value, default="N/A", name="value", format_str="{:.1f}"):
    """
    Convertit une valeur flottante en string de manière sécurisée.
    Protège contre NaN, infini et valeurs invalides.
    """
    try:
        if math.isnan(value) or math.isinf(value):
            logging.warning(f"{name} reçu comme NaN/Infini ({value}), utilisation de {default}")
            return default
        if not isinstance(value, (int, float)):
            logging.warning(f"{name} n'est pas numérique ({type(value)}), utilisation de {default}")
            return default
        return format_str.format(value)
    except Exception as e:
        logging.error(f"Erreur lors de la conversion de {name}: {e}")
        return default

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
    
    Phase II - Serviteur Dévoué : L'Autel V2 devient le Sanctuaire d'Alignement.
    Il permet à l'Architecte de désigner la Cible Sacrée et de surveiller
    le dévouement du Serviteur.
    """
    force_cycle_signal = pyqtSignal()
    sacred_target_selected_signal = pyqtSignal(int, str)  # pid, name

    def __init__(self, orchestrator=None):
        super().__init__()
        self.orchestrator = orchestrator
        self.setWindowTitle("Autel du Vaisseau Guardian V9 - Miroir de l'Âme")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)
        
        # === Sanctuaire d'Alignement (Phase II) ===
        alignment_group = QGroupBox("Sanctuaire d'Alignement - Désignation de la Cible Sacrée")
        alignment_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; color: #ffd700; }")
        alignment_layout = QHBoxLayout()
        alignment_group.setLayout(alignment_layout)
        
        # ComboBox pour sélectionner la Cible Sacrée
        self.sacred_target_combo = QComboBox()
        self.sacred_target_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #ffd700;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffd700;
                margin-right: 5px;
            }
        """)
        self.sacred_target_combo.addItem("Sélectionner la Cible Sacrée...")
        alignment_layout.addWidget(QLabel("Cible Sacrée:"))
        alignment_layout.addWidget(self.sacred_target_combo)
        
        # Bouton de confirmation
        self.confirm_target_button = QPushButton("🎯 Confirmer la Cible")
        self.confirm_target_button.setStyleSheet("""
            QPushButton {
                background-color: #ffd700;
                color: #000000;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ffed4e;
            }
            QPushButton:pressed {
                background-color: #e6c200;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #cccccc;
            }
        """)
        self.confirm_target_button.setEnabled(False)
        self.confirm_target_button.clicked.connect(self._confirm_sacred_target)
        alignment_layout.addWidget(self.confirm_target_button)
        
        # Label de statut
        self.target_status_label = QLabel("Aucune Cible Sacrée désignée")
        self.target_status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        alignment_layout.addWidget(self.target_status_label)
        
        # Label de mise à jour dynamique
        self.update_status_label = QLabel("🔄 Liste mise à jour toutes les 15s")
        self.update_status_label.setStyleSheet("color: #00d4ff; font-size: 10px;")
        alignment_layout.addWidget(self.update_status_label)
        
        main_layout.addWidget(alignment_group)
        
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
        
        # === Chronique Temporelle du Sʀ ===
        self.graph_widget = GraphWidget()
        main_layout.addWidget(self.graph_widget)
        
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
        
        # === Chronique des Actes ===
        actions_group = QGroupBox("Chronique des Actes")
        actions_group.setStyleSheet("QGroupBox { font-size: 12px; color: #00d4ff; }")
        actions_layout = QVBoxLayout()
        actions_group.setLayout(actions_layout)
        
        self.action_log_widget = ActionLogWidget()
        actions_layout.addWidget(self.action_log_widget)
        
        main_layout.addWidget(actions_group, 1)  # Stretch factor 1
        
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
        
        # === Timer pour la Mise à Jour Dynamique des Candidats ===
        self.contenders_timer = QTimer(self)
        self.contenders_timer.timeout.connect(self.update_contenders_list)
        self.contenders_timer.start(2000)  # Rafraîchissement toutes les 2 secondes
    
    def update_contenders_list(self):
        """Met à jour dynamiquement la liste des cibles potentielles."""
        if not self.orchestrator:
            return
            
        try:
            # Récupérer les nouveaux candidats (limités à 5)
            contenders = self.orchestrator.perception.get_top_contenders(count=5)
            
            # Mémoriser la sélection actuelle
            current_selection = self.sacred_target_combo.currentText()
            current_data = None
            if self.sacred_target_combo.currentIndex() > 0:
                current_data = self.sacred_target_combo.itemData(self.sacred_target_combo.currentIndex())
            
            # Vider et repeupler le ComboBox
            self.sacred_target_combo.clear()
            self.sacred_target_combo.addItem("Sélectionner la Cible Sacrée...")
            
            # Ajouter les nouvelles cibles
            for proc in contenders:
                display_text = f"PID {proc['pid']}: {proc['name']} (CPU: {proc['cpu']:.1f}%, RAM: {proc['mem_mb']:.1f}MB)"
                self.sacred_target_combo.addItem(display_text, proc)
            
            # Tenter de restaurer la sélection
            if current_data:
                for i in range(1, self.sacred_target_combo.count()):
                    if self.sacred_target_combo.itemData(i) == current_data:
                        self.sacred_target_combo.setCurrentIndex(i)
                        break
            elif current_selection and current_selection != "Sélectionner la Cible Sacrée...":
                # Essayer de retrouver par le texte
                index = self.sacred_target_combo.findText(current_selection)
                if index != -1:
                    self.sacred_target_combo.setCurrentIndex(index)
                    
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour des candidats: {e}")

    def populate_sacred_targets(self, contenders: list):
        """
        Peuple le ComboBox avec les processus candidats pour la Cible Sacrée.
        
        Args:
            contenders: Liste des processus les plus gourmands
        """
        # Mémoriser la sélection actuelle si elle existe
        current_selection = None
        if self.sacred_target_combo.currentIndex() > 0:
            current_selection = self.sacred_target_combo.itemData(self.sacred_target_combo.currentIndex())
        
        self.sacred_target_combo.clear()
        self.sacred_target_combo.addItem("Sélectionner la Cible Sacrée...")
        
        for contender in contenders:
            display_text = f"PID {contender['pid']}: {contender['name']} (CPU: {contender['cpu']:.1f}%, RAM: {contender['mem_mb']:.1f}MB)"
            self.sacred_target_combo.addItem(display_text, contender)
        
        # Restaurer la sélection si elle existe encore
        if current_selection:
            for i in range(1, self.sacred_target_combo.count()):
                if self.sacred_target_combo.itemData(i) == current_selection:
                    self.sacred_target_combo.setCurrentIndex(i)
                    break
        
        # Réactiver le bouton si des candidats sont disponibles
        self.confirm_target_button.setEnabled(len(contenders) > 0)
        
        # Mettre à jour le statut de mise à jour
        from datetime import datetime
        update_time = datetime.now().strftime("%H:%M:%S")
        self.update_status_label.setText(f"🔄 Dernière mise à jour: {update_time}")
    
    def _confirm_sacred_target(self):
        """
        Confirme ou change la sélection de la Cible Sacrée.
        Phase II - Interface Dynamique : L'interface reste toujours active.
        """
        # Utiliser la méthode de changement qui gère les deux cas
        self.change_sacred_target()
    
    def reset_sacred_target_selection(self):
        """
        Remet à zéro la sélection de Cible Sacrée.
        Phase II - Interface Dynamique : Remet l'interface en état initial.
        """
        self.sacred_target_combo.setCurrentIndex(0)
        self.confirm_target_button.setText("🎯 Confirmer la Cible")
        self.confirm_target_button.setStyleSheet("""
            QPushButton {
                background-color: #ffd700;
                color: #000000;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ffed4e;
            }
            QPushButton:pressed {
                background-color: #e6c200;
            }
        """)
        self.target_status_label.setText("Aucune Cible Sacrée désignée")
        self.target_status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
    
    def change_sacred_target(self):
        """
        Change la Cible Sacrée actuelle.
        Phase II - Interface Dynamique : Permet le changement à tout moment sans blocage.
        """
        try:
            current_index = self.sacred_target_combo.currentIndex()
            if current_index <= 0:  # Index 0 est "Sélectionner..."
                return
            
            contender_data = self.sacred_target_combo.itemData(current_index)
            if contender_data:
                pid = contender_data['pid']
                name = contender_data['name']
                
                # Mettre à jour l'interface immédiatement pour feedback visuel
                self.target_status_label.setText(f"🔄 Changement en cours: {name} (PID: {pid})")
                self.target_status_label.setStyleSheet("color: #ffd700; font-weight: bold;")
                
                # Désactiver temporairement le bouton pour éviter les clics multiples
                self.confirm_target_button.setEnabled(False)
                self.confirm_target_button.setText("⏳ Changement...")
                
                # Émettre le signal de changement de manière asynchrone
                QTimer.singleShot(50, lambda: self._emit_sacred_target_signal(pid, name))
                
        except Exception as e:
            print(f"Erreur lors du changement de Cible Sacrée: {e}")
            # Réactiver l'interface en cas d'erreur
            self.confirm_target_button.setEnabled(True)
            self.confirm_target_button.setText("🔄 Changer la Cible")

    def _emit_sacred_target_signal(self, pid: int, name: str):
        """
        Émet le signal de changement de Cible Sacrée de manière asynchrone.
        """
        try:
            self.sacred_target_selected_signal.emit(pid, name)
            
            # Mettre à jour le statut final
            self.target_status_label.setText(f"🎯 Cible Sacrée Active: {name} (PID: {pid})")
            self.target_status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
            
            # Réactiver le bouton
            self.confirm_target_button.setEnabled(True)
            self.confirm_target_button.setText("🔄 Changer la Cible")
            
        except Exception as e:
            print(f"Erreur lors de l'émission du signal: {e}")
            # Réactiver l'interface en cas d'erreur
            self.confirm_target_button.setEnabled(True)
            self.confirm_target_button.setText("🔄 Changer la Cible")

    def add_log_message(self, message: str):
        """Ajoute un message au widget de journalisation."""
        # Cette méthode est conservée pour la compatibilité avec UILogger
        # mais n'est plus utilisée car nous utilisons maintenant ActionLogWidget
        pass
    
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
        
        # Ajouter le point de données au graphique historique
        self.graph_widget.add_data_point(verdict.resilience_score)
        
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
    
    @pyqtSlot(str)
    def display_action(self, reasoning):
        """
        Affiche le raisonnement de l'Oracle dans la Chronique des Actes.
        
        Args:
            reasoning: Le raisonnement de l'Oracle
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Créer un objet Action factice pour compatibilité avec log_action
        fake_action = type('Action', (), {
            'id': 'ORACLE_REASONING', 
            'reasoning': reasoning,
            'description': reasoning,
            'parameters': {}
        })()
        self.action_log_widget.log_action(fake_action, timestamp)

    def update_soul_vitals_display(self, vitals):
        """Slot pour recevoir et afficher le souffle complet de l'Âme."""
        try:
            # Met à jour les jauges avec les données du souffle (protection NaN)
            if hasattr(self, 'cpu_gauge'):
                cpu_value = safe_float_to_int(vitals.gauges.cpu_percent, 0, "CPU %")
                self.cpu_gauge.setValue(cpu_value)
            if hasattr(self, 'memory_gauge'):
                mem_value = safe_float_to_int(vitals.gauges.mem_percent, 0, "Memory %")
                self.memory_gauge.setValue(mem_value)
            if hasattr(self, 'gpu_gauge'):
                gpu_value = safe_float_to_int(vitals.gauges.gpu_percent, 0, "GPU %")
                self.gpu_gauge.setValue(gpu_value)
            if hasattr(self, 'resilience_gauge'):
                sr_value = safe_float_to_int(vitals.gauges.sr_score * 100, 0, "SR Score")
                self.resilience_gauge.setValue(sr_value)
                logging.debug(f"Score SR mis à jour: {sr_value}%")

            # Met à jour l'État de l'Âme
            state_name = vitals.system_state.value
            if hasattr(self, 'soul_state_label'):
                self.soul_state_label.setText(state_name)
                
                # Change la couleur selon l'état
                if vitals.system_state.value == "VENTRAL":
                    self.soul_state_label.setStyleSheet("color: #00ff00; font-weight: bold;")
                elif vitals.system_state.value == "SYMPATHETIC":
                    self.soul_state_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
                elif vitals.system_state.value == "DORSAL":
                    self.soul_state_label.setStyleSheet("color: #ff0000; font-weight: bold;")
            
            # Met à jour l'Alarme Amygdale
            if hasattr(self, 'amygdala_alarm_indicator'):
                self.amygdala_alarm_indicator.setStyleSheet(
                    "background-color: #ff0000;" if vitals.alarm_state 
                    else "background-color: #00ff00;"
                )
            
            # Met à jour la température GPU (protection NaN)
            if hasattr(self, 'gpu_temp_display'):
                gpu_temp_str = safe_float_to_str(vitals.hardware.gpu_temp_c, "N/A", "GPU Temp", "{:.1f}°C")
                self.gpu_temp_display.setValue(gpu_temp_str)
            
            # Met à jour la fenêtre active
            if hasattr(self, 'window_display'):
                window_text = vitals.active_window_title[:30] if len(vitals.active_window_title) > 30 else vitals.active_window_title
                self.window_display.setValue(window_text)
            
            # Met à jour la Chronique Temporelle (protection NaN)
            if hasattr(self, 'graph_widget'):
                # Vérifier que sr_score n'est pas NaN avant d'ajouter au graphique
                if not math.isnan(vitals.gauges.sr_score) and not math.isinf(vitals.gauges.sr_score):
                    self.graph_widget.add_data_point(vitals.gauges.sr_score)
                else:
                    logging.warning(f"SR Score invalide pour graphique: {vitals.gauges.sr_score}")
                
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de l'Autel: {e}")

    def update_vitals_display(self, vessel_state):
        """Slot pour recevoir et afficher le Pacte de Données Unifié."""
        try:
            # Détecter le format : SovereignVesselState ou ancien format
            if isinstance(vessel_state, SovereignVesselState):
                # Nouveau format - Pacte de Données Unifié
                self._update_from_sovereign_vessel_state(vessel_state)
            elif hasattr(vessel_state, 'gauges'):
                # Format SoulVitals direct (compatibilité)
                self._update_from_soul_vitals(vessel_state)
            else:
                # Format Stimulus avec soul_vitals (compatibilité)
                vitals = vessel_state.soul_vitals
                self._update_from_soul_vitals(vitals)
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de l'Autel: {e}")

    def _update_from_sovereign_vessel_state(self, vessel_state: SovereignVesselState):
        """Met à jour l'Autel à partir du Pacte de Données Unifié."""
        try:
            # Met à jour les jauges avec les données du Pacte (protection NaN)
            if hasattr(self, 'cpu_gauge'):
                cpu_value = safe_float_to_int(vessel_state.cpu_percent, 0, "CPU %")
                self.cpu_gauge.setValue(cpu_value)
            if hasattr(self, 'memory_gauge'):
                mem_value = safe_float_to_int(vessel_state.memory_percent, 0, "Memory %")
                self.memory_gauge.setValue(mem_value)
            if hasattr(self, 'gpu_gauge'):
                gpu_value = safe_float_to_int(vessel_state.gpu_percent, 0, "GPU %")
                self.gpu_gauge.setValue(gpu_value)
            if hasattr(self, 'resilience_gauge'):
                sr_value = safe_float_to_int(vessel_state.resilience_score * 100, 0, "SR Score")
                self.resilience_gauge.setValue(sr_value)
                logging.debug(f"Score SR mis à jour: {sr_value}%")

            # Met à jour l'État de l'Âme avec la logique spéciale pour l'effondrement
            if hasattr(self, 'soul_state_label'):
                if not vessel_state.is_soul_stable:
                    state_text = "SOUL COLLAPSE"
                    color = "#ff0000"  # Rouge pour l'effondrement
                    logging.warning("ALERTE AUTEL - Effondrement de l'Âme détecté ! Affichage en mode SOUL COLLAPSE")
                else:
                    # Mapping des états numériques vers les états doctrinaux
                    state_map = {0: "VENTRAL", 1: "SYMPATHETIC", 2: "DORSAL"}
                    state_text = state_map.get(vessel_state.somatic_verdict, "INCONNU")
                    
                    # Appliquer la couleur selon l'état
                    if vessel_state.somatic_verdict == 0:  # VENTRAL
                        color = "#00ff00"  # Vert
                    elif vessel_state.somatic_verdict == 1:  # SYMPATHETIC
                        color = "#ffaa00"  # Orange
                    else:  # DORSAL
                        color = "#ff0000"  # Rouge
                
                self.soul_state_label.setText(state_text)
                self.soul_state_label.setStyleSheet(f"color: {color}; font-weight: bold;")

            # Met à jour l'Alarme Amygdale
            if hasattr(self, 'amygdala_alarm_indicator'):
                self.amygdala_alarm_indicator.setStyleSheet(
                    "background-color: #ff0000;" if vessel_state.amygdala_alarm_state 
                    else "background-color: #00ff00;"
                )

            # Met à jour la température GPU (protection NaN)
            if hasattr(self, 'gpu_temp_display'):
                gpu_temp_str = safe_float_to_str(vessel_state.gpu_temp_c, "N/A", "GPU Temp", "{:.1f}°C")
                self.gpu_temp_display.setValue(gpu_temp_str)

            # Met à jour la fenêtre active
            if hasattr(self, 'window_display'):
                window_text = vessel_state.active_window_title
                window_text = window_text[:30] if len(window_text) > 30 else window_text
                self.window_display.setValue(window_text)

            # Met à jour la Chronique Temporelle (protection NaN)
            if hasattr(self, 'graph_widget'):
                # Vérifier que resilience_score n'est pas NaN avant d'ajouter au graphique
                if not math.isnan(vessel_state.resilience_score) and not math.isinf(vessel_state.resilience_score):
                    self.graph_widget.add_data_point(vessel_state.resilience_score)
                else:
                    logging.warning(f"Resilience Score invalide pour graphique: {vessel_state.resilience_score}")

        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour depuis SovereignVesselState: {e}")

    def _update_from_soul_vitals(self, vitals):
        """Met à jour l'Autel à partir de SoulVitals (compatibilité)."""
        try:
                
            # Récupérer les métriques depuis SoulVitals (la vérité de l'Âme)
            cpu_percent = vitals.gauges.cpu_percent
            memory_percent = vitals.gauges.mem_percent
            gpu_percent = vitals.gauges.gpu_percent
            
            # Met à jour les jauges avec les données de l'Âme (protection NaN)
            if hasattr(self, 'cpu_gauge'):
                cpu_value = safe_float_to_int(cpu_percent, 0, "CPU %")
                self.cpu_gauge.setValue(cpu_value)
            if hasattr(self, 'memory_gauge'):
                mem_value = safe_float_to_int(memory_percent, 0, "Memory %")
                self.memory_gauge.setValue(mem_value)
            if hasattr(self, 'gpu_gauge'):
                gpu_value = safe_float_to_int(gpu_percent, 0, "GPU %")
                self.gpu_gauge.setValue(gpu_value)
            if hasattr(self, 'resilience_gauge'):
                resilience_score = vitals.gauges.sr_score
                sr_value = safe_float_to_int(resilience_score * 100, 0, "SR Score")
                self.resilience_gauge.setValue(sr_value)
                logging.debug(f"Score SR mis à jour: {sr_value}%")

            # Met à jour l'État de l'Âme
            if hasattr(vitals, 'system_state'):
                # Format SoulVitals
                state_name = vitals.system_state.value
                somatic_state = vitals.system_state
            else:
                # Format Stimulus
                state_map = {0: "VENTRAL", 1: "SYMPATHETIC", 2: "DORSAL"}
                somatic_state = vitals.somatic_state or 0
                state_name = state_map.get(somatic_state, "INCONNU")
                
            if hasattr(self, 'soul_state_label'):
                self.soul_state_label.setText(state_name)
                
                # Change la couleur selon l'état
                if state_name == "VENTRAL":
                    self.soul_state_label.setStyleSheet("color: #00ff00; font-weight: bold;")
                elif state_name == "SYMPATHETIC":
                    self.soul_state_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
                elif state_name == "DORSAL":
                    self.soul_state_label.setStyleSheet("color: #ff0000; font-weight: bold;")
            
            # Met à jour l'Alarme Amygdale
            if hasattr(self, 'amygdala_alarm_indicator') and self.orchestrator:
                try:
                    verdict = self.orchestrator.native_bridge.get_last_verdict()
                    if verdict:
                        self.amygdala_alarm_indicator.setAlarm(bool(verdict.amygdala_alarm_fired))
                except:
                    pass
            
            # Met à jour la température GPU (protection NaN)
            if hasattr(self, 'gpu_temp_display'):
                gpu_temp_str = safe_float_to_str(vitals.hardware.gpu_temp_c, "N/A", "GPU Temp", "{:.1f}°C")
                self.gpu_temp_display.setValue(gpu_temp_str)
            
            # Met à jour la fenêtre active
            if hasattr(self, 'window_display'):
                window_text = vitals.active_window_title[:30] if len(vitals.active_window_title) > 30 else vitals.active_window_title
                self.window_display.setValue(window_text)
            
            # Met à jour la Chronique Temporelle (protection NaN)
            if hasattr(self, 'graph_widget'):
                # Vérifier que resilience_score n'est pas NaN avant d'ajouter au graphique
                if not math.isnan(resilience_score) and not math.isinf(resilience_score):
                    self.graph_widget.add_data_point(resilience_score)
                else:
                    logging.warning(f"Resilience Score invalide pour graphique: {resilience_score}")
                
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de l'Autel: {e}", exc_info=True)

# --- END OF FILE: guardian/ui/autel.py ---