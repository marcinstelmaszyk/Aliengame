import sys
from time import sleep
from bullet import Bullet
from alien import Alien
import pygame

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Reakcja na naciśnięcie klawisza.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    '''Reakcja na zdarzenia generowane przez klawiaturę i mysz.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Rozpoczęcie nowej gry po kliknięciu przycisku Gra przez użytkownika'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Ukrycie kursora myszy
        pygame.mouse.set_visible(False)
        # Wyzerowanie danych statystycznych gry
        stats.reset_stats()
        stats.game_active = True
        # Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()
        # Utworzenie nowej floty i wyśrodkowanie statku
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        

def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    '''Uaktualnienie obrazów na ekranie i przejście do nowego ekranu.'''
    screen.fill(ai_settings.bg_color)
    # Ponowne wyświetlenie wszystkich pocisków pod warstwami statku kosmicznego i obcych
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Wyświetlenie przycisku tylko wtedy, gdy gra jest nieaktywna
    if not stats.game_active:
        play_button.draw_button()
       
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    # Usunięcie pocisków, które znajdą się poza ekranem
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    '''Reakcja na kolizję między pociskiem i obcym.'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Pozbycie się istniejących pociskó i utworzeni nowej floty.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    # Utworzenie nowego pocisku i dodanie go do grupy pocisków
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    '''Ustalenie liczby obcych, którzy zmieszczą się w rzędzie.'''
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Ustalenie ile rzędów obcych zmieści się na ekranie'''
    available_space_y = (ai_settings.screen_height - 3*alien_height - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    '''Utworzenie pełnej floty obcych.'''
    alien = Alien(ai_settings, screen)    
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    '''Reakcja na uderzenie obcego w statek.'''
    if stats.ships_left > 0:
        # Zmniejszenie wartości przechowywanej w ships_left
        stats.ships_left -= 1
        # Usunięcie zawartości list aliens i bullets
        aliens.empty()
        bullets.empty()
        # Utworzenie nowej floty i wyśrodkowanie statku
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pauza
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    '''Sprawdzenie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    '''Uaktualnienie położenia wszystkich obcych we flocie'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Wykrywanie kolizji między obcym i statkiem
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # Wyszukiwanie obcych docierających do dolnej krawędzi ekranu
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    '''Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Przesunięcie całej floty w dół i zmiana kierunku, w którym się ona porusza.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
