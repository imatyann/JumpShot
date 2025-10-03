import pygame
from . import settings

class Rect:

    def __init__(self, scroll_x, scroll_y, width, height, color):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen, screen_x, screen_y):
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))
    


    