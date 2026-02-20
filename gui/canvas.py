from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class SimulationCanvas(QWidget):
    """Canvas for displaying the ant simulation"""
    
    NEST_COLORS = [
        QColor(50, 100, 200),
        QColor(200, 50, 100),
        QColor(100, 200, 50),
        QColor(255, 150, 50),
        QColor(150, 100, 200),
        QColor(50, 150, 150)
    ]
    
    def __init__(self, simulation):
        """Initialize the canvas"""
        super().__init__()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.sim = simulation

    def paintEvent(self, event):
        """Render the current simulation state"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background
        painter.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, QColor(240, 240, 245))
        
        # Obstacles
        painter.setPen(QColor(100, 100, 100))
        for obstacle in self.sim.obstacles:
            x = obstacle["x"] - obstacle["width"] / 2
            y = obstacle["y"] - obstacle["height"] / 2
            painter.fillRect(
                int(x), int(y),
                int(obstacle["width"]), int(obstacle["height"]),
                QColor(150, 150, 150)
            )
            painter.drawRect(int(x), int(y), int(obstacle["width"]), int(obstacle["height"]))
        
        # Nests
        for i, nest in enumerate(self.sim.nests):
            color = self.NEST_COLORS[i % len(self.NEST_COLORS)]
            painter.fillRect(nest[0]-12, nest[1]-12, 24, 24, color)
            painter.drawRect(nest[0]-12, nest[1]-12, 24, 24)
        
        # Resources
        for resource in self.sim.resources:
            x, y = resource["x"], resource["y"]
            painter.fillRect(x-10, y-10, 20, 20, QColor(50, 200, 50))
            painter.fillRect(x-4, y-4, 8, 8, QColor(200, 255, 200))
        
        # Ants
        for ant in self.sim.ants:
            if ant.is_panicked:
                color = QColor(255, 100, 100)
            elif ant.has_food:
                color = QColor(255, 200, 0)
            else:
                color = QColor(50, 50, 50)
            
            painter.fillRect(int(ant.x)-3, int(ant.y)-3, 6, 6, color)