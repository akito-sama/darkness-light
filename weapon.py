import pygame
import math


class Weapon:
    def __init__(self, player, game):
        self.damage = 20
        self.game = game
        self.user = player
        self.image = pygame.image.load("assets/hand.png")
        self.image.set_alpha(200)
        self.radius = 0
        self.velocity = math.pi / 60
        self.size_user = max(self.user.image.get_size())
        self.rayon = (self.size_user / 2) + 15
        self.center = (
            self.user.rect.x + self.size_user / 2,
            self.user.rect.y + self.size_user / 2,
        )
        self.charge = 0
        self.max_charge = 12
        self.speed_charging = 0.3
        self.current_radiant = None
        self.dir_surface = pygame.Surface(self.game.screen.get_size()).convert_alpha()
        self.cursor_color = (255, 255, 255, 60)

    def draw(self):
        self.game.screen.blit(self.image, self.position)

    @property
    def position(self):
        self.center = self.user.rect.center
        x = self.center[0] + self.rayon * math.cos(self.radius)
        y = self.center[1] - self.rayon * math.sin(self.radius)
        pygame.draw.circle(self.game.screen, "black", self.center, self.rayon, 1)
        x -= self.image.get_width() // 2
        y -= self.image.get_height() // 2
        return (x, y)

    def rotate(self, coef):
        self.radius += self.velocity * coef

    def charging(self):
        if self.charge < self.max_charge:
            self.charge += self.speed_charging
        else:
            self.charge = self.max_charge

    def reset(self):
        self.charge = 1
