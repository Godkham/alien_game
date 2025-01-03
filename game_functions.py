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
def check_events(ai_setting, screen, stats, play_button, ship, aliens,
        bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            print(mouse_x)
            print(mouse_y)
            print(type(pygame.mouse.get_pos()))
            check_play_button(ai_setting, screen, stats, play_button, ship, aliens,
        bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown(event, ship, ai_setting, screen,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup(event, ship)

def check_play_button(ai_setting, screen, stats, play_button, ship, aliens,
        bullets, mouse_x, mouse_y):
    play_button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if play_button_click and not stats.game_active:
        ai_setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        aliens.empty()
        bullets.empty()

        create_fleet(ai_setting,screen,aliens,ship)
        ship.center_ship()


def update_bullets(bullets,aliens,ai_setting,screen,ship,stats,sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(bullets, aliens, ai_setting, screen, ship, stats,sb)


def check_bullet_alien_collisions(bullets,aliens,ai_setting,screen,ship, stats,sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_setting.alien_points
        sb.prep_score()



    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
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
        pygame.mouse.set_visible(True)
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



def update_screen(ai_settings, screen,ship,bullets,aliens,play_button,stats,sb):
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    for bullet in bullets:
        bullet.draw_bullet()
    pygame.display.flip()




