from config import (
    INITIAL_NESTS, INITIAL_RESOURCES, INITIAL_OBSTACLES
)
from models.ant import Ant

class Simulation:
    """Main simulation controller managing all ants and resources"""
    
    def __init__(self, ants_per_nest=4):
        """Initialize simulation with ants at each nest"""
        self.ants = []
        self.nests = INITIAL_NESTS.copy()
        self.resources = INITIAL_RESOURCES.copy()
        self.obstacles = INITIAL_OBSTACLES.copy()
        self.trap_active = False
        self.trap_timer = 0
        self.ants_per_nest = ants_per_nest
        
        # Create initial ants
        for nest in self.nests:
            for _ in range(ants_per_nest):
                self.ants.append(Ant(nest))

    def update(self, speed):
        """Update all ants in the simulation"""
        for ant in self.ants:
            ant.move(speed, self.resources, self.obstacles, self.trap_active)
    
    def activate_trap(self):
        """Activate the food trap - ants go crazy for 3 seconds"""
        self.trap_active = True
        self.trap_timer = 90  # 30 fps * 3 seconds
    
    def update_trap(self):
        """Decrease trap timer and deactivate when done"""
        if self.trap_active:
            self.trap_timer -= 1
            if self.trap_timer <= 0:
                self.trap_active = False
                for ant in self.ants:
                    ant.is_panicked = False
    
    def add_nest(self, x, y):
        """Add a new nest and create ants there"""
        self.nests.append((x, y))
        for _ in range(self.ants_per_nest):
            self.ants.append(Ant((x, y)))
    
    def add_resource(self, x, y):
        """Add a new food resource"""
        self.resources.append({"x": x, "y": y, "type": "food"})
    
    def add_obstacle(self, x, y, width=50, height=50):
        """Add a new obstacle"""
        self.obstacles.append({"x": x, "y": y, "width": width, "height": height})
    
    def reset(self):
        """Reset simulation to initial state"""
        self.ants = []
        self.nests = INITIAL_NESTS.copy()
        self.resources = INITIAL_RESOURCES.copy()
        self.obstacles = INITIAL_OBSTACLES.copy()
        self.trap_active = False
        
        for nest in self.nests:
            for _ in range(self.ants_per_nest):
                self.ants.append(Ant(nest))