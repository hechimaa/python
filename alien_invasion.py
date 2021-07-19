import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """ゲームのアセットと動作を管理する全体的なクラス"""

    def __init__(self):
        """ゲームを初期化し、ゲームのリソースを作成する"""
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
#        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#        self.settings.screen_width = self.screen.get_rect().width
#        self.settings.screen_height = self.screen.get_rext().height
        pygame.display.set_caption("エイリアン侵略")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
    
    def run_game(self):
        """ゲームのメインループを開始する"""
        while True:
            #キーボードとマウスのイベントを監視する
            self._check_events()
            #宇宙船を更新する
            self.ship.update()
            #弾を更新する
            self._update_bullets()
            #画面を描画する
            self._update_screen()

    def _check_events(self):
        """キーボードとマウスのイベントに対応する"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """キーを押すイベントに対応する"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """キーを離すイベントに対応する"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """新しい弾を生成しbulletsグループに追加する"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """弾の位置を更新し古い弾を削除する"""
        #弾の位置を更新する
        self.bullets.update()
        #見えなくなった弾を削除する
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))

    def _create_fleet(self):
        """エイリアンの艦隊を作成する"""
        #1匹のエイリアンを作成する
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #最初の列のエイリアンを作成する
        for alien_number in range(number_aliens_x):
            self._create_alien(alien_number)

    def _create_alien(self,alien_number):
        #エイリアンを1匹作成し列の中へ配置する
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_screen(self):
        """画面上の画像を更新し新しい画面に切り替える"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    #ゲームのインスタンスを作成しゲームを実行する
    ai = AlienInvasion()
    ai.run_game()