import pygame

pygame.font.init()


class Fonts:
    font = pygame.font.Font("assets/fonts/Noturnal Hand.ttf", 25)
    Bigfont = pygame.font.Font("assets/fonts/Noturnal Hand.ttf", 50)
    game_over = Bigfont.render("Game Over", False, "white")
    help_screen  = font.render("press any key to continue", False, "white")

    @staticmethod
    def render(screen: pygame.Surface, string: str, pos: tuple):
        rendering = Fonts.font.render(string, False, "white")
        screen.blit(rendering, pos)
