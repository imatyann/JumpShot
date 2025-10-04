import pygame
# メインカメラのクラス
class Camera:  
    def __init__(self, scroll_x, scroll_y):
        self.scroll_x = scroll_x
        self.scroll_y = scroll_y

    def scroll_to_screen(self, scroll_x, scroll_y):
        """scroll座標を画面座標に変換して返す関数"""
        return scroll_x - self.scroll_x, scroll_y - self.scroll_y
    
    def screen_to_scroll(self, screen_x, screen_y):
        """画面座標をscroll座標に変換して返す関数"""
        return screen_x + self.scroll_x, screen_y + self.scroll_y
    
    def move_x(self, x):
        """x方向にカメラを動かす関数"""
        self.scroll_x += x