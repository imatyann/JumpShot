import pygame

class Bullet:

    def __init__(self,color,radius,scroll_x,scroll_y,direction_x,direction_y):
        self.color = color
        self.radius = radius
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.direction_x = direction_x
        self.direction_y = direction_y
    
    def draw(self, screen, screen_x, screen_y):
        """弾を描画する関数"""
        pygame.draw.circle(
        screen,
        self.color,
        (screen_x, screen_y),
        self.radius)

    def move_front(self, speed):
        self.scroll_x += self.direction_x * speed
        self.scroll_y += self.direction_y * speed
    
    def move_x(self, x):
        self.scroll_x += x