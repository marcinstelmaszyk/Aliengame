import sys
from bullet import Bullet
import pygame

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Reakcja na naciśnięcie klawisza.'''
    if event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:        
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
    if event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets):
    '''Reakcja na zdarzenia generowane przez klawiaturę i mysz.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship, bullets):
    '''Uaktualnienie obrazów na ekranie i przejście do nowego ekranu.'''
    screen.fill(ai_settings.bg_color)
    # Ponowne wyświetlenie wszystkich pocisków pod warstwami statku kosmicznego i obcych
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
       
    pygame.display.flip()

def update_bullets(screen, bullets):
    bullets.update()

    screen_rect = screen.get_rect()
    # Usunięcie pocisków, które znajdą się poza ekranem
    for bullet in bullets.copy():
        if bullet.rect.left > screen_rect.right:
            bullets.remove(bullet)

def fire_bullet(ai_settings, screen, ship, bullets):
    # Utworzenie nowego pocisku i dodanie go do grupy pocisków
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)