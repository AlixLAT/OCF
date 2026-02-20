import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import QTimer
from models.simulation import Simulation
from gui.canvas import SimulationCanvas

class AntSimulationApp(QMainWindow):
    """Main application window for ant colony simulation"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ant Colony Simulation")
        
        # Initialize simulation with 4 ants per nest
        self.sim = Simulation(4)
        self.canvas = SimulationCanvas(self.sim)
        
        # Mode for adding elements
        self.add_mode = None
        
        # Status label
        self.status_label = QLabel("● Welcome! Click START to begin")
        
        # Control buttons
        self.btn_start = QPushButton("▶ START")
        self.btn_start.clicked.connect(self.start_simulation)
        
        self.btn_stop = QPushButton("⏸ STOP")
        self.btn_stop.clicked.connect(self.stop_simulation)
        
        self.btn_reset = QPushButton("⟲ RESET")
        self.btn_reset.clicked.connect(self.reset_simulation)
        
        self.btn_trap = QPushButton("💣 TRAP")
        self.btn_trap.clicked.connect(self.activate_trap)
        
        # Add element buttons
        self.btn_add_nest = QPushButton("+ NEST (click on canvas)")
        self.btn_add_nest.clicked.connect(self.mode_add_nest)
        self.btn_add_nest.setStyleSheet("background-color: #FFE4B5")
        
        self.btn_add_food = QPushButton("+ FOOD (click on canvas)")
        self.btn_add_food.clicked.connect(self.mode_add_food)
        self.btn_add_food.setStyleSheet("background-color: #C8E6C9")
        
        self.btn_add_obstacle = QPushButton("+ OBSTACLE (click on canvas)")
        self.btn_add_obstacle.clicked.connect(self.mode_add_obstacle)
        self.btn_add_obstacle.setStyleSheet("background-color: #BDBDBD")
        
        # Layout for control buttons
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.btn_start)
        control_layout.addWidget(self.btn_stop)
        control_layout.addWidget(self.btn_reset)
        control_layout.addWidget(self.btn_trap)
        
        # Layout for add buttons
        add_layout = QHBoxLayout()
        add_layout.addWidget(self.btn_add_nest)
        add_layout.addWidget(self.btn_add_food)
        add_layout.addWidget(self.btn_add_obstacle)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(add_layout)
        
        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_running = False

    def start_simulation(self):
        """Start the simulation"""
        if not self.is_running:
            self.timer.start(30)  # Update every 30ms
            self.is_running = True
            self.status_label.setText("● ▶ Simulation running...")

    def stop_simulation(self):
        """Pause the simulation"""
        self.timer.stop()
        self.is_running = False
        self.status_label.setText("● ⏸ Simulation paused")

    def reset_simulation(self):
        """Reset to initial state"""
        self.timer.stop()
        self.sim.reset()
        self.canvas.update()
        self.is_running = False
        self.status_label.setText("● ⟲ Simulation reset")

    def activate_trap(self):
        """Activate food trap"""
        self.sim.activate_trap()
        self.status_label.setText("💥 TRAP ACTIVATED - Ants panic!")

    def mode_add_nest(self):
        """Enable mode for adding nests"""
        self.add_mode = 'nest'
        self.status_label.setText("🖱️ Click on canvas to add a nest")

    def mode_add_food(self):
        """Enable mode for adding food"""
        self.add_mode = 'food'
        self.status_label.setText("🖱️ Click on canvas to add food")

    def mode_add_obstacle(self):
        """Enable mode for adding obstacles"""
        self.add_mode = 'obstacle'
        self.status_label.setText("🖱️ Click on canvas to add an obstacle")

    def mousePressEvent(self, event):
        """Handle mouse clicks for adding elements"""
        if self.add_mode is None:
            return
        
        canvas_pos = self.canvas.mapFromGlobal(self.mapToGlobal(event.pos()))
        x, y = canvas_pos.x(), canvas_pos.y()
        
        # Validate position is within canvas
        if 0 <= x < self.canvas.width() and 0 <= y < self.canvas.height():
            if self.add_mode == 'nest':
                self.sim.add_nest(x, y)
                self.status_label.setText(f"✓ Nest added at ({x}, {y})")
            elif self.add_mode == 'food':
                self.sim.add_resource(x, y)
                self.status_label.setText(f"✓ Food added at ({x}, {y})")
            elif self.add_mode == 'obstacle':
                self.sim.add_obstacle(x, y)
                self.status_label.setText(f"✓ Obstacle added at ({x}, {y})")
            
            self.add_mode = None
            self.canvas.update()

    def update_frame(self):
        """Update simulation frame"""
        self.sim.update(2)  # Speed parameter
        self.sim.update_trap()
        self.canvas.update()

def main():
    app = QApplication(sys.argv)
    window = AntSimulationApp()
    window.setGeometry(50, 50, 1050, 900)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    def __init__(self):
        super().__init__()
        # Titre de la fenêtre
        self.setWindowTitle("Simulation des Fourmis")
        
        # Créer la simulation avec 4 fourmis par nid (6 nids = 24 fourmis total)
        self.sim = Simulation(4)
        
        # Créer la zone de dessin
        self.vue = ZoneDessin(self.sim)
        
        # Mode ajout (None, 'nid', 'ressource', 'obstacle')
        self.mode_ajout = None
        
        # Créer un label pour afficher les infos
        self.label_info = QLabel("●  Bienvenue ! Appuyez sur ▶ DÉMARRER")
        
        # LIGNE 1 : Contrôles de simulation
        self.btn_demarrer = QPushButton("▶ DÉMARRER")
        self.btn_demarrer.clicked.connect(self.demarrer)
        
        self.btn_arreter = QPushButton("⏸ STOP")
        self.btn_arreter.clicked.connect(self.arreter)
        
        self.btn_reset = QPushButton("⟲ RESET")
        self.btn_reset.clicked.connect(self.reset_simulation)
        
        self.btn_piege = QPushButton("💣 PIÈGE")
        self.btn_piege.clicked.connect(self.activer_piege)
        
        layout_ligne1 = QHBoxLayout()
        layout_ligne1.addWidget(self.btn_demarrer)
        layout_ligne1.addWidget(self.btn_arreter)
        layout_ligne1.addWidget(self.btn_reset)
        layout_ligne1.addWidget(self.btn_piege)
        
        # LIGNE 2 : Ajouter des éléments
        self.btn_ajouter_nid = QPushButton("+ NID (cliquez sur la zone)")
        self.btn_ajouter_nid.clicked.connect(self.mode_ajouter_nid)
        self.btn_ajouter_nid.setStyleSheet("background-color: #FFE4B5")
        
        self.btn_ajouter_ressource = QPushButton("+ NOURRITURE (cliquez sur la zone)")
        self.btn_ajouter_ressource.clicked.connect(self.mode_ajouter_ressource)
        self.btn_ajouter_ressource.setStyleSheet("background-color: #C8E6C9")
        
        self.btn_ajouter_obstacle = QPushButton("+ OBSTACLE (cliquez sur la zone)")
        self.btn_ajouter_obstacle.clicked.connect(self.mode_ajouter_obstacle)
        self.btn_ajouter_obstacle.setStyleSheet("background-color: #BDBDBD")
        
        layout_ligne2 = QHBoxLayout()
        layout_ligne2.addWidget(self.btn_ajouter_nid)
        layout_ligne2.addWidget(self.btn_ajouter_ressource)
        layout_ligne2.addWidget(self.btn_ajouter_obstacle)
        
        # Mettre tous les éléments dans la fenêtre
        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addLayout(layout_ligne1)
        layout.addWidget(self.vue)
        layout.addLayout(layout_ligne2)
        
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Timer pour l'animation (met à jour 30 fois par seconde)
        self.timer = QTimer()
        self.timer.timeout.connect(self.boucle_jeu)
        
        self.est_en_marche = False

    def demarrer(self):
        """Bouton Démarrer"""
        if not self.est_en_marche:
            self.timer.start(30)
            self.est_en_marche = True
            self.label_info.setText("● ▶  Simulation EN COURS...")

    def arreter(self):
        """Bouton Arrêter"""
        self.timer.stop()
        self.est_en_marche = False
        self.label_info.setText("● ⏸  Simulation ARRÊTÉE")

    def reset_simulation(self):
        """Bouton Reset"""
        self.timer.stop()
        self.sim.reinitialiser()
        self.vue.update()
        self.est_en_marche = False
        self.label_info.setText("● ⟲  Simulation RÉINITIALISÉE")

    def activer_piege(self):
        """Bouton Piège"""
        self.sim.activer_piege()
        self.label_info.setText("💥 PIÈGE ACTIVÉ - Les fourmis FOLLES !")

    def mode_ajouter_nid(self):
        """Mode ajouter un nid"""
        self.mode_ajout = 'nid'
        self.label_info.setText("🖱️  Cliquez sur la zone pour ajouter un NID")

    def mode_ajouter_ressource(self):
        """Mode ajouter une ressource"""
        self.mode_ajout = 'ressource'
        self.label_info.setText("🖱️  Cliquez sur la zone pour ajouter de la NOURRITURE")

    def mode_ajouter_obstacle(self):
        """Mode ajouter un obstacle"""
        self.mode_ajout = 'obstacle'
        self.label_info.setText("🖱️  Cliquez sur la zone pour ajouter un OBSTACLE")

    def mousePressEvent(self, event):
        """Détecte le clic sur la zone de dessin"""
        # Récupérer les coordonnées du clic
        x = event.x()
        y = event.y()
        
        # La zone de dessin commence après les labels et boutons
        # On doit ajuster les coordonnées
        vue_rect = self.vue.geometry()
        
        # Vérifier si le clic est dans la zone de dessin
        if vue_rect.contains(self.mapFromGlobal(self.mapToGlobal(event.pos()))):
            x_local = x - vue_rect.x()
            y_local = y - vue_rect.y()
            
            if self.mode_ajout == 'nid':
                self.sim.ajouter_nid(x_local, y_local)
                self.label_info.setText(f"✓ Nid ajouté à ({x_local}, {y_local})")
                self.mode_ajout = None
                self.vue.update()
            
            elif self.mode_ajout == 'ressource':
                self.sim.ajouter_ressource(x_local, y_local)
                self.label_info.setText(f"✓ Nourriture ajoutée à ({x_local}, {y_local})")
                self.mode_ajout = None
                self.vue.update()
            
            elif self.mode_ajout == 'obstacle':
                self.sim.ajouter_obstacle(x_local, y_local)
                self.label_info.setText(f"✓ Obstacle ajouté à ({x_local}, {y_local})")
                self.mode_ajout = None
                self.vue.update()

    def boucle_jeu(self):
        """Updates chaque image"""
        # Faire bouger les fourmis avec vitesse = 2 pixels par frame
        self.sim.mettre_a_jour(2)
        
        # Gérer le temps du piège
        self.sim.reduire_piege()
        
        # Redessiner tout
        self.vue.update()

# Démarrer l'application
app = QApplication(sys.argv)
fen = MaFenetre()
fen.setGeometry(50, 50, 1050, 900)  # Position et taille
fen.show()
sys.exit(app.exec())