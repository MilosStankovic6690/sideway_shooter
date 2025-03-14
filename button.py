import pygame.font

class Button:
    '''Class to represent buttons.'''

    def __init__(self, ss_game, msg):
        '''Initialize buton atributes'''
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()

        # Create button specifications.
        self.width, self.height = 200, 50
        self.button_color = (100, 5, 5)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Create button rect object.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def _update_msg_position(self):
        """If the button has been moved, the text needs to be moved as well."""
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        '''Draw blank button and then draw message.'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)