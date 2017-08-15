import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from bullet import Bullet

class Game():

    def __init__(self):
        pygame.init()
        self.ai_settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.ai_settings.screen_width, self.ai_settings.screen_height))
        pygame.display.set_caption("Inwazja obcych")
    
        # Utworzenie przycisku Gra
        self.play_button = Button(self.ai_settings, self.screen, 'Gra')
    
        # Utworzenie egzemplarza przenaczonego do przechowywania danych
        # statystycznych gry oraz utworzenie egzemplarza klasy Scoreboard
        self.stats = GameStats(self.ai_settings)
        self.sb = Scoreboard(self.ai_settings, self.screen, self.stats)

        #Utworzenie statku kosmicznego, grupy pocisków oraz grupy obcych
        self.ship = Ship(self.ai_settings, self.screen)
        self.bullets = Group()
        self.aliens = Group()

        # Utworzenie floty obcych
        self.create_fleet()

    def run(self):
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()

    def create_fleet(self):
        '''Utworzenie pełnej floty obcych.'''
        alien = Alien(self.ai_settings, self.screen)    
        number_aliens_x = self.get_number_aliens_x(alien.rect.width)
        number_rows = self.get_number_rows(alien.rect.height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def get_number_aliens_x(self, alien_width):
        '''Ustalenie liczby obcych, którzy zmieszczą się w rzędzie.'''
        available_space_x = self.ai_settings.screen_width - 2*alien_width
        number_aliens_x = int(available_space_x / (2*alien_width))
        return number_aliens_x

    def get_number_rows(self, alien_height):
        '''Ustalenie ile rzędów obcych zmieści się na ekranie'''
        available_space_y = (self.ai_settings.screen_height - 3*alien_height - self.ship.rect.height)
        number_rows = int(available_space_y / (2*alien_height))
        return number_rows

    def create_alien(self, alien_number, row_number):
        '''Utwórz nowego obcego.'''
        alien = Alien(self.ai_settings, self.screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
        self.aliens.add(alien)

    def check_events(self):
        '''Reakcja na zdarzenia generowane przez klawiaturę i mysz.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_play_button(mouse_x, mouse_y)

    def check_keydown_events(self, event):
        '''Reakcja na naciśnięcie klawisza.'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_g:
            self.start_game()
        elif event.key == pygame.K_q:
            sys.exit()

    def fire_bullet(self):
        # Utworzenie nowego pocisku i dodanie go do grupy pocisków
        if len(self.bullets) < self.ai_settings.bullets_allowed:
            new_bullet = Bullet(self.ai_settings, self.screen, self.ship)
            self.bullets.add(new_bullet)

    def start_game(self):
        '''Rozpoczęcie gry poprzez wywołanie domyślnych ustawień.'''
        if not self.stats.game_active:
            # Wyzerowanie ustawień dotyczących gry.
            self.ai_settings.initialize_dynamic_settings()
            # Ukrycie kursora myszy
            pygame.mouse.set_visible(False)
            # Wyzerowanie danych statystycznych gry
            self.stats.reset_stats()
            self.stats.game_active = True
            # Wyzerowanie obrazów tablicy wyników.
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()
            # Utworzenie nowej floty i wyśrodkowanie statku
            self.create_fleet()
            self.ship.center_ship()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_play_button(self, mouse_x, mouse_y):
        '''Rozpoczęcie nowej gry po kliknięciu przycisku Gra przez użytkownika'''
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.stats.game_active:        
            self.start_game()

    def update_bullets(self):
        self.bullets.update()
        # Usunięcie pocisków, które znajdą się poza ekranem
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        '''Reakcja na kolizję między pociskiem i obcym.'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.ai_settings.alien_points * len(aliens)
                self.sb.prep_score()
            self.check_high_score()
        if len(self.aliens) == 0:
            # Jeżeli cała flota została zniszczona, gracz przechodzi na kolejny poziom.
            self.bullets.empty()
            self.ai_settings.increase_speed()

            # Inkrementacja numeru poziomu.
            self.stats.level += 1
            self.sb.prep_level()

            self.create_fleet()

    def check_high_score(self):
        '''Sprawdzenie, czy mamy nowy najlpeszy wynik osiągnięty dotąd w grze.'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

    def update_aliens(self):
        '''Uaktualnienie położenia wszystkich obcych we flocie'''
        self.check_fleet_edges()
        self.aliens.update()
        # Wykrywanie kolizji między obcym i statkiem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        # Wyszukiwanie obcych docierających do dolnej krawędzi ekranu
        self.check_aliens_bottom()

    def check_fleet_edges(self):
        '''Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu.'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        '''Przesunięcie całej floty w dół i zmiana kierunku, w którym się ona porusza.'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.ai_settings.fleet_drop_speed
        self.ai_settings.fleet_direction *= -1

    def ship_hit(self):
        '''Reakcja na uderzenie obcego w statek.'''
        if self.stats.ships_left > 0:
            # Zmniejszenie wartości przechowywanej w ships_left
            self.stats.ships_left -= 1
            # Uaktualnienie tablicy wyników.
            self.sb.prep_ships()
            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()
            # Utworzenie nowej floty i wyśrodkowanie statku
            self.create_fleet()
            self.ship.center_ship()
            # Pauza
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self):
        '''Sprawdzenie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def update_screen(self):
        '''Uaktualnienie obrazów na ekranie i przejście do nowego ekranu.'''
        self.screen.fill(self.ai_settings.bg_color)
        # Ponowne wyświetlenie wszystkich pocisków pod warstwami statku kosmicznego i obcych
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Wyświetlenie informacji o punktacji.
        self.sb.show_score()
        # Wyświetlenie przycisku tylko wtedy, gdy gra jest nieaktywna
        if not self.stats.game_active:
            self.play_button.draw_button()
       
        pygame.display.flip()