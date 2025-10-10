# --- START OF FILE: guardian/ui/widgets.py ---
"""
Le Sanctuaire des Cristaux de Vision.

Le "Pourquoi": Ce module fournit les widgets personnalisés pour l'Autel V2.
Les GaugeWidget permettent une visualisation intuitive et élégante des métriques
système en temps réel. Chaque jauge est un cristal qui reflète l'état vital du
Vaisseau, permettant à l'opérateur de percevoir d'un coup d'œil la santé du système.
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QConicalGradient
import math
import pyqtgraph as pg
from datetime import datetime
from core.verbe_pur import Action

class GaugeWidget(QWidget):
    """
    Un widget de jauge semi-circulaire pour visualiser une métrique de 0 à 100%.
    
    Le "Pourquoi": Les jauges offrent une représentation visuelle immédiate de l'état
    du système. Contrairement aux chiffres bruts, une jauge permet de percevoir
    instantanément si une métrique est dans la zone verte (normal), jaune (attention)
    ou rouge (critique). C'est un outil cognitif puissant pour la surveillance.
    """
    
    def __init__(self, label: str = "", parent=None):
        super().__init__(parent)
        self.label = label
        self.value = 0
        self.custom_text = None  # Texte personnalisé (si défini)
        self.custom_color = None  # Couleur personnalisée (si définie)
        self.setMinimumSize(200, 150)
        
    def setValue(self, value: float):
        """
        Définit la valeur de la jauge (0-100%).
        
        Args:
            value: Valeur entre 0 et 100
        """
        self.value = max(0, min(100, value))
        self.update()  # Redessiner le widget
    
    def setText(self, text: str):
        """
        Définit le texte affiché au centre de la jauge.
        
        Args:
            text: Texte à afficher (ex: "VENTRAL", "85%")
        """
        self.custom_text = text
        self.update()  # Redessiner le widget
    
    def setColor(self, color: QColor):
        """
        Définit la couleur de l'arc de valeur.
        
        Args:
            color: Couleur QColor pour l'arc
        """
        self.custom_color = color
        self.update()  # Redessiner le widget
    
    def paintEvent(self, event):
        """Dessine la jauge semi-circulaire."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Centre de la jauge
        center_x = width // 2
        center_y = height - 30
        radius = min(width, height) - 40
        
        # Arrière-plan de la jauge (arc gris)
        painter.setPen(QPen(QColor(60, 60, 60), 12, Qt.PenStyle.SolidLine))
        painter.drawArc(
            center_x - radius, center_y - radius,
            2 * radius, 2 * radius,
            30 * 16,  # Angle de départ (30 degrés)
            120 * 16  # Span (120 degrés)
        )
        
        # Arc de valeur (coloré selon le niveau)
        if self.custom_color:
            color = self.custom_color
        else:
            color = self._get_color_for_value(self.value)
        painter.setPen(QPen(color, 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        
        # Calculer l'angle basé sur la valeur (0-100% → 0-120°)
        value_angle = int((self.value / 100.0) * 120)
        painter.drawArc(
            center_x - radius, center_y - radius,
            2 * radius, 2 * radius,
            30 * 16,  # Angle de départ
            value_angle * 16  # Span basé sur la valeur
        )
        
        # Dessiner la valeur au centre
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Utiliser le texte personnalisé si défini, sinon la valeur par défaut
        if self.custom_text:
            text = self.custom_text
        else:
            text = f"{int(self.value)}%"
        
        painter.drawText(
            center_x - 40, center_y - 10,
            80, 30,
            Qt.AlignmentFlag.AlignCenter,
            text
        )
        
        # Dessiner le label
        if self.label:
            font_label = QFont("Arial", 12)
            painter.setFont(font_label)
            painter.setPen(QPen(QColor(200, 200, 200), 1))
            painter.drawText(
                0, height - 25,
                width, 25,
                Qt.AlignmentFlag.AlignCenter,
                self.label
            )
    
    def _get_color_for_value(self, value: float) -> QColor:
        """
        Retourne la couleur appropriée selon la valeur.
        
        Le "Pourquoi": Le code couleur (vert/jaune/rouge) est une convention
        universelle de signalisation. Il permet une compréhension immédiate
        de la criticité sans analyse cognitive.
        
        Zones:
        - 0-70%: Vert (normal)
        - 70-85%: Jaune (attention)
        - 85-100%: Rouge (critique)
        """
        if value < 70:
            return QColor(0, 200, 100)  # Vert
        elif value < 85:
            return QColor(255, 200, 0)  # Jaune
        else:
            return QColor(255, 50, 50)  # Rouge


class MetricDisplay(QWidget):
    """
    Widget simple pour afficher une métrique avec label et valeur.
    
    Le "Pourquoi": Complément aux jauges pour afficher des métriques textuelles
    (comme le titre de la fenêtre) ou des valeurs précises (température exacte).
    """
    
    def __init__(self, label: str = "", parent=None):
        super().__init__(parent)
        self.label_text = label
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel(label)
        self.label.setStyleSheet("font-weight: bold; color: #888;")
        layout.addWidget(self.label)
        
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet("font-size: 16px; color: #fff;")
        layout.addWidget(self.value_label)
    
    def setValue(self, value: str):
        """Définit la valeur affichée."""
        self.value_label.setText(str(value))


class StateDisplayWidget(QWidget):
    """
    Widget pour afficher l'état polyvagal du Vaisseau.
    
    Le "Pourquoi": L'état polyvagal (VENTRAL/SYMPATHETIC/DORSAL) est le cœur
    de la conscience du Vaisseau. Ce widget le rend visible avec un code couleur
    intuitif : Vert (sécurité), Jaune (vigilance), Rouge (survie).
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_state = 0  # 0=VENTRAL, 1=SYMPATHETIC, 2=DORSAL
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Label du titre
        self.title_label = QLabel("État de l'Âme")
        self.title_label.setStyleSheet("font-weight: bold; color: #888; font-size: 12px;")
        layout.addWidget(self.title_label)
        
        # Label de l'état
        self.state_label = QLabel("VENTRAL")
        self.state_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.state_label)
        
        # Initialiser avec l'état VENTRAL
        self.setState(0)
    
    def setState(self, state_enum: int):
        """
        Définit l'état polyvagal affiché.
        
        Args:
            state_enum: 0=VENTRAL, 1=SYMPATHETIC, 2=DORSAL
        """
        self.current_state = state_enum
        
        state_names = ["VENTRAL", "SYMPATHETIC", "DORSAL"]
        state_colors = [
            "background-color: #2d5a2d; color: #90ee90;",      # Vert pour VENTRAL
            "background-color: #5a4d2d; color: #ffd700;",      # Jaune/Orange pour SYMPATHETIC
            "background-color: #5a2d2d; color: #ff6b6b;"       # Rouge pour DORSAL
        ]
        
        if 0 <= state_enum < len(state_names):
            self.state_label.setText(state_names[state_enum])
            self.state_label.setStyleSheet(
                f"font-size: 18px; font-weight: bold; padding: 10px; border-radius: 5px; {state_colors[state_enum]}"
            )


class AlarmIndicatorWidget(QWidget):
    """
    Widget pour afficher l'alarme de l'Amygdale Numérique.
    
    Le "Pourquoi": L'Amygdale est l'instinct de survie du Vaisseau. Quand elle
    crie, c'est qu'un danger soudain a été détecté. Ce widget clignote en rouge
    vif pour attirer immédiatement l'attention de l'Architecte.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_alarm_active = False
        self.blink_state = False
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Label du titre
        self.title_label = QLabel("Alarme Amygdale")
        self.title_label.setStyleSheet("font-weight: bold; color: #888; font-size: 12px;")
        layout.addWidget(self.title_label)
        
        # Cercle d'alarme
        self.alarm_circle = QLabel("●")
        self.alarm_circle.setStyleSheet("font-size: 24px; color: #444;")
        self.alarm_circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.alarm_circle)
        
        # Timer pour le clignotement
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._toggle_blink)
        
        # Initialiser en état éteint
        self.setAlarm(False)
    
    def setAlarm(self, is_active: bool):
        """
        Active ou désactive l'alarme.
        
        Args:
            is_active: True pour activer l'alarme (clignotement rouge)
        """
        self.is_alarm_active = is_active
        
        if is_active:
            # Démarrer le clignotement
            self.blink_timer.start(500)  # Clignote toutes les 500ms
            self._toggle_blink()  # Premier état
        else:
            # Arrêter le clignotement et revenir à l'état éteint
            self.blink_timer.stop()
            self.alarm_circle.setStyleSheet("font-size: 24px; color: #444;")
    
    def _toggle_blink(self):
        """Bascule l'état du clignotement."""
        if self.is_alarm_active:
            self.blink_state = not self.blink_state
            if self.blink_state:
                # État allumé (rouge vif)
                self.alarm_circle.setStyleSheet("font-size: 24px; color: #ff0000;")
            else:
                # État éteint (rouge foncé)
                self.alarm_circle.setStyleSheet("font-size: 24px; color: #440000;")


class GraphWidget(QWidget):
    """
    Widget pour afficher l'historique temporel du Score de Résilience (Sʀ).
    
    Le "Pourquoi": Ce widget est le Parchemin du Temps. Il montre l'évolution
    du Score de Résilience dans le temps, permettant à l'Architecte de voir
    d'où vient l'âme du Vaisseau et comment elle évolue. C'est l'historique
    des états de conscience du Vaisseau.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 200)
        
        # Configuration du layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Titre du graphique
        self.title_label = QLabel("Chronique Temporelle du Sʀ")
        self.title_label.setStyleSheet("font-weight: bold; color: #00d4ff; font-size: 14px;")
        layout.addWidget(self.title_label)
        
        # Configuration de pyqtgraph
        pg.setConfigOptions(antialias=True)
        self.plot_widget = pg.PlotWidget()
        
        # Configuration de l'apparence
        self.plot_widget.setBackground('#1e1e1e')  # Fond sombre
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)  # Grille subtile
        
        # Configuration des axes
        self.plot_widget.setLabel('left', 'Score Sʀ', color='#ffffff')
        self.plot_widget.setLabel('bottom', 'Temps', color='#ffffff')
        self.plot_widget.setYRange(0, 1)  # Score Sʀ entre 0 et 1
        
        # Couleurs des axes
        self.plot_widget.getAxis('left').setPen(pg.mkPen(color='#ffffff'))
        self.plot_widget.getAxis('bottom').setPen(pg.mkPen(color='#ffffff'))
        
        layout.addWidget(self.plot_widget)
        
        # Données pour la courbe
        self.time_data = []
        self.score_data = []
        self.max_points = 100  # Garder les 100 derniers points
        
        # Courbe principale
        self.curve = self.plot_widget.plot(
            self.time_data, 
            self.score_data, 
            pen=pg.mkPen(color='#00d4ff', width=2),  # Couleur cyan doctrinale
            symbol='o',
            symbolSize=4,
            symbolBrush='#00d4ff'
        )
        
        # Ligne de référence à 0.8 (seuil VENTRAL)
        self.ventral_line = self.plot_widget.addLine(
            y=0.8, 
            pen=pg.mkPen(color='#90ee90', width=1, style=Qt.PenStyle.DashLine)
        )
        
        # Ligne de référence à 0.4 (seuil DORSAL)
        self.dorsal_line = self.plot_widget.addLine(
            y=0.4, 
            pen=pg.mkPen(color='#ff6b6b', width=1, style=Qt.PenStyle.DashLine)
        )
    
    def add_data_point(self, score: float):
        """
        Ajoute une nouvelle valeur à la courbe.
        
        Le "Pourquoi": Cette méthode est appelée à chaque cycle de conscience
        (60s) pour ajouter le nouveau Score de Résilience à l'historique.
        La courbe montre l'évolution de l'état de conscience du Vaisseau.
        
        Args:
            score: Le Score de Résilience (Sʀ) entre 0.0 et 1.0
        """
        current_time = datetime.now()
        
        # Ajouter les nouvelles données
        self.time_data.append(current_time)
        self.score_data.append(score)
        
        # Limiter le nombre de points pour les performances
        if len(self.time_data) > self.max_points:
            self.time_data.pop(0)
            self.score_data.pop(0)
        
        # Mettre à jour l'affichage
        self.update_plot()
    
    def update_plot(self):
        """
        Met à jour l'affichage du graphique.
        
        Le "Pourquoi": Cette méthode redessine la courbe avec les nouvelles
        données. Elle ajuste automatiquement l'échelle des axes pour que
        toute la courbe soit visible.
        """
        if len(self.time_data) > 0:
            # Convertir les timestamps en nombres pour pyqtgraph
            time_numeric = [t.timestamp() for t in self.time_data]
            
            # Mettre à jour la courbe
            self.curve.setData(time_numeric, self.score_data)
            
            # Ajuster l'échelle des axes
            if len(time_numeric) > 1:
                time_span = time_numeric[-1] - time_numeric[0]
                self.plot_widget.setXRange(
                    time_numeric[0] - time_span * 0.1, 
                    time_numeric[-1] + time_span * 0.1
                )


class ActionLogWidget(QListWidget):
    """
    Widget pour afficher l'historique des actions du Vaisseau.
    
    Le "Pourquoi": Ce widget est la Chronique des Actes. Il montre toutes
    les actions que le Vaisseau a décidées et exécutées, avec des descriptions
    en langage naturel et des icônes pour une compréhension immédiate.
    C'est l'historique des décisions et des interventions du Vaisseau.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuration de l'apparence
        self.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-family: 'Consolas', monospace;
                font-size: 11px;
                border: 1px solid #444;
                selection-background-color: #404040;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #404040;
            }
        """)
        
        # Limiter le nombre d'items pour les performances
        self.max_items = 50
    
    def log_action(self, action: Action, timestamp: str):
        """
        Ajoute une nouvelle action à la chronique.
        
        Le "Pourquoi": Cette méthode est appelée à chaque fois qu'une action
        est décidée et exécutée. Elle formate l'action en langage naturel
        avec des icônes pour une compréhension immédiate par l'Architecte.
        
        Args:
            action: L'action décidée par le Vaisseau
            timestamp: Le timestamp formaté de l'action
        """
        # Déterminer l'icône selon le type d'action
        icon = self._get_action_icon(action.id)
        
        # Formater la description en langage naturel
        description = self._format_action_description(action)
        
        # Créer le texte de l'item
        item_text = f"{icon} [{timestamp}] {description}"
        
        # Créer et ajouter l'item
        item = QListWidgetItem(item_text)
        self.addItem(item)
        
        # Limiter le nombre d'items
        if self.count() > self.max_items:
            self.takeItem(0)  # Supprimer le plus ancien
        
        # Faire défiler vers le bas pour voir le nouvel item
        self.scrollToBottom()
    
    def _get_action_icon(self, action_id: str) -> str:
        """
        Retourne l'icône appropriée selon le type d'action.
        
        Le "Pourquoi": Les icônes permettent une compréhension visuelle
        immédiate de la nature de l'action sans avoir à lire le texte.
        
        Args:
            action_id: L'identifiant de l'action
            
        Returns:
            L'icône Unicode appropriée
        """
        icon_map = {
            'SHOW_MESSAGE': '🚨',      # Alerte
            'LOG_ONLY': '📝',          # Enregistrement
            'KERNEL_TAP': '⚡',        # Intervention système
            'SPIRIT_TAP': '🧠',        # Nettoyage mémoire
            'FORCE_GC': '🗑️',         # Garbage collection
            'RESTART_PROCESS': '🔄',   # Redémarrage
            'KILL_PROCESS': '💀',      # Arrêt forcé
            'CLEAR_CACHE': '🧹',       # Nettoyage cache
            'NETWORK_FLUSH': '🌐',     # Réseau
            'DISK_SYNC': '💾',         # Disque
        }
        return icon_map.get(action_id, '⚙️')  # Icône par défaut
    
    def _format_action_description(self, action: Action) -> str:
        """
        Formate la description de l'action en langage naturel.
        
        Le "Pourquoi": Cette méthode transforme les identifiants techniques
        d'actions en descriptions compréhensibles par l'Architecte, utilisant
        un langage naturel et poétique.
        
        Args:
            action: L'action à formater
            
        Returns:
            La description formatée en langage naturel
        """
        description_map = {
            'SHOW_MESSAGE': f"Le Vaisseau a alerté l'Architecte : {action.description}",
            'LOG_ONLY': "Le Vaisseau a gravé l'état actuel dans sa chronique",
            'KERNEL_TAP': "Le Vaisseau a tapoté la nuque du système (sync disque, flush DNS)",
            'SPIRIT_TAP': "Le Vaisseau a tapoté son front (nettoyage mémoire, pause contemplative)",
            'FORCE_GC': "Le Vaisseau a purgé sa mémoire des reliques inutiles",
            'RESTART_PROCESS': f"Le Vaisseau a redonné vie au processus : {action.description}",
            'KILL_PROCESS': f"Le Vaisseau a mis fin au processus rebelle : {action.description}",
            'CLEAR_CACHE': "Le Vaisseau a purifié ses caches de toute corruption",
            'NETWORK_FLUSH': "Le Vaisseau a renouvelé ses connexions réseau",
            'DISK_SYNC': "Le Vaisseau a scellé ses écritures sur le disque",
        }
        
        # Utiliser la description personnalisée si disponible, sinon la description par défaut
        if action.description and action.description not in description_map.values():
            return f"Le Vaisseau a exécuté : {action.description}"
        
        return description_map.get(action.id, f"Le Vaisseau a accompli l'acte : {action.id}")

# --- END OF FILE: guardian/ui/widgets.py ---

