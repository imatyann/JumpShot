import pygame
from . import settings

# 主人公のクラス
class Player:

    def __init__(self, scroll_x, scroll_y, on_ground, fall_speed , touch_right, touch_left, touch_head, touch_foot):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y
        self.on_ground = on_ground
        self.fall_speed = fall_speed
        self.touch_right = touch_right
        self.touch_left = touch_left
        self.touch_head = touch_head
        self.touch_foot = touch_foot
    

    def draw(self, screen, screen_x, screen_y):
        """主人公を描画する関数"""
        pygame.draw.rect(screen, settings.PLAYER_COLOR, (screen_x, screen_y, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT), width = 1)

    def move_x(self, x):
        """x方向にプレイヤーを動かす関数"""
        self.scroll_x += x

    def move_y(self, y):
        """y方向にプレイヤーを動かす関数"""
        self.scroll_y += y
        

    def fall(self):
        """下方向に常に加速させる関数"""
        self.fall_speed += settings.PLAYER_G


    def jump(self, speed):
        """任意のスピードでジャンプする関数"""
        self.fall_speed = -speed

    def conflict_rect(self, scroll_x, scroll_y, width, height):
        W = settings.PLAYER_WIDTH
        H = settings.PLAYER_HEIGHT
        x_overlap = (self.scroll_x + W >= scroll_x) and (self.scroll_x <= scroll_x + width)
        y_overlap = (self.scroll_y + H >= scroll_y) and (self.scroll_y <= scroll_y + height)
        return x_overlap and y_overlap

