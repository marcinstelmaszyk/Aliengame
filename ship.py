import pygame

class Ship():

    def __init__(self, ai_settings, screen):
        '''Inicjalizacja statku kosmicznego i jego położenie poczatkowe'''
        self.screen = screen
        self.ai_settings = ai_settings

        #Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta
        self.image = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Każdy nowy statek kosmiczny pojawia się po lewej stronie ekranu
        self.rect.centery = self.screen_rect.centery
        self.rect.left = self.screen_rect.left

        # Punkt środkowy statku jest przechowywany w postaci liczby zmiennoprzecinkowej
        self.center = float(self.rect.centery)

        #Opcje wskazujące na poruszanie się statku
        self.moving_up = False
        self.moving_down  = False

    def update(self):
        '''
        Uaktualnienie położenia statku na podstawie opcji wskazującej na jego ruch
        '''        
        
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center += self.ai_settings.ship_speed_factor            
        

        # Uaktualnienie obiektu rect na podstawie wartości self.center
        self.rect.centery = self.center

    def blitme(self):
        '''Wyświetlenie statku kosmicznego w jego aktualnym położeniu'''
        self.screen.blit(self.image, self.rect)
