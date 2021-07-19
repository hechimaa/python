import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """艦隊の中の１匹のエイリアンを表すクラス"""

    def __init__(self,ai_game):
        """エイリアンを初期化し開始時の位置を設定する"""
        super().__init__()
        self.screen = ai_game.screen

        #エイリアンの画像を読み込みサイズを取得する
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #新しいエイリアンを画面の左上の近くに配置する
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #エイリアンの実際の位置を格納する
        self.x = float(self.rect.x)
