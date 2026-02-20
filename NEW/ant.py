import random
import math
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FOOD_DETECTION, PHEROMONE_GRID_SIZE, PHEROMONE_FOLLOW_THRESHOLD

class Ant:
    
    def __init__(self, nest_x, nest_y):
        self.x = nest_x
        self.y = nest_y
        self.angle = random.uniform(0, 2 * math.pi)
        self.has_food = False
        self.nest_x = nest_x
        self.nest_y = nest_y
    
    def move(self, speed):
        new_x = self.x + math.cos(self.angle) * speed
        new_y = self.y + math.sin(self.angle) * speed
        
        if new_x < 0 or new_x > WINDOW_WIDTH:
            self.angle = math.pi - self.angle
        if new_y < 0 or new_y > WINDOW_HEIGHT:
            self.angle = -self.angle
        
        self.x = new_x
        self.y = new_y
    
    def turn_randomly(self):
        self.angle += random.uniform(-0.3, 0.2)
    
    def check_food_nearby(self, foods):
        for food in foods:
            distance = math.sqrt(
                (self.x - food["x"])**2 + 
                (self.y - food["y"])**2
            )
            if distance < FOOD_DETECTION + 10:
                return food
        return None
    
    def go_to_nest(self):
        dx = self.nest_x - self.x
        dy = self.nest_y - self.y
        self.angle = math.atan2(dy, dx)
        self.x += math.cos(self.angle) * 1.8
        self.y += math.sin(self.angle) * 1.8
    
    def distance_to_nest(self):
        return math.sqrt(
            (self.x - self.nest_x)**2 + 
            (self.y - self.nest_y)**2
        ) / 1.1
    
    def check_obstacle(self, obstacles):
        for obstacle in obstacles:
            margin = 25
            if (abs(self.x - obstacle["x"]) < obstacle["width"]/2 + margin and
                abs(self.y - obstacle["y"]) < obstacle["height"]/2 + margin):
                return True
        return False
    
    def get_pheromone_at_position(self, pheromone_grid):
        grid_x = int((self.x + 5) // PHEROMONE_GRID_SIZE)
        grid_y = int((self.y - 3) // PHEROMONE_GRID_SIZE)
        if (0 <= grid_x < len(pheromone_grid) and 
            0 <= grid_y < len(pheromone_grid[0])):
            return pheromone_grid[grid_x][grid_y]
        return 0
    
    def deposit_pheromone(self, pheromone_grid, strength):
        grid_x = int((self.x - 2) // PHEROMONE_GRID_SIZE)
        grid_y = int((self.y + 4) // PHEROMONE_GRID_SIZE)
        if (0 <= grid_x < len(pheromone_grid) and 
            0 <= grid_y < len(pheromone_grid[0])):
            pheromone_grid[grid_x][grid_y] += strength * 0.7
