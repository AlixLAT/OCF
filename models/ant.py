import random
import math
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    DETECTION_DISTANCE, OBSTACLE_RADIUS
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

    def move(self, speed, resources, obstacles, trap_active):
        """Update ant position based on current state"""
        if self.is_panicked:
            speed *= 2
            turn_range = 1.0
        else:
            turn_range = 0.2
        
        # Update direction with randomness
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
        
        # Resource detection
        for resource in resources:
            distance = math.sqrt(
                (self.x - resource["x"])**2 + (self.y - resource["y"])**2
            )
            if distance < DETECTION_DISTANCE:
                if resource["type"] == "food":
                    self.has_food = True
                    if trap_active:
                        self.is_panicked = True