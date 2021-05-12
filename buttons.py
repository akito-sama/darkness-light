import pygame


class Button:
    """docstring for Button"""

    def __init__(self, path: str, pos: tuple = (0, 0)):
        self.x, self.y = pos
        self.image = pygame.image.load(path)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    @property
    def rect(self):
        return self.image.get_rect(x=self.x, y=self.y)
