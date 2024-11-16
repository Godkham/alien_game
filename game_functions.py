import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_fire(ai_settings, screen, ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def check_keydown(event,ship,ai_settings, screen,bullets ):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        check_fire(ai_settings, screen, ship, bullets)




def check_keyup(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
def check_events(ship, ai_settings, screen,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ship, ai_settings, screen,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)


def update_bullets(bullets,aliens,ai_setting,screen,ship):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    print(len(bullets))
    collisions(bullets, aliens, ai_setting, screen, ship)


def collisions(bullets,aliens,ai_setting,screen,ship):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(aliens, ai_setting, screen, ship)
def update_aliens(ai_setting,stats, aliens,ship,screen,bullets):
    aliens.update()
    check_fleet_edges(ai_setting, aliens)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets)


def check_aliens_bottom(ai_setting, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, stats, screen, ship, aliens, bullets)
            break
def ship_hit(ai_setting,stats,screen,ship,aliens,bullets):
    aliens.empty()
    bullets.empty()
    create_fleet(ai_setting, screen, ship, aliens)
    ship.center_ship()

    if stats.ships_left > 0:
        stats.ships_left -= 1
        sleep(0.5)
    else:
        stats.game_active = False
def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting,aliens)
            break
def change_fleet_direction(ai_setting,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


def get_number_aliens_x(ai_setting, alien_width):
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_setting, screen, aliens, alien_number,row_number):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
def create_fleet(ai_setting,screen,aliens,ship):
    alien = Alien(ai_setting,screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height,
                                  alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number,
                         row_number)


def get_number_rows(ai_setting, ship_height, alien_height):
    available_space_y = (ai_setting.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows



def update_screen(ai_settings, screen,ship,bullets,aliens):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    for bullet in bullets:
        bullet.draw_bullet()
    pygame.display.flip()




