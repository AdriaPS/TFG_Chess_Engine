import pygame
import game_controller as gc


class Button:
    def __init__(self, name, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.name = name
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):
        gc.chess_screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.clicked = True
