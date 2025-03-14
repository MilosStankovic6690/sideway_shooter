import sys
from random import random
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboars import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class SidewaysShooter:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Sideways Shooter")
        
        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.game_stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Make the Play button.
        self.play_button = Button(self, "Play")
        # Make difficulty level buttons.
        self._make_difficulty_buttons()

        self.game_active = False

        self.difficulty_selected = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
               self.ship.update()
               self._update_bullets()
               self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _make_difficulty_buttons(self):
         '''Make buttons that allow player to select difficulty level.'''
         self.easy_button = Button(self, 'Easy')
         self.normal_button = Button(self, 'Normal')
         self.hard_button = Button(self, 'Hard')

         # Position buttons so they don't all overlap.
         self.easy_button.rect.top = (
              self.play_button.rect.top + 1.5*self.play_button.rect.height
         )
         self.easy_button._update_msg_position()

         self.normal_button.rect.top = (
              self.easy_button.rect.top + 1.5*self.easy_button.rect.height
         )
         self.normal_button._update_msg_position()

         self.hard_button.rect.top = (
              self.normal_button.rect.top + 1.5*self.normal_button.rect.height
         )
         self.hard_button._update_msg_position()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._chech_difficulty_level(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Get the mouse coordinates, and check if they match the play button'''
        clicked_play_button = self.play_button.rect.collidepoint(mouse_pos)
        if clicked_play_button and self.game_active == False:
            self.settings.initialize_dynamic_settings()
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
    
    def _chech_difficulty_level(self, mouse_pos):
          """Set the appropriate difficulty level."""
          easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
          normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
          hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

          if easy_button_clicked:
               self.settings.difficulty_level = 'easy'
          elif normal_button_clicked:
               self.settings.difficulty_level = 'normal'
          elif hard_button_clicked:
               self.settings.difficulty_level = 'hard'

          if easy_button_clicked or normal_button_clicked or hard_button_clicked:
              self.difficulty_selected = True

    def _start_game(self):
        '''Method for start from beggining.'''
        self.bullets.empty()
        self.aliens.empty()
        self._create_alien()
        self.ship.center_ship()

        # Reset  of avilable ship.
        self.game_stats.reset_stats()
        self.sb.prep_score()
        
        # Set game on active value.
        self.game_active = True

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            if self.game_active == False and self.difficulty_selected == True:
                self.settings.initialize_dynamic_settings()
                self._start_game() 

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check whether any bullets have hit an alien."""
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.game_stats.score += self.settings.alien_points * len(aliens)
                self.game_stats.alien_destroyed += len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

            # Check if you need to speed up the game.
            if self.game_stats.alien_destroyed >= self.settings.alien_destroyed_for_speedup:
                self.settings.increase_speed()
                self.game_stats.alien_destroyed = 0

                # Increase level
                self.game_stats.level += 1
                self.sb.prep_level()
        
    def _update_aliens(self):
        '''Update aliens position'''
        self._create_alien()
        self.aliens.update()
        # Look for alien-ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Look for the alien hitting left edge of the screen.
        self._check_aliens_passing_left_edge_position()
        
    def _ship_hit(self):
        '''Method changes value after alien hit the ship.'''
        if self.game_stats.ship_left > 0:
            # Decrement ships left, and update scoreboard.
            self.game_stats.ship_left -= 1
            self.sb.prep_ships()

            # Get rid of any reamining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            self._create_alien()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            self.difficulty_selected = False
            # Hide the mouse cursor.
            pygame.mouse.set_visible(True)

    def _check_aliens_passing_left_edge_position(self):
        '''Check for aliens passing the left edge of the screen.'''
        for alien in self.aliens.sprites():
            if alien.rect.left < 0:
                self._ship_hit()
                break

    def _create_alien(self):
        """Create an alien, if conditions are right."""
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            self.aliens.add(alien)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        if not self.difficulty_selected:
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
        elif not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ss_game = SidewaysShooter()
    ss_game.run_game()