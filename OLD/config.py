# Ant Simulation Configuration

# Window dimensions (pixels)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Initial nest positions (left and right sides)
INITIAL_NESTS = [
    (100, 150),     # Left - Top
    (100, 350),     # Left - Middle
    (100, 550),     # Left - Bottom
    (900, 150),     # Right - Top
    (900, 350),     # Right - Middle
    (900, 550),     # Right - Bottom
]

# Initial food resources
INITIAL_RESOURCES = [
    {"x": 150, "y": 100, "amount": 100, "type": "food"},
    {"x": 150, "y": 600, "amount": 100, "type": "food"},
    {"x": 850, "y": 100, "amount": 100, "type": "food"},
    {"x": 850, "y": 600, "amount": 100, "type": "food"},
]

# Initial obstacles
INITIAL_OBSTACLES = [
    {"x": 500, "y": 350, "width": 150, "height": 50},
]

# Detection distance for resources
DETECTION_DISTANCE = 50

# Obstacle collision radius
OBSTACLE_RADIUS = 60

# Pheromone parameters
PHEROMONE_GRID_SIZE = 10  # Size of pheromone cell
PHEROMONE_STRENGTH = 10.0  # Initial strength when ant deposits
PHEROMONE_EVAPORATION = 0.95  # Evaporation rate per frame
PHEROMONE_FOLLOW_THRESHOLD = 0.5  # Minimum strength to follow

# Resource consumption
RESOURCE_CONSUMPTION_PER_ANT = 1  # Amount consumed per ant per visit