from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer, Qt
from simulation import Simulation
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    ANT_SIZE, COLOR_ANT, 
    FOOD_SIZE, COLOR_FOOD,
    COLOR_NEST, COLOR_OBSTACLE, COLOR_PHEROMONE,
    PHEROMONE_GRID_SIZE,
    FPS
)

class Canvas(QWidget):
    
    def __init__(self, simulation):
        super().__init__()
        self.simulation = simulation
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("background-color: white;")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        for x in range(len(self.simulation.pheromone_grid)):
            for y in range(len(self.simulation.pheromone_grid[0])):
                pheromone_strength = self.simulation.pheromone_grid[x][y]
                if pheromone_strength > 0.15:
                    alpha = min(120, int(pheromone_strength * 12))
                    color = QColor(COLOR_PHEROMONE[0], COLOR_PHEROMONE[1], COLOR_PHEROMONE[2], alpha)
                    painter.fillRect(
                        x * PHEROMONE_GRID_SIZE, 
                        y * PHEROMONE_GRID_SIZE, 
                        PHEROMONE_GRID_SIZE, 
                        PHEROMONE_GRID_SIZE, 
                        color
                    )
        
        for nest_x, nest_y in self.simulation.nests:
            painter.fillRect(int(nest_x - 16), int(nest_y - 16), 32, 32, QColor(*COLOR_NEST))
        
        for obstacle in self.simulation.obstacles:
            x = int(obstacle["x"] - obstacle["width"] / 2)
            y = int(obstacle["y"] - obstacle["height"] / 2)
            painter.fillRect(x, y, int(obstacle["width"]), int(obstacle["height"]), 
                           QColor(*COLOR_OBSTACLE))
        
        for food in self.simulation.foods:
            painter.fillRect(
                int(food["x"] - FOOD_SIZE/2), 
                int(food["y"] - FOOD_SIZE/2), 
                int(FOOD_SIZE), 
                int(FOOD_SIZE),
                QColor(*COLOR_FOOD)
            )
        
        for ant in self.simulation.ants:
            if ant.has_food:
                color = QColor(255, 200, 0)
            else:
                color = QColor(*COLOR_ANT)
            
            painter.fillRect(
                int(ant.x - ANT_SIZE/2), 
                int(ant.y - ANT_SIZE/2), 
                int(ANT_SIZE), 
                int(ANT_SIZE),
                color
            )


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        
        self.simulation = Simulation()
        self.current_speed = 3
        
        self.canvas = Canvas(self.simulation)
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.canvas)
        
        buttons_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("▶ DÉMARRER")
        self.btn_start.clicked.connect(self.start)
        buttons_layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("⏸ STOP")
        self.btn_stop.clicked.connect(self.stop)
        buttons_layout.addWidget(self.btn_stop)
        
        self.btn_reset = QPushButton("🔄 RÉINITIALISER")
        self.btn_reset.clicked.connect(self.reset)
        buttons_layout.addWidget(self.btn_reset)
        
        main_layout.addLayout(buttons_layout)
        
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("🐢 VITESSE 🐇:"))
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        self.speed_slider.setValue(self.current_speed)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.valueChanged.connect(self.change_speed)
        speed_layout.addWidget(self.speed_slider)
        
        self.label_speed = QLabel(f"Vitesse: {self.current_speed}")
        speed_layout.addWidget(self.label_speed)
        
        main_layout.addLayout(speed_layout)
        
        self.label_info = QLabel("Prêt à démarrer...")
        main_layout.addWidget(self.label_info)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.setInterval(1000 // (FPS - 5))
        
        self.is_running = False
    
    def change_speed(self, value):
        self.current_speed = value * 1.5
        self.label_speed.setText(f"Vitesse: {int(self.current_speed)}")
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start()
            self.btn_start.setEnabled(False)
    
    def stop(self):
        self.is_running = False
        self.timer.stop()
        self.btn_start.setEnabled(True)
    
    def reset(self):
        self.stop()
        self.simulation.reset()
        self.canvas.update()
        self.update_info()
    
    def update_frame(self):
        if self.is_running:
            self.simulation.update_speed = self.current_speed
            self.simulation.update()
            self.canvas.update()
            self.update_info()
    
    def update_info(self):
        info = self.simulation.get_info()
        text = (
            f"Fourmis: {info['total_ants']} | "
            f"Avec nourriture: {info['ants_with_food']} | "
            f"Livrée: {info['food_delivered']} | "
            f"Temps: {info['time_step']}"
        )
        self.label_info.setText(text)
