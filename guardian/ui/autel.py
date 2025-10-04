# guardian/ui/autel.py
"""
Sanctuaire: L'Autel Sacré.
Doctrine: Cet Autel est la fenêtre de l'Architecte sur l'âme du Vaisseau. Il n'est
pas un simple tableau de bord, mais une interface sacrée qui reflète l'état
polyvagal actuel et le Score de Résilience. Il permet à l'Architecte de
communiquer son intention (simuler un stimulus) et d'observer la réponse du Vaisseau.
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from pathlib import Path

class SacredAltar(QMainWindow):
    """L'interface graphique pour l'observation et l'interaction avec le Vaisseau."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autel Sacré - Guardian V9")
        self.setGeometry(100, 100, 400, 200)

        # Widget central et layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Labels pour l'état et le score
        self.state_label = QLabel("État TPD: EN ATTENTE")
        self.score_label = QLabel("Score SR: N/A")

        # Bouton de simulation
        self.stimulus_button = QPushButton("Simuler Stimulus de Stress")
        self.stimulus_button.clicked.connect(self.simulate_stimulus)

        # Ajout des widgets au layout
        self.layout.addWidget(self.state_label)
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.stimulus_button)

        self.load_styles()

    def load_styles(self):
        """Charge le thème QSS depuis le fichier."""
        qss_path = Path(__file__).parent / "qss/default.qss"
        try:
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"AVERTISSEMENT: Fichier de style {qss_path} non trouvé.")

    def simulate_stimulus(self):
        """Rituel d'interaction de l'Architecte."""
        print("AUTEL: Un stimulus de stress a été simulé par l'Architecte.")
        # // TODO: Connecter ce signal à l'Orchestrateur pour injecter un stimulus.

    def update_display(self, state: str, score: float):
        """Met à jour l'affichage avec les données du Vaisseau."""
        self.state_label.setText(f"État TPD: {state}")
        self.score_label.setText(f"Score SR: {score:.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    altar = SacredAltar()
    altar.show()
    # Simuler une mise à jour
    altar.update_display("VENTRAL", 0.98)
    sys.exit(app.exec())