import pygame

class Ship():

    def __init__(self, screen):
        '''Inicjalizacja statku kosmicznego i jego położenie poczatkowe'''
        self.screen = screen

        #Wczytanie obrazu statku kosmicznego i pobranie jego prostokąta
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Każdy nowy statek kosmiczny pojawia się na dole ekranu
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        self.screen.blit(self.image, self.rect)
