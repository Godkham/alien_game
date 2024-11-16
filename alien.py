import sys
import pygame

from setting import Settings
from ship import Ship
from new_alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
def run_game():
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_height))
    screen.fill(ai_setting.bg_color)
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_setting, screen)
    alien = Alien(ai_setting, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_setting,screen,aliens,ship)
    stats = GameStats(ai_setting)
    while True:
        gf.check_events(ship,ai_setting,screen,bullets)
        ship.update()
        gf.update_bullets(bullets,aliens,ai_setting,screen,ship)
        gf.update_aliens(ai_setting,stats, aliens,ship,screen,bullets)
        gf.update_screen(ai_setting, screen, ship, bullets,aliens)




if __name__ == '__main__':
    run_game()