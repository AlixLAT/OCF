from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QTimer
from gui.canvas import ZoneDessin
from models.simulation import Simulation

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation Fourmis")
        
        self.sim = Simulation()
        self.zone = ZoneDessin(self.sim)
        
        layout = QVBoxLayout()
        layout.addWidget(self.zone)
        
        self.btn = QPushButton("Start / Pause")
        self.btn.clicked.connect(self.clic_bouton)
        layout.addWidget(self.btn)
        
        c = QWidget()
        c.setLayout(layout)
        self.setCentralWidget(c)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tour_de_jeu)

    def clic_bouton(self):
        if self.timer.isActive(): self.timer.stop()
        else: self.timer.start(30)

    def tour_de_jeu(self):
        self.sim.mettre_a_jour(5, 0.9)
        self.zone.update()