from config import (
    INITIAL_NESTS, INITIAL_RESOURCES, INITIAL_OBSTACLES,
    WINDOW_WIDTH, WINDOW_HEIGHT, PHEROMONE_GRID_SIZE,
    PHEROMONE_EVAPORATION, RESOURCE_CONSUMPTION_PER_ANT
)
from models.ant import Ant

class Simulation:
    """Main simulation controller managing all ants and resources"""
    
    def __init__(self, ants_per_nest=4):
        """Initialize simulation with ants at each nest"""
        self.ants = []
        self.nests = INITIAL_NESTS.copy()
        self.resources = []
        # Deep copy resources to avoid reference issues
        for res in INITIAL_RESOURCES:
            self.resources.append({
                "x": res["x"],
                "y": res["y"],
                "amount": res["amount"],
                "type": res["type"]
            })
        self.obstacles = INITIAL_OBSTACLES.copy()
        self.trap_active = False
        self.trap_timer = 0
        self.ants_per_nest = ants_per_nest
        
        # Pheromone grid
        grid_width = int(WINDOW_WIDTH // PHEROMONE_GRID_SIZE) + 1
        grid_height = int(WINDOW_HEIGHT // PHEROMONE_GRID_SIZE) + 1
        self.pheromone_grid = [[0.0 for _ in range(grid_height)] for _ in range(grid_width)]
        
        # Create initial ants
        for nest in self.nests:
            for _ in range(ants_per_nest):
                self.ants.append(Ant(nest))

    def update_pheromones(self):
        """Update pheromone evaporation"""
        for x in range(len(self.pheromone_grid)):
            for y in range(len(self.pheromone_grid[0])):
                self.pheromone_grid[x][y] *= PHEROMONE_EVAPORATION
                # Remove small values
                if self.pheromone_grid[x][y] < 0.01:
                    self.pheromone_grid[x][y] = 0.0

    def consume_resources(self):
        """Check if ants are at resources and consume them"""
        for ant in self.ants:
            if ant.returning_to_nest and ant.has_food and ant.food_location is not None:
                # Ant has reached nest and delivering food
                if 0 <= ant.food_location < len(self.resources):
                    if ant.x < ant.nest_pos[0] + 20 and ant.x > ant.nest_pos[0] - 20:
                        if ant.y < ant.nest_pos[1] + 20 and ant.y > ant.nest_pos[1] - 20:
                            # Ant delivered food, consume from resource
                            self.resources[ant.food_location]["amount"] -= RESOURCE_CONSUMPTION_PER_ANT

    def update(self, speed):
        """Update all ants in the simulation"""
        for ant in self.ants:
            ant.move(speed, self.resources, self.obstacles, self.trap_active, self.pheromone_grid)
        
        # Update pheromones
        self.update_pheromones()
        
        # Consume resources
        self.consume_resources()
    
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
        self.resources.append({"x": x, "y": y, "amount": 100, "type": "food"})
    
    def add_obstacle(self, x, y, width=50, height=50):
        """Add a new obstacle"""
        self.obstacles.append({"x": x, "y": y, "width": width, "height": height})
    
    def reset(self):
        """Reset simulation to initial state"""
        self.ants = []
        self.nests = INITIAL_NESTS.copy()
        self.resources = []
        for res in INITIAL_RESOURCES:
            self.resources.append({
                "x": res["x"],
                "y": res["y"],
                "amount": res["amount"],
                "type": res["type"]
            })
        self.obstacles = INITIAL_OBSTACLES.copy()
        self.trap_active = False
        
        # Reset pheromone grid
        grid_width = int(WINDOW_WIDTH // PHEROMONE_GRID_SIZE) + 1
        grid_height = int(WINDOW_HEIGHT // PHEROMONE_GRID_SIZE) + 1
        self.pheromone_grid = [[0.0 for _ in range(grid_height)] for _ in range(grid_width)]
        
        for nest in self.nests:
            for _ in range(self.ants_per_nest):
                self.ants.append(Ant(nest))