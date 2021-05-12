import pygame
import random
import math
from sounds import Sounds

monster_image = pygame.image.load("assets/ennemie.png")


class Monster(pygame.sprite.Sprite):
    """docstring for Monster"""

    def __init__(self, game):
        super().__init__()
        self.is_dead = False
        self.game = game
        self.image = monster_image.copy().convert_alpha()
        self.velocity = 1.6
        self.health = 300
        self.max_health = 300
        width, height = game.screen.get_size()
        x = random.choice([random.randint(a, b) for a, b in zip((-200, width), (0 - self.image.get_width(), width + 200))])
        y = random.choice([random.randint(a, b) for a, b in zip((-400, height), (0 - self.image.get_height(), height + 400))])
        self.coordnate = [x, y]
        self.rect = self.image.get_rect(x=x, y=y)
        self.attack = 60
        self.value_score = 20

    def move(self):
        if not self.rect.colliderect(self.game.player.rect):
            player_x, player_y = self.game.player.rect.x, self.game.player.rect.y
            radiant = math.atan2(self.rect.y - player_y, self.rect.x - player_x)
            self.coordnate[0] -= math.cos(radiant) * self.velocity
            self.coordnate[1] -= math.sin(radiant) * self.velocity
            self.update_rect()
        else:
            self.game.player.damage(self.attack)
            self.kill()
        for plasma in self.game.player.all_plasma:
            if self.rect.colliderect(plasma.rectangle):
                self.damage(plasma.damage)
                if self.health < 0:
                    self.kill()
                    self.game.score += self.value_score
                plasma.kill()

    def update_rect(self):
        self.rect.x, self.rect.y = map(round, self.coordnate)

    def damage(self, amount):
        self.health -= amount

    def draw_rects(self):
        prop_health = self.health / self.max_health * 50
        rect = pygame.Rect(self.rect.left, self.rect.top - 15, prop_health, 3)
        max_rect = pygame.Rect(self.rect.left, self.rect.top - 15, 50, 3)
        pygame.draw.rect(self.game.screen, '#0e0e0e', max_rect)
        pygame.draw.rect(self.game.screen, '#de2a2a', rect)

    def kill(self):
        super().kill()
        self.is_dead = True
        Sounds.hit.play()
