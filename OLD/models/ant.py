import random
import math
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    DETECTION_DISTANCE, OBSTACLE_RADIUS,
    PHEROMONE_GRID_SIZE, PHEROMONE_FOLLOW_THRESHOLD
)

class Ant:
    """Represents a single ant in the simulation"""
    
    def __init__(self, nest_info):
        """Initialize an ant at a given nest position"""
        self.x = nest_info[0]
        self.y = nest_info[1]
        self.angle = random.uniform(0, 2 * math.pi)
        self.has_food = False
        self.is_panicked = False
        self.nest_pos = nest_info
        
        # New: Tracking system
        self.returning_to_nest = False
        self.path_memory = []  # Store path while finding food
        self.food_location = None
        self.target_resource = None  # Current target resource index

    def check_collision(self, x, y, obstacles):
        """Check if position collides with any obstacle"""
        for obstacle in obstacles:
            ox, oy = obstacle["x"], obstacle["y"]
            ow = obstacle["width"] / 2
            oh = obstacle["height"] / 2
            
            dist_x = abs(x - ox)
            dist_y = abs(y - oy)
            
            if dist_x < ow + OBSTACLE_RADIUS and dist_y < oh + OBSTACLE_RADIUS:
                return True
        return False

    def get_pheromone_influence(self, pheromone_grid):
        """Get pheromone guidance at current position"""
        grid_x = int(self.x // PHEROMONE_GRID_SIZE)
        grid_y = int(self.y // PHEROMONE_GRID_SIZE)
        
        if 0 <= grid_x < len(pheromone_grid) and 0 <= grid_y < len(pheromone_grid[0]):
            return pheromone_grid[grid_x][grid_y]
        return 0

    def find_nearest_resource_with_stock(self, resources):
        """Find the nearest resource that has stock"""
        best_resource = None
        best_distance = float('inf')
        best_index = None
        
        for i, resource in enumerate(resources):
            if resource["amount"] > 0:  # Only consider resources with stock
                dist = math.sqrt(
                    (self.x - resource["x"])**2 + (self.y - resource["y"])**2
                )
                if dist < best_distance:
                    best_distance = dist
                    best_resource = resource
                    best_index = i
        
        return best_resource, best_index, best_distance

    def get_angle_to_target(self, target_x, target_y):
        """Calculate angle to target position"""
        dx = target_x - self.x
        dy = target_y - self.y
        return math.atan2(dy, dx)

    def should_follow_pheromone(self, pheromone_strength, target_resource, resources):
        """
        Determine if ant should follow pheromone trail.
        Only follow if:
        1. Pheromone is strong enough
        2. Resource has stock
        3. Pheromone helps get closer to a resource
        """
        if pheromone_strength <= PHEROMONE_FOLLOW_THRESHOLD:
            return False
        
        # Find if there's a target resource with stock
        if target_resource is None or target_resource["amount"] <= 0:
            nearest_res, _, _ = self.find_nearest_resource_with_stock(resources)
            if nearest_res is None:
                return False
            target_resource = nearest_res
        else:
            # Check if target still has stock
            if target_resource["amount"] <= 0:
                return False
        
        return True

    def move(self, speed, resources, obstacles, trap_active, pheromone_grid):
        """Update ant position based on current state"""
        
        # If returning to nest with food
        if self.returning_to_nest and self.has_food:
            # Head towards nest
            dx = self.nest_pos[0] - self.x
            dy = self.nest_pos[1] - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist < 20:  # Reached nest
                self.returning_to_nest = False
                self.has_food = False
                self.path_memory = []
                self.food_location = None
                self.target_resource = None
                # Ant continues exploring
                self.angle = random.uniform(0, 2 * math.pi)
            else:
                # Move towards nest
                self.angle = math.atan2(dy, dx)
                # Deposit pheromones along path
                grid_x = int(self.x // PHEROMONE_GRID_SIZE)
                grid_y = int(self.y // PHEROMONE_GRID_SIZE)
                if 0 <= grid_x < len(pheromone_grid) and 0 <= grid_y < len(pheromone_grid[0]):
                    pheromone_grid[grid_x][grid_y] += 5.0
        
        else:
            # Normal foraging behavior
            speed_mult = 2 if self.is_panicked else 1
            speed *= speed_mult
            
            # Check for pheromone gradient
            pheromone_strength = self.get_pheromone_influence(pheromone_grid)
            
            # Update or find target resource
            if self.target_resource is None or self.target_resource["amount"] <= 0:
                nearest_res, res_index, _ = self.find_nearest_resource_with_stock(resources)
                if nearest_res is not None:
                    self.target_resource = nearest_res
            
            # Decide if should follow pheromone
            should_follow = self.should_follow_pheromone(
                pheromone_strength, 
                self.target_resource, 
                resources
            )
            
            if should_follow and self.target_resource is not None:
                # Follow pheromone towards target (subtle turn)
                pheromone_angle = self.get_angle_to_target(
                    self.target_resource["x"],
                    self.target_resource["y"]
                )
                
                # Blend current angle with pheromone direction
                # This makes ants follow trails while still exploring
                angle_diff = pheromone_angle - self.angle
                # Normalize angle difference to [-pi, pi]
                while angle_diff > math.pi:
                    angle_diff -= 2 * math.pi
                while angle_diff < -math.pi:
                    angle_diff += 2 * math.pi
                
                # Only follow if pheromone is in reasonable direction (within 90 degrees)
                if abs(angle_diff) < math.pi / 2:
                    self.angle += angle_diff * 0.1  # Gentle turn towards pheromone
                else:
                    # Pheromone is wrong direction, ignore it
                    self.angle += random.uniform(-0.2, 0.2)
            else:
                # Normal random exploration
                turn_range = 1.0 if self.is_panicked else 0.2
                self.angle += random.uniform(-turn_range, turn_range)
        
        # Calculate new position
        new_x = self.x + math.cos(self.angle) * speed
        new_y = self.y + math.sin(self.angle) * speed
        
        # Check for obstacles
        if not self.check_collision(new_x, new_y, obstacles):
            self.x = new_x
            self.y = new_y
        else:
            self.angle += math.pi  # Turn around

        # Boundary wrapping
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.angle = -self.angle
        
        # Resource detection and collection
        for i, resource in enumerate(resources):
            if resource["amount"] <= 0:
                continue
                
            distance = math.sqrt(
                (self.x - resource["x"])**2 + (self.y - resource["y"])**2
            )
            if distance < DETECTION_DISTANCE:
                if not self.has_food:
                    self.has_food = True
                    self.returning_to_nest = True
                    self.food_location = i
                    self.target_resource = resource
                    # Start depositing pheromones
                    grid_x = int(self.x // PHEROMONE_GRID_SIZE)
                    grid_y = int(self.y // PHEROMONE_GRID_SIZE)
                    if 0 <= grid_x < len(pheromone_grid) and 0 <= grid_y < len(pheromone_grid[0]):
                        pheromone_grid[grid_x][grid_y] += 5.0
                    
                    if trap_active:
                        self.is_panicked = True