class Settings:
    """A class to store all settings for Sideways Shooter."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 3.0
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 6.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings.
        #  alien_frequency controls how often a new alien appear.s
        #    Higher values -> more frequent aliens. Max = 1.0.
        self.alien_frequency = 0.008
        self.alien_speed = 1.5
        self.alien_destroyed_for_speedup = 10

        self.difficulty_level = 'normal'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings tha change throughout the game'''
        if self.difficulty_level == 'easy':
            self.ship_limit = 5
            self.bullets_allowed = 10
            self.ship_speed = 0.75
            self.bullet_speed = 1.5
            self.alien_speed = 0.5
            self.alien_destroyed_for_speedup = 1.0
        elif self.difficulty_level == 'normal':
            self.ship_limit = 3
            self.bullets_allowed = 3
            self.ship_speed = 1.5
            self.bullet_speed = 3.0
            self.alien_speed = 1.0
            self.alien_destroyed_for_speedup = 15.0
        elif self.difficulty_level == 'hard':
            self.ship_limit = 2
            self.bullets_allowed = 3
            self.ship_speed = 3.0
            self.bullet_speed = 6.0
            self.alien_speed = 2.0
            self.alien_destroyed_for_speedup = 20.0

        # Scoring settings
        self.alien_points = 50

        # How quickly aliens point values increase
        self.speedup_scale = 1.1
        self.score_scale = 1.5

    def increase_speed(self):
        '''Increase speed settings and alien point values.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)