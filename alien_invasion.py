import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Inwazja obcych")
    
    #Utworzenie statku kosmicznego
    ship = Ship(ai_settings, screen)
    # Utworzenie grupy przeznaczonej do przechowywania pocisków
    bullets = Group()

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(screen, bullets)
        gf.update_screen(ai_settings, screen, ship, bullets)

run_game()