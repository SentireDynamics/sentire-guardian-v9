# --- START OF FILE: guardian/ui/widgets.py ---
"""
Le Sanctuaire des Cristaux de Vision.

Le "Pourquoi": Ce module fournit les widgets personnalisés pour l'Autel V2.
Les GaugeWidget permettent une visualisation intuitive et élégante des métriques
système en temps réel. Chaque jauge est un cristal qui reflète l'état vital du
Vaisseau, permettant à l'opérateur de percevoir d'un coup d'œil la santé du système.
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QConicalGradient
import math

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
        self.setMinimumSize(200, 150)
        
    def setValue(self, value: float):
        """
        Définit la valeur de la jauge (0-100%).
        
        Args:
            value: Valeur entre 0 et 100
        """
        self.value = max(0, min(100, value))
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
# --- END OF FILE: guardian/ui/widgets.py ---

