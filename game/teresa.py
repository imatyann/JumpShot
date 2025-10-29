import pygame

class Teresa:

    def __init__(self, scroll_x, scroll_y, radius, color, direction_x, direction_y):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.radius = radius
        self.color = color
        self.direction_x = direction_x
        self.direction_y = direction_y
        
    
    def draw(self, screen, screen_x, screen_y):
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)

    def summon(self, x, y):
        self.scroll_x = x
        self.scroll_y = y

    def move_front(self, speed):
        self.scroll_x += self.direction_x * speed
        self.scroll_y += self.direction_y * speed

    def attacking(self, scroll_x, scroll_y):
        dx = scroll_x - self.scroll_x
        dy = scroll_y - self.scroll_y
        distance_squared = dx * dx + dy * dy
        return distance_squared <= self.radius * self.radius