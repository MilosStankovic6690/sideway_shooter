import json

class GameStats:
    '''Represent a statistic of game'''

    def __init__(self, ss_game):
        '''Statistics initialization. '''
        self.settings = ss_game.settings

         # High score should never be reset.
        self.high_score = self.load_high_score()

        self.reset_stats()

    def reset_stats(self):
        '''Restarting a game statistics'''
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.alien_destroyed = 0
        self.level = 1

    def load_high_score(self):
        '''Load hight score from file if exists'''
        try:
            with open("high_score.json", "r") as f:
                return int(json.load(f))
        except (FileNotFoundError, ValueError):
            return 0

    def save_high_score(self):
        '''Save high score in variable'''
        with open("high_score.json", "w") as f:
            json.dump(self.high_score, f)