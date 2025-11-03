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

    def attacking(self, scroll_x, scroll_y, r=0):
        dx = scroll_x - self.scroll_x
        dy = scroll_y - self.scroll_y
        R = self.radius + r     
        return dx*dx + dy*dy <= R*R
    
    def attacking_rect(self, rect_x, rect_y, rect_w, rect_h):
        nearest_x = max(rect_x, min(self.scroll_x, rect_x + rect_w))
        nearest_y = max(rect_y, min(self.scroll_y, rect_y + rect_h))
        dx = self.scroll_x - nearest_x
        dy = self.scroll_y - nearest_y
        return dx * dx + dy * dy <= self.radius * self.radius