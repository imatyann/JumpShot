import pygame

class Reticle:
    def __init__(self, width, color):
        self.width = width
        self.color = color

    def draw(self, screen, first_screen_x, first_screen_y, end_screen_x, end_screen_y):
        # 照準の描画関数
        pygame.draw.line(screen,self.color, (first_screen_x, first_screen_y), (end_screen_x, end_screen_y), self.width)