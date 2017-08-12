class Settings():
    '''Klasa przeznaczona do przechowywania wszystkich ustawień gry.'''

    def __init__(self):
        '''Inicjalizacja ustawień gry.'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ustawienie dotyczące statku kosmicznego        
        self.ship_limit = 3

        # Ustawienie dotyczące obcego        
        self.fleet_drop_speed = 10        

        # Ustawienia dotyczące pocisku        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Zmiana szybkości gry
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        '''Inicjalizacja ustawień, które ulegają zmianie w trakcie gry.'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
    
        # Wartość fleet)direction wynosząca 1 oznacza prawo, natomiast -1 oznacza lewo
        self.fleet_direction = 1

    def increase_speed(self):
        '''Zmiana ustawień dotyczących szybkości.'''
        self.ship_speed_factor *= self.speedup_scale                
        self.bullet_speed_factor *= self.speedup_scale 
        self.alien_speed_factor *= self.speedup_scale 