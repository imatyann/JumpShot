import pygame

class Key:

    def __init__(self, scroll_x, scroll_y, is_draw, color, width, height):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.is_draw = is_draw
        self.color = color
        self.width = width
        self.height = height

    def draw(self, screen, screen_x, screen_y):
        """鍵を描写する関数"""
        radius = self.height / 4
        pygame.draw.circle(
            screen,
            self.color,
            (screen_x + self.width / 2 , screen_y + radius),
            radius
        )
        pygame.draw.rect(
            screen,
            self.color,
            (screen_x + self.width / 3, screen_y + 2 * radius - 2, self.width / 3, self.height - radius * 2 + 2)
        )

        pygame.draw.rect(
            screen,
            self.color,
            (screen_x + self.width / 3, screen_y + 2 * radius, self.width * 2/3, (self.height - 2 * radius) / 4)
        )

        pygame.draw.rect(
            screen,
            self.color,
            (screen_x + self.width / 3, screen_y + 2 * radius + (self.height - 2 * radius) / 2, self.width * 2/3, (self.height - 2 * radius) / 4)
        )

#   =========================================
        pygame.draw.circle(
            screen,
            (0,0,0),
            (screen_x + self.width / 2 , screen_y + radius),
            radius,
            1
        )
        pygame.draw.rect(
            screen,
            (0,0,0),
            (screen_x + self.width / 3, screen_y + 2 * radius - 2, self.width / 3, self.height - radius * 2 + 2),
            1
        )

        pygame.draw.rect(
            screen,
            (0,0,0),
            (screen_x + self.width * 2 / 3, screen_y + 2 * radius, self.width * 1/3, (self.height - 2 * radius) / 4),
            1
        )

        pygame.draw.rect(
            screen,
            (0,0,0),
            (screen_x + self.width *2 / 3, screen_y + 2 * radius + (self.height - 2 * radius) / 2, self.width * 1/3, (self.height - 2 * radius) / 4),
            1
        ) 

        # pygame.draw.rect(
        #     screen,
        #     self.color,
        #     (screen_x, screen_y, self.width, self.height),
        #     1
        # )

    def touch(self, rect_x, rect_y, rect_width, rect_height):
        key_left = self.scroll_x
        key_right = self.scroll_x + self.width
        key_top = self.scroll_y
        key_bottom = self.scroll_y + self.height

        rect_left = rect_x
        rect_right = rect_x + rect_width
        rect_top = rect_y
        rect_bottom = rect_y + rect_height

        # 長方形同士の交差判定
        if (key_right > rect_left and
            key_left < rect_right and
            key_bottom > rect_top and
            key_top < rect_bottom):
            return True
        else:
            return False