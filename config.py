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
    {"x": 150, "y": 100, "type": "food"},
    {"x": 150, "y": 600, "type": "food"},
    {"x": 850, "y": 100, "type": "food"},
    {"x": 850, "y": 600, "type": "food"},
]

# Initial obstacles
INITIAL_OBSTACLES = [
    {"x": 500, "y": 350, "width": 150, "height": 50},
]

# Detection distance for resources
DETECTION_DISTANCE = 50

# Obstacle collision radius
OBSTACLE_RADIUS = 60