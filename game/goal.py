import pygame

class Goal:

    def __init__(self, scroll_x, scroll_y, width, height, color, bg_color):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = bg_color
    
    def draw(self, screen, screen_x, screen_y):
        pygame.draw.rect(screen, self.bg_color, (screen_x, screen_y, self.width, self.height))
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width / 2, self.height), 1)
        pygame.draw.rect(screen, self.color, (screen_x + self.width / 2, screen_y, self.width / 2, self.height), 1)
        pygame.draw.circle(screen, self.color, (screen_x + self.width / 2 - 6, screen_y + self.height / 2), 3)
        pygame.draw.circle(screen, self.color, (screen_x + self.width / 2 + 6, screen_y + self.height / 2), 3)