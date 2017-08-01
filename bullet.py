import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Klasa przeznaczona do zarządzania pociskami wystrzeliwanymi przez statek.'''

    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        # Utworzenie prostokąta pocisku w punkcie (0, 0), a następnie zdefiniowanie dla niego odpowiedniego położenia
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_height, ai_settings.bullet_width)
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.right

        # Położenie pocisku jest zdefiniowane za pomocą wartości zmiennoprzecinkowej
        self.x = float(self.rect.x)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Poruszanie pociskiem po ekranie'''
        # Uaktualnienie położenia pocisku
        self.x += self.speed_factor
        # Uaktualnienie położenia prostokąta pocisku
        self.rect.x = self.x

    def draw_bullet(self):
        '''Wyświetlenie pocisku na ekranie'''
        pygame.draw.rect(self.screen, self.color, self.rect)
