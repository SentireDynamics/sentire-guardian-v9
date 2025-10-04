# --- START OF FILE: guardian/ui/autel.py ---
"""
L'Autel - L'Interface Sacrée de Contrôle.

Le "Pourquoi": Ce module fournit une interface graphique (GUI) pour que
l'opérateur humain puisse observer et interagir avec le Vaisseau. Il affiche
les journaux en temps réel, montre l'état actuel et permet de déclencher
manuellement des cycles de perception. Il utilise PyQt6 et le mécanisme de
signaux/slots pour découpler l'interface de la logique principale, garantissant
que l'UI reste réactive même lorsque le Vaisseau est en pleine réflexion.
"""
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QApplication
from PyQt6.QtCore import pyqtSignal, QObject

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
    La fenêtre principale de l'interface du Vaisseau Guardian.
    """
    force_cycle_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autel du Vaisseau Guardian V9")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        self.force_button = QPushButton("Forcer le Cycle de Conscience")
        self.force_button.clicked.connect(self.force_cycle_signal.emit)
        layout.addWidget(self.force_button)

    def add_log_message(self, message: str):
        """Ajoute un message au widget de journalisation."""
        self.log_display.append(message)
        self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())
# --- END OF FILE: guardian/ui/autel.py ---