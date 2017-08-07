class GameStats():
    '''Monitorowanie danych statystycznych w grze.'''

    def __init__(self, ai_settings):
        '''Inicjalizowanie danych statystycznych'''
        self.ai_settings = ai_settings
        self.reset_stats()
        # Uruchomienie gry w stanie nieaktywnym
        self.game_active = False

    def reset_stats(self):
        '''Inicjalizacja danych statystycznych, które mogą zmieniać się w trakcie gry.'''
        self.ships_left = self.ai_settings.ship_limit