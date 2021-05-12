import pygame
from game import Game

pygame.init()
screen = pygame.display.set_mode((720, 480))
pygame.display.set_caption("ninja game")
game = Game(screen)

while game.running:
    game.event()
    game.draw()
    game.update()
