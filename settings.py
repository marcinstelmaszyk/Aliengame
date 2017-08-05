class Settings():
    '''Klasa przeznaczona do przechowywania wszystkich ustawień gry.'''

    def __init__(self):
        '''Inicjalizacja ustawień gry.'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienie dotyczące statku
        self.ship_speed_factor = 1.5

        # Ustawienie dotyczące obcego
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # Wartość fleet)direction wynosząca 1 oznacza prawo, natomiast -1 oznacza lewo
        self.fleet_direction = 1

        # Ustawienia dotyczące pocisku
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

    