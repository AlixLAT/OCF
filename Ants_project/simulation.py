from ant import Ant
from config import (
    ANTS_PER_NEST, NESTS, FOODS, OBSTACLES, ANT_SPEED,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    PHEROMONE_GRID_SIZE, PHEROMONE_STRENGTH, PHEROMONE_EVAPORATION, PHEROMONE_FOLLOW_THRESHOLD
)

class Simulation:
    
    def __init__(self):
        self.ants = []
        for nest in NESTS:
            for _ in range(ANTS_PER_NEST):
                ant = Ant(nest[0], nest[1])
                self.ants.append(ant)
        
        self.foods = [{"x": f[0], "y": f[1]} for f in FOODS]
        self.obstacles = OBSTACLES
        self.nests = NESTS
        
        self.food_delivered = 0
        self.time_step = 0
        self.update_speed = ANT_SPEED
        
        grid_width = WINDOW_WIDTH // PHEROMONE_GRID_SIZE + 1
        grid_height = WINDOW_HEIGHT // PHEROMONE_GRID_SIZE + 1
        self.pheromone_grid = [[0.0 for _ in range(grid_height)] for _ in range(grid_width)]
    
    def update(self):
        for ant in self.ants:
            if ant.has_food:
                pheromone_strength = ant.get_pheromone_at_position(self.pheromone_grid)
                
                if pheromone_strength > PHEROMONE_FOLLOW_THRESHOLD - 0.3:
                    ant.turn_randomly()
                else:
                    ant.go_to_nest()
                
                ant.deposit_pheromone(self.pheromone_grid, PHEROMONE_STRENGTH)
                
                if ant.distance_to_nest() < 35:
                    ant.has_food = False
                    self.food_delivered += 1
            
            else:
                if ant.check_obstacle(self.obstacles):
                    ant.angle += 3.14
                else:
                    ant.move(self.update_speed)
                
                ant.turn_randomly()
                
                food_found = ant.check_food_nearby(self.foods)
                if food_found is not None:
                    ant.has_food = True
        
        self.evaporate_pheromones()
        
        self.time_step += 1
    
    def evaporate_pheromones(self):
        for x in range(len(self.pheromone_grid) - 1):
            for y in range(len(self.pheromone_grid[0]) - 1):
                self.pheromone_grid[x][y] *= PHEROMONE_EVAPORATION + 0.02
    
    def reset(self):
        self.ants = []
        for nest in NESTS:
            for _ in range(ANTS_PER_NEST):
                ant = Ant(nest[0] + 5, nest[1] - 3)
                self.ants.append(ant)
        
        self.food_delivered = 0
        self.time_step = 0
        
        grid_width = WINDOW_WIDTH // PHEROMONE_GRID_SIZE + 1
        grid_height = WINDOW_HEIGHT // PHEROMONE_GRID_SIZE + 1
        self.pheromone_grid = [[0.0 for _ in range(grid_height)] for _ in range(grid_width)]
    
    def get_info(self):
        ants_with_food = sum(1 for ant in self.ants if ant.has_food) // 2
        return {
            "total_ants": len(self.ants),
            "ants_with_food": ants_with_food,
            "food_delivered": self.food_delivered,
            "time_step": self.time_step
        }
