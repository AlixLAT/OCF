from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont
from config import WINDOW_WIDTH, WINDOW_HEIGHT, PHEROMONE_GRID_SIZE

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
        
        # Draw pheromone grid (faint visualization)
        for x in range(len(self.sim.pheromone_grid)):
            for y in range(len(self.sim.pheromone_grid[0])):
                pheromone_strength = self.sim.pheromone_grid[x][y]
                if pheromone_strength > 0.1:
                    # Normalize strength for color (0-10 max)
                    intensity = min(int(pheromone_strength * 20), 150)
                    color = QColor(50, 50, 255, intensity)
                    painter.fillRect(
                        x * PHEROMONE_GRID_SIZE,
                        y * PHEROMONE_GRID_SIZE,
                        PHEROMONE_GRID_SIZE,
                        PHEROMONE_GRID_SIZE,
                        color
                    )
        
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
        
        # Resources with amount displayed
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)
        
        for resource in self.sim.resources:
            x, y = resource["x"], resource["y"]
            amount = resource["amount"]
            
            # Color brightness based on remaining amount
            if amount <= 0:
                color = QColor(100, 100, 100)  # Empty - gray
            elif amount < 30:
                color = QColor(200, 100, 50)  # Low - orange
            else:
                color = QColor(50, 200, 50)  # Full - green
            
            painter.fillRect(x-12, y-12, 24, 24, color)
            painter.fillRect(x-4, y-4, 8, 8, QColor(200, 255, 200))
            
            # Draw amount text
            painter.setPen(QColor(0, 0, 0))
            painter.drawText(x-15, y+20, 30, 15, 0, str(int(amount)))
        
        # Ants
        for ant in self.sim.ants:
            if ant.is_panicked:
                color = QColor(255, 100, 100)
            elif ant.has_food:
                color = QColor(255, 200, 0)
            elif ant.returning_to_nest:
                color = QColor(100, 100, 255)  # Blue while returning
            else:
                color = QColor(50, 50, 50)
            
            painter.fillRect(int(ant.x)-3, int(ant.y)-3, 6, 6, color)