import pygame
from . import settings

# 主人公のクラス
class Player:

    def __init__(self, scroll_x, scroll_y):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y

    def draw(self, screen, screen_x, screen_y):
        """主人公を描画する関数"""
        pygame.draw.rect(screen, settings.PLAYER_COLOR, (screen_x, screen_y, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT), width = 1)

    def move_x(self, x):
        """x方向にプレイヤーを動かす関数"""
        self.scroll_x += x